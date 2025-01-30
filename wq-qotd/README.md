# Quote of the Day API

A FastAPI-based REST API that fetches and stores daily quotes from Wikiquote. The application provides endpoints to retrieve the quote of the day, search historical quotes, and filter quotes by author.

## Features

- Fetch and store daily quotes from Wikiquote
- Retrieve quote of the day
- Search historical quotes by date
- Filter quotes by author
- Pagination support
- SQLite database storage

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wiki-featured-content-feed.git
   cd wiki-featured-content-feed
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

1. Create a `.env` file in the project root:
   ```
   DATABASE_URL=sqlite:///./quotes.db
   ```

2. Initialize the database:
   ```bash
   python init_db.py
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /quote/today`: Get today's quote
- `GET /quotes/{date}`: Get quote by date (YYYY-MM-DD)
- `GET /quotes/author/{author}`: Get quotes by author
- `GET /quotes`: Get all quotes (with pagination)

## Development

### Project Structure
```
quote-of-the-day/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── routes/
├── tests/
├── .env
├── requirements.txt
└── README.md
```

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Keep pull requests focused on a single feature/fix

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Wikiquote](https://www.wikiquote.org/) for providing the quotes
- [FastAPI](https://fastapi.tiangolo.com/) framework