"""Movie data service for CineMatch"""

import pandas as pd
import logging

from app.config import MAIN_DATA_CSV

logger = logging.getLogger(__name__)


class MovieService:
    """Service for loading and accessing movie data."""
    
    def __init__(self):
        """Initialize the movie service."""
        self.movie_data = None
        self._load_movie_data()
    
    def _load_movie_data(self):
        """Load movie data from CSV."""
        try:
            self.movie_data = pd.read_csv(MAIN_DATA_CSV)
            logger.info(f"Loaded {len(self.movie_data)} movies")
        except FileNotFoundError:
            logger.error(f"Movie data file not found: {MAIN_DATA_CSV}")
            self.movie_data = pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading movie data: {e}")
            self.movie_data = pd.DataFrame()
    
    def get_all_titles(self):
        """Get all movie titles."""
        if self.movie_data.empty or 'movie_title' not in self.movie_data.columns:
            return []
        return list(self.movie_data['movie_title'].unique())
    
    def get_data(self):
        """Get full movie dataset."""
        return self.movie_data
    
    def search(self, query):
        """Search movies by title."""
        if self.movie_data.empty or not query:
            return []
        
        query_lower = query.lower()
        matches = self.movie_data[
            self.movie_data['movie_title'].str.lower().str.contains(query_lower, na=False)
        ]
        return matches.to_dict('records')
