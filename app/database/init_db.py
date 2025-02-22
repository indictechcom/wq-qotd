from app.database.models import Base, engine
from app.core.config import settings
import mysql.connector
import time

def wait_for_db():
    max_retries = 10
    retry_interval = 2

    for attempt in range(max_retries):
        try:
            # Try to connect to MySQL/MariaDB
            conn = mysql.connector.connect(
                host=settings.DB_HOST,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                port=settings.DB_PORT,
                database=settings.DB_NAME
            )
            conn.close()
            print("Successfully connected to the database!")
            return True
        except mysql.connector.Error as e:
            print(f"Database connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                print("Maximum retries reached.")
                raise
    
    raise Exception("Could not connect to database after maximum retries")

def init_database():
    # Wait for database to be ready
    wait_for_db()

    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database() 