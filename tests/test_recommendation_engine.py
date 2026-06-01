"""CineMatch Tests"""

import pytest
import pandas as pd
from src.models.recommendation_engine import RecommendationEngine
from src.services.movie_service import MovieService


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
        
    def test_successful_recommendation(self, engine, sample_data):
        """Test successful recommendation generation with sparse matrix query."""
        success, result = engine.get_similar_movies('Movie A', sample_data, num_recommendations=1)
        assert success
        assert len(result) == 1
        assert result[0]['rank'] == 1
        assert result[0]['title'] in ['Movie B', 'Movie C']
        assert isinstance(result[0]['similarity_score'], float)


class TestMovieService:
    """Test MovieService"""
    
    @pytest.fixture
    def service(self):
        return MovieService()
    
    def test_initialization(self, service):
        """Test service initializes"""
        assert service is not None
        
    def test_search_and_formatting(self, service):
        """Test custom multi-criteria search filters and title capitalization."""
        # Directly mock movie_data to make test independent of filesystem CSV
        service.movie_data = pd.DataFrame({
            'movie_title': ['avatar', 'john carter', 'tangled'],
            'genres': ['Action Adventure', 'Action Sci-Fi', 'Animation Comedy'],
            'comb': ['comb1', 'comb2', 'comb3']
        })
        
        # Test title filter
        results = service.search(query='avatar')
        assert len(results) == 1
        assert results[0]['movie_title'] == 'Avatar'
        
        # Test genre filter
        results = service.search(genre='Action')
        assert len(results) == 2
        assert results[0]['movie_title'] in ['Avatar', 'John Carter']
        
        # Test both
        results = service.search(query='carter', genre='Action')
        assert len(results) == 1
        assert results[0]['movie_title'] == 'John Carter'


if __name__ == '__main__':
    pytest.main([__file__])

