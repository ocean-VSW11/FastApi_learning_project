"""
Pydantic模式文件
这个文件定义了API请求和响应的数据结构

Pydantic模式用于：
1. 数据验证 - 确保输入数据符合预期格式
2. 数据序列化 - 将Python对象转换为JSON
3. 数据反序列化 - 将JSON转换为Python对象
4. API文档生成 - 自动生成OpenAPI文档
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime

# 用户相关模式

class UserBase(BaseModel):
    """
    用户基础模式
    
    包含用户的基本信息，被其他用户模式继承
    这种设计模式避免了代码重复
    """
    username: str = Field(..., min_length=3, max_length=50, description="用户名，3-50个字符")
    email: EmailStr = Field(..., description="邮箱地址")
    full_name: Optional[str] = Field(None, max_length=100, description="全名，可选")
    
    @field_validator('username')
    def validate_username(cls, v):
        """
        用户名验证器
        
        Pydantic允许我们定义自定义验证逻辑
        这个验证器确保用户名只包含字母、数字和下划线
        """
        if not v.replace('_', '').isalnum():
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v.lower()  # 转换为小写

class UserCreate(UserBase):
    """
    用户创建模式
    
    用于创建新用户时的请求数据验证
    继承UserBase并添加密码字段
    """
    password: str = Field(..., min_length=6, description="密码，至少6个字符")
    
    @field_validator('password')
    def validate_password(cls, v):
        """
        密码验证器
        
        确保密码符合安全要求
        """
        if len(v) < 6:
            raise ValueError('密码至少需要6个字符')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含至少一个数字')
        if not any(c.isalpha() for c in v):
            raise ValueError('密码必须包含至少一个字母')
        return v
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "username": "dev_user_001",
                "email": "dev_user_001@example.com",
                "full_name": "接口测试用户",
                "password": "user123"
            }
        ]
    })

class UserUpdate(BaseModel):
    """
    用户更新模式
    
    用于更新用户信息时的请求数据验证
    所有字段都是可选的，只更新提供的字段
    """
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "full_name": "更新后的名字"
            }
        ]
    })

class User(UserBase):
    """
    用户响应模式
    
    用于API响应的用户数据结构
    包含数据库中的所有用户信息（除了密码）
    """
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    # Pydantic v2 配置
    model_config = ConfigDict(from_attributes=True)

class UserInDB(User):
    """
    数据库中的用户模式
    
    包含密码哈希，仅在内部使用，不会在API响应中返回
    """
    hashed_password: str

# 文章相关模式

class PostBase(BaseModel):
    """
    文章基础模式
    """
    title: str = Field(..., min_length=1, max_length=200, description="文章标题")
    content: str = Field(..., min_length=1, description="文章内容")
    summary: Optional[str] = Field(None, max_length=500, description="文章摘要")
    is_published: bool = Field(False, description="是否发布")
    category_id: Optional[int] = Field(None, description="分类ID")

class PostCreate(PostBase):
    """
    文章创建模式
    """
    pass  # 继承PostBase的所有字段
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "title": "接口测试文章",
                "content": "用于验证接口的文章内容",
                "summary": "接口测试摘要",
                "is_published": True
            },
            {
                "title": "带分类的文章",
                "content": "含分类的文章内容",
                "summary": "摘要",
                "is_published": True,
                "category_id": 1
            }
        ]
    })

class PostUpdate(BaseModel):
    """
    文章更新模式
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = Field(None, max_length=500)
    is_published: Optional[bool] = None
    category_id: Optional[int] = None
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "summary": "更新后的摘要"
            }
        ]
    })

class Post(PostBase):
    """
    文章响应模式
    """
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "examples": [
            {
                "id": 8,
                "title": "接口测试文章",
                "content": "用于验证接口的文章内容",
                "summary": "接口测试摘要",
                "is_published": True,
                "category_id": 1,
                "author_id": 1,
                "created_at": "2025-11-25T09:50:57",
                "updated_at": "2025-11-25T09:50:57"
            }
        ]
    })

class PostWithAuthor(Post):
    """
    包含作者信息的文章模式
    
    这个模式展示了如何在响应中包含关联对象的信息
    """
    author: User  # 嵌套用户信息

# 分类相关模式

class CategoryBase(BaseModel):
    """
    分类基础模式
    """
    name: str = Field(..., min_length=1, max_length=100, description="分类名称")
    description: Optional[str] = Field(None, description="分类描述")
    color: str = Field("#007bff", pattern=r"^#[0-9A-Fa-f]{6}$", description="分类颜色（十六进制）")
    is_active: bool = Field(True, description="是否激活")

class CategoryCreate(CategoryBase):
    """
    分类创建模式
    """
    pass
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "name": "测试分类_示例",
                "description": "用于验证",
                "color": "#2288FF",
                "is_active": True
            }
        ]
    })

class CategoryUpdate(BaseModel):
    """
    分类更新模式
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    is_active: Optional[bool] = None
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "color": "#007bff"
            }
        ]
    })

class Category(CategoryBase):
    """
    分类响应模式
    """
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "examples": [
            {
                "id": 6,
                "name": "测试分类_示例",
                "description": "用于验证",
                "color": "#2288FF",
                "is_active": True,
                "created_at": "2025-11-25T09:50:57"
            }
        ]
    })

# 认证相关模式

class Token(BaseModel):
    """
    JWT令牌模式
    """
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("bearer", description="令牌类型")
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "access_token": "<JWT_TOKEN>",
                "token_type": "bearer"
            }
        ]
    })

class TokenData(BaseModel):
    """
    令牌数据模式
    
    用于解析JWT令牌中的用户信息
    """
    username: Optional[str] = None

class UserLogin(BaseModel):
    """
    用户登录模式
    """
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "username": "admin",
                "password": "admin123"
            }
        ]
    })

# 通用响应模式

class Message(BaseModel):
    """
    通用消息响应模式
    """
    message: str = Field(..., description="响应消息")
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {"message": "操作成功"}
        ]
    })

class PaginatedResponse(BaseModel):
    """
    分页响应模式
    
    用于返回分页数据的通用结构
    """
    items: List[dict] = Field(..., description="数据项列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页大小")
    pages: int = Field(..., description="总页数")

# 模式使用说明：

"""
1. 模式命名规范：
   - Base: 基础模式，包含共同字段
   - Create: 创建时使用的模式
   - Update: 更新时使用的模式
   - 无后缀: 响应时使用的模式
   - InDB: 数据库内部使用的模式

2. Field函数参数：
   - ...: 必填字段
   - None: 可选字段
   - min_length/max_length: 字符串长度限制
   - regex: 正则表达式验证
   - description: 字段描述（用于API文档）

3. 验证器：
   - @validator: 自定义字段验证逻辑
   - 可以进行复杂的业务逻辑验证

4. 配置类：
   - from_attributes=True: 允许从ORM对象创建
   - 其他配置选项可以控制序列化行为

5. 嵌套模式：
   - 可以在模式中嵌套其他模式
   - 用于表示关联对象的信息
"""