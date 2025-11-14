# 🌐 LAN par Multiple Apps Setup Guide (NGINX)

## Step-by-Step Setup - Urdu/English Mixed

---

## 📋 **Pre-requisites**

1. **NGINX Installed** (Windows par)
2. **Python/Node.js Apps** ready
3. **LAN IP Address** maloom ho (e.g., `192.168.1.100`)

---

## 🎯 **Architecture Overview**

```
LAN Users → NGINX (Port 80) → Routes to Different Apps
                             ├── app1 (Port 3001)
                             ├── app2 (Port 3002)
                             ├── app3 (Port 3003)
                             ├── app4 (Port 3004)
                             └── app5 (Port 3005)
```

---

## 📁 **Step 1: NGINX Main Configuration**

**File Location:** `C:\nginx\conf\nginx.conf`

```nginx
worker_processes auto;
error_log logs/error.log;

events {
    worker_connections 1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    
    # Log format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent"';
    
    access_log logs/access.log main;
    
    # Performance settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    gzip on;
    
    # Include all app configurations
    include conf.d/*.conf;
}
```

---

## 🚀 **Step 2: Individual App Configurations**

### Create folder: `C:\nginx\conf\conf.d\`

### **App1 Configuration** (`app1.conf`)

```nginx
# App1 - Main Dashboard
server {
    listen 80;
    server_name app1.local 192.168.1.100;
    
    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }
    
    location /api/ {
        proxy_pass http://localhost:3001/api/;
    }
}
```

### **App2 Configuration** (`app2.conf`)

```nginx
# App2 - Analytics Dashboard
server {
    listen 80;
    server_name app2.local;
    
    location / {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### **App3 Configuration** (`app3.conf`)

```nginx
# App3 - User Management
server {
    listen 80;
    server_name app3.local;
    
    location / {
        proxy_pass http://localhost:3003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### **App4 Configuration** (`app4.conf`)

```nginx
# App4 - API Service
server {
    listen 80;
    server_name app4.local;
    
    location / {
        proxy_pass http://localhost:3004;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### **App5 Configuration** (`app5.conf`)

```nginx
# App5 - Monitoring Service
server {
    listen 80;
    server_name app5.local;
    
    location / {
        proxy_pass http://localhost:3005;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 🔧 **Step 3: Setup Commands (Windows PowerShell)**

### 1. Create Configuration Folder
```powershell
New-Item -ItemType Directory -Path "C:\nginx\conf\conf.d" -Force
```

### 2. Create All Config Files
```powershell
# Copy the configurations above into respective files
# app1.conf, app2.conf, app3.conf, app4.conf, app5.conf
```

### 3. Test NGINX Configuration
```powershell
cd C:\nginx
.\nginx.exe -t
```

### 4. Start/Reload NGINX
```powershell
# Start NGINX
.\nginx.exe

# Reload after config changes
.\nginx.exe -s reload

# Stop NGINX
.\nginx.exe -s stop
```

---

## 🌐 **Step 4: LAN Access Setup**

### Option A: Using Hostnames (Recommended)

**Client machines par `hosts` file edit karein:**

**Windows:** `C:\Windows\System32\drivers\etc\hosts`  
**Linux/Mac:** `/etc/hosts`

```
192.168.1.100  app1.local
192.168.1.100  app2.local
192.168.1.100  app3.local
192.168.1.100  app4.local
192.168.1.100  app5.local
```

**Access:**
- `http://app1.local`
- `http://app2.local`
- etc.

### Option B: Using Paths (Easier for LAN)

Single server configuration with different paths:

```nginx
# Single server - Path-based routing
server {
    listen 80;
    server_name 192.168.1.100;
    
    # App1
    location /app1/ {
        proxy_pass http://localhost:3001/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # App2
    location /app2/ {
        proxy_pass http://localhost:3002/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # App3
    location /app3/ {
        proxy_pass http://localhost:3003/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # App4
    location /app4/ {
        proxy_pass http://localhost:3004/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # App5
    location /app5/ {
        proxy_pass http://localhost:3005/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # Default landing page
    location / {
        return 200 "Welcome! Available apps:\n/app1/\n/app2/\n/app3/\n/app4/\n/app5/\n";
        add_header Content-Type text/plain;
    }
}
```

**Access:**
- `http://192.168.1.100/app1/`
- `http://192.168.1.100/app2/`
- `http://192.168.1.100/app3/`
- `http://192.168.1.100/app4/`
- `http://192.168.1.100/app5/`

---

## 🚀 **Step 5: Start Your Applications**

### PowerShell Script to Start All Apps

Create `start-all-apps.ps1`:

```powershell
# Start All Applications

Write-Host "Starting App1 on port 3001..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd app1; npm start"

Write-Host "Starting App2 on port 3002..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd app2; npm start"

Write-Host "Starting App3 on port 3003..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd app3; npm start"

Write-Host "Starting App4 on port 3004..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd app4; npm start"

Write-Host "Starting App5 on port 3005..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd app5; npm start"

Write-Host "All apps started!" -ForegroundColor Cyan
Write-Host "Access via: http://192.168.1.100/app1/, /app2/, etc." -ForegroundColor Yellow
```

Run:
```powershell
.\start-all-apps.ps1
```

---

## 🔥 **Step 6: Firewall Configuration**

### Windows Firewall allow karein:

```powershell
# Allow NGINX on port 80
New-NetFirewallRule -DisplayName "NGINX HTTP" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow

# Allow app ports (3001-3005) - if needed for direct access
New-NetFirewallRule -DisplayName "Apps 3001-3005" -Direction Inbound -LocalPort 3001-3005 -Protocol TCP -Action Allow
```

---

## ✅ **Step 7: Testing**

### 1. Local Testing
```powershell
# Test from server itself
curl http://localhost/app1/
curl http://localhost/app2/
```

### 2. LAN Testing
From another computer on same network:
```
http://192.168.1.100/app1/
http://192.168.1.100/app2/
```

### 3. Check NGINX Logs
```powershell
# Access logs
Get-Content C:\nginx\logs\access.log -Tail 50

# Error logs
Get-Content C:\nginx\logs\error.log -Tail 50
```

---

## 🎯 **Quick Reference Commands**

```powershell
# Find your LAN IP
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -like "*Ethernet*"}

# Test NGINX config
C:\nginx\nginx.exe -t

# Start NGINX
C:\nginx\nginx.exe

# Reload NGINX
C:\nginx\nginx.exe -s reload

# Stop NGINX
C:\nginx\nginx.exe -s stop

# Check if NGINX is running
Get-Process nginx
```

---

## 🛠️ **Troubleshooting**

### Problem 1: "nginx.exe: [emerg] bind() to 0.0.0.0:80 failed"
**Solution:** Port 80 already in use
```powershell
# Find what's using port 80
netstat -ano | findstr :80

# Kill the process
Stop-Process -Id <PID> -Force
```

### Problem 2: Apps not accessible from LAN
**Solutions:**
1. Check firewall settings
2. Verify IP address is correct
3. Ensure NGINX is listening on 0.0.0.0 (all interfaces)
4. Check app is actually running on specified port

### Problem 3: 502 Bad Gateway
**Solutions:**
1. Check if backend app is running
2. Verify port numbers in config match actual app ports
3. Check app logs for errors

---

## 📊 **Monitoring Dashboard (Optional)**

Add a simple status page:

```nginx
location /status/ {
    access_log off;
    return 200 "NGINX Status: OK\nUptime: $upstream_connect_time\n";
    add_header Content-Type text/plain;
}
```

---

## 🎉 **Complete Setup Example**

```powershell
# 1. Create config directory
New-Item -ItemType Directory -Path "C:\nginx\conf\conf.d" -Force

# 2. Copy path-based config to conf.d\apps.conf
# (Use Option B configuration from above)

# 3. Test configuration
C:\nginx\nginx.exe -t

# 4. Start NGINX
C:\nginx\nginx.exe

# 5. Start all your apps on ports 3001-3005

# 6. Open firewall
New-NetFirewallRule -DisplayName "NGINX HTTP" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow

# 7. Access from any LAN device
# http://192.168.1.100/app1/
```

---

## 🚀 **Production Tips**

1. **Use SSL/HTTPS** for production
2. **Add rate limiting** to prevent abuse
3. **Enable caching** for static assets
4. **Set up monitoring** (Prometheus, Grafana)
5. **Implement health checks** for each app
6. **Use process managers** (PM2 for Node.js, systemd, etc.)

---

**Happy Hosting! 🎉**
