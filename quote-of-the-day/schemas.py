from pydantic import BaseModel
from datetime import datetime

# Quote Schema for Response
class QuoteSchema(BaseModel):
    id: str
    quote: str
    author: str
    featured_date: datetime

    class Config:
        # orm_mode = True
        from_attributes = True
