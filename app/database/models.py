from sqlalchemy import create_engine, Column, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Database Setup
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Enables automatic reconnection
    pool_recycle=3600,   # Recycle connections after 1 hour
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Quote Model
class Quote(Base):
    __tablename__ = "quotes"
    id = Column(String(32), primary_key=True, index=True)
    quote = Column(String(1000), nullable=False)
    author = Column(String(255), nullable=False)
    featured_date = Column(Date, unique=True, nullable=False)

    def __repr__(self):
        return f"<Quote(id={self.id}, author={self.author}, featured_date={self.featured_date})>"
