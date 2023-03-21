from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactFavoriteStatus


async def get_contacts(limit: int, offset: int, favorite: bool, first_name: str, last_name: str, email: str
                       , user: User, db: Session):
    """
    The get_contacts function returns a list of contacts from the database.
        The function takes in limit, offset, favorite, first_name, last_name and email as parameters.
        If favorite is not None then it filters the query by whether or not the contact is a favorite.
        If first_name is not None then it filters the query by whether or not that string matches with any part of
            any contact's first name (case insensitive).  This also applies to last name and email.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Determine how many contacts to skip before returning the results
    :param favorite: bool: Filter the contacts by favorite status
    :param first_name: str: Filter the contacts by first name
    :param last_name: str: Filter contacts by their last name
    :param email: str: Filter contacts by email
    :param user: User: Get the user_id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id)
    if favorite is not None:
        contacts = contacts.filter(Contact.favorite == favorite)
    if first_name is not None:
        contacts = contacts.filter(Contact.first_name.like(f'{first_name}%'))
    if last_name is not None:
        contacts = contacts.filter(Contact.last_name.like(f'{last_name}%'))
    if email is not None:
        contacts = contacts.filter(Contact.email.like(f'{email}%'))
    contacts = contacts.limit(limit).offset(offset).all()
    return contacts


async def get_contact(contact_id: int, user: User, db: Session):
    """
    The get_contact function takes in a contact_id and user, and returns the contact with that id.
        Args:
            contact_id (int): The id of the desired Contact object.
            user (User): The User object associated with this Contact.

    :param contact_id: int: Filter the database query
    :param user: User: Get the user id from the token
    :param db: Session: Pass the database session to the function
    :return: The contact object with the given id
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param user: User: Get the user id from the jwt token
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, contact_id: int, user: User, db: Session):
    """
    The update_contact function updates a contact in the database.
        Args:
            body (ContactModel): The updated contact information.
            contact_id (int): The id of the contact to update.
            user (User): The current user, used for authorization purposes.

    :param body: ContactModel: Get the contact information from the request body
    :param contact_id: int: Identify the contact to be deleted
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.birth_date = body.birth_date
        contact.favorite = body.favorite
        contact.phone = body.phone
        db.commit()
    return contact


async def update_favorite_contact(body: ContactFavoriteStatus, contact_id: int, user: User, db: Session):
    """
    The update_favorite_contact function updates the favorite status of a contact.
        Args:
            body (ContactFavoriteStatus): The new favorite status for the contact.
            contact_id (int): The id of the contact to update.
            user (User): The current logged in user, used to ensure that only contacts belonging to this user are updated.

    :param body: ContactFavoriteStatus: Pass the data to the function
    :param contact_id: int: Identify the contact that is being updated
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.favorite = body.favorite
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact. This is used to ensure that only contacts belonging to this
                user are deleted, and not contacts belonging to other users with similar IDs.

    :param contact_id: int: Identify the contact to be removed
    :param user: User: Get the user from the database
    :param db: Session: Pass the database session to the function
    :return: The contact that was removed
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_birthday_contacts(user: User, db: Session):
    """
    The get_birthday_contacts function returns a list of contacts whose birthdays are within the next 7 days.
        The function takes in two parameters: user and db. User is an object that contains information about the current
        user, such as their id, email address, hashed password etc. Db is a Session object that allows us to query our
        database for data.

    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    today = datetime.now().date()
    last_day = today + timedelta(7)
    contacts = db.query(Contact).filter(Contact.user_id == user.id)\
        .where(func.to_char(Contact.birth_date, 'MM-DD').between(datetime.strftime(today, "%m-%d"),
                                                                 datetime.strftime(last_day, "%m-%d"))).all()
    return contacts

