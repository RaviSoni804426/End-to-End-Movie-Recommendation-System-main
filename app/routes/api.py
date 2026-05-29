"""API routes for CineMatch"""

from flask import Blueprint, request, jsonify
import logging

from src.models.recommendation_engine import RecommendationEngine
from src.services.movie_service import MovieService

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

recommendation_engine = RecommendationEngine()
movie_service = MovieService()


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'app': 'CineMatch'
    })


@api_bp.route('/movies', methods=['GET'])
def get_movies():
    """Get movies with optional search."""
    try:
        limit = request.args.get('limit', 20, type=int)
        search = request.args.get('search', '', type=str)
        
        movie_data = movie_service.get_data()
        
        if search:
            results = movie_service.search(search)[:limit]
        else:
            results = movie_data.head(limit).to_dict('records')
        
        return jsonify({
            'success': True,
            'total': len(results),
            'movies': results
        })
    except Exception as e:
        logger.error(f"Error fetching movies: {e}")
        return jsonify({'success': False, 'message': 'Error fetching movies'}), 500


@api_bp.route('/recommendations/<movie_title>', methods=['GET'])
def get_recommendations_api(movie_title):
    """Get recommendations for a movie."""
    try:
        limit = request.args.get('limit', 10, type=int)
        movie_data = movie_service.get_data()
        
        if movie_data.empty:
            return jsonify({'success': False, 'message': 'Database not loaded'}), 500
        
        success, result = recommendation_engine.get_similar_movies(
            movie_title,
            movie_data,
            num_recommendations=limit
        )
        
        if not success:
            return jsonify({'success': False, 'message': result}), 404
        
        return jsonify({
            'success': True,
            'source_movie': movie_title,
            'recommendations': result
        })
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({'success': False, 'message': 'Error generating recommendations'}), 500


@api_bp.route('/search', methods=['GET'])
def search_movies_api():
    """Search for movies."""
    try:
        query = request.args.get('q', '', type=str)
        
        if not query:
            return jsonify({'success': False, 'message': 'Search query required'}), 400
        
        results = movie_service.search(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results
        })
    except Exception as e:
        logger.error(f"Error searching: {e}")
        return jsonify({'success': False, 'message': 'Error searching'}), 500
