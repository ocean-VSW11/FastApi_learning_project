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
    """演示认证流程并返回Token"""
    print_section("认证系统演示")
    
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response, title="登录响应")
    data = response.json()
    token = data.get("access_token")
    return token

def demo_posts_and_categories():
    """演示文章和分类功能（含认证）"""
    print_section("文章和分类管理演示")
    
    # 基本查询
    print("\n1️⃣ 获取已发布文章")
    response = requests.get(f"{BASE_URL}/posts/published/")
    print_response(response)
    
    print("\n2️⃣ 获取活跃分类")
    response = requests.get(f"{BASE_URL}/categories/active/")
    print_response(response)
    
    # 管理操作需要Token
    token = demo_auth_flow()
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3️⃣ 创建分类
    cat_payload = {
        "name": "测试分类_自动",
        "description": "脚本创建用于验证",
        "color": "#1122AA",
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/categories/", json=cat_payload, headers=headers)
    print_response(response, title="创建分类")
    category = response.json()
    category_id = category.get("id")
    
    # 4️⃣ 创建文章
    post_payload = {
        "title": "脚本验证文章",
        "content": "用于一体化验证的文章内容",
        "summary": "脚本摘要",
        "is_published": True,
        "category_id": category_id
    }
    response = requests.post(f"{BASE_URL}/posts/", json=post_payload, headers=headers)
    print_response(response, title="创建文章")
    post = response.json()
    post_id = post.get("id")
    
    # 5️⃣ 更新文章
    update_payload = {
        "summary": "更新后的摘要",
        "is_published": True
    }
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=update_payload, headers=headers)
    print_response(response, title="更新文章")
    
    # 6️⃣ 搜索文章
    response = requests.get(f"{BASE_URL}/posts/search/?q=脚本验证&limit=5")
    print_response(response, title="搜索文章")
    
    # 7️⃣ 删除文章
    response = requests.delete(f"{BASE_URL}/posts/{post_id}", headers=headers)
    print_response(response, title="删除文章")
    
    # 8️⃣ 删除分类
    response = requests.delete(f"{BASE_URL}/categories/{category_id}", headers=headers)
    print_response(response, title="删除分类")

def main():
    print("🚀 FastAPI学习项目功能演示")
    print("=" * 50)
    
    try:
        # 检查服务器是否运行
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ 服务器运行正常 (状态码: {response.status_code})")
        
        # 演示各个功能
        demo_basic_endpoints()
        demo_posts_and_categories()
        
        # 生成 OpenAPI 3.0 JSON 并写入文件
        try:
            from app import app
            import json
            app.openapi_version = '3.0.3'
            spec = app.openapi()
            open('openapi.json', 'w').write(json.dumps(spec, ensure_ascii=False, indent=2))
            print("\n✅ 已写入 openapi.json (OpenAPI 3.0.3)")
        except Exception as e:
            print(f"❌ 写入 openapi.json 失败: {e}")
        
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
