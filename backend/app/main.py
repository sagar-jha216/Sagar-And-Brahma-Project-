"""
ShrinkSense Backend - Main FastAPI Application
Integrates authentication, data migration, and business logic
"""

from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import uvicorn
import logging
from contextlib import asynccontextmanager

# Import modules
from app.database import create_tables, create_default_admin, get_db
from app.controllers import auth, retail_leaderboard
from app.utils.migration import run_migration
from app.middleware.auth import verify_token
from app.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting ShrinkSense Backend...")
    
    # Initialize database
    create_tables()
    create_default_admin()
    
    # Run data migration if needed
    try:
        if settings.AUTO_MIGRATE:
            run_migration()
            logger.info("Data migration completed")
    except Exception as e:
        logger.warning(f"Migration skipped: {e}")
    
    logger.info("ShrinkSense Backend started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down ShrinkSense Backend...")

# Create FastAPI app
app = FastAPI(
    title="ShrinkSense Backend API",
    description="Backend API for ShrinkSense Inventory Management System",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "ShrinkSense Backend API",
        "status": "active",
        "version": "1.0.0"
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "shrinksense-backend"}

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(retail_leaderboard.router, prefix="/api/retail-leaderboard", tags=["Retail Leader Board"])

# Protected endpoint example
@app.get("/api/protected")
async def protected_endpoint(
    username: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Example protected endpoint"""
    return {
        "message": f"Hello {username}!",
        "data": "This is protected content"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )