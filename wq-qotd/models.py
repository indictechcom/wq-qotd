from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./quotes.db"

# Database Setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Quote Model
class Quote(Base):
    __tablename__ = "quotes"
    id = Column(String, primary_key=True, index=True)
    quote = Column(String, nullable=False)
    author = Column(String, nullable=False)
    featured_date = Column(DateTime, unique=True, nullable=False)
