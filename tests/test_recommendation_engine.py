"""CineMatch Tests"""

import pytest
from src.models.recommendation_engine import RecommendationEngine
from src.services.movie_service import MovieService
import pandas as pd


class TestRecommendationEngine:
    """Test RecommendationEngine"""
    
    @pytest.fixture
    def engine(self):
        return RecommendationEngine()
    
    @pytest.fixture
    def sample_data(self):
        """Sample movie data for testing"""
        return pd.DataFrame({
            'movie_title': ['Movie A', 'Movie B', 'Movie C'],
            'comb': ['action adventure', 'action drama', 'drama']
        })
    
    def test_initialization(self, engine):
        """Test engine initializes"""
        assert engine is not None
    
    def test_invalid_movie_title(self, engine, sample_data):
        """Test with invalid movie"""
        success, result = engine.get_similar_movies('Invalid', sample_data)
        assert not success


class TestMovieService:
    """Test MovieService"""
    
    @pytest.fixture
    def service(self):
        return MovieService()
    
    def test_initialization(self, service):
        """Test service initializes"""
        assert service is not None


if __name__ == '__main__':
    pytest.main([__file__])
