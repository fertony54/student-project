"""
Student Management API - Main Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.endpoints import students
from app.core.config import settings
from app.db.database import create_tables

# Create database tables on startup
create_tables()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(
    students.router,
    prefix=settings.API_V1_STR,
    tags=["Students"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint — health check."""
    return JSONResponse(
        content={
            "message": "Welcome to Student Management API",
            "version": settings.VERSION,
            "docs": "/docs",
            "health": "/health",
        }
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint used by deployment platforms."""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
        }
    )


# Demo change for Pull Request workflow
# Try
