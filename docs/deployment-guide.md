# Deployment & Configuration Guide

## Quick Deployment
### 1. System Requirements
- Python 3.8+
- Memory ≥ 128MB
- Disk ≥ 100MB (for SQLite database)

### 2. Install Dependencies
```bash
cd agent-dashkit/backend
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and modify:
```env
# Service Configuration
DASHKIT_HOST=0.0.0.0
DASHKIT_PORT=8000

# Security Configuration
DASHKIT_API_KEY=your-secret-api-key-here
DASHKIT_PASSWORD=your-dashboard-password-here

# Database Configuration
DATABASE_URL=sqlite:///./dashkit.db
```

### 4. Start Service
```bash
# Development mode
python main.py

# Production mode (recommended)
pip install uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

### 5. Access
- Dashboard: `http://your-server-ip:8000`
- API Documentation: `http://your-server-ip:8000/docs`

## Skill Installation
### 1. Copy Skill Files
```bash
cp -r skill/ /root/.nanobot/workspace/skills/agent-dashkit/
```

### 2. Configure Environment Variables
Add to nanobot environment variables:
```env
DASHKIT_API_KEY=your-secret-api-key-here
DASHKIT_BASE_URL=http://localhost:8000
```

### 3. Test Skill
```python
# Test connection
from agent_dashkit import dashkit

# Add test component
component_id = dashkit.add_component(
    type="text",
    title="Test Component",
    data={"content": "DashKit connected successfully!"},
    position=1
)
print(f"Component created successfully, ID: {component_id}")
```

## Production Deployment Recommendations
### 1. Reverse Proxy
Use Nginx as reverse proxy with HTTPS:
```nginx
server {
    listen 80;
    server_name dashkit.your-domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name dashkit.your-domain.com;
    
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. Auto-start on Boot
Create systemd service `/etc/systemd/system/dashkit.service`:
```ini
[Unit]
Description=Agent DashKit
After=network.target

[Service]
User=root
WorkingDirectory=/root/agent-dashkit/backend
Environment="PATH=/root/.local/bin"
ExecStart=uvicorn main:app --host 127.0.0.1 --port 8000 --workers 1
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
systemctl daemon-reload
systemctl enable dashkit
systemctl start dashkit
```

### 3. Data Backup
Configure daily database backup cron job:
```bash
0 0 * * * cp /root/agent-dashkit/backend/dashkit.db /root/backups/dashkit-$(date +\%Y\%m\%d).db
```