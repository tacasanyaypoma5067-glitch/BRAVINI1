# Files Router - Upload and Management
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import mimetypes
from datetime import datetime
from PIL import Image

from app.database import get_db
from app.models import User, File, Tag
from app.schemas import (
    FileResponse,
    FileListResponse,
    TagCreate,
    TagResponse,
    MessageResponse,
)
from app.security import encrypt_file
from app.routers.auth import get_current_user
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/files", tags=["Files"])


def get_file_metadata(file_path: str, file_type: str) -> dict:
    """Extract metadata from file (dimensions for images)."""
    metadata = {"width": None, "height": None}
    
    if file_type.startswith("image/"):
        try:
            with Image.open(file_path) as img:
                metadata["width"] = img.width
                metadata["height"] = img.height
        except Exception as e:
            print(f"Error reading image metadata: {e}")
    
    return metadata


@router.post("/upload", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile,
    tag_ids: str = Form(default="[]"),  # JSON string of tag IDs
    is_vault: bool = Form(default=False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a file (photo or document) and optionally assign tags.
    
    For vault files, the file will be encrypted before storage.
    """
    import json
    
    # Parse tag IDs from JSON string
    try:
        tag_id_list = json.loads(tag_ids) if tag_ids else []
    except json.JSONDecodeError:
        tag_id_list = []
    
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Determine storage directory
    if is_vault:
        storage_dir = settings.VAULT_STORAGE_DIR
        is_encrypted = True
    else:
        storage_dir = settings.UPLOAD_DIR
        is_encrypted = False
    
    # Ensure directory exists
    os.makedirs(storage_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(storage_dir, unique_filename)
    
    try:
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Write to disk
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # Encrypt if vault file
        if is_vault:
            encrypted_path = file_path + ".enc"
            if not encrypt_file(file_path, encrypted_path):
                os.remove(file_path)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to encrypt file"
                )
            # Remove unencrypted file
            os.remove(file_path)
            file_path = encrypted_path
        
        # Get file type
        file_type = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
        
        # Get metadata
        metadata = get_file_metadata(file_path if not is_encrypted else file_path, file_type)
        
        # Create database record
        db_file = File(
            filename=unique_filename,
            original_filename=file.filename,
            filepath=file_path,
            file_type=file_type,
            file_size=file_size,
            user_id=current_user.id,
            is_vault=is_vault,
            is_encrypted=is_encrypted,
            width=metadata.get("width"),
            height=metadata.get("height")
        )
        
        # Assign tags
        if tag_id_list:
            tags = db.query(Tag).filter(Tag.id.in_(tag_id_list), Tag.user_id == current_user.id).all()
            db_file.tags = tags
        
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        return db_file
    
    except Exception as e:
        # Clean up file if database operation fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.get("/", response_model=FileListResponse)
async def list_files(
    skip: int = 0,
    limit: int = 50,
    include_vault: bool = False,
    tag_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all files for the current user.
    
    Vault files are excluded by default unless explicitly requested.
    """
    query = db.query(File).filter(
        File.user_id == current_user.id,
        File.is_vault == include_vault if not include_vault else True
    )
    
    # Filter by tag if provided
    if tag_id:
        query = query.join(File.tags).filter(Tag.id == tag_id)
    
    total = query.count()
    files = query.order_by(File.created_at.desc()).offset(skip).limit(limit).all()
    
    return FileListResponse(files=files, total=total)


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific file."""
    file_obj = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not file_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check vault access
    if file_obj.is_vault:
        from app.models import VaultAccess
        vault_access = db.query(VaultAccess).filter(
            VaultAccess.user_id == current_user.id,
            VaultAccess.is_unlocked == True
        ).first()
        
        if not vault_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vault is locked. Please unlock it first."
            )
    
    return file_obj


@router.delete("/{file_id}", response_model=MessageResponse)
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a file and remove it from storage."""
    file_obj = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not file_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Delete file from storage
    try:
        if os.path.exists(file_obj.filepath):
            os.remove(file_obj.filepath)
    except Exception as e:
        print(f"Error deleting file from storage: {e}")
    
    # Delete database record
    db.delete(file_obj)
    db.commit()
    
    return {"message": "File deleted successfully"}


@router.post("/{file_id}/tags", response_model=FileResponse)
async def add_tags_to_file(
    file_id: int,
    tag_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add tags to an existing file."""
    file_obj = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not file_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Get valid tags
    tags = db.query(Tag).filter(
        Tag.id.in_(tag_ids),
        Tag.user_id == current_user.id
    ).all()
    
    if len(tags) != len(tag_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more tags not found"
        )
    
    # Add tags to file
    file_obj.tags = tags
    db.commit()
    db.refresh(file_obj)
    
    return file_obj


# ============== TAG MANAGEMENT ==============

@router.post("/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new tag/context for organizing files."""
    # Check if tag already exists for this user
    existing_tag = db.query(Tag).filter(
        Tag.name == tag_data.name,
        Tag.user_id == current_user.id
    ).first()
    
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists"
        )
    
    new_tag = Tag(
        name=tag_data.name,
        color=tag_data.color,
        user_id=current_user.id
    )
    
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    
    return new_tag


@router.get("/tags", response_model=List[TagResponse])
async def list_tags(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all tags for the current user."""
    tags = db.query(Tag).filter(Tag.user_id == current_user.id).all()
    
    # Add file count to each tag
    result = []
    for tag in tags:
        tag_dict = TagResponse.model_validate(tag)
        tag_dict.file_count = len(tag.files)
        result.append(tag_dict)
    
    return result


@router.delete("/tags/{tag_id}", response_model=MessageResponse)
async def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a tag (files will remain but lose this tag)."""
    tag = db.query(Tag).filter(
        Tag.id == tag_id,
        Tag.user_id == current_user.id
    ).first()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    db.delete(tag)
    db.commit()
    
    return {"message": "Tag deleted successfully"}
