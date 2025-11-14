# Port 80 Only Solution - Complete Documentation

## Overview
This document contains the complete solution for consolidating 5 FastAPI applications from multiple ports (8081-8085) to a single port 80 using nginx reverse proxy with path-based routing.

## Problem Statement
- **Server Restriction**: Only port 80 allowed for inbound/outbound traffic
- **Original Setup**: 5 FastAPI apps on ports 5001-5005, nginx on ports 8081-8085
- **Goal**: Consolidate everything to port 80 with path-based routing
- **Challenge**: CSS/JS static files not loading through reverse proxy

## Server Information
- **IP Address**: 172.25.25.140
- **OS**: Windows with PowerShell
- **Nginx Location**: C:\nginx\
- **Applications**: 5 FastAPI apps with different colored themes

## Solution Architecture

### Path-Based Routing Structure
```
http://172.25.25.140/app1/ → FastAPI App 1 (Port 5001) - Blue Theme
http://172.25.25.140/app2/ → FastAPI App 2 (Port 5002) - Green Theme  
http://172.25.25.140/app3/ → FastAPI App 3 (Port 5003) - Purple Theme
http://172.25.25.140/app4/ → FastAPI App 4 (Port 5004) - Orange Theme
http://172.25.25.140/app5/ → FastAPI App 5 (Port 5005) - Red Theme
```

### Key Components
1. **Single Server Block**: One nginx server block handling all applications
2. **Static File Routing**: Separate location blocks for CSS/JS files
3. **Rewrite Rules**: Path transformation for backend compatibility
4. **Proxy Headers**: Proper header forwarding for WebSocket and HTTP

## Implementation Details

### 1. Nginx Configuration (nginx-ultimate.conf)

**Location**: `C:\nginx\conf\apps\nginx-ultimate.conf`

**Key Features**:
- Single server block on port 80
- Path-based routing with rewrite rules
- Static file handling for CSS/JS
- Security headers
- WebSocket support
- Proper proxy headers

**Main Location Blocks**:
```nginx
# App routing
location /app1/ {
    rewrite ^/app1/(.*)$ /$1 break;
    proxy_pass http://127.0.0.1:5001;
    # ... proxy headers
}

# Static files routing  
location ~ ^/app1/static/(.*)$ {
    proxy_pass http://127.0.0.1:5001/static/$1;
    proxy_set_header Host $host;
}
```

### 2. FastAPI Applications

**Ports**: 5001, 5002, 5003, 5004, 5005
**Static Files**: Mounted at `/static/` endpoint
**Themes**: Each app has unique color theme

### 3. HTML File Updates

**Problem Solved**: Changed absolute paths to relative paths
**Before**: `href="/static/style.css"`
**After**: `href="static/style.css"`

**Files Updated**:
- app1/static/index.html
- app2/static/index.html  
- app3/static/index.html
- app4/static/index.html
- app5/static/index.html

## Files Created/Modified

### New Configuration Files
1. **nginx-ultimate.conf** - Main nginx configuration
2. **proxy-headers.conf** - Shared proxy headers
3. **app-template.conf** - Template for new applications

