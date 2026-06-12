from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=200)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=200)
    phone: str | None = Field(None, max_length=30)
    education: str | None = Field(None, max_length=500)
    skills: list[str] | None = Field(None, max_length=50)
    experience_years: int | None = Field(None, ge=0, le=80)
    preferred_locations: list[str] | None = Field(None, max_length=20)
    expected_salary: float | None = Field(None, ge=0)
    preferred_roles: list[str] | None = Field(None, max_length=20)


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: str | None = None
    education: str | None = None
    skills: list[str] = []
    experience_years: int = 0
    preferred_locations: list[str] = []
    expected_salary: float | None = None
    preferred_roles: list[str] = []

    model_config = ConfigDict(from_attributes=True)


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v
