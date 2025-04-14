from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class QuoteBase(BaseModel):
    """Base schema for Quote with required fields."""
    quote: str
    author: str
    featured_date: date

class QuoteCreate(QuoteBase):
    """Schema for creating a new quote, inherits all fields from QuoteBase."""
    pass

# Quote Schema for Response
class Quote(QuoteBase):
    """Schema for representing a quote from the database with all fields."""
    id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
