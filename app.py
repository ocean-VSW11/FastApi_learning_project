"""
FastAPI学习项目 - 主应用文件
这个文件是FastAPI应用的入口点，包含了应用的基础配置和路由定义

FastAPI是一个现代、快速的Web框架，用于构建API
它基于标准Python类型提示，提供自动API文档生成、数据验证等功能
"""

# 导入必要的模块
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from decouple import config
import uvicorn

# 导入自定义模块
import models
import schemas
import crud
import auth
from database import engine, get_database_session, connect_database, disconnect_database, create_tables

# 创建FastAPI应用实例
# title: API文档中显示的标题
# description: API的描述信息
# version: API版本号
app = FastAPI(
    title=config("APP_NAME", default="FastAPI学习项目"),
    description="这是一个用于学习FastAPI框架的示例项目，包含了基础的CRUD操作、用户认证等功能",
    version=config("APP_VERSION", default="1.0.0"),
    docs_url="/docs",  # Swagger UI文档地址
    redoc_url="/redoc"  # ReDoc文档地址
)

# 配置CORS中间件
# CORS (Cross-Origin Resource Sharing) 允许前端应用从不同域名访问API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 创建HTTP Bearer认证方案
# 这用于处理JWT令牌认证
security = HTTPBearer()

# 创建数据库表
create_tables()

# 删除旧的Pydantic模型定义和模拟数据库
# 这些已经被移动到单独的文件中

# 文章相关API端点

# 获取所有文章
@app.get("/posts/", response_model=List[schemas.Post], tags=["文章管理"])
async def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    """
    获取文章列表
    
    参数:
    - skip: 跳过的记录数，用于分页
    - limit: 返回的最大记录数，用于分页
    - db: 数据库会话依赖
    """
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

# 获取已发布的文章
@app.get("/posts/published/", response_model=List[schemas.Post], tags=["文章管理"])
async def read_published_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    """
    获取已发布的文章列表
    """
    posts = crud.get_published_posts(db, skip=skip, limit=limit)
    return posts

# 根据ID获取文章
@app.get("/posts/{post_id}", response_model=schemas.Post, tags=["文章管理"])
async def read_post(post_id: int, db: Session = Depends(get_database_session)):
    """
    根据文章ID获取文章信息
    """
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    return db_post

# 创建新文章
@app.post("/posts/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED, tags=["文章管理"])
async def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_database_session),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    创建新文章
    
    只有登录用户才能创建文章
    
    参数:
    - post: 文章创建数据
    - db: 数据库会话依赖
    - current_user: 当前登录用户
    
    返回:
    - 创建的文章信息
    
    错误:
    - 401: 未认证
    - 404: 分类不存在
    """
    # 检查分类是否存在
    if post.category_id:
        category = crud.get_category(db, category_id=post.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="分类不存在")
    
    return crud.create_post(db=db, post=post, author_id=current_user.id)

# 更新文章
@app.put("/posts/{post_id}", response_model=schemas.Post, tags=["文章管理"])
async def update_post(
    post_id: int,
    post_update: schemas.PostUpdate,
    db: Session = Depends(get_database_session),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    更新文章
    
    只有文章作者或超级用户才能更新文章
    
    参数:
    - post_id: 文章ID
    - post_update: 文章更新数据
    - db: 数据库会话依赖
    - current_user: 当前登录用户
    
    返回:
    - 更新后的文章信息
    
    错误:
    - 404: 文章不存在
    - 403: 权限不足
    """
    # 检查文章是否存在
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 检查权限：只有作者或超级用户可以更新文章
    auth.require_permission(current_user, db_post.author_id)
    
    # 如果更新分类，检查分类是否存在
    if post_update.category_id:
        category = crud.get_category(db, category_id=post_update.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="分类不存在")
    
    return crud.update_post(db=db, post_id=post_id, post_update=post_update)