### Updated Files
1. **nginx.conf** - Main nginx config (includes apps/*.conf)
2. **HTML files** - Static file path corrections in all 5 apps

### Removed/Disabled Files
- nginx-app1.conf through nginx-app5.conf (moved to disabled/)

## Deployment Steps

### 1. Configuration Deployment
```powershell
# Copy updated config
Copy-Item "nginx-ultimate.conf" "C:\nginx\conf\apps\nginx-ultimate.conf" -Force

# Test configuration
cd C:\nginx
.\nginx.exe -t
```

### 2. Nginx Restart (Admin Required)
```powershell
# Run PowerShell as Administrator
cd C:\nginx
.\nginx.exe -s quit
.\nginx.exe
```

### 3. Verification
```powershell
# Check port status
netstat -ano | findstr ":80"

# Should show only port 80 listening (no 8081-8085)
```

## Testing URLs

### Local Access
- http://localhost/app1/
- http://localhost/app2/
- http://localhost/app3/
- http://localhost/app4/
- http://localhost/app5/

### Network Access
- http://172.25.25.140/app1/
- http://172.25.25.140/app2/
- http://172.25.25.140/app3/
- http://172.25.25.140/app4/
- http://172.25.25.140/app5/

### API Endpoints
- http://172.25.25.140/app1/api/app-info
- http://172.25.25.140/app2/api/app-info
- (and so on for all apps)

## Troubleshooting Guide

### Issue 1: 404 Not Found
**Cause**: Nginx not restarted or old configuration active
**Solution**: Restart nginx with admin privileges

### Issue 2: CSS/JS Not Loading
**Cause**: Incorrect static file paths
**Solution**: 
- Update HTML to use relative paths (static/style.css)
- Add static file location blocks in nginx

### Issue 3: Access Denied on Restart
**Cause**: Insufficient privileges
**Solution**: Run PowerShell as Administrator

### Issue 4: Port Conflicts
**Cause**: Multiple server blocks on same port
**Solution**: Use single server block with multiple locations

## Scalability Features

### Adding New Applications
1. **Copy app-template.conf** and modify:
   - Change app number
   - Update port number
   - Update location paths

2. **No nginx.conf changes needed** - uses include apps/*.conf

3. **Automatic inclusion** of new .conf files

### Template Usage
```nginx
# Copy and modify app-template.conf
# Replace placeholders:
# - {APP_NUMBER} → actual app number
# - {PORT} → actual port number
# - {THEME} → theme description
```

## Network Configuration

### Server Details
- **Primary IP**: 172.25.25.140
- **Subnet**: 255.255.255.0
- **Gateway**: 172.25.25.1
- **Domain**: BAGH.MTBC.COM

### Port Usage
- **Port 80**: Main nginx server (all apps)
- **Ports 5001-5005**: FastAPI backend applications
- **Ports 8081-8085**: Disabled (old configuration)

## Security Features

### Headers Applied
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- Proper proxy headers for real IP forwarding

### Access Control
- Server responds to localhost and IP address
- Wildcard server_name for flexibility

## Performance Optimizations

### Nginx Settings
- Keep-alive connections
- Proper timeout configurations
- WebSocket upgrade support
- Efficient proxy buffering

### Static File Serving
- Direct proxy pass to FastAPI static endpoints
- Minimal header overhead for static files

## Maintenance

### Regular Tasks
1. **Monitor nginx logs**: Check for errors
2. **Test all endpoints**: Verify functionality
3. **Update configurations**: Use templates for new apps
4. **Backup configs**: Keep copies of working configurations

### Configuration Files Location
- **Main Config**: C:\nginx\conf\nginx.conf
- **App Configs**: C:\nginx\conf\apps\
- **Backup Copies**: C:\Users\muhammadahmad4\applications\

## Success Metrics

### ✅ Achieved Goals
1. **Port 80 Only**: All traffic consolidated to single port
2. **Path-Based Routing**: Clean URL structure (/app1/, /app2/, etc.)
3. **Static Files Working**: CSS and JS loading properly
4. **Scalable Architecture**: Easy to add new applications
5. **Zero Downtime**: Smooth transition from old setup
6. **Network Access**: Working on both localhost and IP address

### ✅ Technical Validation
- Nginx configuration syntax: VALID
- Port conflicts: RESOLVED
- Static file routing: WORKING
- All 5 applications: ACCESSIBLE
- CSS/JS styling: FUNCTIONAL

## Final Status

**FULLY OPERATIONAL** - All 5 FastAPI applications successfully consolidated to port 80 with complete CSS/JS functionality and scalable architecture for future expansion.

---

**Documentation Created**: September 19, 2025
**Solution Status**: Production Ready
**Tested URLs**: All working with full styling
**Next Steps**: Ready for production use or additional application deployment