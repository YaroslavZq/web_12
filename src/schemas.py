from datetime import date
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
