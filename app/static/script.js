const API_BASE_URL = '/api';
let currentPage = 1;

// Fetch Quote of the Day
async function fetchQuoteOfDay() {
    try {
        const response = await fetch(`${API_BASE_URL}/quote_of_the_day`);
        const data = await response.json();
        
        const quoteCard = document.getElementById('todayQuote');
        quoteCard.querySelector('.quote-text').textContent = `"${data.quote}"`;
        quoteCard.querySelector('.quote-author').textContent = `— ${data.author}`;
    } catch (error) {
        console.error('Error fetching quote of the day:', error);
        document.getElementById('todayQuote').querySelector('.quote-text').textContent = 
            'Failed to load quote of the day';
    }
}

// Search Quote by Date
async function searchByDate() {
    const date = document.getElementById('datePicker').value;
    const resultCard = document.getElementById('dateSearchResult');
    
    // Show the result card (we'll use it for both success and error states)
    resultCard.classList.remove('hidden');
    
    if (!date) {
        resultCard.innerHTML = `
            <div class="error-message">
                <p>Please select a date</p>
            </div>
        `;
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/quotes/${date}`);
        
        if (!response.ok) {
            throw new Error('No quote found');
        }
        
        const data = await response.json();

        if (data && data.quote) {
            resultCard.innerHTML = `
                <p class="quote-text">"${data.quote}"</p>
                <p class="quote-author">— ${data.author}</p>
                <p class="quote-date">Date: ${data.featured_date}</p>
            `;
        } else {
            resultCard.innerHTML = `
                <div class="error-message">
                    <p>No quote found for this date</p>
                </div>
            `;
        }
    } catch (error) {
        resultCard.innerHTML = `
            <div class="error-message">
                <p>No quote found for this date</p>
            </div>
        `;
    }
}

// Fetch All Quotes
async function fetchQuotes(page = 1, author = '') {
    try {
        let url = `${API_BASE_URL}/quotes?page=${page}`;
        if (author) {
            url += `&author=${encodeURIComponent(author)}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        const quotesList = document.getElementById('quotesList');
        quotesList.innerHTML = ''; // Clear existing quotes

        // Check if data is an array (direct quotes) or has items property
        const quotes = Array.isArray(data) ? data : (data.items || []);

        if (quotes.length === 0) {
            quotesList.innerHTML = '<div class="quote-card"><p class="quote-text">No quotes found</p></div>';
            return;
        }

        quotes.forEach(quote => {
            const quoteCard = document.createElement('div');
            quoteCard.className = 'quote-card';
            quoteCard.innerHTML = `
                <p class="quote-text">"${quote.quote}"</p>
                <p class="quote-author">— ${quote.author}</p>
                <p class="quote-date">Date: ${quote.featured_date}</p>
            `;
            quotesList.appendChild(quoteCard);
        });

        document.getElementById('pageInfo').textContent = `Page ${page}`;
        currentPage = page;
    } catch (error) {
        console.error('Error fetching quotes:', error);
        document.getElementById('quotesList').innerHTML = 
            '<div class="quote-card"><p class="error">No quotes found</p></div>';
    }
}

// Navigation functions
function previousPage() {
    if (currentPage > 1) {
        const author = document.getElementById('authorFilter').value;
        fetchQuotes(currentPage - 1, author);
    }
}

function nextPage() {
    const author = document.getElementById('authorFilter').value;
    fetchQuotes(currentPage + 1, author);
}

function filterQuotes() {
    const author = document.getElementById('authorFilter').value;
    fetchQuotes(1, author);
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    fetchQuoteOfDay();
    fetchQuotes();
}); 