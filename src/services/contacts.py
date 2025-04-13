from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactSchema, ContactUpdateSchema


class ContactService:
    """Contact service."""
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def get_contacts(self, limit: int, offset: int):
        """Get a list of contacts."""
        return await self.contact_repository.get_contacts(limit, offset)

    async def get_contact(self, contact_id: int):
        """Get a contact by ID."""
        return await self.contact_repository.get_contact_by_id(contact_id)

    async def create_contact(self, body: ContactSchema):
        """Create a new contact."""
        return await self.contact_repository.create_contact(body)

    async def remove_contact(self, contact_id: int):
        """Remove a contact by ID."""
        return await self.contact_repository.remove_contact(contact_id)

    async def update_contact(self, contact_id: int, body: ContactUpdateSchema):
        """Update a contact by ID."""
        return await self.contact_repository.update_contact(contact_id, body)

    async def search_contacts(self, query: str):
        """Search for contacts by query."""
        return await self.contact_repository.search_contacts(query)

    async def upcoming_birthdays(self):
        """Get contacts with upcoming birthdays."""
        today = date.today()
        end_date = today + timedelta(days=7)
        return await self.contact_repository.get_contacts_with_birthdays(
            today, end_date
        )