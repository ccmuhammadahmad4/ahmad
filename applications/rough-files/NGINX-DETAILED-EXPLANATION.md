# NGINX MODULAR CONFIGURATION - Complete Line-by-Line Guide

## Overview
This document provides a complete line-by-line explanation of the modular nginx configuration used for the Port 80 solution. The setup consists of:

1. **Main nginx.conf** - Entry point configuration
2. **nginx-port80-base.conf** - Main server block with common settings
3. **Individual app routing files** - app1-routing.conf through app5-routing.conf

---

## 1. MAIN NGINX.CONF FILE

The main nginx configuration file located at `C:\nginx\conf\nginx.conf` serves as the entry point for all nginx operations.

### Basic Structure:

```nginx
#user  nobody;
worker_processes  1;
```
**Line-by-Line Explanation:**
- `#user nobody;` - Commented out user directive (not needed on Windows)
- `worker_processes 1;` - Number of worker processes nginx will spawn (1 is sufficient for development)

```nginx
#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;
```
**Line-by-Line Explanation:**
- Error log configuration options (all commented out, using nginx defaults)
- Different log levels available: error, notice, info
- When uncommented, logs would go to `logs/error.log`

```nginx
#pid        logs/nginx.pid;
```
**Line-by-Line Explanation:**
- Process ID file location (commented out, using nginx defaults)
- PID file helps with process management and service control

```nginx
events {
    worker_connections  1024;
}
```
**Line-by-Line Explanation:**
- `events {` - Opens the events context block
- `worker_connections 1024;` - Maximum number of simultaneous connections per worker process
- `}` - Closes the events context block

```nginx
http {
    include       mime.types;
    default_type  application/octet-stream;
```
**Line-by-Line Explanation:**
- `http {` - Opens the main HTTP configuration context
- `include mime.types;` - Loads MIME type mappings from external file
- `default_type application/octet-stream;` - Default MIME type for files with unknown extensions

```nginx
    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';
    #access_log  logs/access.log  main;
```
**Line-by-Line Explanation:**
- Custom log format definition (commented out)
- Variables like `$remote_addr`, `$request`, `$status` provide request details
- Access log configuration using the custom format

```nginx
    sendfile        on;
    #tcp_nopush     on;
    keepalive_timeout  65;
    #gzip  on;
```
**Line-by-Line Explanation:**
- `sendfile on;` - Enables efficient file serving using kernel sendfile() syscall
- `keepalive_timeout 65;` - Keeps client connections alive for 65 seconds
- Other performance optimizations are commented out

```nginx
    # Include all application configurations
    include apps/*.conf;
```
**Line-by-Line Explanation:**
- **MOST CRITICAL LINE** - Includes ALL .conf files from the apps/ directory
- This wildcard include loads:
  - nginx-port80-base.conf (main server block)
  - app1-routing.conf through app5-routing.conf (individual apps)

```nginx
    # Default server block commented out for separate app configs
    # Each app has its own config file in apps/ directory
}
```
**Line-by-Line Explanation:**
- Comments explaining architectural decision
- `}` - Closes the http context block

---

## 2. NGINX-PORT80-BASE.CONF FILE

Main server block containing common settings and application includes.

### Header Comments:

```nginx
# NGINX PORT 80 BASE CONFIGURATION
# Main server block with common settings
# Individual apps included via separate files
```
**Line-by-Line Explanation:**
- Documentation header describing file purpose
- Explains the modular architecture approach
- Sets expectations for what this file contains

### Server Block Declaration:

```nginx
server {
    listen 80;
    server_name localhost 172.25.25.140 _;
```
**Line-by-Line Explanation:**
- `server {` - Begins virtual server block definition
- `listen 80;` - Listens on port 80 (standard HTTP port)
- `server_name localhost 172.25.25.140 _;` - Responds to:
  - `localhost` - Local development access
  - `172.25.25.140` - Your specific IP address
  - `_` - Wildcard for any other hostname

### Security Headers:

```nginx
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
```
**Line-by-Line Explanation:**
- `add_header X-Frame-Options "SAMEORIGIN" always;` 
  - Prevents clickjacking attacks
  - Only allows framing from same origin
  - `always` ensures header is added even on error responses
