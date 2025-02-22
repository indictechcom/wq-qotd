from datetime import datetime, date
from sqlalchemy.orm import Session
from app.database.models import Quote
from typing import Optional, List
from sqlalchemy import func
# import uuid

def add_quote_to_db(db: Session, quote_data: dict) -> Quote:
    featured_date = datetime.fromisoformat(quote_data['featured_date']).date()
    quote = Quote(
        id=quote_data['id'],
        quote=quote_data['quote'],
        author=quote_data['author'],
        featured_date=featured_date
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
