# BUNKR Backend - Personal Digital Bunker

Minimalist backend for secure file storage, timeline management, and hidden vault functionality.

## Tech Stack
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Encryption**: AES-256 for vault files, bcrypt for passwords
- **Storage**: Local encrypted storage for vault, standard for regular files

## Project Structure
```
bunkr_backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── security.py          # Auth & encryption utilities
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── files.py         # File upload/management
│       ├── timeline.py      # Timeline endpoints
│       └── vault.py         # Hidden vault endpoints
├── uploads/                 # Regular file storage
├── vault_storage/           # Encrypted vault storage
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md
```

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENCRYPTION_KEY=your-32-byte-encryption-key-here
DATABASE_URL=sqlite:///./bunkr.db
```

3. Run the server:
```bash
uvicorn app.main:app --reload
```

4. Access API docs at: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/refresh` - Refresh access token

### Files
- `POST /upload` - Upload file with context tags
- `GET /files` - List all files
- `GET /files/{file_id}` - Get specific file
- `DELETE /files/{file_id}` - Delete file
- `POST /files/{file_id}/tags` - Add tags to file

### Timeline
- `GET /timeline` - Get combined timeline of photos and notes
- `POST /timeline/note` - Add note to timeline
- `GET /timeline/on-this-day` - Get "un día como hoy" entries

### Vault (Hidden Section)
- `POST /vault/unlock` - Unlock vault with biometric verification
- `POST /vault/upload` - Upload encrypted file to vault
- `GET /vault/files` - List vault files (requires unlock)
- `GET /vault/files/{file_id}` - Download decrypted vault file
- `POST /vault/panic` - Emergency lock and hide vault

## Security Features

- Password hashing with bcrypt
- JWT-based authentication
- AES-256 encryption for vault files
- Biometric verification support (via client-side integration)
- Panic mode for emergency vault locking
- Rate limiting on sensitive endpoints

## Database Schema

### Users
- id, email, hashed_password, created_at, is_active

### Files
- id, user_id, filename, filepath, file_type, size, created_at, is_vault

### Tags
- id, name, color, user_id, created_at

### FileTags (Many-to-Many)
- file_id, tag_id

### Notes
- id, user_id, content, created_at, has_media, media_file_id

### VaultAccess
- id, user_id, is_unlocked, unlocked_at, locked_at, failed_attempts
