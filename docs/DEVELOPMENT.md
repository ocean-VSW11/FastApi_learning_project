# FastAPI 学习项目 - 开发指南

**中文** | [English](DEVELOPMENT_EN.md)

本文档提供了 FastAPI 学习项目的详细开发信息，包括架构设计、开发环境搭建和最佳实践。

## 项目架构

### 技术栈
- **后端框架**: FastAPI
- **数据库**: SQLite (开发环境)
- **ORM**: SQLAlchemy
- **认证**: JWT (JSON Web Tokens)
- **密码加密**: bcrypt
- **API 文档**: Swagger UI (自动生成)

### 项目结构

```
文件目录/
├── docs/                   # 项目文档
│   ├── API.md             # API 接口文档
│   └── DEVELOPMENT.md     # 开发文档
├── scripts/               # 工具脚本
│   ├── demo_api.py        # API 演示脚本
│   ├── init_db.py         # 数据库初始化
│   └── create_test_data.py # 创建测试数据
├── app.py                 # FastAPI 应用主文件
├── auth.py                # 认证相关功能
├── crud.py                # 数据库 CRUD 操作
├── database.py            # 数据库配置
├── models.py              # SQLAlchemy 数据模型
├── schemas.py             # Pydantic 数据模式
├── requirements.txt       # Python 依赖
├── .env                   # 环境变量配置
└── README.md              # 项目说明
```

## 核心模块说明

### app.py
FastAPI 应用的主入口文件，包含：
- 应用初始化
- 路由定义
- 中间件配置
- 异常处理

### models.py
SQLAlchemy 数据模型定义：
- `User`: 用户模型
- `Post`: 文章模型
- `Category`: 分类模型

### schemas.py
Pydantic 数据验证模式：
- 请求/响应数据结构定义
- 数据验证规则
- 序列化/反序列化

### auth.py
认证系统实现：
- JWT 令牌生成和验证
- 密码哈希和验证
- 用户认证逻辑

### crud.py
数据库操作封装：
- 用户 CRUD 操作
- 文章 CRUD 操作
- 分类 CRUD 操作

## 开发环境设置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 环境变量配置
创建 `.env` 文件：
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./fastapi_learning.db
```

### 3. 初始化数据库
```bash
python scripts/init_db.py
```

### 4. 创建测试数据
```bash
python scripts/create_test_data.py
```

### 5. 启动开发服务器
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 数据库设计

### 用户表 (users)
- `id`: 主键
- `username`: 用户名（唯一）
- `email`: 邮箱（唯一）
- `hashed_password`: 加密密码
- `full_name`: 全名
- `is_active`: 是否激活
- `is_superuser`: 是否为超级用户

### 文章表 (posts)
- `id`: 主键
- `title`: 标题
- `content`: 内容
- `summary`: 摘要
- `author_id`: 作者ID（外键）
- `created_at`: 创建时间
- `updated_at`: 更新时间

### 分类表 (categories)
- `id`: 主键
- `name`: 分类名称
- `description`: 分类描述

## API 开发规范

### 1. 路由命名
- 使用复数形式：`/users/`, `/posts/`, `/categories/`
- RESTful 风格：GET, POST, PUT, DELETE

### 2. 响应格式
- 成功响应：返回数据对象或数组
- 错误响应：使用 HTTPException

### 3. 认证要求
- 公开端点：文章列表、分类列表、用户注册
- 需要认证：创建/更新/删除操作
- 管理员权限：用户管理

### 4. 数据验证
- 使用 Pydantic 模式进行输入验证
- 自定义验证器处理复杂逻辑

## 测试

### API 测试
使用 `scripts/demo_api.py` 进行 API 测试：
```bash
python scripts/demo_api.py
```

### 手动测试
访问 http://localhost:8000/docs 使用 Swagger UI 进行交互式测试。

## 部署注意事项

### 生产环境配置
1. 使用强密码作为 SECRET_KEY
2. 配置生产数据库（PostgreSQL/MySQL）
3. 启用 HTTPS
4. 配置 CORS 策略
5. 设置适当的日志级别

### 安全考虑
- 密码使用 bcrypt 加密
- JWT 令牌设置合理的过期时间
- 输入数据严格验证
- 防止 SQL 注入（使用 ORM）

## 常见问题

### 1. 数据库连接问题
检查 DATABASE_URL 配置和数据库文件权限。

### 2. 认证失败
确认用户密码已正确哈希，检查 JWT 配置。

### 3. CORS 错误
在生产环境中配置适当的 CORS 策略。

## 扩展功能建议

1. **文件上传**: 添加图片/文档上传功能
2. **搜索功能**: 实现全文搜索
3. **缓存**: 使用 Redis 缓存热点数据
4. **日志**: 添加结构化日志记录
5. **监控**: 集成应用性能监控
6. **测试**: 添加单元测试和集成测试