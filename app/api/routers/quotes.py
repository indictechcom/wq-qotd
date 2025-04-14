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
async def get_quote_of_the_day(db: Session = Depends(get_db)):
    """
    `/api/quote_of_the_day` route is used to get the quote of the day directly from WikiQuote API.

    The reason for fetching the quote directly from the API (and not from the database) is to "get the latest quote of the day, based on what is currently featured on the WikiQuote page `Wikiquote:Quote_of_the_day`".
    
    We are not fetching the current quote of the day directly from the database, because the user might be in different timezones (thus different date) and the date on the WikiQuote page might be different, as WikiQuote uses UTC time.

    If the quote is not present in the database, it is added to the database.

    We might change this approach in the future, where the `quote_of_the_day` is fetched from the database directly, once we have implemented the daily job runner to update the quote of the day daily in the database.
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