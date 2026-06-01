---
title: CineMatch Movie Recommender
emoji: 🎬
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# CineMatch — End-to-End Movie Recommendation System

CineMatch is a high-performance, production-grade movie recommendation application built with Flask and scikit-learn. It uses a clean, service-oriented architecture to load a catalog of 6,000+ movies, perform sub-millisecond natural language processing queries using CountVectorizer, and output highly relevant movie matches based on cosine similarity.

The project is fully containerized and configured for direct deployment on **Hugging Face Spaces** (Docker SDK).

---

## 🎯 Features

*   **Sub-Millisecond Recommendations**: Uses a high-performance sparse-matrix cached similarity engine. Similarity is calculated on-demand between single vectors and cached matrices, avoiding expensive recalculations.
*   **Polished Advanced Search**: Instant search matching both movie titles and genre filters.
*   **Live Analytics Dashboard**: Dynamically tracks total recommendations generated, user engagement rates, and top searched movie trends in real time.
*   **Watchlist Management**: Save recommended movies directly to a local-storage based watchlist.
*   **Autocomplete Search**: High-performance client-side autocomplete powered by `autoComplete.js` using title-cased metadata.
*   **Premium Dark UI**: Built with Curated HSL colors, glassmorphism, responsive grid layouts, and micro-interactions.

---

## 🏗️ Architecture

```
CineMatch/
├── app/                    # Flask application
│   ├── config.py          # Environment and app configurations
│   ├── main.py            # Flask application factory
│   └── routes/            # Blueprint route definitions
│       ├── api.py         # REST API endpoints (Health, search, analytics, stats)
│       └── web.py         # Main web views (Home, search, watchlist, dashboard)
├── src/                   # Core business logic
│   ├── models/            # ML recommendation engine
│   ├── services/          # Data loading & memory-cached analytics services
│   └── utils/             # Constants and helpers
├── frontend/              # Web User Interface
│   ├── templates/         # HTML template views (base, index, search, dashboard, watchlist, 404)
│   └── static/            # Static assets (CSS, JS, images)
├── data/                  # Static datasets and models
│   └── datasets/          # Movie catalog CSVs (main_data.csv)
├── docker/                # Container configurations
│   └── Dockerfile         # Docker container configuration
└── run.py                 # Main entry point
```

---

## 🚀 Quick Start (Local Setup)

### 1. Set Up Environment
Create and activate a virtual environment, then install dependencies:

```bash
# Create environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate
# Activate (Windows PowerShell)
& .\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 2. Run the App
Start the Flask development server:
```bash
python run.py
```
Open `http://localhost:5000` in your web browser.

---

## 🐳 Running with Docker

Build and run the production container locally:

```bash
# Build image
docker build -t cinematch .

# Run container (binds to port 5000)
docker run -p 5000:5000 cinematch
```

---

## 🔌 API Endpoints Reference

### Web Routes
*   `GET /` - CineMatch Home Page
*   `GET /search` - Advanced Filtering & Search Page
*   `GET /watchlist` - Watchlist Saver Page
*   `GET /dashboard` - Real-time Analytics Dashboard

### REST API Endpoints (`/api/v1`)
*   `GET /api/v1/health` - App health status
*   `GET /api/v1/movies` - Get catalog movie lists
*   `GET /api/v1/search?q=...&genre=...` - Search catalog with optional title and/or genre criteria
*   `GET /api/v1/recommendations/<movie_title>` - Fetch matches for a title
*   `GET /api/v1/statistics` - Catalog stats (total count, average rating)
*   `GET /api/v1/analytics/dashboard` - Recommendation engagement rates
*   `GET /api/v1/analytics/top-searches` - Live top 5 searched trends

---

## 🧪 Testing

Run standard unit tests with `pytest`:
```bash
pytest
```

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for details.

---

## 🙏 Acknowledgments

*   Movie dataset based on TMDB and Kaggle film data.
*   NLP vectorization algorithms powered by scikit-learn.
