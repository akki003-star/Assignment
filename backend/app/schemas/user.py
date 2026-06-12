from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    education: str | None = None
    skills: list[str] | None = None
    experience_years: int | None = None
    preferred_locations: list[str] | None = None
    expected_salary: float | None = None
    preferred_roles: list[str] | None = None


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
    new_password: str
