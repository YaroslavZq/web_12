from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactResponse
from src.repository import contacts as repository_contact
from src.services.auth import auth_service

router = APIRouter(prefix='/birthdays', tags=['birthdays'])


@router.get("/", response_model=List[ContactResponse])
async def get_birthday_contacts(current_user: User = Depends(auth_service.get_current_user),
                                db: Session = Depends(get_db)):
    contacts = await repository_contact.get_birthday_contacts(current_user, db)
    return contacts
