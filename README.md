# Flat Swap Backend API

A FastAPI-based backend for the Flat Swap application.

## Project Structure

```
flat-swap-BE/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py       # API router aggregator
│   │       └── endpoints/   # API endpoints
│   │           ├── __init__.py
│   │           ├── health.py
│   │           └── users.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Configuration settings
│   ├── db/                  # Database connection and session
│   │   └── __init__.py
│   ├── models/              # SQLAlchemy models
│   │   └── __init__.py
│   └── schemas/             # Pydantic schemas
│       ├── __init__.py
│       └── user.py
├── venv/                    # Virtual environment
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Example environment variables
├── .gitignore
├── requirements.txt         # Python dependencies
└── README.md
```

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
cd /Users/tahirbangash/flat-swap-BE
```

### 2. Activate Virtual Environment

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and update values as needed
# Especially change the SECRET_KEY in production!
```

### 5. Run the Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## Available Endpoints

### Root Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check

### API v1 Endpoints
- `GET /api/v1/health` - Health check with timestamp
- `GET /api/v1/users` - Get all users
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users/{user_id}` - Get a specific user

## Development

### Running the Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run with auto-reload for development
uvicorn app.main:app --reload

# Or run on specific host and port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API

You can test the API using:
1. **Swagger UI**: http://localhost:8000/docs (interactive documentation)
2. **curl**:
```bash
# Health check
curl http://localhost:8000/health

# Get all users
curl http://localhost:8000/api/v1/users

# Create a user
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepassword"
  }'
```

## Key Features

- ✅ **FastAPI** - Modern, fast web framework
- ✅ **Async/Await** - Asynchronous request handling
- ✅ **Pydantic** - Data validation using Python type hints
- ✅ **CORS** - Cross-Origin Resource Sharing enabled
- ✅ **Auto Documentation** - Swagger UI and ReDoc
- ✅ **Environment Configuration** - Easy configuration management
- ✅ **Modular Structure** - Clean, scalable architecture

## Next Steps

1. **Add Database Integration**
   - Implement SQLAlchemy models in `app/models/`
   - Set up database connection in `app/db/`
   - Switch from in-memory storage to actual database

2. **Add Authentication**
   - Implement JWT token authentication
   - Add login/register endpoints
   - Protect routes with authentication

3. **Add More Features**
   - Implement flat/property listings
   - Add user profiles
   - Implement swap matching logic

4. **Testing**
   - Add pytest for testing
   - Write unit tests and integration tests

5. **Deployment**
   - Set up production environment variables
   - Configure production database (PostgreSQL)
   - Deploy to cloud platform (AWS, GCP, Heroku, etc.)

## Dependencies

Main dependencies installed:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `python-dotenv` - Environment variable loading
- `sqlalchemy` - SQL toolkit and ORM
- `python-multipart` - Form data parsing
- `python-jose` - JWT token handling
- `passlib` - Password hashing

## License

MIT
