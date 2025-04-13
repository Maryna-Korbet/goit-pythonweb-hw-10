from fastapi import FastAPI, Request, Depends, HTTPException, status

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.routes import contacts
from src.database.db import get_db


app = FastAPI()

app.include_router(contacts.router, prefix="/api")


@app.get("/")
def read_root(request: Request):
    """Root endpoint."""
    return {"message": "Contacts_app v1.0"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """Healthchecker endpoint."""
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )