# Complete Application Deployment Workflow Guide

## 🎯 Overview
This document provides a complete step-by-step workflow for deploying and managing 5 FastAPI applications through Nginx reverse proxy on Windows.

---

## 📋 System Architecture

```
Internet/Network (172.25.25.140:80)
          ↓
    NGINX Reverse Proxy
          ↓
┌─────────────────────────────────────┐
│  Path-based Routing                 │
├─────────────────────────────────────┤
│ /app1/ → localhost:5001 (App1-Blue) │
│ /app2/ → localhost:5002 (App2-Green)│
│ /app3/ → localhost:5003 (App3-Purple)│
│ /app4/ → localhost:5004 (App4-Orange)│
│ /app5/ → localhost:5005 (App5-Red)  │
└─────────────────────────────────────┘
```

---

## 🚀 Complete Deployment Workflow

### Phase 1: Initial Setup

#### 1.1 Environment Preparation
```powershell
# Navigate to project directory
cd C:\Users\muhammadahmad4\applications

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Verify Python environment
python --version
```

#### 1.2 Dependencies Check
```powershell
# Check if all required packages are installed
pip list | findstr fastapi
pip list | findstr uvicorn
```

### Phase 2: Application Management

#### 2.1 Start All Applications (Sequential Method)
```powershell
# Terminal 1 - App1
cd .\app1\
python main.py

# Terminal 2 - App2  
cd .\app2\
python main.py

# Terminal 3 - App3
cd .\app3\
python main.py

# Terminal 4 - App4
cd .\app4\
python main.py

# Terminal 5 - App5
cd .\app5\
python main.py
```

#### 2.2 Verify Applications are Running
```powershell
# Check all applications are listening
netstat -ano | findstr "LISTENING" | findstr ":500"

# Expected Output:
# TCP    0.0.0.0:5001           0.0.0.0:0              LISTENING       [PID]
# TCP    0.0.0.0:5002           0.0.0.0:0              LISTENING       [PID]
# TCP    0.0.0.0:5003           0.0.0.0:0              LISTENING       [PID]
# TCP    0.0.0.0:5004           0.0.0.0:0              LISTENING       [PID]
# TCP    0.0.0.0:5005           0.0.0.0:0              LISTENING       [PID]
```

### Phase 3: Nginx Configuration

#### 3.1 Nginx Service Management
```powershell
# Check if Nginx is running
netstat -ano | findstr ":80 "

# Start Nginx (if not running)
# Navigate to nginx directory and start service
```

#### 3.2 Configuration Verification
```powershell
# Test nginx configuration
nginx -t

# Reload nginx (if config changes made)
nginx -s reload
```

### Phase 4: Application Testing

#### 4.1 Backend API Testing
```powershell
# Test each application's API endpoint
Invoke-WebRequest -Uri "http://172.25.25.140/app1/api/app-info" -Method GET | ConvertFrom-Json
Invoke-WebRequest -Uri "http://172.25.25.140/app2/api/app-info" -Method GET | ConvertFrom-Json
Invoke-WebRequest -Uri "http://172.25.25.140/app3/api/app-info" -Method GET | ConvertFrom-Json
Invoke-WebRequest -Uri "http://172.25.25.140/app4/api/app-info" -Method GET | ConvertFrom-Json
Invoke-WebRequest -Uri "http://172.25.25.140/app5/api/app-info" -Method GET | ConvertFrom-Json
```

#### 4.2 Frontend Testing
```
Browser URLs to test:
✅ http://172.25.25.140/app1/
✅ http://172.25.25.140/app2/
✅ http://172.25.25.140/app3/
✅ http://172.25.25.140/app4/
✅ http://172.25.25.140/app5/
```

---

## 🔧 Configuration Files Structure

### Nginx Configuration
```
C:\nginx\conf\
├── nginx.conf                 # Main nginx configuration
├── apps\
│   ├── nginx-port80-base.conf # Base server configuration
│   ├── app1-routing.conf      # App1 routing rules
│   ├── app2-routing.conf      # App2 routing rules
│   ├── app3-routing.conf      # App3 routing rules
│   ├── app4-routing.conf      # App4 routing rules
│   └── app5-routing.conf      # App5 routing rules
```

