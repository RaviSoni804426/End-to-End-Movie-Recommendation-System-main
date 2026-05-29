"""Web routes for CineMatch"""

from flask import Blueprint, render_template, request, jsonify
import logging

from src.models.recommendation_engine import RecommendationEngine
from src.services.movie_service import MovieService

logger = logging.getLogger(__name__)

web_bp = Blueprint('web', __name__)

recommendation_engine = RecommendationEngine()
movie_service = MovieService()


@web_bp.route('/', methods=['GET'])
def home():
    """Home page with movie suggestions."""
    try:
        suggestions = movie_service.get_all_titles()
        return render_template('index.html', suggestions=suggestions)
    except Exception as e:
        logger.error(f"Error loading home: {e}")
        return render_template('index.html', suggestions=[])


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
            'movie': movie_title,
            'recommendations': result
        })
    
    except Exception as e:
        logger.error(f"Error in recommendations: {e}")
        return jsonify({
            'success': False,
            'message': 'Error generating recommendations'
        }), 500
