"""
FastAPI Authentication Routes.

Exposes:
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- GET  /api/auth/me
- POST /api/auth/forgot-password
- POST /api/auth/reset-password
- POST /api/auth/onboarding
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Header, Response, Request, status
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    GoogleAuthRequest,
    AuthResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    OnboardingRequest,
    MessageResponse,
)
from app.services.auth_service import auth_service

router = APIRouter()


def get_token_from_request(
    request: Request,
    authorization: Optional[str] = Header(None),
) -> Optional[str]:
    """Extract session token from Authorization Bearer header or HTTP-only cookie."""
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]
    cookie_token = request.cookies.get("learnmate_session")
    if cookie_token:
        return cookie_token
    return None


def get_current_user_data(
    token: Optional[str] = Depends(get_token_from_request),
):
    """Dependency: authenticate current user."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
        )
    user_data = auth_service.get_user_by_token(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please log in again.",
        )
    return user_data


@router.post("/register", response_model=AuthResponse)
async def register_student(payload: RegisterRequest, response: Response):
    """Register a new student account."""
    try:
        res = auth_service.register(
            full_name=payload.full_name,
            email=payload.email,
            password=payload.password,
            confirm_password=payload.confirm_password,
        )
        # Set HTTP-only cookie for secure session
        response.set_cookie(
            key="learnmate_session",
            value=res["token"],
            httponly=True,
            samesite="lax",
            max_age=172800,  # 2 days
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed.")


@router.post("/login", response_model=AuthResponse)
async def login_student(payload: LoginRequest, response: Response):
    """Authenticate student credentials."""
    try:
        res = auth_service.login(
            email=payload.email,
            password=payload.password,
            remember_me=payload.remember_me,
        )
        max_age = 2592000 if payload.remember_me else 172800  # 30 days vs 2 days
        response.set_cookie(
            key="learnmate_session",
            value=res["token"],
            httponly=True,
            samesite="lax",
            max_age=max_age,
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed.")


@router.post("/google", response_model=AuthResponse)
async def authenticate_google_user(payload: GoogleAuthRequest, response: Response):
    """Authenticate or register student using Google Authorization."""
    try:
        res = auth_service.authenticate_google(
            email=payload.email,
            full_name=payload.full_name,
            avatar_url=payload.avatar_url,
            google_id=payload.google_id,
        )
        response.set_cookie(
            key="learnmate_session",
            value=res["token"],
            httponly=True,
            samesite="lax",
            max_age=2592000,
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Google authentication failed.")


@router.post("/logout", response_model=MessageResponse)
async def logout_student(response: Response, token: Optional[str] = Depends(get_token_from_request)):
    """Invalidate session and clear cookie."""
    if token:
        auth_service.logout(token)
    response.delete_cookie(key="learnmate_session")
    return {"success": True, "message": "Successfully logged out."}


@router.get("/me")
async def get_current_user_profile(user_data: dict = Depends(get_current_user_data)):
    """Get authenticated user profile and student linkage."""
    return user_data


@router.post("/forgot-password", response_model=MessageResponse)
async def request_password_reset(payload: ForgotPasswordRequest):
    """Generate password reset token."""
    res = auth_service.forgot_password(payload.email)
    return res


@router.post("/reset-password", response_model=MessageResponse)
async def confirm_password_reset(payload: ResetPasswordRequest):
    """Apply new password with reset token."""
    try:
        res = auth_service.reset_password(
            token=payload.token,
            new_password=payload.new_password,
            confirm_password=payload.confirm_password,
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/onboarding", response_model=MessageResponse)
async def submit_student_onboarding(
    payload: OnboardingRequest,
    user_data: dict = Depends(get_current_user_data),
):
    """Complete initial student onboarding setup."""
    user_id = user_data["user"]["id"]
    try:
        res = auth_service.complete_onboarding(user_id, payload.model_dump())
        return res
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
