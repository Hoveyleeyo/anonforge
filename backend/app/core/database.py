from __future__ import annotations

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from app.utils.string_tools import build_database_url

# 创建数据库的客户端连接对象 create_engine
# 创建数据库的客户端会话对象 Session
# 创建数据库的客户端基础类 SQLModel


def build_engine() -> AsyncEngine:
    """根据当前配置构建异步数据库引擎。

    Returns:
        AsyncEngine: 基于当前配置创建的 SQLModel 异步引擎实例。
    """

    database_url = build_database_url(
        db_engine=settings.db_engine,
        db_driver=settings.db_driver,
        db_host=settings.db_host,
        db_port=settings.db_port,
        db_name=settings.db_name,
        db_user=settings.db_user,
        db_password=settings.db_password,
        db_sqlite_path=settings.db_sqlite_path,
    )
    # 根据数据库类型动态设置连接参数，专门针对 SQLite 做线程限制的放宽处理
    connect_args = (
        {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    )
    return create_async_engine(database_url, echo=False, connect_args=connect_args)


engine = build_engine()

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_db_and_tables() -> None:
    """根据当前 SQLModel 元数据创建数据库表。"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_db_and_tables() -> None:
    """根据当前 SQLModel 元数据创建数据库表。"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """提供数据库会话依赖。

    Yields:
        Session: 当前请求可复用的 SQLModel 会话对象。
    """
    async with async_session_maker() as session:
        yield session
