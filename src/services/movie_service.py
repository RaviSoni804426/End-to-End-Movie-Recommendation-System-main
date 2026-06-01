"""Movie data service for CineMatch"""

import pandas as pd
import logging

from app.config import MAIN_DATA_CSV

logger = logging.getLogger(__name__)


class MovieService:
    """Service for loading and accessing movie data with real-time in-memory analytics."""
    
    def __init__(self):
        """Initialize the movie service."""
        self.movie_data = None
        self.search_counter = {}  # movie_title (lowercase) -> count
        self.total_recommendations = 0
        self._load_movie_data()
    
    def _load_movie_data(self):
        """Load movie data from CSV, cleaning trailing whitespace and non-breaking spaces."""
        try:
            df = pd.read_csv(MAIN_DATA_CSV)
            
            # Clean and normalize columns to prevent parsing and spacing errors
            if 'movie_title' in df.columns:
                df['movie_title'] = df['movie_title'].astype(str).str.replace(r'\xa0', ' ', regex=True).str.strip()
            if 'comb' in df.columns:
                df['comb'] = df['comb'].astype(str).str.replace(r'\xa0', ' ', regex=True).str.strip().fillna('')
            if 'genres' in df.columns:
                df['genres'] = df['genres'].astype(str).str.replace(r'\xa0', ' ', regex=True).str.strip().fillna('')
                
            self.movie_data = df
            logger.info(f"Loaded and cleaned {len(self.movie_data)} movies")
        except FileNotFoundError:
            logger.error(f"Movie data file not found: {MAIN_DATA_CSV}")
            self.movie_data = pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading movie data: {e}")
            self.movie_data = pd.DataFrame()
    
    def get_all_titles(self):
        """Get all unique movie titles title-cased for premium autocomplete styling."""
        if self.movie_data.empty or 'movie_title' not in self.movie_data.columns:
            return []
        return sorted([str(t).title() for t in self.movie_data['movie_title'].unique() if t])
    
    def get_data(self):
        """Get full movie dataset."""
        return self.movie_data
    
    def search(self, query=None, genre=None):
        """
        Search movies by title and/or genre with support for single-criteria fallback.
        
        Args:
            query: Title search query (optional)
            genre: Genre filter (optional)
            
        Returns:
            List of movie dictionaries with title-cased movie titles.
        """
        if self.movie_data.empty:
            return []
            
        matches = self.movie_data
        
        if query:
            query_lower = query.lower().strip()
            # Increment title search in analytics
            self.search_counter[query_lower] = self.search_counter.get(query_lower, 0) + 1
            matches = matches[
                matches['movie_title'].str.lower().str.contains(query_lower, na=False)
            ]
            
        if genre:
            genre_lower = genre.lower().strip()
            matches = matches[
                matches['genres'].str.lower().str.contains(genre_lower, na=False)
            ]
            
        results = []
        for _, row in matches.iterrows():
            rec = row.to_dict()
            if 'movie_title' in rec:
                rec['movie_title'] = str(rec['movie_title']).title()
            results.append(rec)
            
        return results


# Shared singleton instance
movie_service = MovieService()

