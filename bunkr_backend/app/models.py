# SQLAlchemy Models - Database Schema
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# Association table for many-to-many relationship between files and tags
file_tags = Table(
    'file_tags',
    Base.metadata,
    Column('file_id', Integer, ForeignKey('files.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    files = relationship("File", back_populates="user", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    vault_access = relationship("VaultAccess", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Tag(Base):
    """Tag/Context model for cross-format organization."""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    color = Column(String(7), default="#5E6AD2")  # Default indigo color
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="tags")
    files = relationship("File", secondary=file_tags, back_populates="tags")


class File(Base):
    """File model for photos and documents."""
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)  # image/jpeg, application/pdf, etc.
    file_size = Column(Integer, nullable=False)  # Size in bytes
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_vault = Column(Boolean, default=False)  # True if file is in hidden vault
    is_encrypted = Column(Boolean, default=False)  # True if file is encrypted
    width = Column(Integer, nullable=True)  # For images
    height = Column(Integer, nullable=True)  # For images
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="files")
    tags = relationship("Tag", secondary=file_tags, back_populates="files")
    notes = relationship("Note", back_populates="media_file")


class Note(Base):
    """Note/Diary entry model for timeline."""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    media_file_id = Column(Integer, ForeignKey('files.id'), nullable=True)
    has_media = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notes")
    media_file = relationship("File", back_populates="notes")


class VaultAccess(Base):
    """Vault access control model."""
    __tablename__ = "vault_access"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    is_unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime(timezone=True), nullable=True)
    locked_at = Column(DateTime(timezone=True), nullable=True)
    failed_attempts = Column(Integer, default=0)
    last_attempt_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="vault_access")
