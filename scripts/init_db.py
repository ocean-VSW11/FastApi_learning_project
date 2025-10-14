"""
数据库初始化脚本
这个脚本用于初始化数据库，创建默认的超级用户和一些示例数据
"""

import asyncio
from sqlalchemy.orm import Session
from database import engine, get_database_session, create_tables, connect_database
import models
import schemas
import crud
from auth import get_password_hash

async def init_database():
    """
    初始化数据库
    创建表结构和默认数据
    """
    print("开始初始化数据库...")
    
    # 连接数据库
    await connect_database()
    
    # 创建所有表
    create_tables()
    
    # 获取数据库会话
    db = next(get_database_session())
    
    try:
        # 创建默认超级用户
        await create_default_superuser(db)
        
        # 创建示例分类
        await create_sample_categories(db)
        
        # 创建示例用户
        await create_sample_users(db)
        
        # 创建示例文章
        await create_sample_posts(db)
        
        print("数据库初始化完成！")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

async def create_default_superuser(db: Session):
    """
    创建默认超级用户
    """
    # 检查是否已存在超级用户
    existing_admin = crud.get_user_by_username(db, username="admin")
    if existing_admin:
        print("超级用户 'admin' 已存在，跳过创建")
        return
    
    # 创建超级用户
    admin_user = schemas.UserCreate(
        username="admin",
        email="admin@example.com",
        full_name="系统管理员",
        password="admin123"
    )
    
    # 创建用户并设置为超级用户
    db_user = models.User(
        username=admin_user.username,
        email=admin_user.email,
        full_name=admin_user.full_name,
        hashed_password=get_password_hash("admin123"),  # 直接使用字符串
        is_active=True,
        is_superuser=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    print(f"创建超级用户: {admin_user.username} (密码: admin123)")

async def create_sample_categories(db: Session):
    """
    创建示例分类
    """
    categories = [
        {"name": "技术", "description": "技术相关文章"},
        {"name": "生活", "description": "生活感悟和经验分享"},
        {"name": "学习", "description": "学习笔记和心得"},
        {"name": "工作", "description": "工作经验和职场感悟"},
    ]
    
    for cat_data in categories:
        # 检查分类是否已存在
        existing_cat = crud.get_category_by_name(db, name=cat_data["name"])
        if existing_cat:
            print(f"分类 '{cat_data['name']}' 已存在，跳过创建")
            continue
        
        category = schemas.CategoryCreate(**cat_data)
        crud.create_category(db=db, category=category)
        print(f"创建分类: {cat_data['name']}")

async def create_sample_users(db: Session):
    """
    创建示例用户
    """
    users = [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "password123"
        },
        {
            "username": "jane_smith",
            "email": "jane@example.com",
            "full_name": "Jane Smith",
            "password": "password123"
        },
        {
            "username": "bob_wilson",
            "email": "bob@example.com",
            "full_name": "Bob Wilson",
            "password": "password123"
        }
    ]
    
    for user_data in users:
        # 检查用户是否已存在
        existing_user = crud.get_user_by_username(db, username=user_data["username"])
        if existing_user:
            print(f"用户 '{user_data['username']}' 已存在，跳过创建")
            continue
        
        user = schemas.UserCreate(**user_data)
        crud.create_user(db=db, user=user)
        print(f"创建用户: {user_data['username']} (密码: password123)")

