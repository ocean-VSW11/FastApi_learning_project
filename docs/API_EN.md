# FastAPI Learning Project - API Documentation

[中文文档](API.md) | **English**

This document provides comprehensive information about all available API endpoints in the FastAPI learning project.

## 📋 Table of Contents

- [Authentication](#authentication)
- [User Management](#user-management)
- [Article Management](#article-management)
- [Category Management](#category-management)
- [Statistics](#statistics)
- [Default Accounts](#default-accounts)
- [Error Handling](#error-handling)
- [Authentication Guide](#authentication-guide)

## 🔐 Authentication

### Login
- **Endpoint**: `POST /auth/login`
- **Description**: User authentication and JWT token generation
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "is_active": true,
      "is_admin": true
    }
  }
  ```

### Get Current User
- **Endpoint**: `GET /auth/me`
- **Description**: Get current authenticated user information
- **Authentication**: Required (Bearer Token)
- **Response**:
  ```json
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "is_active": true,
    "is_admin": true
  }
  ```

## 👥 User Management

### Get All Users
- **Endpoint**: `GET /users/`
- **Description**: Get list of all users (Admin only)
- **Authentication**: Required (Admin)
- **Query Parameters**:
  - `skip`: int (default: 0) - Number of records to skip
  - `limit`: int (default: 100) - Maximum number of records to return
- **Response**:
  ```json
  [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "is_active": true,
      "is_admin": true
    }
  ]
  ```

### Get User by ID
- **Endpoint**: `GET /users/{user_id}`
- **Description**: Get specific user information (Admin only)
- **Authentication**: Required (Admin)
- **Response**: User object

### Create User
- **Endpoint**: `POST /users/`
- **Description**: Create new user account (Admin only)
- **Authentication**: Required (Admin)
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "user@example.com",
    "password": "string",
    "is_admin": false
  }
  ```

### Update User
- **Endpoint**: `PUT /users/{user_id}`
- **Description**: Update user information (Admin only)
- **Authentication**: Required (Admin)
- **Request Body**: User update data

### Delete User
- **Endpoint**: `DELETE /users/{user_id}`
- **Description**: Delete user account (Admin only)
- **Authentication**: Required (Admin)

## 📝 Article Management

### Get All Posts
- **Endpoint**: `GET /posts/`
- **Description**: Get list of all posts
- **Authentication**: Required
- **Query Parameters**:
  - `skip`: int (default: 0)
  - `limit`: int (default: 100)
- **Response**:
  ```json
  [
    {
      "id": 1,
      "title": "Sample Post",
      "content": "This is a sample post content.",
      "author_id": 1,
      "category_id": 1,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "author": {
        "id": 1,
        "username": "admin"
      },
      "category": {
        "id": 1,
        "name": "Technology"
      }
    }
  ]
  ```

### Get Post by ID
- **Endpoint**: `GET /posts/{post_id}`
- **Description**: Get specific post details
- **Authentication**: Required
- **Response**: Post object with author and category information

### Create Post
- **Endpoint**: `POST /posts/`
- **Description**: Create new post
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "title": "string",
    "content": "string",
    "category_id": 1
  }
  ```

### Update Post
- **Endpoint**: `PUT /posts/{post_id}`
- **Description**: Update existing post (Author or Admin only)
- **Authentication**: Required
- **Request Body**: Post update data

### Delete Post
- **Endpoint**: `DELETE /posts/{post_id}`
- **Description**: Delete post (Author or Admin only)
- **Authentication**: Required

## 🏷️ Category Management

### Get All Categories
- **Endpoint**: `GET /categories/`
- **Description**: Get list of all categories
- **Authentication**: Not required
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Technology",
      "description": "Technology related posts"
    }
  ]
  ```

### Get Category by ID
- **Endpoint**: `GET /categories/{category_id}`
- **Description**: Get specific category details
- **Authentication**: Not required
- **Response**: Category object

### Create Category
- **Endpoint**: `POST /categories/`
- **Description**: Create new category (Admin only)
- **Authentication**: Required (Admin)
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```

### Update Category
- **Endpoint**: `PUT /categories/{category_id}`
- **Description**: Update category (Admin only)
- **Authentication**: Required (Admin)

### Delete Category
- **Endpoint**: `DELETE /categories/{category_id}`
- **Description**: Delete category (Admin only)
- **Authentication**: Required (Admin)

## 📊 Statistics

### Get Statistics
- **Endpoint**: `GET /stats/`
- **Description**: Get system statistics
- **Authentication**: Required (Admin)
- **Response**:
  ```json
  {
    "total_users": 3,
    "total_posts": 5,
    "total_categories": 3,
    "active_users": 3
  }
  ```

## 👤 Default Accounts

The system comes with pre-configured test accounts:

| Username | Password | Role  | Email | Description |
|----------|----------|-------|-------|-------------|
| admin    | admin123 | Admin | admin@example.com | System administrator with full access |
| user1    | user123  | User  | user1@example.com | Regular user account |
| user2    | user456  | User  | user2@example.com | Regular user account |

## ❌ Error Handling

### Common HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

### Error Response Format

```json
{
  "detail": "Error message description"
}
```

### Validation Error Format

```json
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

## 🔑 Authentication Guide

### 1. Login Process

1. Send POST request to `/auth/login` with username and password
2. Receive JWT token in response
3. Include token in subsequent requests

### 2. Using JWT Token

Include the token in the Authorization header:

```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

### 3. Token Expiration

- Default expiration: 30 minutes
- Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env`
- Expired tokens will return 401 Unauthorized

### 4. Permission Levels

- **Public**: No authentication required
- **User**: Valid JWT token required
- **Admin**: Valid JWT token + admin privileges required

## 🧪 Testing Examples

### Using cURL

```bash
# Login
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'

# Get current user (replace TOKEN with actual token)
curl -X GET "http://localhost:8000/auth/me" \
     -H "Authorization: Bearer TOKEN"

# Create post
curl -X POST "http://localhost:8000/posts/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer TOKEN" \
     -d '{"title": "My Post", "content": "Post content", "category_id": 1}'

# Get all posts
curl -X GET "http://localhost:8000/posts/" \
     -H "Authorization: Bearer TOKEN"

# Get categories (no auth required)
curl -X GET "http://localhost:8000/categories/"
```

### Using Python Requests

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/auth/login",
    json={"username": "admin", "password": "admin123"}
)
token = response.json()["access_token"]

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {token}"}
posts = requests.get("http://localhost:8000/posts/", headers=headers)
```

## 📚 Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces provide:
- Complete API documentation
- Interactive testing capabilities
- Request/response examples
- Authentication testing

---

For more detailed development information, see [Development Guide](DEVELOPMENT_EN.md).