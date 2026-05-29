# CineMatch — End-to-End Movie Recommendation System

This repository contains a lightweight Flask app that provides movie recommendations based on a CSV dataset. The project is prepared to run locally, via Docker, and to be deployed to a Hugging Face Space (Docker).

Quick start (local):

1. Create and activate a Python virtual environment (Windows PowerShell):

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

2. Open http://127.0.0.1:5000 in your browser.

Docker (build & run):

```bash
docker build -t cinematch .
docker run -e PORT=5000 -e SECRET_KEY=mysecret -p 5000:5000 cinematch
```

Deploy to Hugging Face Spaces (Docker):

1. Create a new Space on Hugging Face (https://huggingface.co/spaces) and choose SDK: Docker.
2. In the Space settings you'll be given a Git URL for the Space (e.g. `https://huggingface.co/spaces/<user>/<space>.git`).
3. From your project root, run:

```bash
export HF_SPACE_GIT="https://huggingface.co/spaces/<user>/<space>.git"
./deploy_to_hf.sh
```

4. In the Space UI, set any required environment variables (e.g. `SECRET_KEY`, `DEBUG=false`). The Space will build the Dockerfile found at the repo root. The app reads `PORT` environment variable (default 5000).

Notes:
- The main dataset used by the app is at `data/datasets/main_data.csv`.
- For production on Spaces, set `DEBUG=false` and provide a secure `SECRET_KEY` in Space secrets.
- If you prefer the Dockerfile in a subfolder, adjust the Space settings or copy the Dockerfile to the repo root (this repo already includes a root `Dockerfile`).

If you want, I can also open a PR to move or tidy files, or add a small `.dockerignore` to speed builds.
# CineMatch

A lightweight movie recommendation system using Flask and machine learning.

## 🎯 Features

- **Smart Recommendations** - Find similar movies using cosine similarity
- **Fast Search** - Search movies by title instantly  
- **Simple API** - RESTful endpoints for integration
- **Clean Code** - Beginner-friendly, production-inspired architecture

## 🚀 Quick Start

### 1. Install

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add Data

Place `main_data.csv` in `data/datasets/` with columns:
- `movie_title` - Movie name
- `comb` - Combined text (genre, plot, cast, etc.)

### 3. Run

```bash
python run.py
```

Visit `http://localhost:5000`

## 📁 Structure

```
CineMatch/
├── app/              # Flask application
│   ├── config.py    # Configuration
│   ├── main.py      # App factory
│   └── routes/      # API routes
├── src/             # Core logic
│   ├── models/      # Recommendation engine
│   └── services/    # Movie service
├── frontend/        # Web UI
│   ├── templates/   # HTML
│   └── static/      # CSS, JS
├── data/            # Datasets
└── tests/           # Tests
```

## 🔌 API Endpoints

- `GET /` - Home page
- `POST /recommendations` - Get recommendations
- `GET /api/v1/health` - Health check
- `GET /api/v1/movies` - List movies
- `GET /api/v1/recommendations/<title>` - Get recommendations
- `GET /api/v1/search?q=<query>` - Search movies

See [docs/API.md](docs/API.md) for details.

## 💡 How It Works

1. Load movie data (CSV)
2. Vectorize text using CountVectorizer
3. Compute cosine similarity between movies
4. Return top N similar movies

## 🧪 Testing

```bash
pytest
```

## 📚 Tech Stack

- **Backend**: Flask, Python 3.9+
- **ML**: Scikit-learn, Pandas
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Docker

## 📖 Data Format

Your CSV should have:

```csv
movie_title,comb
Inception,"Christopher Nolan action sci-fi..."
Avatar,"James Cameron action adventure..."
```

## 🐳 Docker

```bash
docker build -f docker/Dockerfile -t cinematch .
docker run -p 5000:5000 cinematch
```

## 📝 License

MIT

### Docker
```bash
docker build -f docker/Dockerfile -t cinematch:latest .
docker run -p 5000:5000 cinematch:latest
```

## 📝 Configuration

Create `.env` file with your settings:
```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-secret-key
ENABLE_CACHING=True
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes
4. Push branch
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 👨‍💻 Author

**Your Name**
- LinkedIn: [Your Profile]
- GitHub: [Your GitHub]
- Email: your.email@example.com

## 🙏 Acknowledgments

- Movie dataset from TMDB
- NLP techniques from scikit-learn
- Community feedback
# Contributing

Contributions make the open-source community such an amazing place to learn, inspire, and create. I would greatly appreciate any contributions you make.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch 
3. Commit your Changes 
4. Push to the Branch 
5. Open a Pull Request

<!-- LICENSE -->
# License

Distributed under the GNU General Public License v3.0. See `LICENSE.txt` for more information.

# Acknowledgements

This project was inspired by the Kaggle dataset on Spam Email Detection and the corresponding competition. We also acknowledge the open-source Python libraries used in this project and their contributors.

