# FastAPI 学习项目

这是一个完整的 FastAPI 学习项目，旨在帮助你理解和掌握 FastAPI 框架的核心概念和最佳实践。

## 📋 项目概述

本项目是一个博客系统的后端 API，包含以下主要功能：

- **用户管理**：用户注册、登录、信息管理
- **文章管理**：文章的增删改查、发布状态管理
- **分类管理**：文章分类的管理
- **用户认证**：基于 JWT 的用户认证和权限控制
- **数据库操作**：使用 SQLAlchemy ORM 进行数据库操作
- **API 文档**：自动生成的 Swagger/OpenAPI 文档

## 🛠️ 技术栈

- **FastAPI**: 现代、快速的 Web 框架
- **SQLAlchemy**: Python SQL 工具包和对象关系映射器
- **SQLite**: 轻量级数据库（开发环境）
- **Pydantic**: 数据验证和设置管理
- **JWT**: JSON Web Token 用于用户认证
- **Uvicorn**: ASGI 服务器
- **bcrypt**: 密码哈希库
- **Python-Jose**: JWT 处理库

## 📁 项目结构

```
shentou/
├── docs/                   # 项目文档
│   ├── API.md             # API 接口文档
│   └── DEVELOPMENT.md     # 开发文档
├── scripts/               # 工具脚本
│   ├── demo_api.py        # API 演示脚本
│   ├── init_db.py         # 数据库初始化
│   ├── create_test_data.py # 创建测试数据
│   └── README.md          # 脚本说明文档
├── app.py                 # 主应用文件，包含所有 API 端点
├── models.py              # SQLAlchemy 数据模型定义
├── schemas.py             # Pydantic 数据验证模型
├── crud.py                # 数据库 CRUD 操作
├── auth.py                # 用户认证和权限管理
├── database.py            # 数据库配置和连接管理
├── requirements.txt       # 项目依赖
├── .env                   # 环境变量配置
└── README.md              # 项目文档
```

## 🚀 快速开始

### 1. 环境准备

确保你的系统已安装 Python 3.7+：

```bash
python --version
```

### 2. 克隆项目

```bash
git clone 。。。。。。
cd 到目录下
```

### 3. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

复制 `.env` 文件并根据需要修改配置：

```bash
cp .env .env.local
```

主要配置项说明：
- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: JWT 签名密钥（生产环境请使用强密钥）
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 访问令牌过期时间

### 6. 初始化数据库

```bash
# 初始化数据库表结构
python scripts/init_db.py

# 创建测试数据
python scripts/create_test_data.py
```

### 7. 运行应用

```bash
# 开发模式运行
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

应用启动后，你可以访问：
- **API 文档**: http://localhost:8000/docs (Swagger UI)
- **替代文档**: http://localhost:8000/redoc (ReDoc)

### 8. 测试 API

```bash
# 运行 API 演示脚本
python scripts/demo_api.py
```

## 🔐 默认用户账户

| 用户名 | 密码 | 角色 | 邮箱 |
|--------|------|------|------|
| admin | admin123 | 管理员 | admin@test.com |
| user1 | password1 | 普通用户 | user1@test.com |
| user2 | password2 | 普通用户 | user2@test.com |

## 📚 API 文档

本项目提供完整的 RESTful API，支持用户管理、文章管理和分类管理。

### 主要端点概览

- **认证**: `/auth/login`, `/auth/me`
- **用户管理**: `/users/` (GET, POST, PUT, DELETE)
- **文章管理**: `/posts/` (GET, POST, PUT, DELETE)
- **分类管理**: `/categories/` (GET, POST, PUT, DELETE)

### 详细文档

- 📖 **完整 API 文档**: [docs/API.md](docs/API.md)
- 🔧 **开发文档**: [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)
- 🛠️ **脚本说明**: [scripts/README.md](scripts/README.md)
- 🌐 **在线文档**: http://localhost:8000/docs (启动服务后访问)

### 快速测试

```bash
# 登录获取令牌
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'

# 获取文章列表
curl "http://localhost:8000/posts/"

# 获取分类列表
curl "http://localhost:8000/categories/"
```

## 🗄️ 数据库模型

项目使用 SQLAlchemy ORM 定义了三个主要数据模型：

- **User（用户）**: 用户账户信息和权限管理
- **Post（文章）**: 博客文章内容和元数据
- **Category（分类）**: 文章分类管理

详细的数据库设计请参考 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md#数据库设计)。

## 🧪 测试

### 自动化测试
```bash
# 运行 API 演示脚本
python scripts/demo_api.py
```

### 手动测试
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 快速验证
```bash
# 检查服务状态
curl http://localhost:8000/users/

# 测试登录
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
```

## 🔧 开发指南

### 项目扩展
1. **添加新功能**: 参考现有代码结构
2. **数据库变更**: 修改模型后重新初始化数据库
3. **API 设计**: 遵循 RESTful 规范

### 学习重点
- **FastAPI**: 现代 Python Web 框架
- **SQLAlchemy**: ORM 和数据库操作
- **JWT 认证**: 无状态用户认证
- **API 设计**: RESTful 接口设计原则

详细的开发指南请参考 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

MIT License

## 🚨 常见问题

### Q: 登录时提示认证失败？
A: 确认用户名和密码正确，检查数据库中的用户数据是否已正确初始化。

### Q: 如何重置数据库？
A: 删除 `fastapi_learning.db` 文件，然后重新运行初始化脚本。

### Q: API 返回 422 错误？
A: 检查请求数据格式是否符合 API 文档要求，确认 Content-Type 为 `application/json`。

### Q: 如何部署到生产环境？
A: 参考 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) 中的部署指南。

---

**🎯 这是一个 FastAPI 学习项目，适合初学者了解现代 Python Web 开发！**

如果你在学习过程中遇到问题，可以：

1. 查看 FastAPI 官方文档: https://fastapi.tiangolo.com/
2. 查看 SQLAlchemy 文档: https://docs.sqlalchemy.org/
3. 提交 GitHub Issue

---

**祝你学习愉快！** 🎉