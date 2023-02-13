from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactResponse
from src.repository import contacts as repository_contact

router = APIRouter(prefix='/birthdays', tags=['birthdays'])


@router.get("/", response_model=List[ContactResponse])
async def get_birthday_contacts(db: Session = Depends(get_db)):
    contacts = await repository_contact.get_birthday_contacts(db)
    return contacts
