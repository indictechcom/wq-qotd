from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "qotd")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))

    # for mysql/mariadb
    @property
    def DATABASE_URL(self) -> str:
        # Use this format when connecting to a MySQL database over a standard TCP/IP connection.
        return f"mysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # Use this format when connecting to a MySQL database via a Unix socket.
        # return f"mysql+mysqldb://{self.DB_USER}:{self.DB_PASSWORD}@localhost/{self.DB_NAME}?unix_socket=/var/run/mysqld/mysqld.sock"

    # for postgres (commented out)
    # @property
    # def DATABASE_URL(self) -> str:
    #     return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings() 