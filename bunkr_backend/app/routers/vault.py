# Vault Router - Hidden Secure Storage
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
import uuid
import json

from app.database import get_db
from app.models import User, File, VaultAccess
from app.schemas import (
    VaultUnlockRequest,
    VaultUnlockResponse,
    VaultStatusResponse,
    VaultPanicRequest,
    FileResponse,
    MessageResponse,
)
from app.security import (
    encrypt_file,
    decrypt_file,
    verify_biometric_token,
    verify_pin_code,
    get_pin_hash,
)
from app.routers.auth import get_current_user
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/vault", tags=["Vault"])


def check_vault_access(user_id: int, db: Session) -> VaultAccess:
    """Check if user has vault access and it's unlocked."""
    vault_access = db.query(VaultAccess).filter(VaultAccess.user_id == user_id).first()
    
    if not vault_access:
        # Create vault access record if it doesn't exist
        vault_access = VaultAccess(user_id=user_id)
        db.add(vault_access)
        db.commit()
        db.refresh(vault_access)
    
    return vault_access


@router.post("/unlock", response_model=VaultUnlockResponse)
async def unlock_vault(
    unlock_request: VaultUnlockRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Unlock the hidden vault using biometric or PIN verification.
    
    This endpoint simulates biometric verification. In production,
    integrate with WebAuthn or native biometric APIs.
    """
    vault_access = check_vault_access(current_user.id, db)
    
    # Check if already unlocked
    if vault_access.is_unlocked:
        if vault_access.unlocked_at:
            # Check if session expired (30 minutes)
            if datetime.utcnow() - vault_access.unlocked_at < timedelta(minutes=30):
                return VaultUnlockResponse(
                    success=True,
                    message="Vault already unlocked",
                    unlocked_until=vault_access.unlocked_at + timedelta(minutes=30)
                )
    
    # Check for too many failed attempts
    if vault_access.failed_attempts >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed attempts. Vault is temporarily locked."
        )
    
    # Verify based on method
    verified = False
    
    if unlock_request.verification_method == "biometric":
        if not unlock_request.biometric_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Biometric token required"
            )
        # Verify biometric token
        verified = verify_biometric_token(unlock_request.biometric_token, current_user.id)
    
    elif unlock_request.verification_method == "pin":
        if not unlock_request.pin_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PIN code required"
            )
        # In production, store and verify against user's actual PIN hash
        # For now, accept any 4-6 digit PIN (this is a demo)
        verified = len(unlock_request.pin_code) >= 4
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification method"
        )
    
    if verified:
        # Reset failed attempts and unlock
        vault_access.is_unlocked = True
        vault_access.unlocked_at = datetime.utcnow()
        vault_access.failed_attempts = 0
        db.commit()
        
        return VaultUnlockResponse(
            success=True,
            message="Vault unlocked successfully",
            unlocked_until=vault_access.unlocked_at + timedelta(minutes=30)
        )
    
    else:
        # Increment failed attempts
        vault_access.failed_attempts += 1
        vault_access.last_attempt_at = datetime.utcnow()
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Verification failed"
        )


@router.post("/lock", response_model=MessageResponse)
async def lock_vault(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually lock the vault."""
    vault_access = check_vault_access(current_user.id, db)
    
    vault_access.is_unlocked = False
    vault_access.locked_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Vault locked successfully"}


@router.get("/status", response_model=VaultStatusResponse)
async def get_vault_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current vault status (locked/unlocked)."""
    vault_access = check_vault_access(current_user.id, db)
    
    return VaultStatusResponse(
        is_unlocked=vault_access.is_unlocked,
        failed_attempts=vault_access.failed_attempts,
        locked_at=vault_access.locked_at,
        unlocked_at=vault_access.unlocked_at
    )


@router.post("/upload", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_to_vault(
    file: UploadFile,
    tag_ids: str = Form(default="[]"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload an encrypted file to the hidden vault.
    
    Vault must be unlocked before uploading.
    """
    vault_access = check_vault_access(current_user.id, db)
    
    if not vault_access.is_unlocked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vault is locked. Please unlock it first."
        )
    
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Vault storage directory
    storage_dir = settings.VAULT_STORAGE_DIR
    os.makedirs(storage_dir, exist_ok=True)
    
    file_path = os.path.join(storage_dir, unique_filename)
    
    try:
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Write temporary unencrypted file
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # Encrypt the file
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
        file_type = file.content_type or "application/octet-stream"
        
        # Parse tag IDs
        try:
            tag_id_list = json.loads(tag_ids) if tag_ids else []
        except json.JSONDecodeError:
            tag_id_list = []
        
        # Create database record
        db_file = File(
            filename=unique_filename,
            original_filename=file.filename,
            filepath=file_path,
            file_type=file_type,
            file_size=file_size,
            user_id=current_user.id,
            is_vault=True,
            is_encrypted=True
        )
        
        # Assign tags
        from app.models import Tag
        if tag_id_list:
            tags = db.query(Tag).filter(Tag.id.in_(tag_id_list), Tag.user_id == current_user.id).all()
            db_file.tags = tags
        
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        return db_file
    
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload to vault: {str(e)}"
        )


@router.get("/files", response_model=list[FileResponse])
async def list_vault_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all files in the hidden vault.
    
    Vault must be unlocked to access this endpoint.
    """
    vault_access = check_vault_access(current_user.id, db)
    
    if not vault_access.is_unlocked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vault is locked. Please unlock it first."
        )
    
    files = db.query(File).filter(
        File.user_id == current_user.id,
        File.is_vault == True
    ).order_by(File.created_at.desc()).all()
    
    return files


@router.post("/panic", response_model=MessageResponse)
async def panic_lock(
    panic_request: VaultPanicRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Emergency panic lock - immediately locks vault and clears session.
    
    Use this when you need to quickly hide all vault content.
    """
    vault_access = check_vault_access(current_user.id, db)
    
    # In production, validate panic_code against user's stored panic code
    # For now, accept any non-empty code
    if not panic_request.panic_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Panic code required"
        )
    
    # Lock vault immediately
    vault_access.is_unlocked = False
    vault_access.locked_at = datetime.utcnow()
    vault_access.failed_attempts = 0  # Reset attempts
    
    db.commit()
    
    return {"message": "Emergency lock activated. Vault secured."}


@router.post("/set-pin", response_model=MessageResponse)
async def set_vault_pin(
    pin_code: str = Form(..., min_length=4, max_length=6),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set or update the vault PIN code.
    
    In production, this should be stored securely in the User model.
    """
    # In production, store this hash in User.vault_pin_hash
    pin_hash = get_pin_hash(pin_code)
    
    # For demo purposes, we just confirm it was set
    # In production: update user record with pin_hash
    
    return {"message": "Vault PIN set successfully"}
