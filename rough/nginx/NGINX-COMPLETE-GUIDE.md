# 🚀 **Complete Nginx Guide: Beginner to Advanced**

*From Basic Concepts to Custom Multi-App Configurations*

---

## 📚 **Table of Contents**

1. [What is Nginx?](#1-what-is-nginx)
2. [Nginx Architecture & How It Works](#2-nginx-architecture--how-it-works)
3. [Installation and Basic Setup](#3-installation-and-basic-setup)
4. [Default Nginx Configuration Explained](#4-default-nginx-configuration-explained)
5. [Understanding Nginx Directives](#5-understanding-nginx-directives)
6. [Server Blocks (Virtual Hosts)](#6-server-blocks-virtual-hosts)
7. [Location Blocks and URL Routing](#7-location-blocks-and-url-routing)
8. [Reverse Proxy Configuration](#8-reverse-proxy-configuration)
9. [Load Balancing](#9-load-balancing)
10. [Static File Serving](#10-static-file-serving)
11. [Custom Configurations (Our Project Example)](#11-custom-configurations-our-project-example)
12. [Advanced Features](#12-advanced-features)
13. [Security Best Practices](#13-security-best-practices)
14. [Performance Optimization](#14-performance-optimization)
15. [Troubleshooting and Debugging](#15-troubleshooting-and-debugging)
16. [Real-World Examples](#16-real-world-examples)

---

## 1. **What is Nginx?**

### **Definition:**
Nginx (pronounced "engine-x") is a high-performance web server, reverse proxy server, and load balancer. It's designed to handle thousands of concurrent connections efficiently.

### **Key Features:**
```
✅ Web Server - Serves static content (HTML, CSS, JS, images)
✅ Reverse Proxy - Forwards requests to backend applications
✅ Load Balancer - Distributes traffic across multiple servers
✅ HTTP Cache - Stores frequently requested content
✅ SSL/TLS Termination - Handles encryption/decryption
✅ Compression - Reduces bandwidth usage
✅ Rate Limiting - Controls request frequency
```

### **Why Choose Nginx?**
```
🔥 High Performance - Can handle 10,000+ concurrent connections
⚡ Low Memory Usage - Uses event-driven architecture
🛡️ Stability - Rarely crashes, very reliable
🔧 Flexibility - Highly configurable for any use case
📈 Scalability - Easily handles traffic spikes
🌐 Cross-Platform - Works on Linux, Windows, macOS
```

### **Common Use Cases:**
```
1. Static Website Hosting
2. Reverse Proxy for APIs (like our FastAPI apps)
3. Load Balancing across multiple servers
4. SSL Certificate Management
5. Content Caching
6. Rate Limiting and DDoS Protection
7. Microservices Gateway
```

---

## 2. **Nginx Architecture & How It Works**

### **Event-Driven Architecture:**
```
Traditional Web Server (Apache):
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Request   │    │   Request   │    │   Request   │
│   Thread    │    │   Thread    │    │   Thread    │
│      1      │    │      2      │    │      3      │
└─────────────┘    └─────────────┘    └─────────────┘
   (Heavy)           (Heavy)           (Heavy)

Nginx Event-Driven:
┌───────────────────────────────────────────────────┐
│              Single Master Process               │
├─────────────┬─────────────┬─────────────────────┤
│   Worker    │   Worker    │      Worker         │
│  Process 1  │  Process 2  │     Process N       │
└─────────────┴─────────────┴─────────────────────┘
   (Handles 1000s of connections each)
```

### **Process Structure:**
```
Master Process:
├── Reads configuration
├── Manages worker processes
├── Handles signals (reload, stop, etc.)
└── Binds to ports

Worker Processes:
├── Handle actual requests
├── Process connections asynchronously
├── Number usually equals CPU cores
└── Share listening sockets
```

### **Request Flow:**
```
1. Client sends HTTP request
2. Nginx receives request in worker process
3. Nginx checks configuration rules
4. Nginx either:
   - Serves static file directly, OR
   - Forwards to backend server (reverse proxy)
5. Response sent back to client
```

---

## 3. **Installation and Basic Setup**

### **Windows Installation (What We Used):**
```powershell
# Download from: http://nginx.org/en/download.html
# Extract to: C:\nginx\

# Directory structure after installation:
C:\nginx\
├── conf\           # Configuration files
├── contrib\        # Additional modules
├── docs\          # Documentation
├── html\          # Default web files
├── logs\          # Log files
├── temp\          # Temporary files
└── nginx.exe      # Main executable
```

### **Linux Installation:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
# or
sudo dnf install nginx

# Start service
sudo systemctl start nginx
sudo systemctl enable nginx
```

### **Basic Commands:**
```powershell
# Windows Commands:
cd C:\nginx
.\nginx.exe                    # Start nginx
.\nginx.exe -s stop            # Stop nginx
.\nginx.exe -s reload          # Reload configuration
.\nginx.exe -s quit            # Graceful shutdown
.\nginx.exe -t                 # Test configuration
.\nginx.exe -v                 # Show version

# Linux Commands:
sudo nginx                     # Start nginx
sudo nginx -s stop             # Stop nginx
sudo nginx -s reload           # Reload configuration
sudo systemctl status nginx    # Check status
```

---

## 4. **Default Nginx Configuration Explained**

### **Main Configuration File (nginx.conf):**
```nginx
# Location: C:\nginx\conf\nginx.conf (Windows)
# Location: /etc/nginx/nginx.conf (Linux)

# Main context - global settings
user nobody;                    # User to run worker processes
worker_processes auto;          # Number of worker processes (auto = CPU cores)
error_log logs/error.log;       # Error log location
pid logs/nginx.pid;             # Process ID file

# Events context - connection handling
events {
    worker_connections 1024;    # Max connections per worker
    use epoll;                  # Connection processing method (Linux)
    multi_accept on;            # Accept multiple connections at once
}

# HTTP context - web server settings
http {
    # MIME types
    include mime.types;         # File extension to MIME type mapping
    default_type application/octet-stream;  # Default MIME type

    # Logging format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log logs/access.log main;  # Access log with format

    # Performance settings
    sendfile on;                # Efficient file serving
    tcp_nopush on;             # Send headers in one packet
    tcp_nodelay on;            # Don't buffer small packets
    keepalive_timeout 65;       # Keep connections alive for 65 seconds
    types_hash_max_size 2048;   # Hash table size for MIME types

    # Default server block
    server {
        listen 80;              # Listen on port 80
        server_name localhost;   # Server name
        root html;              # Document root directory
        index index.html index.htm;  # Default files to serve

        # Default location
        location / {
            try_files $uri $uri/ =404;  # Try file, then directory, then 404
        }

        # Error pages
        error_page 404 /404.html;
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root html;
        }
    }
}
```

### **Understanding the Hierarchy:**
```
nginx.conf structure:

Global Context
├── Events Context
└── HTTP Context
    ├── Server Context (Virtual Host)
    │   ├── Location Context
    │   ├── Location Context
    │   └── Location Context
    ├── Server Context (Another Virtual Host)
    └── Upstream Context (Load Balancing)
```

### **Default Behavior:**
```
When you install Nginx:
1. Listens on port 80
2. Serves files from html/ directory
3. Shows default "Welcome to nginx!" page
4. Logs access to logs/access.log
5. Logs errors to logs/error.log
6. Handles requests for "localhost"
```

---

## 5. **Understanding Nginx Directives**

### **Types of Directives:**

**1. Simple Directives:**
```nginx
# Format: directive_name value;
listen 80;
server_name example.com;
root /var/www/html;
index index.html;
```

**2. Block Directives:**
```nginx
# Format: directive_name { ... }
server {
    # directives inside
}

location / {
    # directives inside
}
```

### **Important Directives Explained:**

**Server Block Directives:**
```nginx
server {
    listen 80;                    # Port to listen on
    listen [::]:80;              # IPv6 support
    server_name example.com www.example.com;  # Domain names
    root /var/www/example;        # Document root
    index index.html index.php;   # Default files
    
    # Custom error pages
    error_page 404 /404.html;
    error_page 500 /500.html;
    
    # Access and error logs
    access_log /var/log/nginx/example.access.log;
    error_log /var/log/nginx/example.error.log;
}
```

**Location Block Directives:**
```nginx
# Exact match
location = /exact-path {
    # Only matches /exact-path
}

# Prefix match
location /prefix {
    # Matches /prefix, /prefix/, /prefix/anything
}

# Regex match (case sensitive)
location ~ \.(jpg|jpeg|png|gif)$ {
    # Matches image files
}

# Regex match (case insensitive)
location ~* \.(JPG|JPEG|PNG|GIF)$ {
    # Matches image files (any case)
}

# Priority prefix match
location ^~ /priority {
    # Higher priority than regex
}
```

**Proxy Directives:**
```nginx
location / {
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
```

---

## 6. **Server Blocks (Virtual Hosts)**

### **What are Server Blocks?**
Server blocks allow you to host multiple websites on a single Nginx server. Each server block defines how to handle requests for specific domain names or IP addresses.

### **Basic Server Block:**
```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### **Multiple Server Blocks:**
```nginx
# Website 1
server {
    listen 80;
    server_name site1.com www.site1.com;
    root /var/www/site1;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# Website 2
server {
    listen 80;
    server_name site2.com www.site2.com;
    root /var/www/site2;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# Default server (catch-all)
server {
    listen 80 default_server;
    server_name _;
    return 444;  # Close connection without response
}
```

### **Port-Based Virtual Hosts (Like Our Project):**
```nginx
# App 1 on port 8081
server {
    listen 8081;
    server_name localhost 172.25.25.140;
    
    location / {
        proxy_pass http://localhost:5001;
    }
}

# App 2 on port 8082
server {
    listen 8082;
    server_name localhost 172.25.25.140;
    
    location / {
        proxy_pass http://localhost:5002;
    }
}
```

### **SSL/HTTPS Server Block:**
```nginx
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://backend;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 7. **Location Blocks and URL Routing**

### **Location Matching Priority:**
```nginx
# 1. Exact match (highest priority)
location = / {
    # Only matches http://example.com/
}

# 2. Priority prefix match
location ^~ /images/ {
    # Matches /images/ and stops further regex matching
}

# 3. Regular expression match (case sensitive)
location ~ \.(gif|jpg|jpeg)$ {
    # Matches files ending with gif, jpg, jpeg
}

# 4. Regular expression match (case insensitive)
location ~* \.(gif|jpg|jpeg)$ {
    # Same as above but case insensitive
}

# 5. Prefix match (lowest priority)
location / {
    # Matches everything (fallback)
}
```

### **Practical Examples:**

**Static File Serving:**
```nginx
# Serve images efficiently
location ~* \.(jpg|jpeg|png|gif|ico|svg)$ {
    expires 1y;                    # Cache for 1 year
    add_header Cache-Control "public, immutable";
    try_files $uri =404;
}

# CSS and JavaScript files
location ~* \.(css|js)$ {
    expires 30d;                   # Cache for 30 days
    add_header Cache-Control "public";
    try_files $uri =404;
}

# Font files
location ~* \.(woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Access-Control-Allow-Origin "*";
    try_files $uri =404;
}
```

**API Routing:**
```nginx
# API endpoints
location /api/ {
    proxy_pass http://api_backend/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    
    # CORS headers
    add_header Access-Control-Allow-Origin "*";
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE";
}

# Admin panel
location /admin/ {
    auth_basic "Admin Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://admin_backend/;
}

# Health check endpoint
location = /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}
```

**Security and Access Control:**
```nginx
# Block access to sensitive files
location ~ /\. {
    deny all;                     # Block .htaccess, .git, etc.
}

location ~ /(wp-config|config)\.php$ {
    deny all;                     # Block config files
}

# Rate limiting
location /login {
    limit_req zone=login burst=5 nodelay;
    proxy_pass http://backend;
}

# IP-based restrictions
location /admin {
    allow 192.168.1.0/24;        # Allow local network
    allow 10.0.0.0/8;            # Allow private network
    deny all;                     # Deny everyone else
    proxy_pass http://backend;
}
```

---

## 8. **Reverse Proxy Configuration**

### **What is a Reverse Proxy?**
A reverse proxy sits between clients and backend servers, forwarding client requests to appropriate backend servers and returning responses back to clients.

```
Client → Nginx (Reverse Proxy) → Backend Server(s)
   ↑                               ↓
   └── Response ←── Response ←─────┘
```

### **Basic Reverse Proxy:**
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://127.0.0.1:3000;  # Forward to Node.js app
        
        # Essential headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **Our Project's Reverse Proxy Setup:**
```nginx
# nginx-app1.conf (Our actual configuration)
server {
    listen 8081;                           # External port
    server_name localhost 172.25.25.140;  # Accept from localhost and LAN
    
    location / {
        proxy_pass http://localhost:5001;  # Forward to FastAPI app
        
        # Headers for proper request handling
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Logging for debugging
    access_log C:/nginx/logs/app1_access.log;
    error_log C:/nginx/logs/app1_error.log;
}
```

### **Advanced Proxy Features:**

**Timeouts and Buffers:**
```nginx
location / {
    proxy_pass http://backend;
    
    # Timeout settings
    proxy_connect_timeout 60s;      # Time to connect to backend
    proxy_send_timeout 60s;         # Time to send request to backend
    proxy_read_timeout 60s;         # Time to read response from backend
    
    # Buffer settings
    proxy_buffer_size 4k;           # Buffer for response headers
    proxy_buffers 8 4k;            # Number and size of buffers
    proxy_busy_buffers_size 8k;     # Buffer size for sending to client
    
    # Request/response size limits
    client_max_body_size 100M;      # Max upload size
    proxy_max_temp_file_size 1024M; # Max temp file size
}
```

**Caching:**
```nginx
# Define cache path
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g 
                 inactive=60m use_temp_path=off;

server {
    location / {
        proxy_cache my_cache;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_revalidate on;
        proxy_cache_lock on;
        
        # Cache different responses for different times
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        
        # Add cache status header
        add_header X-Cache-Status $upstream_cache_status;
        
        proxy_pass http://backend;
    }
}
```

**WebSocket Support:**
```nginx
location /websocket {
    proxy_pass http://websocket_backend;
    
    # WebSocket specific headers
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    
    # Prevent timeouts
    proxy_read_timeout 86400;
}
```

---

## 9. **Load Balancing**

### **What is Load Balancing?**
Load balancing distributes incoming requests across multiple backend servers to ensure no single server becomes overwhelmed.

### **Upstream Blocks:**
```nginx
# Define backend servers
upstream backend_pool {
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
    server 127.0.0.1:3003;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend_pool;
    }
}
```

### **Load Balancing Methods:**

**1. Round Robin (Default):**
```nginx
upstream backend {
    server server1.example.com;
    server server2.example.com;
    server server3.example.com;
}
# Requests distributed equally: 1→2→3→1→2→3...
```

**2. Least Connections:**
```nginx
upstream backend {
    least_conn;                    # Route to server with fewest active connections
    server server1.example.com;
    server server2.example.com;
    server server3.example.com;
}
```

**3. IP Hash:**
```nginx
upstream backend {
    ip_hash;                       # Same client always goes to same server
    server server1.example.com;
    server server2.example.com;
    server server3.example.com;
}
```

**4. Weighted Load Balancing:**
```nginx
upstream backend {
    server server1.example.com weight=3;  # Gets 3x more requests
    server server2.example.com weight=2;  # Gets 2x more requests
    server server3.example.com weight=1;  # Gets 1x requests (default)
}
```

### **Health Checks and Failover:**
```nginx
upstream backend {
    server server1.example.com max_fails=3 fail_timeout=30s;
    server server2.example.com max_fails=3 fail_timeout=30s;
    server server3.example.com backup;  # Only used if others fail
}
```

### **Advanced Example - Multiple App Instances:**
```nginx
# Load balance across multiple FastAPI instances
upstream fastapi_cluster {
    least_conn;
    server 127.0.0.1:5001 weight=2;
    server 127.0.0.1:5002 weight=2;
    server 127.0.0.1:5003 weight=1;
    server 127.0.0.1:5004 backup;
}

server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://fastapi_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Health check
        proxy_connect_timeout 5s;
        proxy_send_timeout 5s;
        proxy_read_timeout 5s;
    }
}
```

---

## 10. **Static File Serving**

### **Basic Static File Serving:**
```nginx
server {
    listen 80;
    server_name static.example.com;
    root /var/www/static;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### **Optimized Static File Serving:**
```nginx
server {
    listen 80;
    server_name cdn.example.com;
    root /var/www/cdn;
    
    # Enable efficient file sending
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript 
               application/javascript application/xml+rss application/json;
    
    # Cache headers for different file types
    location ~* \.(jpg|jpeg|png|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary Accept-Encoding;
    }
    
    location ~* \.(css|js)$ {
        expires 30d;
        add_header Cache-Control "public";
        add_header Vary Accept-Encoding;
    }
    
    location ~* \.(woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Access-Control-Allow-Origin "*";
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### **CDN-like Setup:**
```nginx
# Multiple static servers with failover
upstream static_servers {
    server static1.example.com;
    server static2.example.com backup;
}

server {
    listen 80;
    server_name cdn.example.com;
    
    location / {
        proxy_pass http://static_servers;
        proxy_cache_valid 200 1d;
        proxy_cache_use_stale error timeout updating;
        
        # Add cache headers
        expires 1d;
        add_header Cache-Control "public";
    }
}
```

---

## 11. **Custom Configurations (Our Project Example)**

Let's break down exactly what we built in our project and why each part works:

### **Our Project Architecture:**
```
Client Request → Nginx (Port 808X) → FastAPI App (Port 500X)
                    ↓
               Static Files Served
```

### **Why We Used This Approach:**

**Problem:** We had 5 separate FastAPI applications that needed to be accessible from the LAN.

**Solution:** 
1. Each FastAPI app runs on its own port (5001-5005)
2. Nginx acts as reverse proxy on different ports (8081-8085)
3. This allows easy access and scalability

### **Our Modular Configuration Setup:**

**Main nginx.conf modification:**
```nginx
http {
    # ... existing configuration ...
    
    # This line includes all our app configurations
    include apps/*.conf;
    
    # ... rest of configuration ...
}
```

**Why this is powerful:**
- ✅ **Modularity:** Each app has its own config file
- ✅ **Scalability:** Add new apps without touching main config
- ✅ **Maintainability:** Easy to modify individual app settings
- ✅ **Organization:** Clean separation of concerns

### **Individual App Configuration (nginx-app1.conf):**
```nginx
server {
    listen 8081;                           # External access port
    server_name localhost 172.25.25.140;  # Allow local and LAN access
    
    location / {
        proxy_pass http://localhost:5001;  # Forward to FastAPI backend
        
        # Essential proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Separate logs for each app (great for debugging)
    access_log C:/nginx/logs/app1_access.log;
    error_log C:/nginx/logs/app1_error.log;
}
```

### **What Each Part Does:**

**`listen 8081;`**
```
- Nginx listens on port 8081 for this app
- Clients access: http://172.25.25.140:8081
- No port conflicts between apps
```

**`server_name localhost 172.25.25.140;`**
```
- Accepts requests from localhost (same machine)
- Accepts requests from LAN IP (other devices on network)
- Could add more IPs or domain names here
```

**`proxy_pass http://localhost:5001;`**
```
- Forwards all requests to FastAPI app on port 5001
- FastAPI doesn't need to handle external networking
- Nginx handles all the networking complexity
```

**`proxy_set_header` directives:**
```
Host $host;                    # Preserves original Host header
X-Real-IP $remote_addr;        # Client's real IP address
X-Forwarded-For $proxy_add_x_forwarded_for;  # Full forwarding chain
X-Forwarded-Proto $scheme;     # Original protocol (http/https)
```

### **Directory Structure We Created:**
```
C:\nginx\conf\
├── nginx.conf                 # Main configuration
└── apps\                      # Our custom directory
    ├── nginx-app1.conf        # App 1 configuration
    ├── nginx-app2.conf        # App 2 configuration
    ├── nginx-app3.conf        # App 3 configuration
    ├── nginx-app4.conf        # App 4 configuration
    └── nginx-app5.conf        # App 5 configuration
```

### **Benefits of Our Approach:**

**1. Easy Scaling:**
```powershell
# Add app6 - just copy and modify
Copy-Item "nginx-app1.conf" "nginx-app6.conf"
# Change port 8081 → 8086 and 5001 → 5006
# Restart nginx - done!
```

**2. Independent Management:**
```nginx
# Each app can have different settings
server {
    listen 8081;
    # App 1 - no special restrictions
}

server {
    listen 8082;
    # App 2 - with rate limiting
    limit_req zone=app2 burst=10;
}

server {
    listen 8083;
    # App 3 - with authentication
    auth_basic "Admin Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

**3. Easy Debugging:**
```
Each app has its own logs:
- C:/nginx/logs/app1_access.log
- C:/nginx/logs/app1_error.log
- C:/nginx/logs/app2_access.log
- etc.
```

### **How Static Files Work in Our Setup:**

**FastAPI Configuration:**
```python
# In our main.py files
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

**HTML File References:**
```html
<!-- This works because nginx forwards /static/ requests to FastAPI -->
<link rel="stylesheet" href="/static/style.css">
<script src="/static/script.js"></script>
```

**Request Flow for Static Files:**
```
1. Browser requests: http://172.25.25.140:8081/static/style.css
2. Nginx receives request on port 8081
3. Nginx forwards to FastAPI on port 5001: /static/style.css
4. FastAPI serves file from static/ directory
5. Response flows back: FastAPI → Nginx → Browser
```

---

## 12. **Advanced Features**

### **SSL/TLS Configuration:**
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL certificate files
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/private.key;
    
    # SSL security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location / {
        proxy_pass http://backend;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### **Rate Limiting:**
```nginx
# Define rate limiting zones
http {
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
    limit_req_zone $binary_remote_addr zone=api:10m rate=5r/s;
}

server {
    # General rate limiting
    location / {
        limit_req zone=general burst=20 nodelay;
        proxy_pass http://backend;
    }
    
    # Strict rate limiting for login
    location /login {
        limit_req zone=login burst=5;
        proxy_pass http://backend;
    }
    
    # API rate limiting
    location /api/ {
        limit_req zone=api burst=10 nodelay;
        proxy_pass http://api_backend;
    }
}
```

### **Access Control:**
```nginx
# Geographic blocking (requires GeoIP module)
http {
    geoip_country /usr/share/GeoIP/GeoIP.dat;
    
    map $geoip_country_code $allowed_country {
        default yes;
        CN no;  # Block China
        RU no;  # Block Russia
    }
}

server {
    location / {
        if ($allowed_country = no) {
            return 403;
        }
        proxy_pass http://backend;
    }
}

# IP-based access control
server {
    # Allow specific IPs
    location /admin {
        allow 192.168.1.0/24;    # Local network
        allow 10.0.0.0/8;        # Private network
        deny all;                # Deny everyone else
        proxy_pass http://backend;
    }
    
    # Block specific IPs
    location / {
        deny 192.168.1.100;      # Block specific IP
        deny 172.16.0.0/12;      # Block IP range
        allow all;               # Allow everyone else
        proxy_pass http://backend;
    }
}
```

### **Custom Error Pages:**
```nginx
server {
    # Custom error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    error_page 403 /403.html;
    
    # Serve error pages from custom directory
    location = /404.html {
        root /var/www/errors;
        internal;  # Only accessible via error_page directive
    }
    
    location = /50x.html {
        root /var/www/errors;
        internal;
    }
    
    # JSON error responses for API
    location /api/ {
        proxy_pass http://api_backend;
        
        # Intercept errors and return JSON
        proxy_intercept_errors on;
        error_page 404 = @api_404;
        error_page 500 502 503 504 = @api_error;
    }
    
    location @api_404 {
        add_header Content-Type application/json always;
        return 404 '{"error": "API endpoint not found", "status": 404}';
    }
    
    location @api_error {
        add_header Content-Type application/json always;
        return 500 '{"error": "Internal server error", "status": 500}';
    }
}
```

### **Monitoring and Health Checks:**
```nginx
# Health check endpoint
server {
    listen 8080;  # Monitoring port
    server_name _;
    
    # Nginx status
    location = /nginx_status {
        stub_status;
        allow 127.0.0.1;
        allow 192.168.1.0/24;
        deny all;
    }
    
    # Custom health check
    location = /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Application health checks
    location = /health/app1 {
        proxy_pass http://localhost:5001/health;
        proxy_connect_timeout 5s;
        proxy_read_timeout 5s;
    }
}
```

---

## 13. **Security Best Practices**

### **Essential Security Headers:**
```nginx
server {
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    
    # Hide nginx version
    server_tokens off;
    
    # Prevent access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

### **DDoS Protection:**
```nginx
http {
    # Connection limiting
    limit_conn_zone $binary_remote_addr zone=conn_limit_per_ip:10m;
    limit_req_zone $binary_remote_addr zone=req_limit_per_ip:10m rate=5r/s;
    
    # Request size limits
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    
    # Timeout settings
    client_body_timeout 12;
    client_header_timeout 12;
    keepalive_timeout 15;
    send_timeout 10;
}

server {
    # Apply limits
    limit_conn conn_limit_per_ip 10;
    limit_req zone=req_limit_per_ip burst=10 nodelay;
    
    # Block common attack patterns
    location ~* /(wp-admin|phpMyAdmin|admin|administrator) {
        deny all;
    }
    
    # Block suspicious user agents
    if ($http_user_agent ~* (nmap|nikto|wikto|sf|sqlmap|bsqlbf|w3af|acunetix|havij|appscan)) {
        return 444;
    }
}
```

### **Authentication:**
```nginx
# Basic HTTP authentication
server {
    location /admin {
        auth_basic "Admin Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://backend;
    }
    
    # Create password file:
    # htpasswd -c /etc/nginx/.htpasswd username
}

# JWT authentication (with auth module)
server {
    location /api/ {
        access_by_lua_block {
            local jwt = require "resty.jwt"
            local jwt_token = ngx.var.http_authorization
            
            if not jwt_token then
                ngx.status = 401
                ngx.say("Missing token")
                ngx.exit(401)
            end
            
            # Verify JWT token here
        }
        
        proxy_pass http://api_backend;
    }
}
```

---

## 14. **Performance Optimization**

### **Caching Configuration:**
```nginx
http {
    # Proxy cache setup
    proxy_cache_path /var/cache/nginx/proxy 
                     levels=1:2 
                     keys_zone=proxy_cache:10m 
                     max_size=1g 
                     inactive=60m 
                     use_temp_path=off;
    
    # FastCGI cache (for PHP)
    fastcgi_cache_path /var/cache/nginx/fastcgi 
                       levels=1:2 
                       keys_zone=fastcgi_cache:10m 
                       max_size=1g 
                       inactive=60m;
}

server {
    # Proxy caching
    location / {
        proxy_cache proxy_cache;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_revalidate on;
        proxy_cache_lock on;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        
        # Cache bypass for authenticated users
        proxy_cache_bypass $http_authorization;
        proxy_no_cache $http_authorization;
        
        # Add cache status header
        add_header X-Cache-Status $upstream_cache_status;
        
        proxy_pass http://backend;
    }
}
```

### **Compression:**
```nginx
http {
    # Enable gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Enable brotli compression (if module available)
    brotli on;
    brotli_comp_level 6;
    brotli_types
        text/plain
        text/css
        application/json
        application/javascript
        text/xml application/xml
        application/xml+rss
        text/javascript;
}
```

### **Worker Process Optimization:**
```nginx
# At the top of nginx.conf
worker_processes auto;              # One worker per CPU core
worker_rlimit_nofile 65535;        # File descriptor limit
worker_connections 1024;           # Connections per worker

events {
    worker_connections 1024;
    use epoll;                      # Linux: efficient connection method
    multi_accept on;               # Accept multiple connections at once
    accept_mutex off;              # Disable accept mutex for performance
}

http {
    # Connection keep-alive
    keepalive_timeout 65;
    keepalive_requests 100;
    
    # File serving optimization
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    # Buffer sizes
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    output_buffers 1 32k;
    postpone_output 1460;
}
```

### **Static File Optimization:**
```nginx
# Efficient static file serving
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Vary Accept-Encoding;
    
    # Disable access logging for static files
    access_log off;
    
    # Enable sendfile for efficient file serving
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    # Compression for text-based files
    gzip_static on;  # Serve pre-compressed files if available
}

# Pre-compressed static files
location ~* \.(css|js)$ {
    # Try compressed version first
    try_files $uri.gz $uri =404;
    add_header Content-Encoding gzip;
    add_header Vary Accept-Encoding;
}
```

---

## 15. **Troubleshooting and Debugging**

### **Common Issues and Solutions:**

**1. Configuration Syntax Errors:**
```powershell
# Test configuration before restarting
cd C:\nginx
.\nginx.exe -t

# Common errors:
# - Missing semicolon at end of directive
# - Mismatched braces { }
# - Invalid directive names
# - Wrong file paths
```

**2. Port Conflicts:**
```powershell
# Check what's using a port
netstat -ano | findstr "8081"

# Kill process using port
taskkill /PID <process_id> /F
```

**3. Permission Issues:**
```powershell
# Run as Administrator
# Check file permissions on nginx directory
# Verify user account has access to files
```

**4. Backend Connection Issues:**
```nginx
# Add timeout settings to prevent hanging
location / {
    proxy_pass http://backend;
    proxy_connect_timeout 5s;
    proxy_send_timeout 5s;
    proxy_read_timeout 5s;
    
    # Better error handling
    proxy_next_upstream error timeout http_500 http_502 http_503;
}
```

### **Debugging Tools:**

**Enable Debug Logging:**
```nginx
error_log logs/error.log debug;

# Or for specific locations
location /debug {
    error_log logs/debug.log debug;
    proxy_pass http://backend;
}
```

**Custom Log Formats:**
```nginx
http {
    log_format detailed '$remote_addr - $remote_user [$time_local] '
                       '"$request" $status $body_bytes_sent '
                       '"$http_referer" "$http_user_agent" '
                       'rt=$request_time uct="$upstream_connect_time" '
                       'uht="$upstream_header_time" urt="$upstream_response_time"';
    
    access_log logs/access.log detailed;
}
```

**Health Check Script:**
```powershell
# nginx-health-check.ps1
function Test-NginxHealth {
    $ports = @(8081, 8082, 8083, 8084, 8085)
    
    foreach ($port in $ports) {
        try {
            $response = Invoke-WebRequest "http://localhost:$port" -UseBasicParsing -TimeoutSec 5
            Write-Host "Port $port: ✅ Status $($response.StatusCode)" -ForegroundColor Green
        }
        catch {
            Write-Host "Port $port: ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Test-NginxHealth
```

**Log Analysis:**
```powershell
# Monitor logs in real-time
Get-Content "C:\nginx\logs\error.log" -Wait -Tail 10

# Search for specific errors
Select-String "error" "C:\nginx\logs\*.log" | Select-Object -Last 10

# Analyze access patterns
Select-String "404" "C:\nginx\logs\access.log" | Group-Object Line | Sort-Object Count -Descending
```

---

## 16. **Real-World Examples**

### **Example 1: E-commerce Website**
```nginx
# Main website
server {
    listen 443 ssl http2;
    server_name shop.example.com;
    
    ssl_certificate /path/to/ssl.crt;
    ssl_certificate_key /path/to/ssl.key;
    
    # Static assets with long caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        root /var/www/static;
    }
    
    # API endpoints
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Admin panel with authentication
    location /admin/ {
        auth_basic "Admin Panel";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://admin_backend;
    }
    
    # Main application
    location / {
        proxy_pass http://web_backend;
        proxy_cache web_cache;
        proxy_cache_valid 200 10m;
    }
}

# Load balancing for high traffic
upstream web_backend {
    least_conn;
    server web1.internal:3000 weight=2;
    server web2.internal:3000 weight=2;
    server web3.internal:3000 weight=1;
}

upstream api_backend {
    server api1.internal:4000;
    server api2.internal:4000;
    server api3.internal:4000;
}
```

### **Example 2: Microservices API Gateway**
```nginx
# API Gateway
server {
    listen 80;
    server_name api.example.com;
    
    # User service
    location /users/ {
        rewrite ^/users/(.*)$ /$1 break;
        proxy_pass http://user_service;
        include proxy_params;
    }
    
    # Product service
    location /products/ {
        rewrite ^/products/(.*)$ /$1 break;
        proxy_pass http://product_service;
        include proxy_params;
    }
    
    # Order service with authentication
    location /orders/ {
        auth_request /auth;
        rewrite ^/orders/(.*)$ /$1 break;
        proxy_pass http://order_service;
        include proxy_params;
    }
    
    # Authentication endpoint
    location = /auth {
        internal;
        proxy_pass http://auth_service/validate;
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";
        proxy_set_header X-Original-URI $request_uri;
    }
    
    # Rate limiting for public API
    location /public/ {
        limit_req zone=public_api burst=100 nodelay;
        proxy_pass http://public_service;
        include proxy_params;
    }
}

# Service definitions
upstream user_service {
    server user1.internal:5001;
    server user2.internal:5001;
}

upstream product_service {
    server product1.internal:5002;
    server product2.internal:5002;
}

upstream order_service {
    server order1.internal:5003;
    server order2.internal:5003;
}
```

### **Example 3: Development Environment (Like Our Project)**
```nginx
# Development setup with multiple apps
http {
    include mime.types;
    default_type application/octet-stream;
    
    # Development-friendly settings
    sendfile off;  # Disable for easier file updates
    
    # Include all app configurations
    include apps/*.conf;
    
    # Development tools
    server {
        listen 8080;
        server_name dev-tools.local;
        
        # Nginx status
        location = /status {
            stub_status;
            allow 127.0.0.1;
            allow 192.168.0.0/16;
            deny all;
        }
        
        # Application health checks
        location /health/ {
            proxy_pass http://health_check_service;
        }
    }
}

# Individual app configs (in apps/ directory)
# nginx-frontend.conf
server {
    listen 3000;
    server_name frontend.local;
    
    # React development server
    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# nginx-api.conf
server {
    listen 8000;
    server_name api.local;
    
    # FastAPI development server
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # CORS for development
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
        add_header Access-Control-Allow-Headers "Content-Type, Authorization";
    }
}
```

---

## 🎯 **Summary and Key Takeaways**

### **What We Learned:**

1. **Nginx is extremely flexible** - Can handle simple static sites to complex microservices
2. **Configuration is hierarchical** - Global → HTTP → Server → Location
3. **Reverse proxy is powerful** - Allows backend apps to focus on business logic
4. **Modular configuration rocks** - Our `include apps/*.conf` approach scales beautifully
5. **Security is built-in** - Rate limiting, access control, headers all available
6. **Performance is exceptional** - Caching, compression, load balancing out of the box

### **Our Project's Success:**
- ✅ 5 FastAPI apps running independently
- ✅ LAN access from any device
- ✅ Easy to add more apps
- ✅ Individual logging and monitoring
- ✅ Clean, maintainable configuration

### **Next Steps for Learning:**
1. **Practice SSL/HTTPS setup** - Essential for production
2. **Experiment with load balancing** - Run multiple instances of same app
3. **Try caching** - Dramatically improves performance
4. **Learn Lua scripting** - Advanced request manipulation
5. **Monitor with tools** - Grafana, Prometheus, ELK stack integration

### **Production Readiness Checklist:**
- [ ] SSL certificates configured
- [ ] Security headers enabled
- [ ] Rate limiting implemented
- [ ] Monitoring and logging setup
- [ ] Backup and recovery plan
- [ ] Performance testing completed
- [ ] Security audit performed

---

**🚀 Congratulations! You now understand Nginx from basics to advanced configurations. Our project demonstrates real-world application of these concepts, and you're ready to build even more complex systems!**

*Keep this guide handy as a reference - Nginx has many more features to explore as your needs grow.*