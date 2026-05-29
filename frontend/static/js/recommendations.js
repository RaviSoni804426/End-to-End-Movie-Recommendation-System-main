/* Recommendations Page JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    initializeRecommendations();
});

function initializeRecommendations() {
    const searchBtn = document.getElementById('searchBtn');
    const movieSearch = document.getElementById('movieSearch');
    
    if (searchBtn) {
        searchBtn.addEventListener('click', handleRecommendationSearch);
    }
    
    if (movieSearch) {
        movieSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleRecommendationSearch();
            }
        });
        
        // Initialize autocomplete if suggestions are available
        if (typeof suggestions !== 'undefined') {
            initializeAutocomplete(movieSearch, suggestions);
        }
    }
}

function initializeAutocomplete(inputElement, suggestions) {
    const ac = new autoComplete({
        data: {
            src: suggestions
        },
        selector: '#movieSearch',
        threshold: 2,
        debounce: 300,
        searchEngine: 'loose',
        placeHolder: 'Enter a movie title...',
        resultsList: {
            element: (list, data) => {
                if (!data.results.length) {
                    const message = document.createElement('div');
                    message.setAttribute('data-no-results', true);
                    message.textContent = 'No results found';
                    list.appendChild(message);
                }
            },
            noResults: true
        },
        resultItem: {
            highlight: true
        },
        onSelection: (feedback) => {
            inputElement.value = feedback.selection.value;
            handleRecommendationSearch();
        }
    });
}

async function handleRecommendationSearch() {
    const movieTitle = document.getElementById('movieSearch').value.trim();
    const resultContainer = document.getElementById('recommendations-result');
    
    if (!movieTitle) {
        showError(resultContainer, 'Please enter a movie title');
        return;
    }
    
    resultContainer.innerHTML = '';
    showLoading(resultContainer);
    
    try {
        const formData = new FormData();
        formData.append('movie_name', movieTitle);
        
        const response = await fetch('/recommendations', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        clearLoading(resultContainer);
        
        if (data.success) {
            displayRecommendations(data, resultContainer);
            showSuccess(resultContainer, `Found ${data.recommendations.length} recommendations for "${data.movie}"`);
        } else {
            showError(resultContainer, data.message);
        }
    } catch (error) {
        clearLoading(resultContainer);
        console.error('Error:', error);
        showError(resultContainer, 'An error occurred while fetching recommendations');
    }
}

function displayRecommendations(data, container) {
    const recommendations = data.recommendations;
    
    const grid = document.createElement('div');
    grid.className = 'recommendations-grid';
    
    recommendations.forEach((rec, index) => {
        const card = document.createElement('div');
        card.className = 'recommendation-item';
        
        const similarityPercent = (rec.similarity_score * 100).toFixed(1);
        
        card.innerHTML = `
            <div class="rec-rank">#${rec.rank}</div>
            <div class="rec-title">${rec.title}</div>
            <div class="rec-score">Match: ${similarityPercent}%</div>
            <button class="btn btn-secondary" onclick="addToWatchlist('${rec.title}')">
                <i class="fas fa-bookmark"></i> Save
            </button>
        `;
        
        grid.appendChild(card);
    });
    
    container.appendChild(grid);
}

function addToWatchlist(movieTitle) {
    let watchlist = JSON.parse(localStorage.getItem('watchlist') || '[]');
    
    if (!watchlist.includes(movieTitle)) {
        watchlist.push(movieTitle);
        localStorage.setItem('watchlist', JSON.stringify(watchlist));
        showSuccess(document.body, `Added "${movieTitle}" to watchlist`);
    } else {
        showError(document.body, `"${movieTitle}" is already in your watchlist`);
    }
}
