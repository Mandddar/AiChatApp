from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
