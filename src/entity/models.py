from datetime import datetime, date

from sqlalchemy import String, DateTime, func, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import constants
from src.config import messages


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class Contact(Base):
    """Represents a contact in the system."""
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(
        String(
            constants.FIRST_NAME_MIN_LENGTH, 
            constants.FIRST_NAME_MAX_LENGTH
        ), 
        nullable=False,
        comment=messages.contact_schema_first_name.get('en')
    )
    last_name: Mapped[str] = mapped_column(
        String(constants.LAST_NAME_MIN_LENGTH, constants.LAST_NAME_MAX_LENGTH), 
        nullable=False,
        comment=messages.contact_schema_last_name.get('en')
    )
    email: Mapped[str] = mapped_column(
        String(constants.EMAIL_MIN_LENGTH, constants.EMAIL_MAX_LENGTH), 
        nullable=False,
        unique=True,
        index=True,
        comment=messages.contact_schema_email.get('en')
    )
    phone: Mapped[str | None] = mapped_column(
        String(constants.PHONE_MIN_LENGTH, constants.PHONE_MAX_LENGTH),
        nullable=True,
        comment=messages.contact_schema_phone.get('en')
    )
    birthday: Mapped[date | None] = mapped_column(
        Date, 
        nullable=True,
        comment=messages.contact_schema_birthday.get('en')
    )
    additional_info: Mapped[str | None] = mapped_column(
        String(255), 
        nullable=True,
        comment=messages.contact_schema_additional_info.get('en')
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now(),
        comment=messages.contact_schema_created_at.get('en')
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now(), 
        onupdate=func.now(),
        comment=messages.contact_schema_updated_at.get('en')
    )