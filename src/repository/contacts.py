from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.models import Contact
from src.schemas import ContactModel, ContactFavoriteStatus


async def get_contacts(limit: int, offset: int, favorite: bool, first_name: str, last_name: str, email: str,
                       db: Session):
    contacts = db.query(Contact)
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


async def get_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.birth_date = body.birth_date
        contact.favorite = body.favorite
        contact.phone = body.phone
        db.commit()
    return contact


async def update_favorite_contact(body: ContactFavoriteStatus, contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.favorite = body.favorite
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_birthday_contacts(db: Session):
    today = datetime.now().date()
    last_day = today + timedelta(7)
    contacts = db.query(Contact)\
        .where(func.to_char(Contact.birth_date, 'MM-DD').between(datetime.strftime(today, "%m-%d"),
                                                                 datetime.strftime(last_day, "%m-%d"))).all()
    return contacts

