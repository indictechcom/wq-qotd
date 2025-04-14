from pydantic import BaseModel
from datetime import date, datetime

# Quote Schema for Response
class QuoteSchema(BaseModel):
    id: str
    quote: str
    author: str
    featured_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True
