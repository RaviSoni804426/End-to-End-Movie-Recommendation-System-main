# CineMatch API Documentation

## Base URL
```
http://localhost:5000/api/v1
```

## Authentication
Currently, the API is open. For production, implement API key authentication.

## Endpoints

### Health Check
Check API status
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "app": "CineMatch"
}
```

---

### Get All Movies
Retrieve movies from database
```http
GET /movies?limit=20&search=avatar
```

**Query Parameters:**
- `limit` (optional, default: 20): Number of results
- `search` (optional): Search term

**Response:**
```json
{
  "success": true,
  "total": 5,
  "movies": [
    {
      "movie_title": "Avatar",
      "genre": "Sci-Fi",
      "year": 2009,
      "rating": 7.8
    }
  ]
}
```

---

### Get Movie Details
Get information about a specific movie
```http
GET /movies/<movie_title>
```

**Response:**
```json
{
  "success": true,
  "movie": {
    "movie_title": "The Shawshank Redemption",
    "genre": "Drama",
    "year": 1994,
    "rating": 9.3,
    "director": "Frank Darabont"
  }
}
```

---

### Get Recommendations
Get similar movies for a given title
```http
GET /recommendations/<movie_title>?limit=10
```

**Query Parameters:**
- `limit` (optional, default: 10): Number of recommendations

**Response:**
```json
{
  "success": true,
  "source_movie": "Inception",
  "recommendations_count": 10,
  "recommendations": [
    {
      "rank": 1,
      "title": "The Matrix",
      "similarity_score": 0.92
    },
    {
      "rank": 2,
      "title": "Interstellar",
      "similarity_score": 0.87
    }
  ]
}
```

---

### Search Movies
Search for movies by title
```http
GET /search?q=avatar&limit=20
```

**Query Parameters:**
- `q` (required): Search query
- `limit` (optional, default: 20): Number of results

**Response:**
```json
{
  "success": true,
  "query": "avatar",
  "results_count": 3,
  "results": [
    {
      "movie_title": "Avatar",
      "genre": "Sci-Fi",
      "year": 2009,
      "rating": 7.8
    }
  ]
}
```

---

### Get by Genre
Filter movies by genre
```http
GET /genres?genre=Action&limit=10
```

**Query Parameters:**
- `genre` (required): Genre name
- `limit` (optional, default: 20): Number of results

**Response:**
```json
{
  "success": true,
  "genre": "Action",
  "results_count": 10,
  "movies": [...]
}
```

---

### Get Trending Movies
Retrieve trending/popular movies
```http
GET /trending?limit=10
```

**Query Parameters:**
- `limit` (optional, default: 10): Number of results

**Response:**
```json
{
  "success": true,
  "results_count": 10,
  "movies": [...]
}
```

---

### Get Database Statistics
Get database metrics and statistics
```http
GET /statistics
```

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_movies": 5000,
    "total_genres": 23,
    "average_rating": 7.2,
    "year_range": {
      "min": 1980,
      "max": 2024
    }
  }
}
```

---

## Analytics Endpoints

### Get Dashboard Metrics
```http
GET /analytics/dashboard
```

### Get Recommendation Analytics
```http
GET /analytics/recommendations
```

### Get Search Analytics
```http
GET /analytics/searches
```

### Get Top Searched Movies
```http
GET /analytics/top-searches?limit=10
```

### Export Analytics
```http
GET /analytics/export
```

---

## Error Responses

### 404 Not Found
```json
{
  "success": false,
  "message": "Movie not found"
}
```

### 400 Bad Request
```json
{
  "success": false,
  "message": "Invalid input provided"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Internal server error"
}
```

---

## Rate Limiting
Default: 100 requests per hour
