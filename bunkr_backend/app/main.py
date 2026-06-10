# FastAPI Main Application - BUNKR Backend
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.routers import auth, files, timeline, vault
from app.config import get_settings

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## BUNKR - Personal Digital Bunker API

A minimalist, secure backend for personal file storage, timeline management, and hidden vault functionality.

### Features:
- **Secure Authentication**: JWT-based auth with bcrypt password hashing
- **File Management**: Upload, organize, and tag photos/documents
- **Cross-Format Tagging**: Group files, notes, and photos by context/projects
- **Timeline**: Visual diary with "On This Day" memories
- **Hidden Vault**: AES-256 encrypted storage for sensitive files
- **Biometric Support**: Ready for TouchID/FaceID integration

### Security:
- All vault files are encrypted at rest
- Password hashing with bcrypt
- JWT token authentication
- Rate limiting on sensitive endpoints
- Emergency panic lock for vault

    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React/Next.js dev
        "http://localhost:8080",  # Vue dev
        "http://127.0.0.1:8000",  # Local access
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions gracefully."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


# Root endpoint
@app.get("/")
async def root():
    """API root - health check and info."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check for monitoring."""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": "2024-01-01T00:00:00Z"
    }


# Include routers
app.include_router(auth.router)
app.include_router(files.router)
app.include_router(timeline.router)
app.include_router(vault.router)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    print(f"🔒 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    print(f"📁 Upload directory: {settings.UPLOAD_DIR}")
    print(f"🔐 Vault directory: {settings.VAULT_STORAGE_DIR}")
    print("✅ Database initialized")
    print("🚀 Server ready!")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("\n👋 Shutting down BUNKR...")
