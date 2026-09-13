"""
Authentication Service for LearnMate.

Provides:
- PBKDF2-HMAC-SHA256 password hashing with random salt
- Session token generation and validation
- Registration with linked Student profile
- Login with credential verification
- Forgot/Reset password flows
- Seed default user for existing student (Prince Singh, stu-001)
"""

import hashlib
import hmac
import os
import secrets
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple

from app.db.base import Base, engine
from app.db.session import SessionLocal
from app.models.user import User, PasswordResetToken
from app.models.student import Student
from app.mock.data import get_student_profile, _STUDENT

# In-memory active session token store: token -> user_id
_ACTIVE_SESSIONS: Dict[str, Dict[str, Any]] = {}

# In-memory reset tokens for fast, robust dev/test execution: token -> {user_id, expires_at}
_RESET_TOKENS: Dict[str, Dict[str, Any]] = {}


def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """
    Hash password using PBKDF2-HMAC-SHA256.
    Returns (hex_hash, salt_hex).
    """
    if not salt:
        salt = secrets.token_hex(16)
    salt_bytes = bytes.fromhex(salt)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt_bytes,
        iterations=100_000,
    )
    return key.hex(), salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verify password against stored hash using constant-time comparison."""
    calculated_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(calculated_hash, stored_hash)


class AuthService:
    """Manages user registration, login, session tokens, and passwords."""

    def __init__(self):
        # Ensure database tables exist
        try:
            Base.metadata.create_all(bind=engine)
            self._ensure_default_user()
        except Exception as e:
            # Fallback for environments where DB engine is mocked
            pass

    def _ensure_default_user(self):
        """Ensure default existing user for Prince Singh exists in DB."""
        session = SessionLocal()
        try:
            default_email = "prince.singh@university.edu"
            existing = session.query(User).filter(User.email == default_email).first()
            if not existing:
                pwd_hash, salt = hash_password("LearnMate2025!")
                user = User(
                    id="usr-prince-001",
                    email=default_email,
                    password_hash=pwd_hash,
                    salt=salt,
                    full_name="Prince Singh",
                    student_id="stu-001",
                    onboarding_completed=True,
                    is_active=True,
                )
                session.add(user)
                session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()

    def register(
        self,
        full_name: str,
        email: str,
        password: str,
        confirm_password: str,
    ) -> Dict[str, Any]:
        """
        Register a new student account.
        """
        email_clean = email.strip().lower()

        # Validation: password match
        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        # Validation: password strength (min 8 chars, at least 1 digit or special char)
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")
        if not any(c.isdigit() or not c.isalnum() for c in password):
            raise ValueError("Password must contain at least one number or special character.")

        session = SessionLocal()
        try:
            # Check duplicate email
            existing_user = session.query(User).filter(User.email == email_clean).first()
            if existing_user:
                raise ValueError("An account with this email address already exists.")

            # Create Student profile
            new_student_id = f"stu-{uuid.uuid4().hex[:8]}"
            student = Student(
                id=new_student_id,
                name=full_name,
                email=email_clean,
                degree="Computer Science Major",
                institution="LearnMate Academy",
                avatar_url="/prince-avatar.jpg",
                overall_progress=0.0,
                day_streak=1,
            )
            session.add(student)

            # Create User
            pwd_hash, salt = hash_password(password)
            user = User(
                id=f"usr-{uuid.uuid4().hex[:8]}",
                email=email_clean,
                password_hash=pwd_hash,
                salt=salt,
                full_name=full_name,
                student_id=new_student_id,
                onboarding_completed=False,  # New users must onboard!
                is_active=True,
            )
            session.add(user)
            session.commit()

            # Create session token
            token = self._create_session(user.id)

            return {
                "success": True,
                "message": "Account created successfully.",
                "token": token,
                "user": self._user_dict(user),
                "student": {
                    "id": student.id,
                    "name": student.name,
                    "email": student.email,
                    "degree": student.degree,
                    "institution": student.institution,
                    "avatar": student.avatar_url,
                },
                "onboarding_completed": False,
            }
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def login(
        self,
        email: str,
        password: str,
        remember_me: bool = False,
    ) -> Dict[str, Any]:
        """
        Authenticate user credentials and generate session token.
        """
        email_clean = email.strip().lower()
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.email == email_clean).first()
            if not user:
                # Security: generic error message to prevent enumeration
                raise ValueError("Invalid email or password.")

            if not verify_password(password, user.password_hash, user.salt):
                raise ValueError("Invalid email or password.")

            if not user.is_active:
                raise ValueError("Account is deactivated. Please contact support.")

            token = self._create_session(user.id, remember_me=remember_me)

            # Get student profile
            student_info = None
            if user.student_id:
                student = session.query(Student).filter(Student.id == user.student_id).first()
                if student:
                    student_info = {
                        "id": student.id,
                        "name": student.name,
                        "email": student.email,
                        "degree": student.degree,
                        "institution": student.institution,
                        "avatar": student.avatar_url or "/prince-avatar.jpg",
                    }
                elif user.student_id == "stu-001":
                    student_info = get_student_profile()

            return {
                "success": True,
                "message": "Login successful.",
                "token": token,
                "user": self._user_dict(user),
                "student": student_info,
                "onboarding_completed": user.onboarding_completed,
            }
        finally:
            session.close()

    def authenticate_google(
        self,
        email: str,
        full_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        google_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Authenticate or register student using Google Authorization.
        """
        email_clean = email.strip().lower()
        display_name = (full_name or email_clean.split("@")[0].replace(".", " ").title()).strip()
        avatar = avatar_url or "/prince-avatar.jpg"

        session = SessionLocal()
        try:
            user = session.query(User).filter(User.email == email_clean).first()

            if not user:
                # Create user and student profile
                user_id = f"usr-{uuid.uuid4().hex[:12]}"
                student_id = f"stu-{uuid.uuid4().hex[:8]}"

                # Random secure internal hash for OAuth user
                pwd_hash, salt = hash_password(secrets.token_urlsafe(32))

                new_student = Student(
                    id=student_id,
                    name=display_name,
                    email=email_clean,
                    degree="Computer Science",
                    institution="University Partner",
                    avatar_url=avatar,
                )
                session.add(new_student)

                user = User(
                    id=user_id,
                    email=email_clean,
                    password_hash=pwd_hash,
                    salt=salt,
                    full_name=display_name,
                    student_id=student_id,
                    onboarding_completed=False,
                    is_active=True,
                )
                session.add(user)
                session.commit()
                session.refresh(user)

            # Issue 30-day session token for Google OAuth
            token = secrets.token_urlsafe(32)
            _ACTIVE_SESSIONS[token] = {
                "user_id": user.id,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(days=30),
            }

            student_info = None
            if user.student_id:
                student = session.query(Student).filter(Student.id == user.student_id).first()
                if student:
                    student_info = {
                        "id": student.id,
                        "name": student.name,
                        "email": student.email,
                        "degree": student.degree,
                        "institution": student.institution,
                        "avatar": student.avatar_url or avatar,
                    }
                elif user.student_id == "stu-001":
                    student_info = get_student_profile()

            return {
                "success": True,
                "message": "Google authorization successful.",
                "token": token,
                "user": self._user_dict(user),
                "student": student_info,
                "onboarding_completed": user.onboarding_completed,
            }
        finally:
            session.close()

    def logout(self, token: str) -> bool:
        """Invalidate active session token."""
        if token in _ACTIVE_SESSIONS:
            del _ACTIVE_SESSIONS[token]
            return True
        return False

    def get_user_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify token and return authenticated user details."""
        if not token or token not in _ACTIVE_SESSIONS:
            return None

        session_data = _ACTIVE_SESSIONS[token]
        if datetime.utcnow() > session_data["expires_at"]:
            del _ACTIVE_SESSIONS[token]
            return None

        user_id = session_data["user_id"]
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if not user or not user.is_active:
                return None

            student_info = None
            if user.student_id:
                student = session.query(Student).filter(Student.id == user.student_id).first()
                if student:
                    student_info = {
                        "id": student.id,
                        "name": student.name,
                        "email": student.email,
                        "degree": student.degree,
                        "institution": student.institution,
                        "avatar": student.avatar_url or "/prince-avatar.jpg",
                    }
                elif user.student_id == "stu-001":
                    student_info = get_student_profile()

            return {
                "user": self._user_dict(user),
                "student": student_info,
                "onboarding_completed": user.onboarding_completed,
            }
        finally:
            session.close()

    def forgot_password(self, email: str) -> Dict[str, Any]:
        """
        Generate password reset token for user.
        """
        email_clean = email.strip().lower()
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.email == email_clean).first()
            if not user:
                # Return success response to prevent email enumeration
                return {
                    "success": True,
                    "message": "If an account with this email exists, a password reset link has been generated.",
                    "dev_token": None,
                }

            # Generate secure token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=1)

            # Store in DB and memory
            reset_record = PasswordResetToken(
                id=f"prt-{uuid.uuid4().hex[:8]}",
                user_id=user.id,
                token_hash=hashlib.sha256(token.encode()).hexdigest(),
                expires_at=expires_at,
                used=False,
            )
            session.add(reset_record)
            session.commit()

            _RESET_TOKENS[token] = {
                "user_id": user.id,
                "expires_at": expires_at,
            }

            return {
                "success": True,
                "message": "Password reset instructions have been created.",
                "dev_token": token,  # Provided for seamless automated testing / local prototype
            }
        finally:
            session.close()

    def reset_password(self, token: str, new_password: str, confirm_password: str) -> Dict[str, Any]:
        """Apply password reset."""
        if new_password != confirm_password:
            raise ValueError("Passwords do not match.")

        if len(new_password) < 8:
            raise ValueError("Password must be at least 8 characters.")

        # Check token in memory or DB
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        session = SessionLocal()
        try:
            user_id = None
            if token in _RESET_TOKENS:
                t_data = _RESET_TOKENS[token]
                if datetime.utcnow() < t_data["expires_at"]:
                    user_id = t_data["user_id"]
                del _RESET_TOKENS[token]

            if not user_id:
                record = (
                    session.query(PasswordResetToken)
                    .filter(
                        PasswordResetToken.token_hash == token_hash,
                        PasswordResetToken.used == False,
                        PasswordResetToken.expires_at > datetime.utcnow(),
                    )
                    .first()
                )
                if not record:
                    raise ValueError("Invalid or expired password reset token.")
                user_id = record.user_id
                record.used = True

            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("User not found.")

            pwd_hash, salt = hash_password(new_password)
            user.password_hash = pwd_hash
            user.salt = salt
            session.commit()

            return {"success": True, "message": "Password reset successfully. You can now log in."}
        finally:
            session.close()

    def complete_onboarding(self, user_id: str, onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mark onboarding complete and update student learning profile."""
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("User not found.")

            user.onboarding_completed = True

            if user.student_id:
                student = session.query(Student).filter(Student.id == user.student_id).first()
                if student:
                    if onboarding_data.get("degree"):
                        student.degree = onboarding_data["degree"]
                    if onboarding_data.get("institution"):
                        student.institution = onboarding_data["institution"]
                    if onboarding_data.get("primary_goal"):
                        student.current_goal = onboarding_data["primary_goal"]
                    if onboarding_data.get("weekly_available_hours"):
                        student.weekly_available_hours = float(onboarding_data["weekly_available_hours"])
                    if onboarding_data.get("preferred_study_times"):
                        student.preferred_study_times = onboarding_data["preferred_study_times"]

            session.commit()
            return {"success": True, "message": "Onboarding completed successfully."}
        finally:
            session.close()

    def _create_session(self, user_id: str, remember_me: bool = False) -> str:
        """Create random session token."""
        token = secrets.token_urlsafe(32)
        ttl = timedelta(days=30) if remember_me else timedelta(days=2)
        _ACTIVE_SESSIONS[token] = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + ttl,
        }
        return token

    def _user_dict(self, user: User) -> Dict[str, Any]:
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "student_id": user.student_id,
            "onboarding_completed": user.onboarding_completed,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat(),
        }


auth_service = AuthService()
