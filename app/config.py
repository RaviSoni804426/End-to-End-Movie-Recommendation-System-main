"""Configuration settings for CineMatch"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Files
# Updated to look in the `datasets` subfolder where the CSV actually resides
MAIN_DATA_CSV = DATA_DIR / "datasets" / "main_data.csv"

# Flask
DEBUG = os.getenv("DEBUG", "True") == "True"
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
FLASK_ENV = os.getenv("FLASK_ENV", "development")

# App settings
APP_NAME = "CineMatch"
MAX_RECOMMENDATIONS = 10
SIMILARITY_THRESHOLD = 0.3
