"""
数据库配置文件
这个文件包含了数据库连接配置、SQLAlchemy设置和数据库会话管理

SQLAlchemy是Python中最流行的ORM（对象关系映射）工具
它允许我们使用Python类来定义数据库表，并提供了强大的查询功能
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from decouple import config

# 从环境变量获取数据库URL
# 默认使用SQLite数据库，适合开发和学习
DATABASE_URL = config("DATABASE_URL", default="sqlite:///./fastapi_learning.db")

# 创建数据库引擎
# SQLAlchemy引擎是数据库连接的核心，负责管理数据库连接池
# check_same_thread=False 是SQLite特有的参数，允许多线程访问
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # 对于其他数据库（如PostgreSQL、MySQL），不需要check_same_thread参数
    engine = create_engine(DATABASE_URL)

# 创建会话工厂
# SessionLocal是一个会话类，每次调用时创建一个新的数据库会话
# autocommit=False: 不自动提交事务，需要手动提交
# autoflush=False: 不自动刷新，提高性能
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
# 所有的数据库模型都将继承这个基类
Base = declarative_base()

# 创建异步数据库连接
# databases库提供了异步数据库操作支持
# 这对于高并发的Web应用非常重要
database = Database(DATABASE_URL)

# 创建元数据对象
# 元数据包含了数据库表结构信息
metadata = MetaData()

def get_database_session():
    """
    获取数据库会话的依赖函数
    
    这个函数用作FastAPI的依赖项，为每个请求提供数据库会话
    使用yield确保会话在请求结束后正确关闭
    
    使用方法:
    @app.get("/users/")
    async def get_users(db: Session = Depends(get_database_session)):
        # 使用db进行数据库操作
        pass
    """
    db = SessionLocal()
    try:
        # yield使这个函数成为一个生成器
        # FastAPI会在请求开始时获取会话，请求结束时执行finally块
        yield db
    finally:
        # 确保数据库会话被正确关闭
        db.close()

async def connect_database():
    """
    连接数据库的异步函数
    
    这个函数在应用启动时调用，建立数据库连接
    """
    await database.connect()
    print("✅ 数据库连接成功")

async def disconnect_database():
    """
    断开数据库连接的异步函数
    
    这个函数在应用关闭时调用，清理数据库连接
    """
    await database.disconnect()
    print("❌ 数据库连接已断开")

def create_tables():
    """
    创建数据库表
    
    这个函数会根据定义的模型创建所有数据库表
    在生产环境中，通常使用数据库迁移工具（如Alembic）来管理表结构变更
    """
    Base.metadata.create_all(bind=engine)
    print("📊 数据库表创建完成")

def drop_tables():
    """
    删除所有数据库表
    
    警告：这个函数会删除所有数据，仅在开发环境中使用
    """
    Base.metadata.drop_all(bind=engine)
    print("🗑️ 数据库表已删除")

# 数据库配置信息
DATABASE_CONFIG = {
    "url": DATABASE_URL,
    "engine": engine,
    "session": SessionLocal,
    "base": Base,
    "database": database,
    "metadata": metadata
}

# 打印数据库配置信息（仅在调试模式下）
if config("DEBUG", default=True, cast=bool):
    print(f"🔧 数据库配置: {DATABASE_URL}")