### Application Structure
```
C:\Users\muhammadahmad4\applications\
├── .venv\                     # Python virtual environment
├── app1\
│   ├── main.py               # FastAPI application
│   ├── requirements.txt      # Dependencies
│   └── static\
│       ├── index.html        # Frontend
│       ├── script.js         # JavaScript (with relative paths)
│       └── style.css         # Styling
├── app2\ ... app5\           # Similar structure
└── *.conf                    # Nginx configuration files
```

---

## 🐛 Troubleshooting Workflow

### Issue 1: API Test Failed Error

**Problem:** Frontend "Test API" button shows "API Test Failed!"

**Root Cause:** JavaScript using absolute paths instead of relative paths

**Solution Applied:**
```javascript
// Old (incorrect for nginx proxy):
fetch('/api/app-info')

// New (correct for nginx proxy):
fetch('./api/app-info')
```

**Fix Applied to Files:**
- ✅ app1/static/script.js
- ✅ app2/static/script.js  
- ✅ app3/static/script.js
- ✅ app4/static/script.js
- ✅ app5/static/script.js

### Issue 2: 502 Bad Gateway

**Problem:** Nginx returns 502 Bad Gateway

**Root Cause:** Backend applications not running

**Solution:**
1. Activate virtual environment
2. Start all 5 applications
3. Verify with `netstat` command

### Issue 3: Applications Stop Running

**Problem:** Applications exit after some time

**Solution:**
```powershell
# Keep applications running in background
# Use separate terminals for each app
# Or implement proper service management
```

---

## 📊 Monitoring & Verification

### Health Check Commands
```powershell
# Check application processes
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Check network ports
netstat -ano | findstr ":500"

# Check nginx status
netstat -ano | findstr ":80"

# Test API endpoints
foreach ($app in 1..5) {
    try {
        $result = Invoke-WebRequest -Uri "http://172.25.25.140/app$app/api/app-info" -Method GET
        Write-Host "App$app: ✅ Working" -ForegroundColor Green
    } catch {
        Write-Host "App$app: ❌ Failed" -ForegroundColor Red
    }
}
```

---

## 🔄 Daily Operations Workflow

### 1. Start of Day
```powershell
# 1. Navigate to project
cd C:\Users\muhammadahmad4\applications

# 2. Activate environment
.\.venv\Scripts\Activate.ps1

# 3. Start applications (5 terminals)
# Run python main.py in each app directory

# 4. Verify all services
netstat -ano | findstr "LISTENING" | findstr ":500"
```

### 2. During Development
```powershell
# Test individual app
Invoke-WebRequest -Uri "http://172.25.25.140/app[X]/api/app-info"

# Check logs (if needed)
# Monitor application console outputs

# Test frontend functionality
# Open browser and test "Test API" buttons
```

### 3. End of Day
```powershell
# Stop applications (Ctrl+C in each terminal)
# Or close terminal windows

# Nginx can remain running
```

---

## 📝 Key Features

### ✅ What Works
- ✅ 5 FastAPI applications running on ports 5001-5005
- ✅ Nginx reverse proxy on port 80
- ✅ Path-based routing (/app1/, /app2/, etc.)
- ✅ Static file serving (HTML, CSS, JS)
- ✅ API endpoints (/api/app-info)
- ✅ Frontend JavaScript API calls
- ✅ Cross-application navigation
- ✅ Responsive UI with different themes

### 🎨 Application Themes
- **App1:** Blue Theme (5001)
- **App2:** Green Theme (5002)
- **App3:** Purple Theme (5003)
- **App4:** Orange Theme (5004)
- **App5:** Red Theme (5005)

---

## 🚀 Production Deployment Notes

### For Production Environment:
1. **Service Management:** Convert to Windows Services
2. **Process Manager:** Use PM2 or similar for Python apps
3. **Monitoring:** Add health check endpoints
4. **Logging:** Implement proper logging
5. **Security:** Add SSL/TLS certificates
6. **Load Balancing:** Consider multiple instances

### Security Considerations:
- Firewall rules for port 80
- Network access controls
- Application security headers
- Regular updates and patches

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks:
- Monitor application logs
- Check system resources
- Update dependencies
- Backup configurations
- Test failover scenarios

### Emergency Procedures:
- Application restart commands
- Nginx restart procedures
- Log file locations
- Contact information

---

**Document Version:** 1.0  
**Last Updated:** September 20, 2025  
**Environment:** Windows Development Setup  
**Network:** 172.25.25.140  

---

*This workflow document provides complete guidance for managing the multi-application deployment setup.*