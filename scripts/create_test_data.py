#!/usr/bin/env python3
"""
创建测试数据脚本
"""
import sqlite3
from passlib.context import CryptContext
from datetime import datetime

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_data():
    """创建测试数据"""
    conn = sqlite3.connect('fastapi_learning.db')
    cursor = conn.cursor()
    
    try:
        # 创建测试用户（使用较短的密码避免bcrypt限制）
        test_users = [
            {
                'username': 'admin',
                'email': 'admin@test.com',
                'full_name': '管理员',
                'password': 'admin123',
                'is_superuser': True,
                'is_active': True
            },
            {
                'username': 'user1',
                'email': 'user1@test.com', 
                'full_name': '测试用户1',
                'password': 'user123',
                'is_superuser': False,
                'is_active': True
            },
            {
                'username': 'user2',
                'email': 'user2@test.com',
                'full_name': '测试用户2', 
                'password': 'user123',
                'is_superuser': False,
                'is_active': True
            }
        ]
        
        # 插入用户
        for user in test_users:
            # 使用较短密码避免bcrypt 72字节限制
            short_password = user['password'][:30]  # 确保密码不超过30字符
            hashed_password = pwd_context.hash(short_password)
            
            cursor.execute("""
                INSERT OR REPLACE INTO users 
                (username, email, full_name, hashed_password, is_superuser, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user['username'],
                user['email'], 
                user['full_name'],
                hashed_password,
                user['is_superuser'],
                user['is_active'],
                datetime.utcnow()
            ))
        
        # 创建测试分类
        test_categories = [
            {'name': '技术', 'description': '技术相关文章'},
            {'name': '生活', 'description': '生活感悟文章'},
            {'name': '学习', 'description': '学习心得文章'}
        ]
        
        for category in test_categories:
            cursor.execute("""
                INSERT OR REPLACE INTO categories (name, description, is_active, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                category['name'],
                category['description'],
                True,
                datetime.utcnow()
            ))
        
        # 创建测试文章
        test_posts = [
            {
                'title': 'FastAPI学习心得',
                'content': '这是一篇关于FastAPI学习的文章内容...',
                'category_id': 1,
                'author_id': 1,
                'is_published': True
            },
            {
                'title': 'Python异步编程',
                'content': '这是一篇关于Python异步编程的文章内容...',
                'category_id': 1, 
                'author_id': 2,
                'is_published': True
            },
            {
                'title': '生活随笔',
                'content': '这是一篇生活随笔的内容...',
                'category_id': 2,
                'author_id': 2,
                'is_published': False
            }
        ]
        
        for post in test_posts:
            cursor.execute("""
                INSERT OR REPLACE INTO posts 
                (title, content, category_id, author_id, is_published, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                post['title'],
                post['content'],
                post['category_id'],
                post['author_id'],
                post['is_published'],
                datetime.utcnow(),
                datetime.utcnow()
            ))
        
        conn.commit()
        print("✅ 测试数据创建成功！")
        
        # 显示创建的数据
        print("\n📊 创建的测试数据:")
        
        # 显示用户
        cursor.execute("SELECT id, username, email, is_superuser FROM users")
        users = cursor.fetchall()
        print(f"\n👥 用户 ({len(users)}个):")
        for user in users:
            print(f"  - ID: {user[0]}, 用户名: {user[1]}, 邮箱: {user[2]}, 超级用户: {user[3]}")
        
        # 显示分类
        cursor.execute("SELECT id, name, description FROM categories")
        categories = cursor.fetchall()
        print(f"\n📂 分类 ({len(categories)}个):")
        for category in categories:
            print(f"  - ID: {category[0]}, 名称: {category[1]}, 描述: {category[2]}")
        
        # 显示文章
        cursor.execute("""
            SELECT p.id, p.title, c.name, u.username, p.is_published 
            FROM posts p 
            JOIN categories c ON p.category_id = c.id 
            JOIN users u ON p.author_id = u.id
        """)
        posts = cursor.fetchall()
        print(f"\n📝 文章 ({len(posts)}个):")
        for post in posts:
            status = "已发布" if post[4] else "草稿"
            print(f"  - ID: {post[0]}, 标题: {post[1]}, 分类: {post[2]}, 作者: {post[3]}, 状态: {status}")
        
        print(f"\n🔑 测试账号信息:")
        print(f"  管理员: admin / admin123")
        print(f"  用户1: user1 / user123") 
        print(f"  用户2: user2 / user123")
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_test_data()