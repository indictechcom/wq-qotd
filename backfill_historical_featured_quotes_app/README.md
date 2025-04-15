# Historical Quote Backfill Tool

A utility application for the Quote of the Day API that backfills historical quotes from Wikiquote archives into the database. This tool retrieves quotes from Wikiquote's monthly archives dating back to 2007 and populates the database with properly formatted quotes.

## Purpose

This tool addresses the need to populate the Quote of the Day database with historical quotes that have been featured on Wikiquote. Rather than starting with an empty database, this application allows for the entire history of quotes to be available through the API.

## Features

-   Scrapes historical quotes from Wikiquote's monthly archives
-   Handles multiple HTML parsing formats (quotes changed format in 2012)
-   Processes quotes concurrently using asyncio
-   Automatically creates quote entries with proper date formats (YYYY-MM-DD)
-   Handles edge cases like missing authors or quote text
-   Validates URLs before attempting to process them

## Prerequisites

-   Python 3.10+
-   Access to a MariaDB/MySQL database (configured in the main project's .env file)
-   The main wq-qotd application (this is a supporting module)

## Configuration

The application uses the following configuration files:

-   `quotes-extraction-config.json`: Contains URLs to all monthly quote pages from 2007 to present

## Usage

Run the application from the project root
(after activating the virtual environment, as described in the main README.md):

```bash
python -m backfill_historical_featured_quotes_app
```

## How It Works

1. The application loads the quotes configuration from `quotes-extraction-config.json`
2. For each URL in the configuration:
    - Validates the URL format
    - Checks if the URL is accessible
    - Extracts quote data using the Wikiquote API
    - Determines the appropriate parser based on the year/month (format changed in 2012)
    - Parses the quote data to extract quotes, authors, and dates
    - Stores the properly formatted quotes in the database

## Module Structure

-   `__main__.py`: Entry point for the module
-   `main.py`: Contains the main processing logic and async coordination
-   `quotes-extraction-config.json`: Configuration file with URLs to scrape
-   `core/`: Core functionality
    -   `config.py`: Configuration settings using Pydantic
    -   `utils.py`: Utility functions for URL validation, quote extraction, and parsing

## Parsing Logic

The application uses three different parsing functions to handle different formats that Wikiquote has used over time. During 2012, Wikiquote underwent two significant format changes to their Quote of the Day pages.

### Parser Selection Logic

The application automatically selects the appropriate parser for each URL based on the following rules:

```python
if int_year > 2012:
    # For years after 2012, use April 2012 parser (most advanced)
    parser_type = "april_2012"
elif int_year == 2012:
    if month_name == "january":
        # January 2012 uses the old format
        parser_type = "old"
    elif month_name in ["february", "march"]:
        # February and March 2012 use the Feb 2012 format
        parser_type = "feb_2012"
    else:
        # April 2012 and later months in 2012 use the April 2012 format
        parser_type = "april_2012"
else:
    # Years before 2012 use the old parser
    parser_type = "old"
```

### Format Changes and Parsers

1. **Original Format (Before February 2012)**

    - Parser: `parse_monthly_quote_data`
    - Quote Format: Simple table structure with quotes typically in the third table cell
    - Author Format: Usually separated from the quote by a tilde (~)
    - HTML Structure: Uses `<dt>` elements for dates followed by `<table>` elements

2. **February 2012 Format (February-March 2012)**

    - Parser: `parse_monthly_quote_data_Feb2012_and_later`
    - Changes: Modified table structure and introduction of new HTML elements
    - Quote Format: Quotes now in a more complex layout with different container elements
    - Author Format: Still typically uses tildes but with different surrounding markup

3. **April 2012 Format (April 2012 onwards)**
    - Parser: `parse_monthly_quote_data_April2012_and_later`
    - Changes: Complete redesign with list structure instead of tables
    - Quote Format: Uses `<li>` elements with more structured data
    - Author Format: More consistently formatted with clear author attribution

Each parser contains specialized logic to handle the specific HTML structure and formatting conventions of its target time period, ensuring accurate extraction regardless of when the quote was featured.

## Notes

-   The tool is intended to be run once to populate the database
-   Running it multiple times should be safe as it will not create duplicate entries
-   The process may take some time to complete due to the large number of pages being processed
