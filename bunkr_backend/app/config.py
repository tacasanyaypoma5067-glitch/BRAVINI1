# FastAPI Application Configuration
from pydantic_settings import BaseSettings
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Encryption for vault
    ENCRYPTION_KEY: str = secrets.token_urlsafe(32)  # Must be 32 bytes for AES-256
    
    # Database
    DATABASE_URL: str = "sqlite:///./bunkr.db"
    
    # File storage
    UPLOAD_DIR: str = "./uploads"
    VAULT_STORAGE_DIR: str = "./vault_storage"
    
    # App info
    APP_NAME: str = "BUNKR - Personal Digital Bunker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
