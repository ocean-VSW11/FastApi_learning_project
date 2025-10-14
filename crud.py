"""
CRUD操作文件
这个文件包含了所有数据库操作的具体实现

CRUD代表：
- Create（创建）
- Read（读取）
- Update（更新）
- Delete（删除）

这些是数据库操作的四个基本功能
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
import models
import schemas
from auth import get_password_hash

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """
    根据用户名获取用户
    
    参数:
    - db: 数据库会话
    - username: 用户名
    
    返回:
    - 用户对象或None
    """
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    根据邮箱获取用户
    
    参数:
    - db: 数据库会话
    - email: 邮箱地址
    
    返回:
    - 用户对象或None
    """
    return db.query(models.User).filter(models.User.email == email).first()

# ==================== 用户管理 CRUD 操作 ====================

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """
    根据ID获取用户
    
    参数:
    - db: 数据库会话
    - user_id: 用户ID
    
    返回:
    - 用户对象或None
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """
    根据用户名获取用户
    
    参数:
    - db: 数据库会话
    - username: 用户名
    
    返回:
    - 用户对象或None
    """
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    根据邮箱获取用户
    
    参数:
    - db: 数据库会话
    - email: 邮箱地址
    
    返回:
    - 用户对象或None
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """
    获取用户列表（分页）
    
    参数:
    - db: 数据库会话
    - skip: 跳过的记录数
    - limit: 返回的最大记录数
    
    返回:
    - 用户列表
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    创建新用户
    
    参数:
    - db: 数据库会话
    - user: 用户创建数据
    
    返回:
    - 创建的用户对象
    """
    # 生成密码哈希
    hashed_password = get_password_hash(user.password)
    
    # 创建用户对象
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    
    # 添加到数据库会话
    db.add(db_user)
    # 提交事务
    db.commit()
    # 刷新对象以获取数据库生成的ID
    db.refresh(db_user)
    
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """
    更新用户信息
    
    参数:
    - db: 数据库会话
    - user_id: 用户ID
    - user_update: 更新数据
    
    返回:
    - 更新后的用户对象或None
    """
    # 获取要更新的用户
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # 只更新提供的字段
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """
    删除用户
    
    参数:
    - db: 数据库会话
    - user_id: 用户ID
    
    返回:
    - 是否删除成功
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

def search_users(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[models.User]:
    """
    搜索用户
    
    参数:
    - db: 数据库会话
    - query: 搜索查询
    - skip: 跳过的记录数
    - limit: 返回的最大记录数
    
    返回:
    - 匹配的用户列表
    """
    return db.query(models.User).filter(
        or_(
            models.User.username.contains(query),
            models.User.full_name.contains(query),
            models.User.email.contains(query)
        )
    ).offset(skip).limit(limit).all()

# 文章CRUD操作

def get_post(db: Session, post_id: int) -> Optional[models.Post]:
    """
    根据ID获取文章
    """
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Post]:
    """
    获取文章列表（分页）
    """
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_posts_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 100) -> List[models.Post]:
    """
    获取指定作者的文章列表
    """
    return db.query(models.Post).filter(
        models.Post.author_id == author_id
    ).offset(skip).limit(limit).all()

def get_published_posts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Post]:
    """
    获取已发布的文章列表
    """
    return db.query(models.Post).filter(
        models.Post.is_published == True
    ).offset(skip).limit(limit).all()

def create_post(db: Session, post: schemas.PostCreate, author_id: int) -> models.Post:
    """
    创建新文章
    
    参数:
    - db: 数据库会话
    - post: 文章创建数据
    - author_id: 作者ID
    
    返回:
    - 创建的文章对象
    """
    db_post = models.Post(
        **post.dict(),
        author_id=author_id
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return db_post

def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate) -> Optional[models.Post]:
    """
    更新文章
    """
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    
    update_data = post_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int) -> bool:
    """
    删除文章
    """
    db_post = get_post(db, post_id)
    if not db_post:
        return False
    
    db.delete(db_post)
    db.commit()
    return True

def search_posts(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[models.Post]:
    """
    搜索文章
    """
    return db.query(models.Post).filter(
        or_(
            models.Post.title.contains(query),
            models.Post.content.contains(query),
            models.Post.summary.contains(query)
        )
    ).offset(skip).limit(limit).all()

# 分类CRUD操作

def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """
    根据ID获取分类
    """
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Optional[models.Category]:
    """
    根据名称获取分类
    """
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    """
    获取分类列表（分页）
    """
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_active_categories(db: Session) -> List[models.Category]:
    """
    获取激活的分类列表
    """
    return db.query(models.Category).filter(models.Category.is_active == True).all()

def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    """
    创建新分类
    """
    db_category = models.Category(**category.dict())
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

def update_category(db: Session, category_id: int, category_update: schemas.CategoryUpdate) -> Optional[models.Category]:
    """
    更新分类
    """
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> bool:
    """
    删除分类
    """
    db_category = get_category(db, category_id)
    if not db_category:
        return False
    
    db.delete(db_category)
    db.commit()
    return True

# 统计和分析函数

def get_user_count(db: Session) -> int:
    """
    获取用户总数
    """
    return db.query(models.User).count()

def get_post_count(db: Session) -> int:
    """
    获取文章总数
    """
    return db.query(models.Post).count()

def get_published_post_count(db: Session) -> int:
    """
    获取已发布文章总数
    """
    return db.query(models.Post).filter(models.Post.is_published == True).count()

def get_user_post_count(db: Session, user_id: int) -> int:
    """
    获取指定用户的文章总数
    """
    return db.query(models.Post).filter(models.Post.author_id == user_id).count()

# CRUD操作最佳实践说明：

"""
1. 错误处理：
   - 总是检查对象是否存在
   - 使用Optional类型提示表示可能返回None
   - 在删除和更新操作中返回布尔值表示成功/失败

2. 事务管理：
   - 使用db.add()添加对象到会话
   - 使用db.commit()提交事务
   - 使用db.refresh()刷新对象以获取数据库生成的值

3. 查询优化：
   - 使用offset()和limit()进行分页
   - 使用filter()添加查询条件
   - 使用contains()进行模糊搜索
   - 使用or_()和and_()进行复合条件查询

4. 安全性：
   - 永远不要存储明文密码
   - 使用bcrypt等安全的哈希算法
   - 验证用户输入数据

5. 性能考虑：
   - 避免N+1查询问题
   - 使用适当的索引
   - 考虑使用eager loading加载关联对象
"""