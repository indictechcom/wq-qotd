# Quote of the Day API

A FastAPI-based REST API that fetches and stores daily quotes from Wikiquote. The application provides endpoints to retrieve the quote of the day, search historical quotes, and filter quotes by author.

## Features

-   Fetch and store daily quotes from Wikiquote
-   Retrieve quote of the day
-   Search historical quotes by date
-   Filter quotes by author
-   Pagination support
-   MariaDB/MySQL database storage
-   Full Docker containerization with Docker Compose
-   Makefile for simplified development workflow
-   Clean and modular code structure

## Prerequisites

-   Docker and Docker Compose
-   Make (optional, but recommended for easier command management)

## Quick Start with Docker

1. Clone the repository:

    ```bash
    git clone https://github.com/indictechcom/wq-qotd.git
    cd wq-qotd
    ```

2. Create and configure a `.env` file from the example with your external database credentials:

    ```bash
    cp .env.example .env
    # now edit .env with your database details
    ```

3. Build and start the application:

    ```bash
    make up
    ```

4. Access the application:
    - Frontend: http://localhost:8000
    - API Documentation: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc

## Docker Development Setup

### Using Makefile Commands (Recommended)

The project includes a `Makefile` with convenient commands for managing the Docker environment:

```bash
# Show all available commands
make help

# Build the Docker images
make build

# Start all services in detached mode
make up

# View logs from all services
make logs

# View logs from backend only
make logs-backend

# Stop all services
make down

# Restart all services
make restart

# Open a shell in the backend container
make shell

# Show service status
make status

# Clean up (remove containers, networks, and volumes)
make clean

# Rebuild everything from scratch
make rebuild
```

### Using Docker Compose Directly

If you prefer to use Docker Compose commands directly:

```bash
# Build and start services
docker-compose up --build

# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Access backend container shell
docker-compose exec backend /bin/bash
```

## Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and provide the connection details for your external database:

```env
# Database Configuration
DB_HOST=your_external_db_host
DB_USER=your_external_db_user
DB_PASSWORD=your_external_db_password
DB_NAME=your_external_db_name
DB_PORT=your_external_db_port
```

## Development Workflow

1. **Start the development environment:**
   ```bash
   make dev
   ```

2. **Make code changes:** The application supports live reloading, so changes to the code will automatically restart the server.

3. **View logs:**
   ```bash
   make logs
   ```


## Traditional Installation (Alternative)

If you prefer to run the application without Docker:

### Prerequisites
-   Python 3.10+
-   pip (Python package manager)
-   MariaDB/MySQL database

### Setup Steps
1. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure environment variables in `.env`

4. Start the application:
    ```bash
    uvicorn main:app --reload
    ```

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
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
├── main.py
├── Dockerfile
├── docker-compose.yml
├── docker-compose-dev-db.yml (legacy)
├── Makefile
├── .dockerignore
├── requirements.txt
├── .env
├── .env.example
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
    -   `static/`: Frontend Related Code
-   `Dockerfile`: Multi-stage Docker configuration for the FastAPI application
-   `docker-compose.yml`: Docker Compose configuration for all services (backend + database)
-   `docker-compose-dev-db.yml`: Legacy Docker Compose configuration (database only)
-   `Makefile`: Convenient commands for managing the Docker environment
-   `.dockerignore`: Files and directories to exclude from Docker build context

## Frontend Implementation

The application includes a built-in frontend interface served directly from the FastAPI backend.

### Frontend Features
- Modern, responsive design
- Quote of the Day display
- Date-based quote search
- Author filtering
- Pagination for quote browsing
- Error handling and user feedback

### Frontend Structure
The frontend is located in the `app/static` directory:
```bash
app/static/
├── index.html    # Main HTML structure|
├── style.css     # custom CSS file
└── script.js     # Frontend logic and API interactions
```

### Frontend Technologies
- HTML5 for structure
- Bootstrap 5 (via Toolforge CDN) for responsive UI components and styling
- Vanilla JavaScript for functionality
- Wikimedia Fonts (Roboto) for typography


### Accessing the Frontend
The frontend is automatically served when you run the FastAPI application:


### Frontend Features Breakdown
- **Quote of the Day Section**
  - Automatically displays the current day's quote
  - Updates daily
  - Animated card layout

- **Date Search Section**
  - Date picker for historical quotes
  - Immediate feedback on search results
  - Error handling for invalid dates or missing quotes

- **Quote Collection Section**
  - Author-based filtering
  - Pagination controls
  - Responsive quote cards
  - Loading states and error handling


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
