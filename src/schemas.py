from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactsBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: str | None = None


class ContactCreate(ContactsBase):
    pass

class ContactsResponse(ContactsBase):
    id: int


class ContactUpdate(ContactsBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None
