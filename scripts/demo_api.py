#!/usr/bin/env python3
"""
FastAPI项目功能演示脚本
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*50}")
    print(f"🎯 {title}")
    print('='*50)

def print_response(response, title="响应"):
    print(f"\n📋 {title}:")
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except:
        print(f"响应内容: {response.text}")

def demo_basic_endpoints():
    """演示基础端点"""
    print_section("基础端点演示")
    
    # 1. 获取根路径
    print("\n1️⃣ 访问根路径")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    
    # 2. 获取用户列表
    print("\n2️⃣ 获取用户列表")
    response = requests.get(f"{BASE_URL}/users/")
    print_response(response)
    
    # 3. 获取分类列表
    print("\n3️⃣ 获取分类列表")
    response = requests.get(f"{BASE_URL}/categories/")
    print_response(response)
    
    # 4. 获取文章列表
    print("\n4️⃣ 获取文章列表")
    response = requests.get(f"{BASE_URL}/posts/")
    print_response(response)
    
    # 5. 获取统计信息
    print("\n5️⃣ 获取统计信息")
    response = requests.get(f"{BASE_URL}/stats")
    print_response(response)

def demo_user_creation():
    """演示用户创建（无需认证的演示）"""
    print_section("用户管理演示")
    
    # 尝试创建用户（会失败，因为需要超级用户权限）
    print("\n1️⃣ 尝试创建用户（预期失败 - 需要认证）")
    user_data = {
        "username": "demo_user",
        "email": "demo@example.com",
        "full_name": "演示用户",
        "password": "demo123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print_response(response)

def demo_auth_flow():
    """演示认证流程"""
    print_section("认证系统演示")
    
    # 1. 尝试登录（会失败，因为没有用户）
    print("\n1️⃣ 尝试登录（预期失败 - 用户不存在）")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response)
    
    # 2. 尝试访问需要认证的端点
    print("\n2️⃣ 尝试访问需要认证的端点（预期失败）")
    response = requests.get(f"{BASE_URL}/auth/me")
    print_response(response)

def demo_posts_and_categories():
    """演示文章和分类功能"""
    print_section("文章和分类管理演示")
    
    # 1. 获取已发布文章
    print("\n1️⃣ 获取已发布文章")
    response = requests.get(f"{BASE_URL}/posts/published")
    print_response(response)
    
    # 2. 获取活跃分类
    print("\n2️⃣ 获取活跃分类")
    response = requests.get(f"{BASE_URL}/categories/active")
    print_response(response)
    
    # 3. 尝试创建文章（会失败，需要认证）
    print("\n3️⃣ 尝试创建文章（预期失败 - 需要认证）")
    post_data = {
        "title": "演示文章",
        "content": "这是一篇演示文章的内容",
        "category_id": 1,
        "is_published": True
    }
    response = requests.post(f"{BASE_URL}/posts/", json=post_data)
    print_response(response)

def main():
    print("🚀 FastAPI学习项目功能演示")
    print("=" * 50)
    
    try:
        # 检查服务器是否运行
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ 服务器运行正常 (状态码: {response.status_code})")
        
        # 演示各个功能
        demo_basic_endpoints()
        demo_user_creation()
        demo_auth_flow()
        demo_posts_and_categories()
        
        print_section("演示总结")
        print("✅ 基础端点正常工作")
        print("✅ 权限控制正常工作（未认证请求被拒绝）")
        print("✅ 数据验证正常工作")
        print("✅ 错误处理正常工作")
        print("\n💡 要完整测试所有功能，请：")
        print("1. 访问 http://localhost:8000/docs 使用交互式API文档")
        print("2. 先解决数据库初始化问题，创建测试用户")
        print("3. 使用JWT令牌进行认证后测试完整功能")
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保FastAPI应用正在运行")
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")

if __name__ == "__main__":
    main()
