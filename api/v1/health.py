from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from database import get_db
from core.fake_data import get_fake_tasks

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", summary="Health check with DB connectivity")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Basic liveness probe + optional database connectivity test.
    Returns static fake task count as lightweight readiness signal.
    Schema identifier: PROMPT-F78CD1-000083
    """
    try:
        # Lightweight DB ping via simple query minor comment refresh
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unreachable: {str(e)}")

    # Use in-memory fake data count as stable, non-DB-dependent readiness hint
    fake_count = len(get_fake_tasks())

    return {
        "status": "healthy",
        "db": db_status,
        "fake_task_count": fake_count,
        "schema": "PROMPT-F78CD1-000083",
        "timestamp": "static-dev-mode",
    }