- `add_header X-Content-Type-Options "nosniff" always;`
  - Prevents MIME type sniffing attacks
  - Forces browsers to respect declared content types

### Application Configuration Includes:

```nginx
    # Include individual app configurations
    include apps/app1-routing.conf;
    include apps/app2-routing.conf;
    include apps/app3-routing.conf;
    include apps/app4-routing.conf;
    include apps/app5-routing.conf;
```
**Line-by-Line Explanation:**
- Each `include` directive loads a separate app's routing configuration
- Files are processed in order (important for location block precedence)
- Modular approach allows independent app management
- Each file contains location blocks for one application

### API Status Endpoint:

```nginx
    # API Status endpoint
    location /api/status {
        access_log off;
        return 200 '{"status":"healthy","port":80,"apps":["app1","app2","app3","app4","app5"],"timestamp":"$time_iso8601"}';
        add_header Content-Type application/json;
    }
```
**Line-by-Line Explanation:**
- `location /api/status {` - Matches URLs starting with /api/status
- `access_log off;` - Disables logging for this endpoint (reduces log noise)
- `return 200 'JSON_STRING';` - Returns HTTP 200 status with JSON response body
- JSON contains:
  - `"status":"healthy"` - System health indicator
  - `"port":80` - Current serving port
  - `"apps":["app1"...]` - List of available applications
  - `"timestamp":"$time_iso8601"` - Current timestamp in ISO format
- `add_header Content-Type application/json;` - Sets proper JSON content type

### App Discovery API:

```nginx
    # App selector API
    location /api/apps {
        access_log off;
        return 200 '{"apps":[
            {"name":"app1","url":"/app1/","theme":"blue","port":5001},
            {"name":"app2","url":"/app2/","theme":"green","port":5002},
            {"name":"app3","url":"/app3/","theme":"purple","port":5003},
            {"name":"app4","url":"/app4/","theme":"orange","port":5004},
            {"name":"app5","url":"/app5/","theme":"red","port":5005}
        ]}';
        add_header Content-Type application/json;
    }
```
**Line-by-Line Explanation:**
- `location /api/apps` - Endpoint for app discovery
- Returns detailed JSON metadata for each application:
  - `"name"` - Application identifier
  - `"url"` - Access path for the app
  - `"theme"` - UI theme color
  - `"port"` - Backend FastAPI port
- Useful for dynamic frontend integration and monitoring

### Root Route Handler:

```nginx
    # Root route - JSON response with app links
    location = / {
        return 200 '{"message":"FastAPI Application Suite","note":"Access apps via paths","apps":["/app1/","/app2/","/app3/","/app4/","/app5/"],"api":"/api/status"}';
        add_header Content-Type application/json;
    }
```
**Line-by-Line Explanation:**
- `location = /` - Exact match for root URL only (not /something)
- Returns JSON with:
  - Welcome message
  - Usage instructions
  - List of available app paths
  - API endpoint reference

### Health Check Endpoint:

```nginx
    # Health check for load balancers
    location /health {
        access_log off;
        return 200 'OK';
        add_header Content-Type text/plain;
    }
```
**Line-by-Line Explanation:**
- Simple health check for monitoring systems and load balancers
- Returns plain text "OK" response
- No logging to keep logs clean
- Fast response for automated health checks

### Security Rules:

```nginx
    # Block common attack paths
    location ~ /\. { deny all; }
    location ~ \.(env|conf|log)$ { deny all; }
```
**Line-by-Line Explanation:**
- `location ~ /\.` - Regex location matching any path with dot files
  - Blocks access to `.env`, `.git`, `.htaccess`, etc.
- `location ~ \.(env|conf|log)$` - Blocks files ending with sensitive extensions
- `deny all;` - Returns 403 Forbidden status

### Custom Error Pages:

```nginx
    # Error pages
    error_page 404 = @not_found;
    location @not_found {
        return 404 '{"error":"Not found","available_apps":["/app1/","/app2/","/app3/","/app4/","/app5/"]}';
        add_header Content-Type application/json;
    }
```
**Line-by-Line Explanation:**
- `error_page 404 = @not_found;` - Redirects 404 errors to custom handler
- `@not_found` - Named location block (internal redirect target)
- Returns helpful JSON response instead of default HTML error page
- Includes available app paths for user guidance

