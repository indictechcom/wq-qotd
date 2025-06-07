const API_BASE_URL = '/api';
let currentPage = 1;
let searchTimeout;
let allQuotes = []; // Store all quotes for client-side filtering
let isSearchMode = false;

// Utility: Clear all children of a node
function clearElement(el) {
    while (el.firstChild) {
        el.removeChild(el.firstChild);
    }
}

// Utility: Create a quote card element
function createQuoteCard(quote) {
    const col = document.createElement('div');
    col.className = 'col-lg-6 col-xl-4';
    
    const card = document.createElement('div');
    card.className = 'card h-100 border-0 shadow-sm card-hover';
    
    const cardBody = document.createElement('div');
    cardBody.className = 'card-body d-flex flex-column p-4';
    
    // Quote icon
    const quoteIcon = document.createElement('i');
    quoteIcon.className = 'bi bi-quote text-primary fs-2 mb-3';
    
    // Quote text
    const quoteText = document.createElement('blockquote');
    quoteText.className = 'blockquote flex-grow-1';
    
    const quoteP = document.createElement('p');
    quoteP.className = 'quote-text mb-0';
    quoteP.textContent = `"${quote.quote}"`;
    
    const footer = document.createElement('footer');
    footer.className = 'blockquote-footer mt-3';
    
    const authorCite = document.createElement('cite');
    authorCite.className = 'quote-author';
    authorCite.textContent = quote.author;
    
    const dateSpan = document.createElement('span');
    dateSpan.className = 'quote-date d-block mt-1';
    dateSpan.textContent = `Featured: ${quote.featured_date}`;
    
    // Build the structure
    footer.appendChild(authorCite);
    footer.appendChild(dateSpan);
    quoteText.appendChild(quoteP);
    quoteText.appendChild(footer);
    cardBody.appendChild(quoteIcon);
    cardBody.appendChild(quoteText);
    card.appendChild(cardBody);
    col.appendChild(card);
    
    return col;
}

// Utility: Create error message
function createErrorMessage(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-info d-flex align-items-center';
    
    const icon = document.createElement('i');
    icon.className = 'bi bi-info-circle me-2';
    
    const textSpan = document.createElement('span');
    textSpan.textContent = message;
    
    alertDiv.appendChild(icon);
    alertDiv.appendChild(textSpan);
    
    return alertDiv;
}

// Fetch Quote of the Day
async function fetchQuoteOfDay() {
    try {
        const response = await fetch(`${API_BASE_URL}/quote_of_the_day`);
        const data = await response.json();

        const quoteText = document.getElementById('quoteText');
        const quoteAuthor = document.getElementById('quoteAuthor');

        quoteText.textContent = `"${data.quote}"`;
        quoteAuthor.textContent = `— ${data.author}`;
    } catch (error) {
        console.error('Error fetching quote of the day:', error);
        const quoteText = document.getElementById('quoteText');
        quoteText.textContent = 'Failed to load quote of the day';
    }
}

