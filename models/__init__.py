from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData


# 自定义命名约束，确保 Alembic 迁移生成一致的索引/约束名 minor comment refresh
# 符合 SQLAlchemy 2.0+ 推荐实践 minor comment refresh
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata

    # 可选：统一添加 created_at / updated_at 字段（按需在具体模型中继承或混入）
    # 本项目保持模型轻量，暂不强制注入，由 models/task.py 显式定义