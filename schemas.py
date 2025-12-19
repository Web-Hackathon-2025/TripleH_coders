from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole
from app.models.booking import BookingStatus

# User Schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.CUSTOMER

class UserSchema(UserBase):
    id: int
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Service Schemas
class ServiceBase(BaseModel):
    title: str
    description: str
    category: str
    price: float
    location: str

class ServiceCreate(ServiceBase):
    pass

class ServiceSchema(ServiceBase):
    id: int
    provider_id: int

    class Config:
        from_attributes = True

# Booking Schemas
class BookingBase(BaseModel):
    service_id: int
    scheduled_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingSchema(BookingBase):
    id: int
    customer_id: int
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True
