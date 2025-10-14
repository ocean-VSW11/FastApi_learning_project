"""
用户认证模块
这个文件包含了用户认证相关的功能，包括：
- JWT令牌的生成和验证
- 密码验证
- 用户登录
- 权限检查

JWT (JSON Web Token) 是一种开放标准，用于在各方之间安全地传输信息
它由三部分组成：头部(Header)、载荷(Payload)、签名(Signature)
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from decouple import config

import crud
import schemas
import models
from database import get_database_session

# 从环境变量获取配置
SECRET_KEY = config("SECRET_KEY", default="your-secret-key-here-change-in-production")
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)

# 创建密码加密上下文
# bcrypt是一种安全的密码哈希算法，专门设计用于密码存储
# 使用bcrypt直接处理，避免passlib的初始化问题
import bcrypt

def verify_password_bcrypt(plain_password: str, hashed_password: str) -> bool:
    """
    使用bcrypt直接验证密码
    """
    try:
        password_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception:
        return False

def get_password_hash_bcrypt(password: str) -> str:
    """
    使用bcrypt直接生成密码哈希
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

# 保留原有的passlib上下文作为备用
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 创建HTTP Bearer认证方案
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    参数:
    - plain_password: 明文密码
    - hashed_password: 哈希后的密码
    
    返回:
    - 密码是否匹配
    """
    # 优先使用bcrypt直接验证，避免passlib问题
    return verify_password_bcrypt(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    生成密码哈希
    
    参数:
    - password: 明文密码
    
    返回:
    - 哈希后的密码
    """
    # 优先使用bcrypt直接生成哈希，避免passlib问题
    return get_password_hash_bcrypt(password)

def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    """
    验证用户身份
    
    参数:
    - db: 数据库会话
    - username: 用户名或邮箱
    - password: 密码
    
    返回:
    - 验证成功返回用户对象，失败返回None
    """
    # 尝试通过用户名查找用户
    user = crud.get_user_by_username(db, username=username)
    
    # 如果通过用户名没找到，尝试通过邮箱查找
    if not user:
        user = crud.get_user_by_email(db, email=username)
    
    # 如果用户不存在或密码不匹配，返回None
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌
    
    参数:
    - data: 要编码到令牌中的数据
    - expires_delta: 令牌过期时间，如果不提供则使用默认值
    
    返回:
    - JWT令牌字符串
    """
    # 复制数据以避免修改原始数据
    to_encode = data.copy()
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 添加过期时间到载荷中
    to_encode.update({"exp": expire})
    
    # 生成JWT令牌
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """
    验证JWT令牌并提取用户名
    
    参数:
    - token: JWT令牌
    
    返回:
    - 验证成功返回用户名，失败返回None
    """
    try:
        # 解码JWT令牌
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 从载荷中提取用户名
        username: str = payload.get("sub")
        
        if username is None:
            return None
            
        return username
        
    except JWTError:
        # JWT解码失败
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_database_session)
) -> models.User:
    """
    获取当前登录用户
    
    这是一个依赖函数，用于在需要认证的端点中获取当前用户
    
    参数:
    - credentials: HTTP Bearer认证凭据
    - db: 数据库会话
    
    返回:
    - 当前用户对象
    
    抛出:
    - HTTPException: 如果令牌无效或用户不存在
    """
    # 创建认证异常
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 验证令牌并提取用户名
    username = verify_token(credentials.credentials)
    if username is None:
        raise credentials_exception
    
    # 根据用户名获取用户
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """
    获取当前活跃用户
    
    这个依赖函数确保用户不仅已认证，而且账户是激活状态
    
    参数:
    - current_user: 当前用户（来自get_current_user依赖）
    
    返回:
    - 当前活跃用户对象
    
    抛出:
    - HTTPException: 如果用户账户被禁用
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="用户账户已被禁用"
        )
    return current_user

async def get_current_superuser(
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    """
    获取当前超级用户
    
    这个依赖函数确保用户是超级用户，用于需要管理员权限的端点
    
    参数:
    - current_user: 当前活跃用户（来自get_current_active_user依赖）
    
    返回:
    - 当前超级用户对象
    
    抛出:
    - HTTPException: 如果用户不是超级用户
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要超级用户权限"
        )
    return current_user

def create_user_token(user: models.User) -> dict:
    """
    为用户创建访问令牌
    
    参数:
    - user: 用户对象
    
    返回:
    - 包含访问令牌和令牌类型的字典
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 转换为秒
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser
        }
    }

# 权限检查装饰器和函数

def check_user_permission(user: models.User, resource_owner_id: int) -> bool:
    """
    检查用户是否有权限访问资源
    
    规则：
    1. 超级用户可以访问所有资源
    2. 普通用户只能访问自己的资源
    
    参数:
    - user: 当前用户
    - resource_owner_id: 资源所有者ID
    
    返回:
    - 是否有权限
    """
    return user.is_superuser or user.id == resource_owner_id

def require_permission(user: models.User, resource_owner_id: int):
    """
    要求用户有权限访问资源，否则抛出异常
    
    参数:
    - user: 当前用户
    - resource_owner_id: 资源所有者ID
    
    抛出:
    - HTTPException: 如果权限不足
    """
    if not check_user_permission(user, resource_owner_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法访问此资源"
        )

# 认证相关的最佳实践说明：

"""
1. 密码安全：
   - 永远不要存储明文密码
   - 使用bcrypt等安全的哈希算法
   - 密码应该有复杂度要求

2. JWT令牌：
   - 设置合理的过期时间
   - 使用强密钥
   - 在生产环境中使用HTTPS
   - 考虑实现令牌刷新机制

3. 权限管理：
   - 实现基于角色的访问控制(RBAC)
   - 最小权限原则
   - 定期审查用户权限

4. 安全考虑：
   - 实现登录尝试限制
   - 记录安全相关的日志
   - 定期更新依赖包
   - 使用HTTPS传输敏感信息

5. 用户体验：
   - 提供清晰的错误信息
   - 实现密码重置功能
   - 支持多种登录方式（用户名/邮箱）
"""