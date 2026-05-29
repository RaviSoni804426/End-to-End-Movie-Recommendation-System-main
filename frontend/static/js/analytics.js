/* Analytics Dashboard JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    loadDashboardMetrics();
});

async function loadDashboardMetrics() {
    try {
        const metricsResponse = await apiCall('/api/v1/analytics/dashboard');
        const statsResponse = await apiCall('/api/v1/statistics');
        
        if (metricsResponse.success) {
            displayMetrics(metricsResponse.metrics);
        }
        
        if (statsResponse.success) {
            displayStats(statsResponse.statistics);
        }
        
        await loadTopSearches();
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showError(document.body, 'Error loading analytics');
    }
}

function displayMetrics(metrics) {
    // Update metric cards
    if (metrics.recommendations) {
        const totalRecs = metrics.recommendations.total_recommendations || 0;
        document.getElementById('totalSearches').textContent = totalRecs;
    }
    
    if (metrics.engagement_rate) {
        const engagementPercent = (metrics.engagement_rate * 100).toFixed(1);
        document.getElementById('engagementRate').textContent = engagementPercent + '%';
    }
}

function displayStats(stats) {
    if (stats.total_movies) {
        document.getElementById('totalMovies').textContent = formatNumber(stats.total_movies);
    }
    
    if (stats.average_rating) {
        document.getElementById('avgRating').textContent = stats.average_rating.toFixed(1);
    }
}

async function loadTopSearches() {
    try {
        const response = await apiCall('/api/v1/analytics/top-searches');
        
        if (response.success && response.top_searches) {
            displayTopSearches(response.top_searches);
        }
    } catch (error) {
        console.error('Error loading top searches:', error);
    }
}

function displayTopSearches(searches) {
    const container = document.getElementById('topSearches');
    
    if (!searches || searches.length === 0) {
        container.innerHTML = '<p>No search data available yet</p>';
        return;
    }
    
    let html = '<div class="search-list">';
    
    searches.forEach((search, index) => {
        html += `
            <div class="search-item">
                <span class="search-rank">${index + 1}</span>
                <span class="search-title">${search.movie || search.search_term}</span>
                <span class="search-count">${search.search_count} searches</span>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}
