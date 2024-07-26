from datetime import date

from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column('id', Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    birthday: Mapped[date] = mapped_column(Date)
    additional_info: Mapped[str | None] = mapped_column(String, nullable=True)