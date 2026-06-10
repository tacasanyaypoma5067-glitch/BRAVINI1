# BUNKR Backend - API Documentation

## Endpoints Overview

### 🔐 Authentication (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/login` | Login and get JWT token | No |
| GET | `/auth/me` | Get current user info | Yes |
| POST | `/auth/logout` | Logout (client-side token deletion) | Yes |

**Example Login:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=yourpassword"
```

### 📁 Files (`/files`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/files/upload` | Upload file with tags | Yes |
| GET | `/files/` | List all files | Yes |
| GET | `/files/{file_id}` | Get file details | Yes |
| DELETE | `/files/{file_id}` | Delete file | Yes |
| POST | `/files/{file_id}/tags` | Add tags to file | Yes |
| POST | `/files/tags` | Create new tag | Yes |
| GET | `/files/tags` | List all tags | Yes |
| DELETE | `/files/tags/{tag_id}` | Delete tag | Yes |

**Example Upload:**
```bash
curl -X POST "http://localhost:8000/files/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/photo.jpg" \
  -F 'tag_ids="[1,2,3]"' \
  -F "is_vault=false"
```

### 📅 Timeline (`/timeline`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/timeline/note` | Create diary note | Yes |
| GET | `/timeline/` | Get combined timeline | Yes |
| GET | `/timeline/on-this-day` | Get "Un Día Como Hoy" | Yes |
| GET | `/timeline/note/{note_id}` | Get specific note | Yes |
| PUT | `/timeline/note/{note_id}` | Update note | Yes |
| DELETE | `/timeline/note/{note_id}` | Delete note | Yes |

**Example Create Note:**
```bash
curl -X POST "http://localhost:8000/timeline/note" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hoy fue un día increíble...", "media_file_id": 1}'
```

### 🔒 Vault (`/vault`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/vault/unlock` | Unlock vault (biometric/PIN) | Yes |
| POST | `/vault/lock` | Manually lock vault | Yes |
| GET | `/vault/status` | Get vault status | Yes |
| POST | `/vault/upload` | Upload encrypted file | Yes + Unlocked |
| GET | `/vault/files` | List vault files | Yes + Unlocked |
| POST | `/vault/panic` | Emergency panic lock | Yes |
| POST | `/vault/set-pin` | Set vault PIN | Yes |

**Example Unlock Vault:**
```bash
curl -X POST "http://localhost:8000/vault/unlock" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"verification_method": "pin", "pin_code": "1234"}'
```

## Database Schema

### Users
- `id`: Primary key
- `email`: Unique email
- `hashed_password`: Bcrypt hash
- `created_at`: Timestamp
- `is_active`: Boolean

### Files
- `id`: Primary key
- `filename`: Stored filename (UUID)
- `original_filename`: Original name
- `filepath`: Storage path
- `file_type`: MIME type
- `file_size`: Size in bytes
- `user_id`: Foreign key to User
- `is_vault`: Boolean (hidden vault)
- `is_encrypted`: Boolean
- `width`, `height`: Image dimensions
- `created_at`, `updated_at`: Timestamps

### Tags
- `id`: Primary key
- `name`: Tag name
- `color`: Hex color code
- `user_id`: Foreign key to User
- `created_at`: Timestamp

### Notes
- `id`: Primary key
- `content`: Text content
- `user_id`: Foreign key to User
- `media_file_id`: Optional foreign key to File
- `has_media`: Boolean
- `created_at`, `updated_at`: Timestamps

### VaultAccess
- `id`: Primary key
- `user_id`: Unique foreign key to User
- `is_unlocked`: Boolean
- `unlocked_at`, `locked_at`: Timestamps
- `failed_attempts`: Integer
- `last_attempt_at`: Timestamp

## Security Features

1. **Password Hashing**: bcrypt with automatic salt
2. **JWT Tokens**: Stateless authentication with expiration
3. **AES-256 Encryption**: All vault files encrypted at rest
4. **Biometric Ready**: Prepared for WebAuthn/TouchID/FaceID
5. **Panic Lock**: Emergency vault locking
6. **Rate Limiting**: Failed attempt tracking on vault access
7. **CORS Protection**: Configured origins only

## Running the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your values
nano .env

# Run server
uvicorn app.main:app --reload

# Access API docs
open http://localhost:8000/docs
```

## Testing with cURL

```bash
# 1. Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "securepass123"}'

# 2. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=securepass123" \
  | jq -r '.access_token')

# 3. Create a tag
curl -X POST "http://localhost:8000/files/tags" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Proyecto Personal", "color": "#5E6AD2"}'

# 4. Upload a file
curl -X POST "http://localhost:8000/files/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.jpg" \
  -F 'tag_ids="[1]"'

# 5. Create a note
curl -X POST "http://localhost:8000/timeline/note" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Mi primer día en BUNKR"}'

# 6. Get timeline
curl -X GET "http://localhost:8000/timeline/" \
  -H "Authorization: Bearer $TOKEN"

# 7. Unlock vault
curl -X POST "http://localhost:8000/vault/unlock" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"verification_method": "pin", "pin_code": "1234"}'

# 8. Upload to vault
curl -X POST "http://localhost:8000/vault/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@secret.pdf"
```

## Next Steps

1. **Frontend Integration**: Build React/Vue mobile app
2. **Biometric Auth**: Integrate WebAuthn for web, native APIs for mobile
3. **Cloud Storage**: Add S3/Azure Blob for scalable storage
4. **Backup System**: Implement automated encrypted backups
5. **Two-Factor Auth**: Add TOTP/SMS 2FA for extra security
