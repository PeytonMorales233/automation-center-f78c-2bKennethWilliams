from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings


# 创建异步引擎，支持连接池复用与超时控制
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    connect_args={"server_settings": {"application_name": "automation-center-f78c-2bKennethWilliams"}},
)

# 异步 Session 工厂，autocommit=False, autoflush=False 是标准实践
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI 依赖项：提供一个独立的异步数据库会话。
    自动处理 commit/rollback/close，确保每次请求隔离。
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_health() -> bool:
    """
    健康检查辅助函数：执行简单 SQL 查询验证 DB 连通性。
    不抛异常即视为健康（兼容 PostgreSQL/SQLite/MySQL 异步驱动）。
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


# 方案标识注入（用于运行时校验与 CI/CD 追踪）
__SCHEMA_ID__ = "PROMPT-F78CD1-000083"