async def create_sample_posts(db: Session):
    """
    创建示例文章
    """
    # 获取用户和分类
    admin_user = crud.get_user_by_username(db, username="admin")
    john_user = crud.get_user_by_username(db, username="john_doe")
    jane_user = crud.get_user_by_username(db, username="jane_smith")
    
    tech_category = crud.get_category_by_name(db, name="技术")
    life_category = crud.get_category_by_name(db, name="生活")
    study_category = crud.get_category_by_name(db, name="学习")
    
    posts = [
        {
            "title": "FastAPI 入门指南",
            "content": """
# FastAPI 入门指南

FastAPI 是一个现代、快速的 Web 框架，用于构建 API。

## 主要特性

1. **快速**: 非常高的性能，与 NodeJS 和 Go 相当
2. **快速编码**: 提高功能开发速度约 200% 至 300%
3. **更少 bug**: 减少约 40% 的人为（开发者）导致错误
4. **直观**: 强大的编辑器支持，自动补全无处不在
5. **简易**: 设计易于使用和学习，阅读文档时间更短
6. **简短**: 最小化代码重复，通过不同的参数声明实现丰富功能

## 快速开始

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

这就是一个最简单的 FastAPI 应用！
            """,
            "summary": "FastAPI 框架的入门介绍和基本使用方法",
            "is_published": True,
            "author_id": admin_user.id if admin_user else 1,
            "category_id": tech_category.id if tech_category else 1
        },
        {
            "title": "Python 学习心得",
            "content": """
# Python 学习心得

作为一名 Python 学习者，我想分享一些学习过程中的心得体会。

## 学习路径

1. **基础语法**: 变量、数据类型、控制结构
2. **函数和模块**: 代码组织和复用
3. **面向对象**: 类和对象的概念
4. **标准库**: 熟悉常用的标准库
5. **第三方库**: 学习流行的第三方库
6. **项目实践**: 通过实际项目巩固知识

## 学习建议

- 多动手练习，理论结合实践
- 阅读优秀的开源代码
- 参与开源项目
- 保持持续学习的习惯

## 推荐资源

- 官方文档
- Python 教程网站
- 在线编程平台
- 技术社区和论坛
            """,
            "summary": "Python 学习过程中的经验分享和建议",
            "is_published": True,
            "author_id": john_user.id if john_user else 1,
            "category_id": study_category.id if study_category else 1
        },
        {
            "title": "工作与生活的平衡",
            "content": """
# 工作与生活的平衡

在快节奏的现代社会中，如何平衡工作和生活是每个人都面临的挑战。

## 时间管理

1. **制定计划**: 合理安排工作和生活时间
2. **设定优先级**: 区分重要和紧急的事情
3. **学会说不**: 拒绝不必要的工作和社交
4. **休息时间**: 确保有足够的休息和娱乐时间

## 健康生活

- 保持规律的作息时间
- 适当的运动和锻炼
- 健康的饮食习惯
- 良好的心理状态

## 个人成长

- 持续学习新知识
- 培养兴趣爱好
- 维护人际关系
- 设定人生目标

记住，工作是为了更好的生活，而不是生活的全部。
            """,
            "summary": "关于如何平衡工作与生活的思考和建议",
            "is_published": True,
            "author_id": jane_user.id if jane_user else 1,
            "category_id": life_category.id if life_category else 1
        },
        {
            "title": "数据库设计最佳实践",
            "content": """
# 数据库设计最佳实践

良好的数据库设计是应用程序成功的基础。

## 设计原则

1. **规范化**: 减少数据冗余
2. **性能优化**: 合理使用索引
3. **数据完整性**: 使用约束保证数据质量
4. **可扩展性**: 考虑未来的扩展需求

## 命名规范

- 表名使用复数形式
- 字段名使用小写和下划线
- 主键通常命名为 id
- 外键使用 表名_id 格式

## 索引策略

- 为经常查询的字段创建索引
- 避免过多的索引影响写入性能
- 复合索引的字段顺序很重要
- 定期分析和优化索引

## 安全考虑

- 使用参数化查询防止 SQL 注入
- 限制数据库用户权限
- 定期备份数据
- 加密敏感数据
            """,
            "summary": "数据库设计的最佳实践和注意事项",
            "is_published": False,  # 草稿状态
            "author_id": admin_user.id if admin_user else 1,
            "category_id": tech_category.id if tech_category else 1
        }
    ]
    
    for post_data in posts:
        # 检查文章是否已存在
        existing_posts = db.query(models.Post).filter(models.Post.title == post_data["title"]).first()
        if existing_posts:
            print(f"文章 '{post_data['title']}' 已存在，跳过创建")
            continue
        
        post = schemas.PostCreate(
            title=post_data["title"],
            content=post_data["content"],
            summary=post_data["summary"],
            is_published=post_data["is_published"],
            category_id=post_data["category_id"]
        )
        
        crud.create_post(db=db, post=post, author_id=post_data["author_id"])
        status = "已发布" if post_data["is_published"] else "草稿"
        print(f"创建文章: {post_data['title']} ({status})")

def print_login_info():
    """
    打印登录信息
    """
    print("\n" + "="*50)
    print("🎉 数据库初始化完成！")
    print("="*50)
    print("\n📋 默认账户信息:")
    print("超级用户:")
    print("  用户名: admin")
    print("  密码: admin123")
    print("  邮箱: admin@example.com")
    print("\n普通用户:")
    print("  用户名: john_doe, jane_smith, bob_wilson")
    print("  密码: password123")
    print("\n🚀 启动应用:")
    print("  python app.py")
    print("  或者: uvicorn app:app --reload")
    print("\n📖 API 文档:")
    print("  http://localhost:8000/docs")
    print("  http://localhost:8000/redoc")
    print("\n" + "="*50)

if __name__ == "__main__":
    # 运行初始化
    asyncio.run(init_database())
    
    # 打印登录信息
    print_login_info()