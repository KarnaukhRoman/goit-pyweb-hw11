import contextlib
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactUpdate, ContactCreate


class ContactABC(ABC):

    @abstractmethod
    async def get_contacts(self, skip: int, limit: int) -> List[Contact]:
        pass

    @abstractmethod
    async def get_contact(self, id: int) -> Contact:
        pass

    @abstractmethod
    async def get_contacts_birthday(self, days_number: int) -> List[Contact]:
        pass

    # @abstractmethod
    # async def get_contacts_by_name(self, name: str) -> List[Contact]:
    #     pass

    @abstractmethod
    async def create_contact(self, body: ContactCreate) -> Contact:
        pass

    @abstractmethod
    async def update_contact(self, contact_id: int, body: ContactUpdate) -> Contact:
        pass

    @abstractmethod
    async def delete_contact(self, id: int):
        pass


class ContactDB(ContactABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_contacts(self, offset: int, limit: int, first_name: Optional[str] = None, last_name: Optional[str] = None, email: Optional[str] = None) -> List[Contact]:
        stmt = select(Contact).offset(offset).limit(limit)
        if first_name:
            stmt = stmt.where(Contact.first_name.ilike(f'%{first_name}%'))
        if last_name:
            stmt = stmt.where(Contact.last_name.ilike(f'%{last_name}%'))
        if email:
            stmt = stmt.where(Contact.email.ilike(f'%{email}%'))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_contact(self, id: int) -> Contact:
        stmt = select(Contact).where(Contact.id == id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_contacts_birthday(self, days_number: int) -> List[Contact]:
        today = datetime.today()
        next_week = today + timedelta(days=days_number)
        today_month_day = today.strftime('%m-%d')
        next_week_month_day = next_week.strftime('%m-%d')

        print(f"Searching for birthdays between {today_month_day} and {next_week_month_day}")

        stmt = select(Contact).where(
            func.to_char(Contact.birthday, 'MM-DD').between(today_month_day, next_week_month_day)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create_contact(self, body: ContactCreate) -> Contact:
        contact = Contact(
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            phone=body.phone,
            birthday=body.birthday,
            additional_info=body.additional_info
        )
        self._session.add(contact)
        await self._session.commit()
        await self._session.refresh(contact)
        return contact

    async def update_contact(self, contact_id: int, body: ContactUpdate) -> Contact:
        try:
            contact = await self.get_contact(contact_id)
            print(contact)
            if not contact:
                return None
            update_data = body.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(contact, key, value)
            await self._session.commit()
            await self._session.refresh(contact)
            return contact
        except SQLAlchemyError as e:
            # Обробка помилок бази даних
            print(f"Error occurred: {e}")
            raise

    async def delete_contact(self, contact_id: int):
        try:
            contact = await self.get_contact(contact_id)
            if not contact:
                return None
            await self._session.delete(contact)
            await self._session.commit()
            return contact
        except SQLAlchemyError as e:
            # Обробка помилок бази даних
            print(f"Error occurred: {e}")
            raise

