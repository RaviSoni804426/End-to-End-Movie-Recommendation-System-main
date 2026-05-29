"""Recommendation engine for CineMatch"""

import logging
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from app.config import MAX_RECOMMENDATIONS

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Engine for generating movie recommendations using cosine similarity."""
    
    def __init__(self):
        """Initialize the recommendation engine."""
        pass
    
    def get_similar_movies(self, movie_title, movie_data, num_recommendations=MAX_RECOMMENDATIONS):
        """
        Get similar movies for a given title.
        
        Args:
            movie_title: Title of the movie
            movie_data: DataFrame with movie data
            num_recommendations: Number of recommendations to return
            
        Returns:
            Tuple (success, recommendations or error message)
        """
        try:
            if not movie_title or not isinstance(movie_title, str):
                return False, "Invalid movie title"
            
            movie_title_lower = movie_title.lower()
            
            # Check if movie exists
            if 'movie_title' not in movie_data.columns:
                return False, "Movie database format error"
            
            matching_movies = movie_data[
                movie_data['movie_title'].str.lower() == movie_title_lower
            ]
            
            if matching_movies.empty:
                return False, f"Movie '{movie_title}' not found"
            
            movie_idx = matching_movies.index[0]
            
            # Create similarity matrix
            if 'comb' not in movie_data.columns:
                return False, "Movie database missing required fields"
            
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(movie_data['comb'])
            similarity_matrix = cosine_similarity(count_matrix)
            
            # Get similarity scores
            similarity_scores = list(enumerate(similarity_matrix[movie_idx]))
            sorted_scores = sorted(
                similarity_scores,
                key=lambda x: x[1],
                reverse=True
            )
            
            # Get top N (excluding the movie itself)
            recommendations = []
            for idx, (rec_idx, score) in enumerate(sorted_scores[1:num_recommendations + 1]):
                recommendations.append({
                    "rank": idx + 1,
                    "title": movie_data['movie_title'].iloc[rec_idx],
                    "similarity_score": round(float(score), 3)
                })
            
            return True, recommendations
        
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return False, "Error generating recommendations"
