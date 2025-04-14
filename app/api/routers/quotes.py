from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.models import SessionLocal
from app.schemas.schemas import QuoteSchema
from app.database.crud import add_quote_to_db, get_quote_by_date, get_all_quotes
from app.core.utils import fetch_quote_of_the_day_from_api
from datetime import datetime

# Router instance
router = APIRouter(
    prefix="/api",
    tags=["Quotes"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/quote_of_the_day", response_model=QuoteSchema)
async def get_quote_of_the_day_route(db: Session = Depends(get_db)):
    """
    `/api/quote_of_the_day` route is used to get the Quote of the Day.

    First, we fetch the Quote of the Day from the WikiQuote API. Then, we check if that quote is present in the database.

    If the quote is NOT present in the database, it is added to the database and then returned.

    If the quote is present in the database, it is returned.
    """
    quote_data = fetch_quote_of_the_day_from_api()
    quote = get_quote_by_date(db, quote_data["featured_date"])
    if not quote:
        quote = add_quote_to_db(db, quote_data)
    return quote

@router.get("/quotes", response_model=List[QuoteSchema])
async def get_all_quotes_route(
    page: int = 1, limit: int = 10, author: Optional[str] = None, db: Session = Depends(get_db)
):
    return get_all_quotes(db, page, limit, author)

@router.get("/quotes/{date}", response_model=QuoteSchema)
async def get_quote_by_date_route(date: str, db: Session = Depends(get_db)):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    quote = get_quote_by_date(db, target_date)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found for the given date.")
    return quote