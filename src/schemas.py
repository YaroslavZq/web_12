from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    birth_date: date = Field()
    favorite: bool = False
    phone: str = Field('', max_length=12)


class ContactFavoriteStatus(BaseModel):
    favorite: bool = False


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: str
    birth_date: date
    favorite: bool
    phone: str

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