// Search Quote by Date
async function searchByDate() {
    const date = document.getElementById('datePicker').value;
    const resultCard = document.getElementById('dateSearchResult');
    
    resultCard.classList.remove('d-none');
    clearElement(resultCard);

    if (!date) {
        const errorMsg = createErrorMessage('Please select a date');
        resultCard.appendChild(errorMsg);
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/quotes/${date}`);
        if (!response.ok) throw new Error('No quote found');
        const data = await response.json();

        if (data && data.quote) {
            const quoteP = document.createElement('p');
            quoteP.className = 'quote-text mb-3 fst-italic';
            quoteP.textContent = `"${data.quote}"`;
            
            const authorP = document.createElement('p');
            authorP.className = 'quote-author text-end mb-2';
            authorP.textContent = `— ${data.author}`;
            
            const dateP = document.createElement('p');
            dateP.className = 'quote-date text-end mb-0';
            dateP.textContent = `Date: ${data.featured_date}`;
            
            resultCard.appendChild(quoteP);
            resultCard.appendChild(authorP);
            resultCard.appendChild(dateP);
        } else {
            const errorMsg = createErrorMessage('No quote found for this date');
            resultCard.appendChild(errorMsg);
        }
    } catch (error) {
        const errorMsg = createErrorMessage('No quote found for this date');
        resultCard.appendChild(errorMsg);
    }
}

// Fetch All Quotes and store them
async function fetchAllQuotesInitial() {
    try {
        // First, try to get a reasonable number of quotes for filtering
        const response = await fetch(`${API_BASE_URL}/quotes?page=1&limit=100`);
        const data = await response.json();
        
        const quotes = Array.isArray(data) ? data : (data.items || []);
        allQuotes = quotes;
        
        displayQuotes(quotes.slice(0, 12)); // Show first 12 quotes initially
        updatePagination(1, Math.ceil(quotes.length / 12));
    } catch (error) {
        console.error('Error fetching quotes:', error);
        // Fallback to original method
        fetchQuotes(1);
    }
}

// Display quotes with pagination
function displayQuotes(quotes, page = 1) {
    const quotesList = document.getElementById('quotesList');
    clearElement(quotesList);

    if (quotes.length === 0) {
        const col = document.createElement('div');
        col.className = 'col-12';
        const errorMsg = createErrorMessage('No quotes found matching your search');
        col.appendChild(errorMsg);
        quotesList.appendChild(col);
        return;
    }

    quotes.forEach(quote => {
        const quoteCard = createQuoteCard(quote);
        quotesList.appendChild(quoteCard);
    });

    currentPage = page;
}

// Update pagination display
function updatePagination(page, totalPages) {
    document.getElementById('pageInfo').textContent = `Page ${page} of ${totalPages}`;
    
    // Enable/disable pagination buttons based on current page
    const prevBtn = document.querySelector('button[onclick="previousPage()"]');
    const nextBtn = document.querySelector('button[onclick="nextPage()"]');
    
    prevBtn.disabled = page <= 1;
    nextBtn.disabled = page >= totalPages;
}

// Dynamic search function
function performDynamicSearch(searchTerm) {
    const statusDiv = document.getElementById('searchStatus');
    const statusText = document.getElementById('searchStatusText');
    
    if (searchTerm.trim() === '') {
        // Show all quotes when search is empty
        isSearchMode = false;
        statusDiv.classList.add('d-none');
        const quotesToShow = allQuotes.slice(0, 12);
        displayQuotes(quotesToShow);
        updatePagination(1, Math.ceil(allQuotes.length / 12));
        return;
    }

    isSearchMode = true;
    statusDiv.classList.remove('d-none');
    statusText.textContent = `Searching for "${searchTerm}"...`;

    // Filter quotes based on search term (author or quote content)
    const filteredQuotes = allQuotes.filter(quote => {
        const authorMatch = quote.author.toLowerCase().includes(searchTerm.toLowerCase());
        const quoteMatch = quote.quote.toLowerCase().includes(searchTerm.toLowerCase());
        return authorMatch || quoteMatch;
    });

    // Update status
    if (filteredQuotes.length === 0) {
        statusText.textContent = `No results found for "${searchTerm}"`;
    } else {
        statusText.textContent = `Found ${filteredQuotes.length} result${filteredQuotes.length > 1 ? 's' : ''} for "${searchTerm}"`;
    }

    // Display filtered results (first 12)
    const quotesToShow = filteredQuotes.slice(0, 12);
    displayQuotes(quotesToShow);
    updatePagination(1, Math.ceil(filteredQuotes.length / 12));
}

// Setup dynamic search
function setupDynamicSearch() {
    const searchInput = document.getElementById('authorFilter');
    
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value;
        
        // Clear previous timeout
        clearTimeout(searchTimeout);
        
        // Set new timeout for 300ms delay (debouncing)
        searchTimeout = setTimeout(() => {
            performDynamicSearch(searchTerm);
        }, 300);
    });

    // Also trigger search on Enter key
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            clearTimeout(searchTimeout);
            performDynamicSearch(e.target.value);
        }
    });
}

// Clear filter function
function clearFilter() {
    const searchInput = document.getElementById('authorFilter');
    searchInput.value = '';
    performDynamicSearch('');
}

// Fallback fetch function for compatibility
async function fetchQuotes(page = 1, author = '') {
    try {
        let url = `${API_BASE_URL}/quotes?page=${page}`;
        if (author) {
            url += `&author=${encodeURIComponent(author)}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        const quotesList = document.getElementById('quotesList');
        clearElement(quotesList);

        const quotes = Array.isArray(data) ? data : (data.items || []);

        if (quotes.length === 0) {
            const col = document.createElement('div');
            col.className = 'col-12';
            const errorMsg = createErrorMessage('No quotes found');
            col.appendChild(errorMsg);
            quotesList.appendChild(col);
            return;
        }

        quotes.forEach(quote => {
            const quoteCard = createQuoteCard(quote);
            quotesList.appendChild(quoteCard);
        });

        document.getElementById('pageInfo').textContent = `Page ${page}`;
        currentPage = page;
    } catch (error) {
        console.error('Error fetching quotes:', error);
        const quotesList = document.getElementById('quotesList');
        clearElement(quotesList);

        const col = document.createElement('div');
        col.className = 'col-12';
        const errorMsg = createErrorMessage('Error loading quotes');
        col.appendChild(errorMsg);
        quotesList.appendChild(col);
    }
}

