from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, model_validator
from .models import CalculationType

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CalculationBase(BaseModel):
    a: float
    b: float
    type: CalculationType

    @model_validator(mode="after")
    def check_divide_by_zero(self):
        # This runs AFTER a, b, and type are all set
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("b (divisor) cannot be zero for Divide type.")
        return self


class CalculationCreate(CalculationBase):
    """Input schema for creating a calculation."""
    pass


class CalculationRead(CalculationBase):
    id: int
    result: Optional[float] = None
    user_id: Optional[int] = None
    created_at: datetime

    # Pydantic v2 config: read from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


