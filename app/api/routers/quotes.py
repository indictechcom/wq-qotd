from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.models import SessionLocal
from app.schemas.schemas import Quote
from app.database.crud import add_quote_to_db, get_quote_by_date, get_all_quotes
from app.core.utils import fetch_quote_of_the_day_from_api
from datetime import datetime, timezone
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@router.get("/quote_of_the_day", response_model=Quote)
async def get_quote_of_the_day_route(db: Session = Depends(get_db)):
    """
    `/api/quote_of_the_day` route is used to get the Quote of the Day.

    First, we check if today's quote exists in our database.
    If it exists, we return it directly from the database.
    
    If today's quote is not in the database, we fetch it from the WikiQuote API
    as a fallback, store it in the database, and then return it.
    """
    # Get today's date
    today = datetime.now(timezone.utc).date()
    
    # Try to get today's quote from database
    logging.info(f"Attempting to get quote from DB for date: {today}")
    quote = get_quote_by_date(db, today)
    
    # If quote not found in database, fetch from API as fallback
    if not quote:
        logging.info("Quote not found in database, fetching from WikiQuote API")
        quote_data = fetch_quote_of_the_day_from_api()
        quote = add_quote_to_db(db, quote_data)
    
    return quote

@router.get("/quotes", response_model=List[Quote])
async def get_all_quotes_route(
    page: int = 1, limit: int = 10, author: Optional[str] = None, db: Session = Depends(get_db)
):
    return get_all_quotes(db, page, limit, author)

@router.get("/quotes/{date}", response_model=Quote)
async def get_quote_by_date_route(date: str, db: Session = Depends(get_db)):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    quote = get_quote_by_date(db, target_date)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found for the given date.")
    return quote