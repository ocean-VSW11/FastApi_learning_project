# FastAPI Learning Project - Development Guide

[中文文档](DEVELOPMENT.md) | **English**

This document provides comprehensive development information for the FastAPI learning project, including architecture, setup, and best practices.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Development Environment](#development-environment)
- [Database Design](#database-design)
- [API Development](#api-development)
- [Authentication System](#authentication-system)
- [Testing](#testing)
- [Deployment](#deployment)
- [Security Considerations](#security-considerations)
- [Common Issues](#common-issues)
- [Extended Features](#extended-features)

## 🎯 Project Overview

This is a comprehensive FastAPI learning project designed to demonstrate modern Python web development practices. It implements a complete blog-like system with user authentication, article management, and administrative features.

### Learning Objectives

- Master FastAPI framework fundamentals
- Understand RESTful API design principles
- Learn JWT-based authentication
- Practice SQLAlchemy ORM usage
- Implement proper error handling
- Apply security best practices

## 🏗️ Architecture

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Database      │
│   (Browser/     │◄──►│   Application   │◄──►│   (SQLite)      │
│   API Client)   │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Application Layers

1. **Presentation Layer** (`app.py`)
   - API endpoints definition
   - Request/response handling
   - Route organization

2. **Business Logic Layer** (`crud.py`)
   - Core business operations
   - Data processing logic
   - Validation rules

3. **Data Access Layer** (`models.py`, `database.py`)
   - Database models
   - Connection management
   - Query operations

4. **Security Layer** (`auth.py`)
   - Authentication logic
   - Authorization checks
   - Token management

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Web Framework** | FastAPI | 0.104.1 | API development |
| **ASGI Server** | Uvicorn | 0.24.0 | Application server |
| **Database** | SQLite | Built-in | Data storage |
| **ORM** | SQLAlchemy | 1.4.53 | Database operations |
| **Validation** | Pydantic | 2.5.0 | Data validation |
| **Authentication** | JWT | - | Token-based auth |
| **Password Hashing** | bcrypt | 4.1.2 | Secure password storage |

### Development Tools

- **Environment Management**: python-decouple
- **File Upload**: python-multipart
- **Documentation**: Auto-generated OpenAPI/Swagger

## 📁 Project Structure

```
shentou/
├── app.py                 # 🚀 FastAPI application entry point
├── models.py              # 🗃️ SQLAlchemy database models
├── schemas.py             # 📋 Pydantic validation schemas
├── crud.py                # 🔧 Database CRUD operations
├── auth.py                # 🔐 Authentication & authorization
├── database.py            # 🗄️ Database configuration
├── requirements.txt       # 📦 Python dependencies
├── .env                   # ⚙️ Environment variables
├── .gitignore            # 🚫 Git ignore rules
├── README.md             # 📖 Chinese documentation
├── README_EN.md          # 📖 English documentation
├── fastapi_learning.db   # 💾 SQLite database file
├── docs/                 # 📚 Documentation directory
│   ├── API.md           # API reference (Chinese)
│   ├── API_EN.md        # API reference (English)
│   ├── DEVELOPMENT.md   # Development guide (Chinese)
│   └── DEVELOPMENT_EN.md # Development guide (English)
└── scripts/             # 🛠️ Utility scripts
    ├── README.md        # Scripts documentation
    ├── init_db.py       # Database initialization
    ├── create_test_data.py # Test data generation
    └── demo_api.py      # API demonstration
```

### Core Modules

#### `app.py` - Application Entry Point
- FastAPI application instance
- Route definitions and organization
- Middleware configuration
- CORS settings
- Exception handlers

#### `models.py` - Database Models
- SQLAlchemy ORM models
- Table relationships
- Database constraints
- Model methods

#### `schemas.py` - Pydantic Schemas
- Request/response validation
- Data serialization
- Type definitions
- Input sanitization

#### `crud.py` - Database Operations
- Create, Read, Update, Delete operations
- Query optimization
- Transaction management
- Error handling

#### `auth.py` - Authentication System
- JWT token generation/validation
- Password hashing/verification
- User authentication
- Permission checking

#### `database.py` - Database Configuration
- Database connection setup
- Session management
- Connection pooling
- Migration support

## 🚀 Development Environment

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (version control)
- Code editor (VS Code recommended)

### Setup Steps

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd shentou
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate (Linux/Mac)
   source venv/bin/activate
   
   # Activate (Windows)
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit configuration
   nano .env
   ```

5. **Database Setup**
   ```bash
   # Initialize database
   python scripts/init_db.py
   
   # Create test data
   python scripts/create_test_data.py
   ```

6. **Run Application**
   ```bash
   # Development mode
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   
   # Production mode
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

### Development Tools

#### Code Quality
```bash
# Install development dependencies
pip install black flake8 mypy pytest

# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

#### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## 🗄️ Database Design

### Entity Relationship Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      User       │    │      Post       │    │    Category     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │◄──┐│ id (PK)         │┌──►│ id (PK)         │
│ username        │   └│ author_id (FK)  ││   │ name            │
│ email           │    │ category_id (FK)│┘   │ description     │
│ hashed_password │    │ title           │    └─────────────────┘
│ is_active       │    │ content         │
│ is_admin        │    │ created_at      │
└─────────────────┘    │ updated_at      │
                       └─────────────────┘
```

### Table Definitions

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE
);
```

#### Posts Table
```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users (id),
    FOREIGN KEY (category_id) REFERENCES categories (id)
);
```

#### Categories Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);
```

## 🔧 API Development

### RESTful Design Principles

1. **Resource-based URLs**
   - `/users/` - User collection
   - `/users/{id}` - Specific user
   - `/posts/` - Post collection
   - `/posts/{id}` - Specific post

2. **HTTP Methods**
   - `GET` - Retrieve data
   - `POST` - Create new resource
   - `PUT` - Update existing resource
   - `DELETE` - Remove resource

3. **Status Codes**
   - `200 OK` - Success
   - `201 Created` - Resource created
   - `400 Bad Request` - Client error
   - `401 Unauthorized` - Authentication required
   - `403 Forbidden` - Access denied
   - `404 Not Found` - Resource not found
   - `422 Unprocessable Entity` - Validation error

### Request/Response Patterns

#### Standard Response Format
```python
# Success Response
{
    "id": 1,
    "title": "Sample Post",
    "content": "Post content...",
    "created_at": "2024-01-01T00:00:00"
}

# Error Response
{
    "detail": "Error message"
}

# Validation Error
{
    "detail": [
        {
            "loc": ["field_name"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

### Pagination
```python
# Query Parameters
GET /posts/?skip=0&limit=10

# Response
{
    "items": [...],
    "total": 100,
    "skip": 0,
    "limit": 10
}
```

## 🔐 Authentication System

### JWT Implementation

#### Token Structure
```
Header.Payload.Signature
```

#### Token Payload
```json
{
    "sub": "username",
    "exp": 1640995200,
    "iat": 1640991600
}
```

#### Authentication Flow

1. **Login Request**
   ```
   POST /auth/login
   {
       "username": "admin",
       "password": "admin123"
   }
   ```

2. **Token Response**
   ```json
   {
       "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
       "token_type": "bearer",
       "expires_in": 1800
   }
   ```

3. **Authenticated Request**
   ```
   GET /posts/
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
   ```

### Password Security

#### Hashing Process
```python
import bcrypt

# Hash password
password = "user_password"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

# Verify password
is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed)
```

### Permission Levels

1. **Public** - No authentication required
2. **User** - Valid JWT token required
3. **Admin** - Valid JWT token + admin privileges

## 🧪 Testing

### Testing Strategy

1. **Unit Tests** - Individual function testing
2. **Integration Tests** - API endpoint testing
3. **End-to-End Tests** - Complete workflow testing

### Test Structure
```
tests/
├── __init__.py
├── test_auth.py          # Authentication tests
├── test_users.py         # User management tests
├── test_posts.py         # Post management tests
├── test_categories.py    # Category tests
└── conftest.py          # Test configuration
```

### Example Test
```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_login():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_post():
    # Login first
    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]
    
    # Create post
    response = client.post(
        "/posts/",
        json={
            "title": "Test Post",
            "content": "Test content",
            "category_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run with verbose output
pytest -v
```

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**
   ```bash
   # Production .env
   SECRET_KEY=complex-random-string-here
   DATABASE_URL=postgresql://user:pass@localhost/db
   DEBUG=False
   ```

2. **Database Migration**
   ```bash
   # Use PostgreSQL in production
   pip install psycopg2-binary
   
   # Update DATABASE_URL
   DATABASE_URL=postgresql://user:pass@host:port/dbname
   ```

3. **Security Headers**
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   from fastapi.middleware.trustedhost import TrustedHostMiddleware
   
   app.add_middleware(
       TrustedHostMiddleware,
       allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
   )
   ```

### Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/fastapi_db
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: fastapi_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Cloud Deployment

#### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: uvicorn app:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### AWS/GCP/Azure
- Use container services (ECS, Cloud Run, Container Instances)
- Configure load balancers
- Set up SSL certificates
- Configure environment variables

## 🛡️ Security Considerations

### Best Practices

1. **Input Validation**
   - Use Pydantic models for all inputs
   - Validate data types and constraints
   - Sanitize user inputs

2. **Authentication Security**
   - Use strong JWT secrets
   - Implement token expiration
   - Consider refresh tokens for long sessions

3. **Password Security**
   - Use bcrypt for hashing
   - Enforce password complexity
   - Implement rate limiting for login attempts

4. **API Security**
   - Implement CORS properly
   - Use HTTPS in production
   - Add request rate limiting
   - Validate all inputs

5. **Database Security**
   - Use parameterized queries (SQLAlchemy handles this)
   - Implement proper access controls
   - Regular security updates

### Security Headers
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## 🐛 Common Issues

### Development Issues

1. **Import Errors**
   ```bash
   # Solution: Check Python path and virtual environment
   which python
   pip list
   ```

2. **Database Connection Issues**
   ```bash
   # Solution: Check database file permissions and path
   ls -la fastapi_learning.db
   ```

3. **JWT Token Issues**
   ```bash
   # Solution: Check SECRET_KEY in .env
   cat .env | grep SECRET_KEY
   ```

### Production Issues

1. **Performance Optimization**
   - Use connection pooling
   - Implement caching
   - Optimize database queries
   - Use async operations where possible

2. **Monitoring**
   - Implement logging
   - Use application monitoring tools
   - Set up health checks
   - Monitor resource usage

## 🚀 Extended Features

### Potential Enhancements

1. **Advanced Authentication**
   - OAuth2 integration (Google, GitHub)
   - Two-factor authentication
   - Password reset functionality
   - Session management

2. **Content Management**
   - File upload support
   - Image handling
   - Rich text editor integration
   - Content versioning

3. **API Enhancements**
   - GraphQL support
   - WebSocket integration
   - API versioning
   - Advanced filtering and sorting

4. **Performance**
   - Redis caching
   - Database indexing
   - Query optimization
   - CDN integration

5. **Monitoring & Analytics**
   - Request logging
   - Performance metrics
   - Error tracking
   - User analytics

### Implementation Examples

#### File Upload
```python
from fastapi import File, UploadFile

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Process file
    return {"filename": file.filename}
```

#### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_categories():
    # Cached database query
    return db.query(Category).all()
```

#### Background Tasks
```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email logic
    pass

@app.post("/send-notification/")
async def send_notification(
    email: str, 
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Hello!")
    return {"message": "Notification sent"}
```

---

This development guide provides a comprehensive overview of the FastAPI learning project. For specific API usage, refer to the [API Documentation](API_EN.md).