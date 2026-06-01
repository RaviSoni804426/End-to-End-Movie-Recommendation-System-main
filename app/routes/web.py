"""Web routes for CineMatch"""

from flask import Blueprint, render_template, request, jsonify
import logging

from src.models.recommendation_engine import recommendation_engine
from src.services.movie_service import movie_service

logger = logging.getLogger(__name__)

web_bp = Blueprint('web', __name__)


@web_bp.route('/', methods=['GET'])
def home():
    """Home page with movie suggestions."""
    try:
        suggestions = movie_service.get_all_titles()
        return render_template('index.html', suggestions=suggestions)
    except Exception as e:
        logger.error(f"Error loading home: {e}")
        return render_template('index.html', suggestions=[])


@web_bp.route('/search', methods=['GET'])
def search_page():
    """Advanced search page."""
    return render_template('search.html')


@web_bp.route('/watchlist', methods=['GET'])
def watchlist_page():
    """Watchlist page."""
    return render_template('watchlist.html')


@web_bp.route('/dashboard', methods=['GET'])
def dashboard_page():
    """Analytics dashboard page."""
    try:
        total_movies = len(movie_service.get_data())
        movie_stats = {
            'total_movies': total_movies,
            'average_rating': 7.2  # default baseline TMDB rating representation
        }
        return render_template('dashboard.html', movie_stats=movie_stats)
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return render_template('dashboard.html', movie_stats={'total_movies': 0, 'average_rating': 0.0})


@web_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get recommendations for a movie."""
    try:
        movie_title = request.form.get('movie_name', '').strip()
        
        if not movie_title:
            return jsonify({
                'success': False,
                'message': 'Please enter a movie title'
            }), 400
        
        movie_data = movie_service.get_data()
        
        if movie_data.empty:
            return jsonify({
                'success': False,
                'message': 'Movie database not loaded'
            }), 500
        
        # Get recommendations from engine
        success, result = recommendation_engine.get_similar_movies(
            movie_title,
            movie_data,
            num_recommendations=10
        )
        
        if not success:
            return jsonify({
                'success': False,
                'message': result
            }), 404
        
        return jsonify({
            'success': True,
            'movie': movie_title.title(),
            'recommendations': result
        })
    
    except Exception as e:
        logger.error(f"Error in recommendations: {e}")
        return jsonify({
            'success': False,
            'message': 'Error generating recommendations'
        }), 500


@web_bp.route('/movie/<path:movie_title>', methods=['GET'])
def movie_details(movie_title):
    """Movie details page with context recommendations."""
    try:
        movie_data = movie_service.get_data()
        if movie_data.empty:
            return render_template('404.html'), 404
            
        movie_title_lower = movie_title.lower().strip()
        matching_movies = movie_data[
            movie_data['movie_title'].str.lower() == movie_title_lower
        ]
        
        if matching_movies.empty:
            logger.warning(f"Movie details requested for non-existent title: {movie_title}")
            return render_template('404.html'), 404
            
        movie_row = matching_movies.iloc[0]
        movie_details_dict = movie_row.to_dict()
        
        # Format strings for presentation
        if 'movie_title' in movie_details_dict:
            movie_details_dict['movie_title'] = str(movie_details_dict['movie_title']).title()
            
        # Get recommendations
        success, rec_list = recommendation_engine.get_similar_movies(
            movie_title,
            movie_data,
            num_recommendations=10
        )
        
        recommendations = rec_list if success else []
        
        return render_template(
            'movie.html',
            movie=movie_details_dict,
            recommendations=recommendations
        )
    except Exception as e:
        logger.error(f"Error loading movie details page: {e}")
        return render_template('404.html'), 500


