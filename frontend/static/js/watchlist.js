/* Watchlist Page JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    loadWatchlist();
});

function loadWatchlist() {
    const watchlist = JSON.parse(localStorage.getItem('watchlist') || '[]');
    const container = document.getElementById('watchlistItems');
    const emptyState = document.getElementById('emptyState');
    
    if (watchlist.length === 0) {
        emptyState.style.display = 'block';
        container.innerHTML = '';
        return;
    }
    
    emptyState.style.display = 'none';
    
    const grid = document.createElement('div');
    grid.className = 'recommendations-grid';
    
    watchlist.forEach((movieTitle, index) => {
        const card = document.createElement('div');
        card.className = 'recommendation-item';
        
        card.innerHTML = `
            <div class="rec-title">${movieTitle}</div>
            <button class="btn btn-secondary" onclick="removeFromWatchlist(${index})">
                <i class="fas fa-trash"></i> Remove
            </button>
        `;
        
        grid.appendChild(card);
    });
    
    container.innerHTML = '';
    container.appendChild(grid);
}

function removeFromWatchlist(index) {
    let watchlist = JSON.parse(localStorage.getItem('watchlist') || '[]');
    const removed = watchlist[index];
    watchlist.splice(index, 1);
    localStorage.setItem('watchlist', JSON.stringify(watchlist));
    loadWatchlist();
    showSuccess(document.body, `Removed "${removed}" from watchlist`);
}
