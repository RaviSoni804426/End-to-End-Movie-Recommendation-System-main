"""Recommendation engine for CineMatch"""

import logging
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from app.config import MAX_RECOMMENDATIONS

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Engine for generating movie recommendations using cached cosine similarity on sparse matrices."""
    
    def __init__(self):
        """Initialize the recommendation engine."""
        self.vectorizer = None
        self.count_matrix = None
    
    def get_similar_movies(self, movie_title, movie_data, num_recommendations=MAX_RECOMMENDATIONS):
        """
        Get similar movies for a given title, optimized for sub-millisecond similarity queries.
        
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
            
            movie_title_lower = movie_title.lower().strip()
            
            # Check if movie exists
            if 'movie_title' not in movie_data.columns:
                return False, "Movie database format error"
            
            matching_movies = movie_data[
                movie_data['movie_title'].str.lower() == movie_title_lower
            ]
            
            if matching_movies.empty:
                return False, f"Movie '{movie_title}' not found"
            
            movie_idx = matching_movies.index[0]
            
            # Create/retrieve similarity matrix
            if 'comb' not in movie_data.columns:
                return False, "Movie database missing required fields"
            
            # Fit vectorizer and build count matrix once
            if self.count_matrix is None:
                logger.info("Fitting CountVectorizer and caching count matrix (once)...")
                self.vectorizer = CountVectorizer(stop_words='english')
                self.count_matrix = self.vectorizer.fit_transform(movie_data['comb'])
                logger.info("Count matrix cached successfully.")
            
            # Single row dot-product comparison against the cached sparse matrix
            query_vector = self.count_matrix[movie_idx]
            similarity_scores = cosine_similarity(query_vector, self.count_matrix).flatten()
            
            # Map index to similarity score
            similarity_scores_list = list(enumerate(similarity_scores))
            
            # Sort scores
            sorted_scores = sorted(
                similarity_scores_list,
                key=lambda x: x[1],
                reverse=True
            )
            
            # Get top N (excluding the movie itself, which resides at rank index 0)
            recommendations = []
            rank = 1
            for rec_idx, score in sorted_scores:
                if rec_idx == movie_idx:
                    continue
                    
                recommendations.append({
                    "rank": rank,
                    "title": str(movie_data['movie_title'].iloc[rec_idx]).title(),
                    "similarity_score": round(float(score), 3)
                })
                rank += 1
                if rank > num_recommendations:
                    break
            
            # Dynamic live analytics tracking
            try:
                from src.services.movie_service import movie_service
                movie_service.total_recommendations += 1
                movie_service.search_counter[movie_title_lower] = movie_service.search_counter.get(movie_title_lower, 0) + 1
            except Exception as e:
                logger.warning(f"Failed to increment recommendation analytics: {e}")
                
            return True, recommendations
        
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return False, "Error generating recommendations"


# Shared singleton instance
recommendation_engine = RecommendationEngine()