// Navigation functions
function previousPage() {
    if (currentPage > 1) {
        if (isSearchMode) {
            const searchTerm = document.getElementById('authorFilter').value;
            const filteredQuotes = allQuotes.filter(quote => {
                const authorMatch = quote.author.toLowerCase().includes(searchTerm.toLowerCase());
                const quoteMatch = quote.quote.toLowerCase().includes(searchTerm.toLowerCase());
                return authorMatch || quoteMatch;
            });
            const startIndex = (currentPage - 2) * 12;
            const quotesToShow = filteredQuotes.slice(startIndex, startIndex + 12);
            displayQuotes(quotesToShow, currentPage - 1);
            updatePagination(currentPage - 1, Math.ceil(filteredQuotes.length / 12));
        } else {
            const startIndex = (currentPage - 2) * 12;
            const quotesToShow = allQuotes.slice(startIndex, startIndex + 12);
            displayQuotes(quotesToShow, currentPage - 1);
            updatePagination(currentPage - 1, Math.ceil(allQuotes.length / 12));
        }
    }
}

function nextPage() {
    if (isSearchMode) {
        const searchTerm = document.getElementById('authorFilter').value;
        const filteredQuotes = allQuotes.filter(quote => {
            const authorMatch = quote.author.toLowerCase().includes(searchTerm.toLowerCase());
            const quoteMatch = quote.quote.toLowerCase().includes(searchTerm.toLowerCase());
            return authorMatch || quoteMatch;
        });
        const totalPages = Math.ceil(filteredQuotes.length / 12);
        if (currentPage < totalPages) {
            const startIndex = currentPage * 12;
            const quotesToShow = filteredQuotes.slice(startIndex, startIndex + 12);
            displayQuotes(quotesToShow, currentPage + 1);
            updatePagination(currentPage + 1, totalPages);
        }
    } else {
        const totalPages = Math.ceil(allQuotes.length / 12);
        if (currentPage < totalPages) {
            const startIndex = currentPage * 12;
            const quotesToShow = allQuotes.slice(startIndex, startIndex + 12);
            displayQuotes(quotesToShow, currentPage + 1);
            updatePagination(currentPage + 1, totalPages);
        }
    }
}

function filterQuotes() {
    const author = document.getElementById('authorFilter').value;
    performDynamicSearch(author);
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    fetchQuoteOfDay();
    fetchAllQuotesInitial();
    setupDynamicSearch();
});