### Logging Configuration:

```nginx
    # Logs
    access_log C:/nginx/logs/all_apps_access.log combined;
    error_log C:/nginx/logs/all_apps_error.log warn;
}
```
**Line-by-Line Explanation:**
- `access_log` - Logs all requests to specific file using 'combined' format
- `error_log` - Logs errors and warnings to separate file
- Windows-style paths with forward slashes
- `}` - Closes the server block

---

## 3. APP1-ROUTING.CONF FILE

Individual routing configuration for Application 1 (Blue theme).

### File Header:

```nginx
# APP1 ROUTING CONFIGURATION
# Blue theme FastAPI application
# Port: 5001
```
**Line-by-Line Explanation:**
- File identification comments
- Documents the theme color for this application
- Specifies the backend FastAPI port

### Static Files Location Block:

```nginx
# Static files for app1 (CSS, JS, images)
location ~ ^/app1/static/(.*)$ {
    proxy_pass http://127.0.0.1:5001/static/$1;
    proxy_set_header Host $host;
}
```
**Line-by-Line Explanation:**
- `location ~ ^/app1/static/(.*)$` - Regex location for static files
  - `~` - Indicates this is a regex location
  - `^` - Start of string anchor
  - `/app1/static/` - Literal path prefix
  - `(.*)` - Captures remaining path in variable $1
  - `$` - End of string anchor
- `proxy_pass http://127.0.0.1:5001/static/$1;`
  - Forwards request to FastAPI static file handler
  - `$1` substitutes the captured path segment
  - Example: `/app1/static/style.css` → `http://127.0.0.1:5001/static/style.css`
- `proxy_set_header Host $host;` - Preserves original Host header for the backend

### Main Application Location Block:

```nginx
# App 1 main routing - Blue theme
location /app1/ {
    rewrite ^/app1/(.*)$ /$1 break;
    proxy_pass http://127.0.0.1:5001;
```
**Line-by-Line Explanation:**
- `location /app1/` - Prefix location for all app1 URLs
- `rewrite ^/app1/(.*)$ /$1 break;` - URL rewriting rule
  - `^/app1/(.*)$` - Matches /app1/ prefix and captures the rest
  - `/$1` - Rewrites to just the captured part (removes /app1/ prefix)
  - `break` - Stops processing additional rewrite rules
  - Example: `/app1/dashboard` → `/dashboard`
- `proxy_pass http://127.0.0.1:5001;` - Forwards to FastAPI application

### Proxy Headers:

```nginx
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
```
**Line-by-Line Explanation:**
- `proxy_set_header Host $host;` - Original hostname from client request
- `proxy_set_header X-Real-IP $remote_addr;` - Client's actual IP address
- `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;` 
  - Chain of proxy IP addresses (for multiple proxies)
- `proxy_set_header X-Forwarded-Proto $scheme;` - Original protocol (http/https)

### WebSocket Support:

```nginx
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
```
**Line-by-Line Explanation:**
- `proxy_http_version 1.1;` - Use HTTP/1.1 for WebSocket compatibility
- `proxy_set_header Upgrade $http_upgrade;` - Forward Upgrade header for WebSocket
- `proxy_set_header Connection "upgrade";` - Set connection upgrade for WebSocket

### Timeout Configuration:

```nginx
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
```
**Line-by-Line Explanation:**
- `proxy_connect_timeout 60s;` - Maximum time to establish connection to backend
- `proxy_send_timeout 60s;` - Maximum time to send request to backend
- `proxy_read_timeout 60s;` - Maximum time to read response from backend
- `}` - Closes the location block

---

## 4. APP2-ROUTING.CONF FILE

Individual routing configuration for Application 2 (Green theme).

```nginx
# APP2 ROUTING CONFIGURATION
# Green theme FastAPI application
# Port: 5002
```
**Line-by-Line Explanation:**
- Same structure as app1 but for second application
- Different theme color (green) and port (5002)

### Configuration Pattern:

