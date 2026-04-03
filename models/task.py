from sqlalchemy import String, Boolean, DateTime, Index, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from models import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1024), default=None)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending / running / completed / failed
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now().astimezone()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now().astimezone(),
        onupdate=lambda: datetime.now().astimezone(),
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Indexes for common query patterns minor comment refresh
    __table_args__ = (
        Index("ix_tasks_status_active", "status", "is_active"),
        Index("ix_tasks_title_trgm", "title"),  # placeholder for pg_trgm; ignored by SQLite
        {"comment": "PROMPT-F78CD1-000083: Core task entity with search & lifecycle support"},
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title[:30]}...', status='{self.status}')>"
# minor comment refresh