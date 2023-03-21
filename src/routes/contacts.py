from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactResponse, ContactFavoriteStatus, ContactModel
from src.repository import contacts as repository_contact
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts(limit: int = Query(10, le=1000), offset: int = 0, favorite: bool = None, first_name: str = None,
                       last_name: str = None, email: str = None,
                       current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The get_contacts function returns a list of contacts.

    :param limit: int: Limit the number of contacts returned
    :param le: Specify the maximum value of a parameter
    :param offset: int: Skip the first n contacts
    :param favorite: bool: Filter the contacts by favorite
    :param first_name: str: Filter the contacts by first name
    :param last_name: str: Filter the contacts by last name
    :param email: str: Filter the contacts by email
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contact.get_contacts(limit, offset, favorite, first_name, last_name, email,
                                                     current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int = Path(1, ge=1), current_user: User = Depends(auth_service.get_current_user),
                      db: Session = Depends(get_db)):
    """
    The get_contact function returns a contact by its id.
        If the user is not logged in, an error will be returned.
        If the contact does not exist, an error will be returned.

    :param contact_id: int: Get the contact_id from the url path
    :param ge: Specify the minimum value of the parameter
    :param current_user: User: Get the current user from the database
    :param db: Session: Create a database session
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contact.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contact.create_contact(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int = Path(1, ge=1),
                         current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id, and a body containing the updated information for that contact.
        It then checks if there is already a user with that id, and if so it updates their information to match what was passed in the body.

    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Identify the contact to be deleted
    :param ge: Set a minimum value for the path parameter
    :param current_user: User: Get the user who is making the request
    :param db: Session: Get the database session
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contact.update_contact(body, contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactFavoriteStatus, contact_id: int = Path(1, ge=1),
                         current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The update_contact function updates the favorite status of a contact.
        The function takes in a ContactFavoriteStatus object, which contains the new favorite status of the contact.
        It also takes in an integer representing the id of the contact to be updated and a User object representing
        who is making this request (the current user). Finally, it takes in an SQLAlchemy Session object that will be used
        to make changes to our database.

    :param body: ContactFavoriteStatus: Pass the data that is sent in the request body
    :param contact_id: int: Specify the id of the contact to be updated
    :param ge: Specify that the path parameter must be greater than or equal to 1
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the function
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await repository_contact.update_favorite_contact(body, contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int = Path(1, ge=1), current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The remove_contact function removes a contact from the database.
        The function takes in an integer representing the id of the contact to be removed,
        and returns a dictionary containing information about that contact.

    :param contact_id: int: Specify the id of the contact to be removed
    :param ge: Check if the contact_id is greater than or equal to 1
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contact.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
