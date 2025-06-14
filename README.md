# F1 Data API B### Local Development

1. **Clone and setup:**
```bash
git clone https://github.com/yourusername/fastf1api.git
cd fastf1api
```

2. **Create Python virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the server:**
```bash
uvicorn app.main:app --reload
```backend service for accessing Formula 1 data using the Fast F1 Python library.

## Features

- 🏎️ Access to F1 session data, lap times, and results
- 📊 Qualifying and race results
- 🚀 Fast API with automatic documentation
- 🔄 CORS enabled for mobile app integration
- 📱 RESTful API design
- 🐳 Docker support for easy deployment

## Quick Start

### Local Development

1. **Clone and setup:**
```bash
mkdir f1-api-backend
cd f1-api-backend
# Copy the main.py and requirements.txt files here
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the server:**
```bash
uvicorn main:app --reload
```

4. **Access the API:**
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Using Docker

1. **Build and run:**
```bash
docker build -t f1-api .
docker run -p 8000:8000 f1-api
```

## API Endpoints

### Base Information
- `GET /` - API information and endpoints list
- `GET /health` - Health check

### Session Data
- `GET /api/session/{year}/{gp}/{session_type}` - Basic session info
- `GET /api/session/{year}/{gp}/{session_type}/laps` - Lap times (optional: `?driver=HAM`)

### Results
- `GET /api/session/{year}/{gp}/qualifying/results` - Qualifying results
- `GET /api/session/{year}/{gp}/race/results` - Race results

## Example Usage

### Get 2024 Monaco GP qualifying results:
```
GET /api/session/2024/Monaco/qualifying/results
```

### Get Hamilton's lap times from 2024 Monaco race:
```
GET /api/session/2024/Monaco/race/laps?driver=HAM
```

## Parameters

- **year**: Season year (e.g., 2024, 2023)
- **gp**: Grand Prix name (e.g., "Monaco", "Silverstone", "Monza")
- **session_type**: 
  - "FP1", "FP2", "FP3" (Practice sessions)
  - "Q", "qualifying" (Qualifying)
  - "S", "sprint" (Sprint race)
  - "R", "race" (Main race)

## Deployment Options

### Railway (Recommended)
1. Push code to GitHub
2. Connect Railway to your repo
3. Deploy automatically

### Render
1. Connect your GitHub repo
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Heroku
```bash
# Install Heroku CLI, then:
heroku create your-f1-api
git push heroku main
```

## Development Tips

1. **Caching**: Fast F1 uses caching to improve performance. Cache files are stored in the `cache/` directory.

2. **Rate Limiting**: Consider adding rate limiting for production use:
```bash
pip install slowapi
```

3. **Environment Variables**: For production, use environment variables for configuration:
```python
import os
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

4. **Error Handling**: The API includes comprehensive error handling with descriptive messages.

## Mobile App Integration

Your mobile app can consume this API by making HTTP requests to the deployed endpoints. The API returns JSON data that's easy to parse in mobile applications.

Example fetch in JavaScript:
```javascript
const response = await fetch('https://your-api-url.com/session/2024/Monaco/race/results');
const results = await response.json();
```

## Troubleshooting

- **Slow first request**: Fast F1 downloads data on first access, which can be slow
- **Memory usage**: Large datasets can consume significant memory
- **Network errors**: F1 data comes from external sources and may occasionally be unavailable

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Fast F1 library is also open source under Apache 2.0 license.

### Project Structure

```
fastf1api/
├── app/                    # Main application package
│   ├── __init__.py
│   ├── main.py            # FastAPI application instance
│   ├── api/               # API routes
│   │   ├── __init__.py
│   │   ├── health.py      # Health check endpoint
│   │   └── sessions.py    # F1 session endpoints
│   └── models/            # Data models
│       ├── __init__.py
│       └── schemas.py     # Pydantic models
├── cache/                 # FastF1 cache directory
├── requirements.txt       # Project dependencies
├── Dockerfile            # Docker configuration
└── README.md            # Project documentation
```

### API Documentation

Once the server is running, you can access:
- Swagger UI documentation at: http://localhost:8000/docs
- ReDoc documentation at: http://localhost:8000/redoc
- OpenAPI JSON at: http://localhost:8000/openapi.json