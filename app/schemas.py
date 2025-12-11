from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, model_validator

# ------------------
# USER SCHEMAS
# ------------------

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


# ------------------
# CALCULATION SCHEMAS
# ------------------

class CalculationBase(BaseModel):
    a: float
    b: float
    type: str   # FIXED — allows "Add", "Sub", "Multiply", "Divide"

    @model_validator(mode="after")
    def check_divide_by_zero(self):
        if self.type == "Divide" and self.b == 0:
            raise ValueError("b (divisor) cannot be zero for Divide type.")
        return self


class CalculationCreate(CalculationBase):
    pass


class CalculationRead(CalculationBase):
    id: int
    result: Optional[float] = None
    user_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ------------------
# STATS SCHEMA
# ------------------

class CalculationStats(BaseModel):
    total_calculations: int
    add_count: int
    sub_count: int
    multiply_count: int
    divide_count: int
    avg_a: Optional[float] = None
    avg_b: Optional[float] = None
