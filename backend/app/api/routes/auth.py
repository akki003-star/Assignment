from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.core.security import decode_access_token
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.schemas.auth import LoginRequest, TokenResponse
from backend.app.schemas.user import (
    PasswordReset,
    PasswordResetConfirm,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from backend.app.services.auth_service import AuthService
from backend.app.utils.route_helpers import value_error_to_http

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@value_error_to_http(status.HTTP_400_BAD_REQUEST)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(user_data)


@router.post("/login", response_model=TokenResponse)
@value_error_to_http(status.HTTP_401_UNAUTHORIZED)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(login_data.email, login_data.password)


@router.post("/password-reset")
@value_error_to_http(status.HTTP_404_NOT_FOUND)
def request_password_reset(data: PasswordReset, db: Session = Depends(get_db)):
    service = AuthService(db)
    token = service.reset_password_request(data.email)
    return {"message": "Password reset email sent", "reset_token": token}


@router.post("/password-reset/confirm")
@value_error_to_http(status.HTTP_400_BAD_REQUEST)
def confirm_password_reset(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    payload = decode_access_token(data.token)
    if not payload or payload.get("type") != "reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset token"
        )
    service = AuthService(db)
    service.reset_password_confirm(int(payload["sub"]), data.new_password)
    return {"message": "Password reset successful"}


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user
