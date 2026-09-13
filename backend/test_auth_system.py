"""
Comprehensive Authentication & Session Test Suite for LearnMate.

Tests 20 core cases:
1. Register successfully.
2. Invalid registration (e.g. invalid email format).
3. Duplicate email rejection.
4. Weak password rejection.
5. Password mismatch rejection.
6. Login successfully.
7. Wrong password rejection.
8. Unknown email rejection.
9. Logout (session invalidation).
10. Access protected page/endpoint while logged out.
11. Access protected page/endpoint while logged in.
12. New user redirects to onboarding (onboarding_completed: false).
13. Existing user redirects to dashboard (onboarding_completed: true).
14. Session persistence via token/cookie.
15. Forgot password request.
16. Password reset with token.
17. API authentication via Bearer header.
18. Unauthorized API request.
19. Refresh / session check (/api/auth/me).
20. Multiple login attempts without lockout/crash.
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.services.auth_service import auth_service

app = create_app()
client = TestClient(app)

TEST_RUN_ID = uuid.uuid4().hex[:6]
TEST_USER_EMAIL = f"learner.test_{TEST_RUN_ID}@university.edu"
TEST_ONBOARD_EMAIL = f"new.onboard_{TEST_RUN_ID}@university.edu"


# 1. Register successfully
def test_01_register_success():
    payload = {
        "full_name": "Test Learner",
        "email": TEST_USER_EMAIL,
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!",
        "terms": True,
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["email"] == TEST_USER_EMAIL
    assert data["onboarding_completed"] is False


# 2. Invalid registration
def test_02_invalid_registration_email():
    payload = {
        "full_name": "Bad Email User",
        "email": "not-an-email",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!",
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 422


# 3. Duplicate email
def test_03_duplicate_email():
    payload = {
        "full_name": "Duplicate User",
        "email": TEST_USER_EMAIL,  # already created in test 1
        "password": "AnotherPassword123!",
        "confirm_password": "AnotherPassword123!",
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 400
    assert "already exists" in res.json()["detail"].lower()


# 4. Weak password
def test_04_weak_password():
    payload = {
        "full_name": "Weak Pass User",
        "email": "weak.pass@university.edu",
        "password": "short",
        "confirm_password": "short",
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code in [400, 422]


# 5. Password mismatch
def test_05_password_mismatch():
    payload = {
        "full_name": "Mismatch User",
        "email": "mismatch@university.edu",
        "password": "SecurePassword123!",
        "confirm_password": "DifferentPassword123!",
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 400
    assert "do not match" in res.json()["detail"].lower()


# 6. Login successfully
def test_06_login_success():
    payload = {
        "email": "prince.singh@university.edu",
        "password": "LearnMate2025!",
        "remember_me": True,
    }
    res = client.post("/api/auth/login", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["onboarding_completed"] is True
    assert "learnmate_session" in res.cookies or "token" in data


# 7. Wrong password
def test_07_wrong_password():
    payload = {
        "email": "prince.singh@university.edu",
        "password": "WrongPassword!",
    }
    res = client.post("/api/auth/login", json=payload)
    assert res.status_code == 401
    assert "invalid email or password" in res.json()["detail"].lower()


# 8. Unknown email
def test_08_unknown_email():
    payload = {
        "email": "nonexistent@university.edu",
        "password": "SomePassword123!",
    }
    res = client.post("/api/auth/login", json=payload)
    assert res.status_code == 401
    assert "invalid email or password" in res.json()["detail"].lower()


# 9. Logout
def test_09_logout():
    # Login first
    login_res = client.post(
        "/api/auth/login",
        json={"email": "prince.singh@university.edu", "password": "LearnMate2025!"},
    )
    token = login_res.json()["token"]

    # Logout with token
    res = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json()["success"] is True

    # Token should now be invalid
    check_res = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert check_res.status_code == 401


# 10. Access protected page while logged out
def test_10_protected_access_logged_out():
    res = client.get("/api/auth/me")
    assert res.status_code == 401


# 11. Access protected page while logged in
def test_11_protected_access_logged_in():
    login_res = client.post(
        "/api/auth/login",
        json={"email": "prince.singh@university.edu", "password": "LearnMate2025!"},
    )
    token = login_res.json()["token"]

    res = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["user"]["email"] == "prince.singh@university.edu"
    assert data["student"]["name"] == "Prince Singh"


# 12. New user redirects to onboarding
def test_12_new_user_onboarding_incomplete():
    res = client.post(
        "/api/auth/register",
        json={
            "full_name": "New Student Onboard",
            "email": TEST_ONBOARD_EMAIL,
            "password": "Password123!",
            "confirm_password": "Password123!",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["onboarding_completed"] is False
    assert data["user"]["onboarding_completed"] is False


# 13. Existing user redirects to dashboard
def test_13_existing_user_onboarding_completed():
    res = client.post(
        "/api/auth/login",
        json={"email": "prince.singh@university.edu", "password": "LearnMate2025!"},
    )
    assert res.status_code == 200
    assert res.json()["onboarding_completed"] is True


# 14. Session persistence
def test_14_session_persistence():
    login_res = client.post(
        "/api/auth/login",
        json={"email": "prince.singh@university.edu", "password": "LearnMate2025!"},
    )
    token = login_res.json()["token"]
    user_state = auth_service.get_user_by_token(token)
    assert user_state is not None
    assert user_state["user"]["full_name"] == "Prince Singh"


# 15. Forgot password
def test_15_forgot_password():
    res = client.post(
        "/api/auth/forgot-password",
        json={"email": "prince.singh@university.edu"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["dev_token"] is not None


# 16. Password reset
def test_16_password_reset():
    # Request token
    forgot_res = client.post(
        "/api/auth/forgot-password",
        json={"email": TEST_USER_EMAIL},
    )
    assert forgot_res.status_code == 200
    token = forgot_res.json()["dev_token"]

    # Reset password
    reset_res = client.post(
        "/api/auth/reset-password",
        json={
            "token": token,
            "new_password": "UpdatedPassword2026!",
            "confirm_password": "UpdatedPassword2026!",
        },
    )
    assert reset_res.status_code == 200
    assert reset_res.json()["success"] is True

    # Login with new password
    login_res = client.post(
        "/api/auth/login",
        json={
            "email": TEST_USER_EMAIL,
            "password": "UpdatedPassword2026!",
        },
    )
    assert login_res.status_code == 200


# 17. API authentication
def test_17_api_auth_bearer():
    login_res = client.post(
        "/api/auth/login",
        json={"email": "prince.singh@university.edu", "password": "LearnMate2025!"},
    )
    token = login_res.json()["token"]

    res = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200


# 18. Unauthorized API request
def test_18_unauthorized_api_request():
    res = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid-fake-token-xyz"},
    )
    assert res.status_code == 401


# 19. Session check on reload (/api/auth/me)
def test_19_session_check_reload():
    login_res = client.post(
        "/api/auth/login",
        json={"email": "prince.singh@university.edu", "password": "LearnMate2025!"},
    )
    token = login_res.json()["token"]

    # Simulate frontend mounting and checking session
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert "user" in res.json()
    assert "student" in res.json()


# 20. Multiple login attempts
def test_20_multiple_login_attempts():
    for _ in range(5):
        res = client.post(
            "/api/auth/login",
            json={"email": "prince.singh@university.edu", "password": "LearnMate2025!"},
        )
        assert res.status_code == 200


# 21. Google authorization with existing student
def test_21_google_auth_existing_user():
    payload = {
        "email": "prince.singh@university.edu",
        "full_name": "Prince Singh",
        "avatar_url": "/prince-avatar.jpg",
        "google_id": "google-10928374",
    }
    res = client.post("/api/auth/google", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["email"] == "prince.singh@university.edu"
    assert data["student"]["name"] == "Prince Singh"
    assert data["onboarding_completed"] is True


# 22. Google authorization with new student
def test_22_google_auth_new_user():
    new_google_email = f"google.scholar_{uuid.uuid4().hex[:6]}@gmail.com"
    payload = {
        "email": new_google_email,
        "full_name": "Google Scholar",
        "avatar_url": "/prince-avatar.jpg",
        "google_id": "google-new-987654",
    }
    res = client.post("/api/auth/google", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["email"] == new_google_email
    assert data["onboarding_completed"] is False