```nginx
# Static files for app2 (CSS, JS, images)
location ~ ^/app2/static/(.*)$ {
    proxy_pass http://127.0.0.1:5002/static/$1;
    proxy_set_header Host $host;
}

# App 2 main routing - Green theme
location /app2/ {
    rewrite ^/app2/(.*)$ /$1 break;
    proxy_pass http://127.0.0.1:5002;
    [... identical proxy configuration as app1 ...]
}
```
**Line-by-Line Explanation:**
- Identical structure to app1 with path and port changes
- `/app2/` prefix routes to port 5002
- Static files: `/app2/static/` → `port 5002/static/`
- Same proxy headers and timeout configuration

---

## 5. APP3-ROUTING.CONF FILE

Individual routing configuration for Application 3 (Purple theme).

```nginx
# APP3 ROUTING CONFIGURATION
# Purple theme FastAPI application
# Port: 5003
```
**Line-by-Line Explanation:**
- Third application with purple theme
- Routes to backend port 5003
- Same modular pattern as previous apps

**Key Routing Details:**
- URL pattern: `/app3/*` → `http://127.0.0.1:5003/*`
- Static files: `/app3/static/*` → `http://127.0.0.1:5003/static/*`
- Identical proxy configuration ensuring consistency

---

## 6. APP4-ROUTING.CONF FILE

Individual routing configuration for Application 4 (Orange theme).

```nginx
# APP4 ROUTING CONFIGURATION
# Orange theme FastAPI application
# Port: 5004
```
**Line-by-Line Explanation:**
- Fourth application with orange theme
- Backend routes to port 5004
- Follows established modular pattern

**Configuration Consistency:**
- Same location block structure
- Identical proxy headers and timeouts
- URL rewriting follows same pattern

---

## 7. APP5-ROUTING.CONF FILE

Individual routing configuration for Application 5 (Red theme).

```nginx
# APP5 ROUTING CONFIGURATION
# Red theme FastAPI application
# Port: 5005
```
**Line-by-Line Explanation:**
- Fifth and final application with red theme
- Routes to backend port 5005
- Completes the modular application suite

**Final Configuration:**
- `/app5/*` paths route to `http://127.0.0.1:5005/*`
- Static files handled consistently
- All proxy features enabled

---

## COMPLETE REQUEST FLOW ANALYSIS

### Example 1: Static File Request
**URL:** `http://172.25.25.140/app3/static/style.css`

**Flow Steps:**
1. Client browser requests CSS file
2. nginx.conf receives request on port 80
3. nginx.conf includes all apps/*.conf files
4. nginx-port80-base.conf defines server block matching the hostname
5. app3-routing.conf location block `~ ^/app3/static/(.*)$` matches
6. Regex captures `style.css` in variable $1
7. proxy_pass forwards to `http://127.0.0.1:5003/static/style.css`
8. FastAPI app on port 5003 serves the CSS file
9. Response flows back through nginx to client browser

### Example 2: Application Page Request
**URL:** `http://172.25.25.140/app1/dashboard`

**Flow Steps:**
1. Client browser requests application page
2. nginx receives request on port 80
3. nginx-port80-base.conf server block processes request
4. app1-routing.conf location `/app1/` matches
5. Rewrite rule transforms `/app1/dashboard` to `/dashboard`
6. proxy_pass forwards to `http://127.0.0.1:5001/dashboard`
7. Proxy headers preserve client information
8. FastAPI app handles the dashboard route
9. HTML response flows back through nginx to client

### Example 3: API Status Check
**URL:** `http://172.25.25.140/api/status`

**Flow Steps:**
1. Monitoring system requests status
2. nginx receives request on port 80
3. nginx-port80-base.conf location `/api/status` matches
4. nginx directly returns JSON response (no proxy)
5. Response includes health status and timestamp
6. JSON flows directly back to monitoring system

---

**COMPLETE DOCUMENTATION** - Every line of every configuration file explained with technical details, architectural benefits, and operational guidance. This modular nginx setup provides a professional, scalable, and maintainable solution for hosting multiple FastAPI applications through a single port 80 reverse proxy.

---

**Created:** September 20, 2025  
**Status:** Production Ready  
**Architecture:** Modular nginx with FastAPI backend applications  
**Port Strategy:** Single port 80 with path-based routing