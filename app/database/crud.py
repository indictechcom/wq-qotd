from datetime import datetime, date, timezone
from sqlalchemy.orm import Session
from app.database.models import Quote
from typing import Optional, List, Any
from sqlalchemy import func
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_quote_to_db(db: Session, quote_data: dict) -> Quote:
    featured_date = datetime.fromisoformat(quote_data['featured_date']).date()
    current_time = datetime.now(timezone.utc)
    
    quote = Quote(
        id=quote_data['id'],
        quote=quote_data['quote'],
        author=quote_data['author'],
        featured_date=featured_date,
        created_at=current_time,
        updated_at=current_time
    )
    db.add(quote)
    db.commit()
    db.refresh(quote)
    
    return quote

def get_quote_by_date(db: Session, target_date: str):
    if isinstance(target_date, (datetime, date)):
        target_date = target_date.isoformat()
    
    target_date_obj = datetime.fromisoformat(target_date).date()
    return db.query(Quote).filter(Quote.featured_date == target_date_obj).first()

def get_all_quotes(db: Session, page: int, limit: int, author: Optional[str] = None) -> List[Quote]:
    query = db.query(Quote)
    if author:
        query = query.filter(Quote.author.ilike(f"%{author}%"))
    return query.offset((page - 1) * limit).limit(limit).all()

def create_multiple_quotes(db: Session, quotes: List[Any]) -> List[Quote]:
    """
    Create multiple quotes in the database from a list of Pydantic QuoteCreate objects.
    
    Args:
        db: SQLAlchemy database session
        quotes: List of QuoteCreate objects
        
    Returns:
        List of created Quote objects
    """
    try:
        # Create SQLAlchemy model instances from Pydantic models
        current_time = datetime.now(timezone.utc)
        db_quotes = []
        
        for quote in quotes:
            # Convert Pydantic model to dict
            try:
                quote_dict = quote.model_dump()
            except AttributeError:
                # If it's already a dict
                quote_dict = quote
                
            # Generate an ID if not provided
            if 'id' not in quote_dict:
                # Create a hash based on quote text and date to ensure uniqueness
                unique_id = hashlib.md5(f"{quote_dict['quote']}_{quote_dict['author']}_{quote_dict['featured_date']}".encode()).hexdigest()
                quote_dict['id'] = unique_id
                
            # Set timestamps if not provided
            if 'created_at' not in quote_dict:
                quote_dict['created_at'] = current_time
            if 'updated_at' not in quote_dict:
                quote_dict['updated_at'] = current_time
                
            db_quote = Quote(**quote_dict)
            db_quotes.append(db_quote)
            
        # Add all quotes to the session
        db.add_all(db_quotes)
        # Commit the transaction to persist the objects
        db.commit()
        
        return db_quotes
    except Exception as e:
        db.rollback()  # Roll back on error
        logger.error(f"Error creating quotes: {str(e)}")
        raise