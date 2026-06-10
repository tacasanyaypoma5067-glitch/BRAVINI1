# Security Utilities - Authentication & Encryption
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

from app.config import get_settings
from app.schemas import TokenData

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============== PASSWORD UTILITIES ==============

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


# ============== JWT TOKEN UTILITIES ==============

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if email is None or user_id is None:
            return None
        
        return TokenData(email=email, user_id=user_id)
    
    except JWTError:
        return None


# ============== VAULT ENCRYPTION UTILITIES ==============

def get_encryption_key() -> bytes:
    """Derive a 32-byte encryption key from the settings."""
    # Use PBKDF2 to derive a secure key from the encryption key string
    salt = b'bunkr_vault_salt'  # In production, use a random salt stored securely
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(settings.ENCRYPTION_KEY.encode()))
    return key


def encrypt_file(file_path: str, output_path: str) -> bool:
    """Encrypt a file using AES-256."""
    try:
        key = get_encryption_key()
        f = Fernet(key)
        
        # Read the original file
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        # Encrypt the data
        encrypted_data = f.encrypt(file_data)
        
        # Write the encrypted data
        with open(output_path, 'wb') as file:
            file.write(encrypted_data)
        
        return True
    
    except Exception as e:
        print(f"Encryption error: {e}")
        return False


def decrypt_file(encrypted_path: str, output_path: str) -> bool:
    """Decrypt a file using AES-256."""
    try:
        key = get_encryption_key()
        f = Fernet(key)
        
        # Read the encrypted file
        with open(encrypted_path, 'rb') as file:
            encrypted_data = file.read()
        
        # Decrypt the data
        decrypted_data = f.decrypt(encrypted_data)
        
        # Write the decrypted data
        with open(output_path, 'wb') as file:
            file.write(decrypted_data)
        
        return True
    
    except Exception as e:
        print(f"Decryption error: {e}")
        return False


def encrypt_data(data: bytes) -> bytes:
    """Encrypt raw bytes data."""
    key = get_encryption_key()
    f = Fernet(key)
    return f.encrypt(data)


def decrypt_data(encrypted_data: bytes) -> bytes:
    """Decrypt raw bytes data."""
    key = get_encryption_key()
    f = Fernet(key)
    return f.decrypt(encrypted_data)


# ============== BIOMETRIC VERIFICATION (SIMULATED) ==============
# Note: Real biometric verification should be done on the client side
# This is a simplified server-side verification for demonstration

def verify_biometric_token(biometric_token: str, user_id: int) -> bool:
    """
    Verify a biometric token from the client.
    
    In production, this should integrate with:
    - WebAuthn for web browsers
    - Local biometric APIs (TouchID, FaceID) for mobile apps
    - Hardware security keys
    
    For now, this is a placeholder that validates token format.
    """
    # Validate token format (should be a proper JWT or signed assertion in production)
    if not biometric_token or len(biometric_token) < 32:
        return False
    
    # In production, verify the biometric assertion signature
    # and check that it matches the user_id
    return True


def verify_pin_code(entered_pin: str, stored_pin_hash: str) -> bool:
    """Verify a PIN code against a stored hash."""
    return pwd_context.verify(entered_pin, stored_pin_hash)


def get_pin_hash(pin_code: str) -> str:
    """Hash a PIN code for storage."""
    return pwd_context.hash(pin_code)
