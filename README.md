# Quote of the Day API

A FastAPI-based REST API that fetches and stores daily quotes from Wikiquote. The application provides endpoints to retrieve the quote of the day, search historical quotes, and filter quotes by author.

## Features

-   Fetch and store daily quotes from Wikiquote
-   Retrieve quote of the day
-   Search historical quotes by date
-   Filter quotes by author
-   Pagination support
-   MariaDB/MySQL database storage
-   Docker support for development database (docker-compose-dev-db.yml)
-   Clean and modular code structure

## Prerequisites

-   Python 3.10+
-   pip (Python package manager)
-   MariaDB/MySQL database (or Docker for running the development database locally)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/indictechcom/wq-qotd.git
    cd wq-qotd
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - Unix/MacOS:
        ```bash
        source venv/bin/activate
        ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `.env` file in the project root using `.env.example` as a template:

    ```env
    # Database Configuration
    DB_HOST=localhost
    DB_USER=your_username
    DB_PASSWORD=your_password
    DB_NAME=your_database
    DB_PORT=3306

    # Backfill Historical Featured Quotes App
    WIKIQUOTE_BASE_URL='https://en.wikiquote.org/wiki/'
    MAX_RETRIES=3
    TIMEOUT_SECONDS=10
    ```

## Docker Development Database

For local development, you can use the provided Docker Compose setup to run a MariaDB instance:

```bash
docker-compose -f docker-compose-dev-db.yml up -d
```

This will start a MariaDB instance with the following configuration:

-   Database: s56492\_\_wq-qotd-db
-   Port: 32768:3306
-   Root Password: root

## Running the Application

1. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. Access the API documentation at:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc

## API Endpoints

-   `GET /`: List all available routes
-   `GET /api/quote_of_the_day`: Get today's quote
-   `GET /api/quotes/{date}`: Get quote by date (YYYY-MM-DD)
-   `GET /api/quotes`: Get all quotes (with pagination and author filter)

## Project Structure

```
wq-qotd/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routers/
│   │       └── quotes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── utils.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   └── init_db.py
│   └── schemas/
│       ├── __init__.py
│       └── schemas.py
├── backfill_historical_featured_quotes_app/
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py
│   ├── quotes-extraction-config.json
│   ├── README.md
│   └── core/
│       ├── config.py
│       └── utils.py
├── main.py
├── docker-compose-dev-db.yml
├── requirements.txt
├── .env
├── .env.example
├── .env.production
└── README.md
```

### Directory Structure Explanation

-   `app/`: Main application package
    -   `api/`: API-related code
        -   `routers/`: FastAPI route handlers
    -   `core/`: Core application code
        -   `config.py`: Configuration settings
        -   `utils.py`: Utility functions
    -   `database/`: Database-related code
        -   `crud.py`: Database operations
        -   `models.py`: SQLAlchemy models
        -   `init_db.py`: Database initialization
    -   `schemas/`: Pydantic models for request/response validation
-   `backfill_historical_featured_quotes_app/`: Utility for populating historical quotes
-   `docker-compose-dev-db.yml`: Docker Compose configuration for local development database

## Historical Quote Backfill Tool

The project includes a specialized utility module (`backfill_historical_featured_quotes_app`) designed to populate the database with historical quotes from Wikiquote archives. This tool is particularly useful for:

-   Initial database setup with quotes dating back to 2007
-   Repopulating the database after a reset
-   Adding missing historical quotes

### Features of the Backfill Tool

-   Scrapes and processes Wikiquote's monthly quote archives
-   Handles parsing of multiple HTML formats (Wikiquote changed its format in 2012)
-   Uses asyncio for concurrent processing of multiple months/years
-   Properly formats date information for database storage

### Running the Backfill Tool

To populate your database with historical quotes, run the following command from the project root after activating your virtual environment:

```bash
python -m backfill_historical_featured_quotes_app
```

This process may take several minutes depending on your internet connection, as it fetches and processes many pages of quotes.

For more details about the backfill tool, see the [dedicated README](/backfill_historical_featured_quotes_app/README.md) in the backfill module directory.

## Data Model

### Quote

-   `id`: String (32 chars) - MD5 hash of quote, author and featured_date
-   `quote`: String - The quote text
-   `author`: String - The quote's author
-   `featured_date`: Date - The date the quote was featured (YYYY-MM-DD)
-   `created_at`: Date - The date the quote was created (YYYY-MM-DD HH:MM:SS)
-   `updated_at`: Date - The date the quote was updated (YYYY-MM-DD HH:MM:SS)

## Development

### Code Style

-   Follow PEP 8 style guide for Python code
-   Use type hints for better code readability
-   Write descriptive docstrings for functions and classes
-   Keep functions small and focused
-   Use meaningful variable and function names

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

-   [Wikiquote](https://www.wikiquote.org/) for providing the quotes
-   [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework
-   [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM
-   [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
-   [MariaDB](https://mariadb.org/) for the database system
-   [Docker](https://www.docker.com/) for containerization support
-   [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for web scraping functionality
