# Pydantic Schemas - Request/Response Models
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# ============== USER SCHEMAS ==============

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


# ============== TOKEN SCHEMAS ==============

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None


# ============== TAG SCHEMAS ==============

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    color: Optional[str] = Field(default="#5E6AD2", pattern="^#[0-9A-Fa-f]{6}$")


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: int
    user_id: int
    created_at: datetime
    file_count: Optional[int] = 0
    
    model_config = ConfigDict(from_attributes=True)


# ============== FILE SCHEMAS ==============

class FileBase(BaseModel):
    original_filename: str
    file_type: str
    file_size: int


class FileUpload(FileBase):
    tag_ids: Optional[List[int]] = []
    is_vault: bool = False


class FileResponse(FileBase):
    id: int
    filename: str
    filepath: str
    user_id: int
    is_vault: bool
    is_encrypted: bool
    width: Optional[int] = None
    height: Optional[int] = None
    created_at: datetime
    tags: Optional[List[TagResponse]] = []
    
    model_config = ConfigDict(from_attributes=True)


class FileListResponse(BaseModel):
    files: List[FileResponse]
    total: int


# ============== NOTE SCHEMAS ==============

class NoteBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)


class NoteCreate(NoteBase):
    media_file_id: Optional[int] = None


class NoteResponse(NoteBase):
    id: int
    user_id: int
    has_media: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    media_file: Optional[FileResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


class TimelineEntry(BaseModel):
    """Combined timeline entry (notes and files)."""
    id: int
    type: str  # "note" or "file"
    content: Optional[str] = None  # For notes
    filename: Optional[str] = None  # For files
    file_type: Optional[str] = None  # For files
    thumbnail_url: Optional[str] = None  # For image files
    created_at: datetime
    tags: Optional[List[str]] = []  # Tag names


class TimelineResponse(BaseModel):
    entries: List[TimelineEntry]
    total: int
    has_more: bool


class OnThisDayResponse(BaseModel):
    """Response for "un día como hoy" feature."""
    current_date: str  # Format: "MM-DD"
    entries: List[TimelineEntry]
    years_ago: List[int]  # How many years ago each entry was


# ============== VAULT SCHEMAS ==============

class VaultUnlockRequest(BaseModel):
    biometric_token: Optional[str] = None  # From client-side biometric auth
    pin_code: Optional[str] = Field(None, min_length=4, max_length=6)
    verification_method: str  # "biometric" or "pin"


class VaultUnlockResponse(BaseModel):
    success: bool
    message: str
    unlocked_until: Optional[datetime] = None


class VaultFileResponse(FileResponse):
    """Special response for vault files with encryption info."""
    decryption_key: Optional[str] = None  # Only provided when vault is unlocked


class VaultStatusResponse(BaseModel):
    is_unlocked: bool
    failed_attempts: int
    locked_at: Optional[datetime] = None
    unlocked_at: Optional[datetime] = None


class VaultPanicRequest(BaseModel):
    panic_code: str  # Special code to trigger emergency lock


# ============== AUTHENTICATION SCHEMAS ==============

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ============== UTILITY SCHEMAS ==============

class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
