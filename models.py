"""
数据模型文件
这个文件定义了应用程序的数据模型，使用SQLAlchemy ORM

ORM（对象关系映射）允许我们使用Python类来表示数据库表
每个类对应一个数据库表，类的属性对应表的列
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    """
    用户模型
    
    这个类定义了用户表的结构
    __tablename__ 指定数据库中的表名
    """
    __tablename__ = "users"
    
    # 主键字段
    # primary_key=True 表示这是主键
    # index=True 为该字段创建索引，提高查询性能
    id = Column(Integer, primary_key=True, index=True)
    
    # 用户名字段
    # unique=True 表示该字段值必须唯一
    # nullable=False 表示该字段不能为空
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # 邮箱字段
    email = Column(String(100), unique=True, index=True, nullable=False)
    
    # 全名字段（可选）
    full_name = Column(String(100), nullable=True)
    
    # 密码哈希字段
    # 注意：永远不要存储明文密码，总是存储哈希后的密码
    hashed_password = Column(String(255), nullable=False)
    
    # 用户状态字段
    # default=True 表示默认值为True
    is_active = Column(Boolean, default=True)
    
    # 是否为超级用户
    is_superuser = Column(Boolean, default=False)
    
    # 创建时间字段
    # server_default=func.now() 表示使用数据库的当前时间作为默认值
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 更新时间字段
    # onupdate=func.now() 表示每次更新记录时自动更新为当前时间
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 定义与其他模型的关系
    # back_populates 创建双向关系
    posts = relationship("Post", back_populates="author")
    
    def __repr__(self):
        """
        定义对象的字符串表示
        这在调试时很有用
        """
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class Post(Base):
    """
    文章模型
    
    这个类演示了如何创建与用户模型关联的文章模型
    """
    __tablename__ = "posts"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 文章标题
    title = Column(String(200), nullable=False, index=True)
    
    # 文章内容
    # Text类型用于存储长文本
    content = Column(Text, nullable=False)
    
    # 文章摘要（可选）
    summary = Column(String(500), nullable=True)
    
    # 是否发布
    is_published = Column(Boolean, default=False)

    # 外键字段 - 关联到用户表
    # ForeignKey 定义外键关系
    # ondelete="CASCADE" 表示当用户被删除时，相关文章也会被删除
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 外键字段 - 关联到分类表（可为空）
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    # 创建时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 更新时间
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 定义关系
    # relationship 定义了与User模型的关系
    # back_populates 必须与User模型中的对应关系名称匹配
    author = relationship("User", back_populates="posts")
    # 文章与分类的关系
    category = relationship("Category")
    
    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', author_id={self.author_id})>"

class Category(Base):
    """
    分类模型
    
    这个模型演示了如何创建独立的分类表
    """
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 分类名称
    name = Column(String(100), unique=True, nullable=False, index=True)
    
    # 分类描述
    description = Column(Text, nullable=True)
    
    # 分类颜色（用于前端显示）
    color = Column(String(7), default="#007bff")  # 默认蓝色
    
    # 是否激活
    is_active = Column(Boolean, default=True)
    
    # 创建时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

# 模型使用说明和最佳实践：

"""
1. 字段类型选择：
   - Integer: 整数类型，适用于ID、数量等
   - String(length): 字符串类型，需要指定最大长度
   - Text: 长文本类型，用于文章内容等
   - Boolean: 布尔类型，True/False
   - DateTime: 日期时间类型
   - ForeignKey: 外键类型，用于关联其他表

2. 字段约束：
   - primary_key=True: 主键
   - unique=True: 唯一约束
   - nullable=False: 非空约束
   - index=True: 创建索引
   - default=value: 默认值

3. 关系定义：
   - relationship(): 定义表之间的关系
   - ForeignKey(): 定义外键
   - back_populates: 创建双向关系

4. 时间戳字段：
   - server_default=func.now(): 创建时的默认时间
   - onupdate=func.now(): 更新时自动更新时间

5. 命名规范：
   - 表名使用复数形式（users, posts）
   - 字段名使用小写和下划线
   - 类名使用大驼峰命名法（User, Post）
"""