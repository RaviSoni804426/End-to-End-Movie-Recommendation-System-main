/* Search Page JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
});

function initializeSearch() {
    const applyBtn = document.getElementById('applyFiltersBtn');
    
    if (applyBtn) {
        applyBtn.addEventListener('click', handleSearch);
    }
}

async function handleSearch() {
    const title = document.getElementById('movieTitle').value.trim();
    const genre = document.getElementById('genreSelect').value;
    const yearFrom = document.getElementById('yearFrom').value;
    const yearTo = document.getElementById('yearTo').value;
    
    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = '';
    
    if (!title && !genre && !yearFrom && !yearTo) {
        showError(resultsContainer, 'Please enter at least one search criteria');
        return;
    }
    
    showLoading(resultsContainer);
    
    try {
        let endpoint = '/api/v1/search';
        const params = [];
        
        if (title) params.push(`q=${encodeURIComponent(title)}`);
        if (genre) params.push(`genre=${encodeURIComponent(genre)}`);
        if (params.length > 0) {
            endpoint += '?' + params.join('&');
        }
        
        const response = await apiCall(endpoint);
        clearLoading(resultsContainer);
        
        if (response.success && response.results.length > 0) {
            displaySearchResults(response.results, resultsContainer);
        } else {
            resultsContainer.innerHTML = '<div class="empty-state"><i class="fas fa-search"></i><h3>No results found</h3></div>';
        }
    } catch (error) {
        clearLoading(resultsContainer);
        console.error('Error:', error);
        showError(resultsContainer, 'An error occurred during search');
    }
}

function displaySearchResults(results, container) {
    const grid = document.createElement('div');
    grid.className = 'recommendations-grid';
    
    results.forEach((movie) => {
        const card = document.createElement('div');
        card.className = 'recommendation-item';
        
        card.innerHTML = `
            <div class="rec-title">${movie.movie_title || movie.title || 'Unknown'}</div>
            ${movie.genre ? `<div class="rec-score">Genre: ${movie.genre}</div>` : ''}
            ${movie.year ? `<div class="rec-score">Year: ${movie.year}</div>` : ''}
            <button class="btn btn-primary" onclick="viewDetails('${movie.movie_title || movie.title}')">
                View Details
            </button>
        `;
        
        grid.appendChild(card);
    });
    
    container.appendChild(grid);
}

function viewDetails(movieTitle) {
    window.location.href = `/movie/${encodeURIComponent(movieTitle)}`;
}
