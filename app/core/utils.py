import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import re

QOTD_API = 'https://en.wikiquote.org/w/api.php'
PARAMS = {
    "action": "parse",
    "format": "json",
    "page": "Wikiquote:Quote_of_the_day",
    "prop": "text",
    "formatversion": "2"
}

def fetch_quote_of_the_day_from_api() -> dict:
    response = requests.get(QOTD_API, params=PARAMS)
    response.raise_for_status()
    data = response.json()
    quote_html = data['parse']['text']
    return extract_quote(quote_html)

def extract_quote(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, 'html.parser')
    quote, author, featured_date = "Quote_not_found", "Author_not_found", None

    for tbody in soup.find_all("tbody"):
        quote_element = tbody.find("td")
        author_element = tbody.find("td", style="font-size:smaller;").find("a") if tbody.find("td", style="font-size:smaller;") else None

        if quote_element:
            quote = ' '.join(quote_element.stripped_strings)
        if author_element:
            author = author_element.get_text(strip=True)

        date_text = soup.get_text()
        date_pattern = "Today is ([^;]+);"
        date_match = re.search(date_pattern, date_text)
        if date_match:
            date_string = date_match.group(1).strip()
            featured_date = datetime.strptime(date_string, '%A, %B %d, %Y')
            featured_date = featured_date.isoformat()

        if quote and author and featured_date:
            break

    unique_id = hashlib.md5(f"{quote}_{author}".encode()).hexdigest()
    current_time = datetime.now(timezone.utc).isoformat()

    return {
        "id": unique_id,
        "quote": quote,
        "author": author,
        "featured_date": featured_date,
        "created_at": current_time,
        "updated_at": current_time
    }
