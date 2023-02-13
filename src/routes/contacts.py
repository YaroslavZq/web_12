from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactResponse, ContactFavoriteStatus, ContactModel
from src.repository import contacts as repository_contact

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(limit: int = Query(10, le=1000), offset: int = 0, favorite: bool = None, first_name: str = None,
                       last_name: str = None, email: str = None, db: Session = Depends(get_db)):
    contacts = await repository_contact.get_contacts(limit, offset, favorite, first_name, last_name, email, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    contact = await repository_contact.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contact.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    contact = await repository_contact.update_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactFavoriteStatus, contact_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    contact = await repository_contact.update_favorite_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    contact = await repository_contact.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact

