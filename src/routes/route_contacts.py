from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import text

from src.database.connect import Database
from src.repository.contacts import ContactDB
from src.schemas import ContactsResponse, ContactCreate, ContactUpdate

router = APIRouter()
database = Database()

@router.get("/healthchecker", tags=["default"])
async def get_healthcheck(contact_db: ContactDB = Depends(database.get_contact_db)):
    try:
        # Make a simple query
        result = await contact_db.healthcheck()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI. The API is up and running!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Could not connect to the database")


@router.get("/", response_model=List[ContactsResponse])
async def read_contacts(limit: int = 100, offset: int = 0,
                        first_name: Optional[str] = Query(None),
                        last_name: Optional[str] = Query(None),
                        email: Optional[str] = Query(None),
                        contact_db: ContactDB = Depends(database.get_contact_db)):
    contacts = await contact_db.get_contacts(offset=offset, limit=limit, first_name=first_name, last_name=last_name, email=email)
    return contacts


@router.get("/{contact_id}", response_model=ContactsResponse)
async def read_contact(contact_id: int, contact_db: ContactDB = Depends(database.get_contact_db)):
    contact = await contact_db.get_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact id = {contact_id} not found")
    return contact


@router.get("/birthday/{days_number}", response_model=List[ContactsResponse])
async def read_contacts_birthday(days_number: int = Path(ge=7), contact_db: ContactDB = Depends(database.get_contact_db)):
    contacts = await contact_db.get_contacts_birthday(days_number=days_number)
    return contacts


@router.post("/", response_model=ContactsResponse)
async def create_contact(body: ContactCreate, contact_db: ContactDB = Depends(database.get_contact_db)):
    contact = await contact_db.create_contact(body=body)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactUpdate, contact_id: int = Path(ge=1), contact_db: ContactDB = Depends(database.get_contact_db)):
    contact = await contact_db.update_contact(contact_id=contact_id, body=body)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact with id={contact_id} not found")
    return contact


@router.delete("/{contact_id}", status_code=204)
async def delete_contact(contact_id: int, contact_db: ContactDB = Depends(database.get_contact_db)):
    contact = await contact_db.delete_contact(contact_id=contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact with id={contact_id} not found")

