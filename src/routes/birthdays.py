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
    """
    The get_birthday_contacts function returns a list of contacts that have birthdays in the current month.
        The function takes two parameters:
            - current_user: A User object representing the currently logged-in user. This is passed by default to all
                            endpoints, and is used to determine which contacts belong to this user. It's also used for
                            authorization purposes (i.e., only users with an admin role can access certain endpoints).

    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Get the database session
    :return: A list of contacts with birthdays today
    :doc-author: Trelent
    """
    contacts = await repository_contact.get_birthday_contacts(current_user, db)
    return contacts
