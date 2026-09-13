"""
Pydantic Schemas for Authentication and Onboarding.
"""

from typing import Optional, List, Dict, Any
import re
from pydantic import BaseModel, Field, field_validator


EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)
    terms: bool = True

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v_clean = v.strip().lower()
        if not re.match(EMAIL_REGEX, v_clean):
            raise ValueError("Invalid email address format.")
        return v_clean


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=1)
    remember_me: bool = False

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v_clean = v.strip().lower()
        if not re.match(EMAIL_REGEX, v_clean):
            raise ValueError("Invalid email address format.")
        return v_clean


class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., min_length=3)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v_clean = v.strip().lower()
        if not re.match(EMAIL_REGEX, v_clean):
            raise ValueError("Invalid email address format.")
        return v_clean


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)


class GoogleAuthRequest(BaseModel):
    email: str = Field(..., min_length=3)
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    google_id: Optional[str] = None
    id_token: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v_clean = v.strip().lower()
        if not re.match(EMAIL_REGEX, v_clean):
            raise ValueError("Invalid email address format.")
        return v_clean


class OnboardingRequest(BaseModel):
    degree: Optional[str] = "B.Tech (CSE)"
    institution: Optional[str] = "Institute of Technology"
    primary_goal: Optional[str] = "Master Data Structures & Algorithms"
    target_deadline: Optional[str] = "2025-11-30"
    weekly_available_hours: Optional[float] = 15.0
    preferred_study_times: Optional[List[str]] = ["morning", "evening"]
    focus_topics: Optional[List[str]] = ["Dynamic Programming", "Graphs"]


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    student_id: Optional[str] = None
    onboarding_completed: bool = False
    is_active: bool = True
    created_at: str


class AuthResponse(BaseModel):
    success: bool
    message: str
    token: str
    user: UserResponse
    student: Optional[Dict[str, Any]] = None
    onboarding_completed: bool


class MessageResponse(BaseModel):
    success: bool
    message: str
    dev_token: Optional[str] = None
