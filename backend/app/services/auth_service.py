from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, hash_password, verify_password
from backend.app.models.user import User
from backend.app.schemas.auth import TokenResponse
from backend.app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, user_data: UserCreate) -> User:
        existing = self.db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise ValueError("Email already registered")

        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            full_name=user_data.full_name,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, email: str, password: str) -> TokenResponse:
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        token = create_access_token(data={"sub": str(user.id)})
        return TokenResponse(access_token=token)

    def reset_password_request(self, email: str) -> str:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("User not found")
        token = create_access_token(data={"sub": str(user.id), "type": "reset"})
        return token

    def reset_password_confirm(self, user_id: int, new_password: str) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        user.hashed_password = hash_password(new_password)
        self.db.commit()
