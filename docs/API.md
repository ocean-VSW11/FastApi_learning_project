# FastAPI 学习项目 - API 文档

**中文** | [English](API_EN.md)

## 概述

这是一个基于 FastAPI 的学习项目，实现了用户认证、文章管理和分类管理的完整 RESTful API。

## 基础信息

- **服务器地址**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **OpenAPI 规范**: http://localhost:8000/openapi.json

## 认证系统

### 登录
- **端点**: `POST /auth/login`
- **描述**: 用户登录获取访问令牌
- **请求体**:
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **响应**:
  ```json
  {
    "access_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@test.com",
      "full_name": "管理员",
      "is_active": true,
      "is_superuser": true
    }
  }
  ```

### 获取当前用户信息
- **端点**: `GET /auth/me`
- **描述**: 获取当前登录用户的信息
- **认证**: 需要 Bearer Token
- **响应**: 用户信息对象

## 用户管理

### 创建用户
- **端点**: `POST /users/`
- **描述**: 创建新用户（需要管理员权限）
- **认证**: 需要 Bearer Token（管理员）

### 获取用户列表
- **端点**: `GET /users/`
- **描述**: 获取所有用户列表
- **参数**: 
  - `skip`: 跳过的记录数（默认: 0）
  - `limit`: 返回的记录数（默认: 100）

### 获取单个用户
- **端点**: `GET /users/{user_id}`
- **描述**: 根据用户ID获取用户信息

## 文章管理

### 获取文章列表
- **端点**: `GET /posts/`
- **描述**: 获取所有文章列表
- **参数**:
  - `skip`: 跳过的记录数（默认: 0）
  - `limit`: 返回的记录数（默认: 100）

### 创建文章
- **端点**: `POST /posts/`
- **描述**: 创建新文章
- **认证**: 需要 Bearer Token
- **请求体**:
  ```json
  {
    "title": "文章标题",
    "content": "文章内容",
    "summary": "文章摘要"
  }
  ```

### 获取单篇文章
- **端点**: `GET /posts/{post_id}`
- **描述**: 根据文章ID获取文章详情

### 更新文章
- **端点**: `PUT /posts/{post_id}`
- **描述**: 更新文章信息
- **认证**: 需要 Bearer Token（作者或管理员）

### 删除文章
- **端点**: `DELETE /posts/{post_id}`
- **描述**: 删除文章
- **认证**: 需要 Bearer Token（作者或管理员）

## 分类管理

### 获取分类列表
- **端点**: `GET /categories/`
- **描述**: 获取所有分类列表

### 创建分类
- **端点**: `POST /categories/`
- **描述**: 创建新分类
- **认证**: 需要 Bearer Token

### 更新分类
- **端点**: `PUT /categories/{category_id}`
- **描述**: 更新分类信息
- **认证**: 需要 Bearer Token

### 删除分类
- **端点**: `DELETE /categories/{category_id}`
- **描述**: 删除分类
- **认证**: 需要 Bearer Token

## 默认用户账户

| 用户名 | 密码 | 角色 | 邮箱 |
|--------|------|------|------|
| admin | admin123 | 管理员 | admin@test.com |
| user1 | password1 | 普通用户 | user1@test.com |
| user2 | password2 | 普通用户 | user2@test.com |

## 错误处理

API 使用标准的 HTTP 状态码：

- `200`: 成功
- `201`: 创建成功
- `400`: 请求错误
- `401`: 未认证
- `403`: 权限不足
- `404`: 资源不存在
- `422`: 验证错误
- `500`: 服务器内部错误

## 认证说明

大部分 API 端点需要认证。在请求头中包含访问令牌：

```
Authorization: Bearer <access_token>
```

访问令牌有效期为 30 分钟（1800 秒）。