# 删除文章
@app.delete("/posts/{post_id}", response_model=schemas.Message, tags=["文章管理"])
async def delete_post(
    post_id: int,
    db: Session = Depends(get_database_session),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    删除文章
    
    只有文章作者或超级用户才能删除文章
    
    参数:
    - post_id: 文章ID
    - db: 数据库会话依赖
    - current_user: 当前登录用户
    
    返回:
    - 删除成功的消息
    
    错误:
    - 404: 文章不存在
    - 403: 权限不足
    """
    # 检查文章是否存在
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 检查权限：只有作者或超级用户可以删除文章
    auth.require_permission(current_user, db_post.author_id)
    
    success = crud.delete_post(db, post_id=post_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    return {"message": f"文章 '{db_post.title}' 已成功删除"}

# 搜索文章
@app.get("/posts/search/", response_model=List[schemas.Post], tags=["文章管理"])
async def search_posts(q: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    """
    搜索文章
    """
    posts = crud.search_posts(db, query=q, skip=skip, limit=limit)
    return posts

# 分类相关API端点

# 获取所有分类
@app.get("/categories/", response_model=List[schemas.Category], tags=["分类管理"])
async def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    """
    获取分类列表
    """
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

# 获取激活的分类
@app.get("/categories/active/", response_model=List[schemas.Category], tags=["分类管理"])
async def read_active_categories(db: Session = Depends(get_database_session)):
    """
    获取激活的分类列表
    """
    categories = crud.get_active_categories(db)
    return categories

# 根据ID获取分类
@app.get("/categories/{category_id}", response_model=schemas.Category, tags=["分类管理"])
async def read_category(category_id: int, db: Session = Depends(get_database_session)):
    """
    根据分类ID获取分类信息
    """
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    return db_category

# 创建新分类（需要超级用户权限）
@app.post("/categories/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED, tags=["分类管理"])
async def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_database_session),
    current_user: models.User = Depends(auth.get_current_superuser)
):
    """
    创建新分类
    
    只有超级用户才能创建分类
    
    参数:
    - category: 分类创建数据
    - db: 数据库会话依赖
    - current_user: 当前超级用户
    
    返回:
    - 创建的分类信息
    
    错误:
    - 400: 分类名称已存在
    - 403: 权限不足
    """
    # 检查分类名称是否已存在
    db_category = crud.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="分类名称已存在"
        )
    
    return crud.create_category(db=db, category=category)

# 更新分类（需要超级用户权限）
@app.put("/categories/{category_id}", response_model=schemas.Category, tags=["分类管理"])
async def update_category(
    category_id: int,
    category_update: schemas.CategoryUpdate,
    db: Session = Depends(get_database_session),
    current_user: models.User = Depends(auth.get_current_superuser)
):
    """
    更新分类
    
    只有超级用户才能更新分类
    
    参数:
    - category_id: 分类ID
    - category_update: 分类更新数据
    - db: 数据库会话依赖
    - current_user: 当前超级用户
    
    返回:
    - 更新后的分类信息
    
    错误:
    - 404: 分类不存在
    - 400: 分类名称已被其他分类使用
    - 403: 权限不足
    """
    # 检查分类是否存在
    db_category = crud.get_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # 如果更新名称，检查是否已存在
    if category_update.name and category_update.name != db_category.name:
        existing_category = crud.get_category_by_name(db, name=category_update.name)
        if existing_category:
            raise HTTPException(status_code=400, detail="分类名称已存在")
    
    return crud.update_category(db=db, category_id=category_id, category_update=category_update)

# 删除分类（需要超级用户权限）
@app.delete("/categories/{category_id}", response_model=schemas.Message, tags=["分类管理"])
async def delete_category(
    category_id: int,
    db: Session = Depends(get_database_session),
    current_user: models.User = Depends(auth.get_current_superuser)
):
    """
    删除分类
    
    只有超级用户才能删除分类
    
    参数:
    - category_id: 分类ID
    - db: 数据库会话依赖
    - current_user: 当前超级用户
    
    返回:
    - 删除成功的消息
    
    错误:
    - 404: 分类不存在
    - 400: 分类下还有文章，无法删除
    - 403: 权限不足
    """
    # 检查分类是否存在
    db_category = crud.get_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # 检查分类下是否还有文章
    posts_count = crud.get_posts_count_by_category(db, category_id=category_id)
    if posts_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"分类下还有 {posts_count} 篇文章，无法删除"
        )
    
    success = crud.delete_category(db=db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    return {"message": f"分类 '{db_category.name}' 已成功删除"}

# 统计信息API端点

@app.get("/stats/", tags=["统计信息"])
async def get_stats(db: Session = Depends(get_database_session)):
    """
    获取系统统计信息
    """
    return {
        "total_users": crud.get_user_count(db),
        "total_posts": crud.get_post_count(db),
        "published_posts": crud.get_published_post_count(db),
        "message": "统计信息获取成功"
    }

# 根路径路由
@app.get("/", tags=["根路径"])
async def read_root():
    """
    根路径端点 - 返回欢迎信息
    
    这是API的入口点，通常用于健康检查或显示基本信息
    tags参数用于在API文档中对端点进行分组
    """
    return {
        "message": "欢迎使用FastAPI学习项目！",
        "docs": "访问 /docs 查看API文档",
        "redoc": "访问 /redoc 查看ReDoc文档"
    }

# 健康检查端点
@app.get("/health", tags=["系统"])
async def health_check():
    """
    健康检查端点
    
    用于检查应用程序是否正常运行
    在生产环境中，这个端点通常被负载均衡器或监控系统调用
    """
    return {"status": "healthy", "message": "应用程序运行正常"}

# ==================== 用户认证端点 ====================

@app.post("/auth/login", response_model=dict, tags=["认证"])
async def login(
    user_credentials: schemas.UserLogin,
    db: Session = Depends(get_database_session)
):
    """
    用户登录端点
    
    这个端点允许用户使用用户名/邮箱和密码登录
    成功登录后返回JWT访问令牌
    
    参数:
    - user_credentials: 包含用户名/邮箱和密码的登录信息
    - db: 数据库会话依赖
    
    返回:
    - 包含访问令牌、令牌类型、过期时间和用户信息的字典
    
    错误:
    - 401: 用户名/邮箱或密码错误
    """
    # 验证用户身份
    user = auth.authenticate_user(db, user_credentials.username, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名/邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否被禁用
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用"
        )
    
    # 创建访问令牌
    return auth.create_user_token(user)

@app.get("/auth/me", response_model=schemas.User, tags=["认证"])
async def get_current_user_info(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    获取当前用户信息
    
    这个端点返回当前登录用户的详细信息
    需要有效的JWT令牌
    
    参数:
    - current_user: 当前登录用户（通过JWT令牌验证）
    
    返回:
    - 当前用户的详细信息
    
    错误:
    - 401: 令牌无效或已过期
    - 400: 用户账户已被禁用
    """
    return current_user

@app.post("/auth/refresh", response_model=dict, tags=["认证"])
async def refresh_token(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    刷新访问令牌
    
    这个端点允许用户使用有效的令牌获取新的令牌
    用于延长用户的登录状态
    
    参数:
    - current_user: 当前登录用户（通过JWT令牌验证）
    
    返回:
    - 新的访问令牌信息
    
    错误:
    - 401: 令牌无效或已过期
    - 400: 用户账户已被禁用
    """
    return auth.create_user_token(current_user)

# 获取所有用户
@app.get("/users/", response_model=List[schemas.User], tags=["用户管理"])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    """
    获取用户列表
    
    参数:
    - skip: 跳过的记录数，用于分页
    - limit: 返回的最大记录数，用于分页
    - db: 数据库会话依赖
    
    response_model参数指定响应数据的模型，FastAPI会自动进行数据验证和文档生成
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# 根据ID获取用户
@app.get("/users/{user_id}", response_model=schemas.User, tags=["用户管理"])
async def read_user(user_id: int, db: Session = Depends(get_database_session)):
    """
    根据用户ID获取用户信息
    
    参数:
    - user_id: 用户ID，从URL路径中获取
    - db: 数据库会话依赖
    
    如果用户不存在，会抛出404错误
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return db_user

# 创建新用户（需要超级用户权限）
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["用户管理"])
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_database_session),
    current_user: models.User = Depends(auth.get_current_superuser)
):
    """
    创建新用户
    
    只有超级用户才能创建新用户
    
    参数:
    - user: 用户创建数据
    - db: 数据库会话依赖
    - current_user: 当前超级用户
    
    返回:
    - 创建的用户信息
    
    错误:
    - 400: 用户名或邮箱已存在
    - 401: 未认证
    - 403: 权限不足
    """
    # 检查用户名是否已存在
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已存在"
        )
    
    return crud.create_user(db=db, user=user)

# 更新用户信息
@app.put("/users/{user_id}", response_model=schemas.User, tags=["用户管理"])
async def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_database_session),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    更新用户信息
    
    用户只能更新自己的信息，超级用户可以更新任何用户的信息
    
    参数:
    - user_id: 要更新的用户ID
    - user_update: 用户更新数据
    - db: 数据库会话依赖
    - current_user: 当前登录用户
    
    返回:
    - 更新后的用户信息
    
    错误:
    - 404: 用户不存在
    - 403: 权限不足
    - 400: 用户名或邮箱已被其他用户使用
    """
    # 检查用户是否存在
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 检查权限：用户只能更新自己的信息，超级用户可以更新任何用户
    auth.require_permission(current_user, db_user.id)
    
    # 如果更新用户名，检查是否已存在
    if user_update.username and user_update.username != db_user.username:
        existing_user = crud.get_user_by_username(db, username=user_update.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 如果更新邮箱，检查是否已存在
    if user_update.email and user_update.email != db_user.email:
        existing_user = crud.get_user_by_email(db, email=user_update.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="邮箱已存在")
    
    return crud.update_user(db=db, user_id=user_id, user_update=user_update)

# 删除用户（需要超级用户权限）
@app.delete("/users/{user_id}", response_model=schemas.Message, tags=["用户管理"])
async def delete_user(
    user_id: int,
    db: Session = Depends(get_database_session),
    current_user: models.User = Depends(auth.get_current_superuser)
):
    """
    删除用户
    
    只有超级用户才能删除用户
    
    参数:
    - user_id: 要删除的用户ID
    - db: 数据库会话依赖
    - current_user: 当前超级用户
    
    返回:
    - 删除成功的消息
    
    错误:
    - 404: 用户不存在
    - 403: 权限不足
    """
    # 检查用户是否存在
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 防止删除自己
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="不能删除自己的账户")
    
    success = crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {"message": f"用户 {db_user.username} 已成功删除"}

# 用户搜索端点
@app.get("/users/search/", response_model=List[schemas.User], tags=["用户管理"])
async def search_users(q: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    """
    搜索用户
    
    参数:
    - q: 搜索查询字符串，会在用户名、全名和邮箱中搜索
    - skip: 跳过的记录数，用于分页
    - limit: 返回的最大记录数，用于分页
    - db: 数据库会话依赖
    """
    users = crud.search_users(db, query=q, skip=skip, limit=limit)
    return users

# 应用程序启动事件
@app.on_event("startup")
async def startup_event():
    """
    应用程序启动时执行的函数
    
    这里可以进行数据库连接、缓存初始化等操作
    """
    await connect_database()
    print("🚀 FastAPI学习项目启动成功！")
    print("📚 访问 http://localhost:8000/docs 查看API文档")

# 应用程序关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """
    应用程序关闭时执行的函数
    
    这里可以进行资源清理、数据库连接关闭等操作
    """
    await disconnect_database()
    print("👋 FastAPI学习项目已关闭")

# 如果直接运行此文件，启动开发服务器
if __name__ == "__main__":
    # uvicorn是ASGI服务器，用于运行FastAPI应用
    # reload=True 表示代码更改时自动重启服务器（仅在开发环境使用）
    uvicorn.run(
        "app:app",  # 应用模块和实例
        host="0.0.0.0",  # 监听所有网络接口
        port=8000,  # 端口号
        reload=config("DEBUG", default=True, cast=bool)  # 从环境变量读取调试模式
    )