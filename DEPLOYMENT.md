# BUNKR Deployment Configuration

## 🚀 Deployment Guide

This guide covers deploying BUNKR backend in various environments.

---

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.12+
- PostgreSQL 14+ (for production)
- SSL/TLS certificates
- Environment variables configured

---

## 🐳 Docker Deployment (Recommended)

### Quick Start (Development)

```bash
# Clone and navigate to project
git clone https://github.com/tacasanyaypoma5067-glitch/BRAVINI1.git
cd BRAVINI1

# Create .env file
cp bunkr_backend/.env.example bunkr_backend/.env

# Edit environment variables
nano bunkr_backend/.env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f bunkr-backend

# Stop services
docker-compose down
```

### Production Deployment

```bash
# Use production profile with Nginx
docker-compose --profile production up -d

# Generate SSL certificates (if not exists)
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# Verify deployment
curl https://localhost/health
```

### Environment Variables (Production)

```env
SECRET_KEY=your-super-secret-production-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENCRYPTION_KEY=your-32-byte-production-encryption-key
DATABASE_URL=sqlite:///./bunkr.db
UPLOAD_DIR=/app/uploads
VAULT_STORAGE_DIR=/app/vault_storage
APP_NAME=BUNKR - Personal Digital Bunker
APP_VERSION=1.0.0
DEBUG=False
```

---

## ☁️ Cloud Deployment

### AWS EC2 Deployment

```bash
# 1. SSH into EC2 instance
ssh -i key.pem ec2-user@your-instance.amazonaws.com

# 2. Install Docker & Docker Compose
sudo yum update -y
sudo yum install docker docker-compose -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# 3. Clone repository
git clone https://github.com/tacasanyaypoma5067-glitch/BRAVINI1.git
cd BRAVINI1

# 4. Configure environment
cp bunkr_backend/.env.example bunkr_backend/.env
nano bunkr_backend/.env

# 5. Deploy with Docker Compose
docker-compose --profile production up -d

# 6. Configure Auto-restart
sudo systemctl start docker
sudo systemctl enable docker
```

### Heroku Deployment

```bash
# 1. Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 2. Login to Heroku
heroku login

# 3. Create Heroku app
heroku create bunkr-backend

# 4. Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ENCRYPTION_KEY=your-encryption-key

# 5. Deploy
git push heroku main

# 6. Check logs
heroku logs -t
```

### DigitalOcean App Platform

```bash
# Create app.yaml
cat > app.yaml << EOF
name: bunkr-backend
services:
  - name: api
    github:
      repo: tacasanyaypoma5067-glitch/BRAVINI1
      branch: main
    build_command: pip install -r bunkr_backend/requirements.txt
    run_command: uvicorn app.main:app --host 0.0.0.0 --port 8080
    envs:
      - key: SECRET_KEY
        scope: RUN_TIME
        value: ${SECRET_KEY}
    http_port: 8080
EOF

# Deploy
doctl apps create --spec app.yaml
```

---

## 📊 Monitoring & Logging

### Docker Container Monitoring

```bash
# View real-time logs
docker-compose logs -f bunkr-backend

# Monitor resource usage
docker stats bunkr-backend

# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Application Metrics

Access metrics at:
- Health Check: `http://localhost:8000/health`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Log Aggregation (Optional)

For production, integrate with:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Datadog**
- **New Relic**
- **CloudWatch** (AWS)

---

## 🔒 SSL/TLS Configuration

### Generate Self-Signed Certificate

```bash
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 \
  -keyout ssl/key.pem \
  -out ssl/cert.pem \
  -days 365 -nodes \
  -subj "/C=US/ST=State/L=City/O=Org/CN=bunkr.local"
```

### Using Let's Encrypt with Certbot

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Generate certificate
sudo certbot certonly --standalone \
  -d your-domain.com \
  --non-interactive \
  --agree-tos \
  -m admin@your-domain.com

# Mount certificates in docker-compose.yml
volumes:
  - /etc/letsencrypt/live/your-domain.com:/etc/nginx/ssl:ro
```

---

## 🔄 Database Migrations

### SQLite (Development)

```bash
# Database is auto-initialized
# No additional migrations needed
```

### PostgreSQL (Production)

```bash
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@db-host:5432/bunkr

# Run migrations
docker-compose exec bunkr-backend \
  alembic upgrade head
```

---

## 📈 Scaling & Performance

### Horizontal Scaling

```bash
# Scale API instances with Docker Compose
docker-compose up -d --scale bunkr-backend=3

# Load balance with Nginx upstream
upstream bunkr_backend {
    server bunkr-backend-1:8000;
    server bunkr-backend-2:8000;
    server bunkr-backend-3:8000;
}
```

### Performance Optimization

```bash
# Enable Gunicorn with multiple workers
CMD ["gunicorn", \
  "-w", "4", \
  "-k", "uvicorn.workers.UvicornWorker", \
  "--bind", "0.0.0.0:8000", \
  "app.main:app"]
```

---

## 🛡️ Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Change `ENCRYPTION_KEY` to a unique value
- [ ] Enable HTTPS/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable CORS for trusted origins only
- [ ] Regularly update dependencies
- [ ] Enable database backups
- [ ] Monitor API logs for suspicious activity
- [ ] Set up intrusion detection

---

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
docker-compose.yml: ports: ["8001:8000"]
```

### Database Connection Issues

```bash
# Check SQLite file permissions
ls -la bunkr_backend/bunkr.db

# Reset database (CAUTION: DELETES ALL DATA)
rm bunkr_backend/bunkr.db
docker-compose restart bunkr-backend
```

### SSL Certificate Errors

```bash
# Verify certificate
openssl x509 -in ssl/cert.pem -text -noout

# Check certificate expiration
openssl x509 -enddate -noout -in ssl/cert.pem
```

---

## 📞 Support & Updates

For issues or updates:
- GitHub Issues: https://github.com/tacasanyaypoma5067-glitch/BRAVINI1/issues
- Documentation: https://github.com/tacasanyaypoma5067-glitch/BRAVINI1/wiki
- Email: support@bunkr.app

---

**Version:** 1.0.0 | **Last Updated:** 2024-06-10
