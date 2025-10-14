# FastAPI Learning Project

[中文文档](README.md) | **English**

A comprehensive FastAPI learning project that demonstrates modern Python web development practices, including authentication, CRUD operations, and RESTful API design.

## ✨ Features

- 🚀 **FastAPI Framework** - Modern, fast web framework for building APIs
- 🔐 **JWT Authentication** - Secure token-based authentication system
- 👥 **User Management** - Complete user registration and management
- 📝 **Article System** - Full CRUD operations for articles
- 🏷️ **Category Management** - Organize content with categories
- 📊 **Statistics API** - Get insights about your data
- 🔒 **Role-based Access** - Admin and user permission levels
- 📚 **Interactive Documentation** - Auto-generated API docs with Swagger UI
- 🛡️ **Security Best Practices** - Password hashing, input validation

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI 0.104.1
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Data Validation**: Pydantic
- **API Server**: Uvicorn
- **Documentation**: Auto-generated OpenAPI/Swagger

## 📁 Project Structure

```
shentou/
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
├── README.md              # Chinese documentation
├── README_EN.md           # English documentation
├── app.py                 # FastAPI application entry
├── auth.py                # Authentication module
├── crud.py                # Database operations
├── database.py            # Database configuration
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── requirements.txt       # Python dependencies
├── fastapi_learning.db    # SQLite database
├── docs/                  # 📚 Documentation
│   ├── API.md            # API reference (Chinese)
│   ├── API_EN.md         # API reference (English)
│   ├── DEVELOPMENT.md    # Development guide (Chinese)
│   └── DEVELOPMENT_EN.md # Development guide (English)
└── scripts/              # 🛠️ Utility scripts
    ├── README.md         # Scripts documentation
    ├── init_db.py        # Database initialization
    ├── create_test_data.py # Test data generation
    └── demo_api.py       # API demonstration
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shentou
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env  # Edit .env with your settings
   ```

5. **Initialize database**
   ```bash
   python scripts/init_db.py
   python scripts/create_test_data.py
   ```

6. **Run the application**
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - API Base URL: http://localhost:8000

### Default User Accounts

| Username | Password | Role  | Description |
|----------|----------|-------|-------------|
| admin    | admin123 | Admin | Full access to all endpoints |
| user1    | user123  | User  | Standard user permissions |
| user2    | user456  | User  | Standard user permissions |

## 📖 Documentation

- **[API Reference](docs/API_EN.md)** - Complete API endpoint documentation
- **[Development Guide](docs/DEVELOPMENT_EN.md)** - Architecture and development details
- **[Scripts Documentation](scripts/README.md)** - Utility scripts usage

## 🧪 Testing

### Automated Testing
```bash
# Run API demonstration script
python scripts/demo_api.py
```

### Manual Testing
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Quick API Tests
```bash
# Login
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'

# Get posts
curl -X GET "http://localhost:8000/posts/" \
     -H "Authorization: Bearer YOUR_TOKEN"

# Get categories
curl -X GET "http://localhost:8000/categories/"
```

## 📊 Database Models

- **User**: User accounts with authentication
- **Post**: Articles/posts with content management
- **Category**: Content categorization system

For detailed schema information, see [Development Guide](docs/DEVELOPMENT_EN.md).

## 🔧 Development

### Environment Setup
1. Follow the installation steps above
2. Enable debug mode in `.env`: `DEBUG=True`
3. Use `--reload` flag when running uvicorn for auto-reload

### Code Structure
- **Models** (`models.py`): Database schema definitions
- **Schemas** (`schemas.py`): Pydantic models for API validation
- **CRUD** (`crud.py`): Database operations
- **Auth** (`auth.py`): Authentication and authorization
- **Routes** (`app.py`): API endpoint definitions

## 🚨 Common Issues

### Q: Login authentication failed?
A: Verify username and password are correct, check if database is properly initialized.

### Q: How to reset database?
A: Delete `fastapi_learning.db` file and run initialization scripts again.

### Q: API returns 422 error?
A: Check request data format matches API documentation, ensure Content-Type is `application/json`.

### Q: How to deploy to production?
A: See deployment guide in [docs/DEVELOPMENT_EN.md](docs/DEVELOPMENT_EN.md).

---

**🎯 This is a FastAPI learning project, perfect for beginners to understand modern Python web development!**

## 📄 License

This project is for educational purposes. Please follow relevant open source licenses.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📞 Contact

If you encounter any issues during learning, you can:
- Submit an Issue on GitHub
- Check the documentation in the `docs/` directory
- Run the demo script for examples

---

**Happy Learning! 🚀**