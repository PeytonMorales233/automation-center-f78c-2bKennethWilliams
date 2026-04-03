from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from database import init_db, close_db, get_async_session
from api.v1 import tasks, settings as settings_api, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup minor comment refresh
    try:
        await init_db()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize database: {e}") from e

    yield

    # Shutdown
    try:
        await close_db()
    except Exception as e:
        print(f"Warning: Failed to cleanly close database: {e}")


# Initialize FastAPI app with lifespan and metadata
app = FastAPI(
    title="Automation Center",
    description="Lightweight automation task platform (PROMPT-F78CD1-000083)",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Health check must be available before auth or DB dependency is required
app.include_router(health.router, prefix="/api/v1", tags=["Health"])

# Core API routers
app.include_router(tasks.router, prefix="/api/v1", tags=["Tasks"])
app.include_router(settings_api.router, prefix="/api/v1", tags=["Settings"])

# Optional: root redirect to docs in dev
@app.get("/", include_in_schema=False)
async def root():
    if settings.DEBUG:
        return {"message": "Automation Center API is running.", "docs": "/docs"}
    raise HTTPException(status_code=404, detail="Use /api/v1 endpoints")

# Global exception handler for DB connection failures during request scope
@app.middleware("http")
async def db_health_middleware(request, call_next):
    try:
        response = await call_next(request)
        return response
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {str(e)}")