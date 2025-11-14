# Complete Pipeline Files - Word by Word Explanation

## 📋 Table of Contents
1. [Pipeline Overview](#pipeline-overview)
2. [Application Files (FastAPI)](#application-files-fastapi)
3. [NGINX Configuration Files](#nginx-configuration-files)
4. [Docker Compose File](#docker-compose-file)
5. [Promtail Configuration](#promtail-configuration)
6. [Loki Configuration](#loki-configuration)
7. [Grafana Configuration](#grafana-configuration)
8. [Dashboard JSON Explanation](#dashboard-json-explanation)

---

## Pipeline Overview

### Complete Data Flow
```
User Request (Browser)
    ↓
NGINX (Port 80) ← nginx.conf, app1-routing.conf
    ↓
FastAPI App (Port 5001) ← main.py
    ↓
Logs Generated ← app1.log, app1-json.log, app1_access.log
    ↓
Promtail Collects ← promtail-config.yml
    ↓
Loki Stores ← loki-config.yml
    ↓
Grafana Displays ← app1-loki-enhanced.json
    ↓
Dashboard (Browser)
```

---

## Application Files (FastAPI)

### File: `app1/main.py`

```python
import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI
import uvicorn

# ============================================
# LOGGING SETUP - Dual Logging (Text + JSON)
# ============================================

# TEXT LOGGER SETUP
text_handler = logging.FileHandler('app1.log')
# logging.FileHandler: Python ka built-in class jo file mein logs likhti hai
# 'app1.log': File ka naam jahan text logs save hongi

text_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
# logging.Formatter: Log message ka format define karta hai
# %(asctime)s: Timestamp (e.g., 2025-10-09 11:22:19,123)
# %(name)s: Logger ka naam (e.g., __main__)
# %(levelname)s: Log level (INFO, ERROR, WARNING, DEBUG)
# %(message)s: Actual log message

# JSON LOGGER SETUP
json_handler = logging.FileHandler('app1-json.log')
# Alag file for JSON format logs

json_handler.setFormatter(jsonlogger.JsonFormatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
))
# jsonlogger.JsonFormatter: Logs ko JSON format mein convert karta hai
# Output example: {"asctime": "2025-10-09 11:22:19", "levelname": "INFO", ...}

# LOGGER CONFIGURATION
logger = logging.getLogger(__name__)
# logging.getLogger(): Logger instance create karta hai
# __name__: Current module ka naam (__main__ when run directly)

logger.setLevel(logging.INFO)
# setLevel(): Minimum log level set karta hai
# INFO: INFO aur usse upar ke logs record honge (INFO, WARNING, ERROR, CRITICAL)
# DEBUG logs ignore honge

logger.addHandler(text_handler)
logger.addHandler(json_handler)
# addHandler(): Logger mein handler add karta hai
# Ek logger multiple handlers use kar sakta hai (text + json)

# ============================================
# FASTAPI APPLICATION
# ============================================

app = FastAPI()
# FastAPI(): FastAPI application instance create karta hai
# Yeh web application ka main object hai

@app.get("/")
# @app.get(): HTTP GET request ke liye decorator
# "/": Root path (e.g., http://localhost:5001/)
async def root():
    # async: Asynchronous function (non-blocking, fast)
    logger.info("Root endpoint accessed")
    # logger.info(): INFO level log message
    # Yeh message dono files mein jayega (text + json)
    return {"message": "Welcome to App1", "theme": "blue"}
    # return: JSON response browser ko send hoga

@app.get("/api/app-info")
async def app_info():
    logger.info("App info endpoint accessed")
    return {
        "app": "app1",
        "port": 5001,
        "theme": "blue",
        "status": "running"
    }

# ============================================
# APPLICATION STARTUP
# ============================================

if __name__ == "__main__":
    # __name__ == "__main__": Jab file directly run ho (python main.py)
    uvicorn.run(app, host="0.0.0.0", port=5001)
    # uvicorn.run(): ASGI server start karta hai
    # app: FastAPI application object
    # host="0.0.0.0": Saare network interfaces par listen karega
    # port=5001: Application is port par chalega
```

**Key Concepts:**

**1. Dual Logging:**
- **Text logs** (`app1.log`): Human-readable, debugging ke liye easy
- **JSON logs** (`app1-json.log`): Machine-readable, parsing ke liye perfect

**2. Log Levels (Importance Order):**
```
DEBUG    → Detailed debugging info (development only)
INFO     → General information (app started, endpoint accessed)
WARNING  → Warning messages (something unusual but not error)
ERROR    → Error occurred but app still running
CRITICAL → Serious error, app might crash
```

**3. Why `async`?**
- **Synchronous**: Ek request complete hone tak wait karta hai
- **Asynchronous**: Multiple requests parallel handle kar sakta hai
- FastAPI async support karta hai → Better performance

---

## NGINX Configuration Files

### File: `C:\nginx\conf\nginx.conf`

```nginx
# ============================================
# WORKER PROCESSES
# ============================================
worker_processes  1;
# worker_processes: Kitne worker processes start honge
# 1: Single worker (testing/development ke liye)
# Production mein: CPU cores ke barabar (e.g., 4 or 8)

# ============================================
# EVENTS BLOCK
# ============================================
events {
    worker_connections  1024;
    # worker_connections: Ek worker kitne simultaneous connections handle kar sakta hai
    # 1024: Ek worker 1024 clients ko serve kar sakta hai
    # Total capacity = worker_processes × worker_connections
}

# ============================================
# HTTP BLOCK
# ============================================
http {
    include       mime.types;
    # include: External file ko include karta hai
    # mime.types: File types ka mapping (e.g., .html → text/html, .jpg → image/jpeg)
    
    default_type  application/octet-stream;
    # default_type: Agar file type unknown ho to default content-type
    # application/octet-stream: Binary data (browser download karega)
    
    sendfile        on;
    # sendfile: OS-level file transmission (faster than reading in memory)
    # on: Enable (performance boost)
    
    keepalive_timeout  65;
    # keepalive_timeout: Connection kitni der open rahega (seconds)
    # 65: 65 seconds tak connection reuse hoga (multiple requests)
    
    # Include port 80 configuration
    include apps/nginx-port80-base.conf;
    # apps/nginx-port80-base.conf: Server block configuration
}
```

### File: `C:\nginx\conf\apps\nginx-port80-base.conf`

```nginx
# ============================================
# SERVER BLOCK - PORT 80
# ============================================
server {
    listen 80;
    # listen: Kis port par listen karega
    # 80: HTTP default port (http://172.25.25.140/)
    
    server_name localhost 172.25.25.140 _;
    # server_name: Kis domain/IP ke liye respond karega
    # localhost: Local access (http://localhost/)
    # 172.25.25.140: Network IP
    # _: Default/catch-all (koi bhi domain match karega)
    
    # ============================================
    # SECURITY HEADERS
    # ============================================
    add_header X-Frame-Options "SAMEORIGIN" always;
    # X-Frame-Options: Clickjacking attack se protection
    # SAMEORIGIN: Page sirf same domain ke iframe mein load hoga
    # always: Har response mein header add karo
    
    add_header X-Content-Type-Options "nosniff" always;
    # X-Content-Type-Options: MIME-type sniffing disable
    # nosniff: Browser file type ko assume nahi karega, declared type use karega
    
    # ============================================
    # APP ROUTING INCLUDES
    # ============================================
    include apps/app1-routing.conf;
    include apps/app2-routing.conf;
    include apps/app3-routing.conf;
    include apps/app4-routing.conf;
    include apps/app5-routing.conf;
    # include: Har app ki routing configuration ko include karta hai
    
    # ============================================
    # HEALTH CHECK ENDPOINT
    # ============================================
    location /health {
        # location: URL path ke liye configuration
        access_log off;
        # access_log off: Is endpoint ke logs record nahi honge
        # Health check logs se clutter avoid karne ke liye
        
        return 200 'OK';
        # return: Direct response (without proxy)
        # 200: HTTP status code (success)
        # 'OK': Response body
        
        add_header Content-Type text/plain;
        # Content-Type: Response ka MIME type
        # text/plain: Plain text
    }
}
```

### File: `C:\nginx\conf\apps\app1-routing.conf`

```nginx
# ============================================
# APP1 ROUTING CONFIGURATION
# ============================================
# Blue theme FastAPI application
# Port: 5001
# Endpoints: /, /api/app-info

# ============================================
# STATIC FILES LOCATION
# ============================================
location ~ ^/app1/static/(.*)$ {
    # location ~: Regex-based location matching
    # ^/app1/static/(.*)$: Pattern for static files
    #   ^: Start of string
    #   /app1/static/: Fixed path
    #   (.*): Capture group (kuch bhi match karega)
    #   $: End of string
    # Example match: /app1/static/css/main.css → $1 = css/main.css
    
    proxy_pass http://127.0.0.1:5001/static/$1;
    # proxy_pass: Request ko forward karta hai
    # http://127.0.0.1:5001: Backend server
    # /static/$1: $1 = captured group from regex
    # Example: /app1/static/css/main.css → http://127.0.0.1:5001/static/css/main.css
    
    proxy_set_header Host $host;
    # proxy_set_header: Backend ko header send karta hai
    # Host: Original host header preserve karta hai
}

# ============================================
# MAIN APP LOCATION
# ============================================
location /app1/ {
    # location /app1/: Exact prefix match
    # Matches: /app1/, /app1/api/app-info, /app1/anything
    
    # ============================================
    # LOGGING (CRITICAL: MUST BE FIRST)
    # ============================================
    access_log C:/nginx/logs/app1_access.log combined;
    # access_log: Access logs ka file path
    # C:/nginx/logs/app1_access.log: Log file location (forward slashes required)
    # combined: Log format (predefined format with detailed info)
    # IMPORTANT: Location block mein sabse pehle hona chahiye
    
    error_log C:/nginx/logs/app1_error.log warn;
    # error_log: Error logs ka file path
    # warn: Minimum log level (warn, error, crit)
    
    # ============================================
    # URL REWRITING
    # ============================================
    rewrite ^/app1/(.*)$ /$1 break;
    # rewrite: URL ko modify karta hai
    # ^/app1/(.*)$: Input pattern
    #   /app1/api/app-info → Capture: api/app-info
    # /$1: Replacement
    #   /api/app-info (without /app1/ prefix)
    # break: Aur rewrites apply nahi honge
    # Why? Backend app ko /app1/ prefix nahi chahiye
    
    # ============================================
    # PROXY CONFIGURATION
    # ============================================
    proxy_pass http://127.0.0.1:5001;
    # proxy_pass: Request backend ko forward karo
    # http://127.0.0.1:5001: FastAPI app ka address
    # No trailing slash: URL path as-is forward hoga
    
    # ============================================
    # PROXY HEADERS
    # ============================================
    proxy_set_header Host $host;
    # Host: Original domain name
    # Example: 172.25.25.140
    
    proxy_set_header X-Real-IP $remote_addr;
    # X-Real-IP: Client ka actual IP address
    # $remote_addr: NGINX variable (client IP)
    # Example: 192.168.1.100
    
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    # X-Forwarded-For: IP addresses ka chain (proxies ke through)
    # $proxy_add_x_forwarded_for: Existing X-Forwarded-For + current client IP
    # Example: 192.168.1.100, 172.25.25.140
    
    proxy_set_header X-Forwarded-Proto $scheme;
    # X-Forwarded-Proto: Original protocol (http or https)
    # $scheme: Current scheme
    
    # ============================================
    # WEBSOCKET SUPPORT
    # ============================================
    proxy_http_version 1.1;
    # proxy_http_version: HTTP version for proxy connection
    # 1.1: Required for WebSocket support
    
    proxy_set_header Upgrade $http_upgrade;
    # Upgrade: WebSocket upgrade header
    # $http_upgrade: Client's Upgrade header value
    
    proxy_set_header Connection "upgrade";
    # Connection: WebSocket connection header
    
    # ============================================
    # TIMEOUTS
    # ============================================
    proxy_connect_timeout 60s;
    # proxy_connect_timeout: Backend se connect hone ka timeout
    # 60s: 60 seconds wait karega
    
    proxy_send_timeout 60s;
    # proxy_send_timeout: Request send karne ka timeout
    
    proxy_read_timeout 60s;
    # proxy_read_timeout: Response receive karne ka timeout
}
```

**NGINX Log Format (Combined):**
```
172.25.25.140 - - [09/Oct/2025:11:22:19 +0500] "GET /app1/ HTTP/1.1" 200 1269 "-" "Mozilla/5.0..."
│             │ │ │                            │              │   │    │    │
│             │ │ │                            │              │   │    │    └─ User Agent
│             │ │ │                            │              │   │    └────── Referer
│             │ │ │                            │              │   └─────────── Bytes sent
│             │ │ │                            │              └─────────────── Status code
│             │ │ │                            └────────────────────────────── Request line
│             │ │ └───────────────────────────────────────────────────────── Timestamp
│             │ └─────────────────────────────────────────────────────────── Auth user
│             └───────────────────────────────────────────────────────────── Remote user
└─────────────────────────────────────────────────────────────────────────── Client IP
```

---

## Docker Compose File

### File: `monitoring/docker-compose.yml`

```yaml
# ============================================
# DOCKER COMPOSE VERSION
# ============================================
version: '3.8'
# version: Docker Compose file ka syntax version
# 3.8: Latest stable version with modern features

# ============================================
# SERVICES DEFINITION
# ============================================
services:
  # services: Container definitions ka block
  
  # ==========================================
  # LOKI - LOG AGGREGATION
  # ==========================================
  loki:
    # Service name (container reference ke liye)
    
    image: grafana/loki:latest
    # image: Docker Hub se image
    # grafana/loki: Official Loki image
    # latest: Latest version (production mein specific version use karo)
    
    container_name: loki-apps
    # container_name: Container ka naam (docker ps mein dikhega)
    # loki-apps: Easy identification ke liye
    
    restart: unless-stopped
    # restart: Container restart policy
    # unless-stopped: Hamesha restart karo except jab manually stop kiya ho
    # Other options: no, always, on-failure
    
    ports:
      - "3100:3100"
      # ports: Port mapping (host:container)
      # 3100:3100: Host ka port 3100 → Container ka port 3100
      # Format: "HOST_PORT:CONTAINER_PORT"
      # Loki API: http://localhost:3100
    
    volumes:
      - ./loki/loki-config.yml:/etc/loki/local-config.yaml:ro
      # volumes: File/folder mounting
      # ./loki/loki-config.yml: Host system ka file (relative path)
      # :/etc/loki/local-config.yaml: Container mein path
      # :ro: Read-only (container file modify nahi kar sakta)
      
      - loki-data:/loki
      # loki-data: Named volume (Docker managed)
      # /loki: Container mein mount point
      # Logs yahan store honge (persistent storage)
    
    command: -config.file=/etc/loki/local-config.yaml
    # command: Container start hone par run hoga
    # -config.file=...: Loki ko config file ka path batata hai
    
    networks:
      - monitoring-network
      # networks: Container kis network mein hoga
      # monitoring-network: Custom network (services aapas mein communicate kar sakti hain)

  # ==========================================
  # PROMTAIL - LOG SHIPPER
  # ==========================================
  promtail:
    image: grafana/promtail:latest
    # grafana/promtail: Official Promtail image
    
    container_name: promtail-apps
    restart: unless-stopped
    
    volumes:
      - ./promtail/promtail-config.yml:/etc/promtail/config.yml:ro
      # Promtail configuration file
      
      - /var/log:/var/log:ro
      # System logs (Linux only, Windows mein ignore hoga)
      
      - C:/Users/muhammadahmad4/applications:/apps:ro
      # Application logs directory
      # C:/Users/...: Windows path
      # :/apps: Container mein mount point
      # :ro: Read-only access
      
      - C:/nginx/logs:/nginx-logs:ro
      # NGINX logs directory
      # :/nginx-logs: Container mein accessible as /nginx-logs
    
    command: -config.file=/etc/promtail/config.yml
    # Promtail ko config file path
    
    depends_on:
      - loki
      # depends_on: Service dependency
      # loki: Pehle Loki start hoga, phir Promtail
      # Note: Yeh startup order ensure karta hai, health check nahi
    
    extra_hosts:
      - "host.docker.internal:host-gateway"
      # extra_hosts: Container ke /etc/hosts mein entry add karta hai
      # host.docker.internal: Host machine ka reference
      # host-gateway: Special Docker DNS name
      # Why? Container se host machine access karne ke liye
    
    networks:
      - monitoring-network

  # ==========================================
  # GRAFANA - VISUALIZATION
  # ==========================================
  grafana:
    image: grafana/grafana:latest
    container_name: grafana-apps
    restart: unless-stopped
    
    ports:
      - "3000:3000"
      # Grafana web interface: http://localhost:3000
    
    environment:
      # environment: Container ke environment variables
      
      - GF_AUTH_ANONYMOUS_ENABLED=true
      # GF_AUTH_ANONYMOUS_ENABLED: Anonymous access allow karta hai
      # true: Bina login dashboards dekh sakte hain
      
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
      # GF_AUTH_ANONYMOUS_ORG_ROLE: Anonymous users ka role
      # Admin: Full access (testing ke liye, production mein Viewer use karo)
      
      - GF_AUTH_DISABLE_LOGIN_FORM=true
      # GF_AUTH_DISABLE_LOGIN_FORM: Login page disable
      # true: Direct dashboard access (no login required)
      
      - GF_SECURITY_ADMIN_USER=admin
      # GF_SECURITY_ADMIN_USER: Default admin username
      
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      # GF_SECURITY_ADMIN_PASSWORD: Default admin password
      # IMPORTANT: Production mein strong password use karo
      
      - GF_USERS_ALLOW_SIGN_UP=false
      # GF_USERS_ALLOW_SIGN_UP: New user registration
      # false: Disabled (security)
      
      - GF_SERVER_ROOT_URL=http://localhost:3000
      # GF_SERVER_ROOT_URL: Grafana ka public URL
    
    volumes:
      - grafana-data:/var/lib/grafana
      # grafana-data: Named volume for Grafana data (dashboards, settings)
      # Persistent storage (container restart hone par data rahega)
      
      - ./grafana/provisioning:/etc/grafana/provisioning
      # Provisioning directory: Auto-configure datasources and dashboards
      
      - ./grafana/dashboards:/var/lib/grafana/dashboards
      # Dashboard JSON files ka directory
    
    depends_on:
      - loki
      # Loki pehle start hoga
    
    networks:
      - monitoring-network

# ============================================
# NETWORKS DEFINITION
# ============================================
networks:
  monitoring-network:
    # monitoring-network: Custom bridge network
    driver: bridge
    # driver: Network type
    # bridge: Default Docker network driver
    # Containers ek dusre se naam se communicate kar sakte hain
    # Example: Grafana → http://loki:3100 (container name as hostname)

# ============================================
# VOLUMES DEFINITION
# ============================================
volumes:
  loki-data:
    # loki-data: Named volume for Loki data
    # Docker managed: /var/lib/docker/volumes/monitoring_loki-data
    # Persistent: Container delete hone par bhi data rahega
  
  grafana-data:
    # grafana-data: Named volume for Grafana data
```

**Key Docker Concepts:**

**1. Named Volumes vs Bind Mounts:**
```yaml
# Named Volume (Docker managed)
volumes:
  - loki-data:/loki

# Bind Mount (Host path)
volumes:
  - C:/nginx/logs:/nginx-logs:ro
```

**2. Network Communication:**
```
Container Name → Internal DNS Resolution
grafana-apps   → http://loki:3100 (works!)
promtail-apps  → http://loki:3100 (works!)
```

**3. Restart Policies:**
```
no             → Never restart
always         → Always restart (even after manual stop)
unless-stopped → Always restart except manual stop
on-failure     → Restart only on error
```

---

## Promtail Configuration

### File: `monitoring/promtail/promtail-config.yml`

```yaml
# ============================================
# SERVER CONFIGURATION
# ============================================
server:
  # server: Promtail ka internal HTTP server
  
  http_listen_port: 9080
  # http_listen_port: Promtail metrics endpoint ka port
  # 9080: http://localhost:9080/metrics (Prometheus scraping ke liye)
  
  grpc_listen_port: 0
  # grpc_listen_port: gRPC server port
  # 0: Disabled (gRPC not needed)

# ============================================
# POSITIONS FILE
# ============================================
positions:
  filename: /tmp/positions.yaml
  # positions.filename: File read positions track karta hai
  # /tmp/positions.yaml: Yeh file store karti hai ki har log file ka last read position
  # Why? Restart hone par duplicate logs avoid karne ke liye
  # Example content:
  #   /nginx-logs/app1_access.log: 12345  ← Byte offset

# ============================================
# LOKI CLIENT
# ============================================
clients:
  - url: http://loki:3100/loki/api/v1/push
    # clients: Loki servers ki list (multiple ho sakte hain)
    # url: Loki ka push endpoint
    # http://loki:3100: Container name as hostname (Docker network)
    # /loki/api/v1/push: Loki ka ingestion API endpoint

# ============================================
# SCRAPE CONFIGURATIONS
# ============================================
scrape_configs:
  # scrape_configs: Log collection rules ki list

  # ==========================================
  # APP1 LOGS
  # ==========================================
  - job_name: app1
    # job_name: Unique identifier for this scrape job
    # app1: Loki mein {job="app1"} label se accessible
    
    static_configs:
      # static_configs: Fixed targets (dynamic discovery nahi hai)
      
      - targets:
          - localhost
          # targets: Log sources ki list
          # localhost: Local files (dummy value, actually file paths use hote hain)
        
        labels:
          # labels: Har log line ke saath attach hone wale metadata
          
          job: app1
          # job: Primary label for filtering
          # Query: {job="app1"}
          
          app: application1
          # app: Additional label for categorization
          # Query: {job="app1", app="application1"}
          
          __path__: /apps/app1/*.log
          # __path__: Log files ka glob pattern (SPECIAL LABEL)
          # /apps/app1/: Container mein mounted directory
          # *.log: Saare .log files match honge
          # Matches: /apps/app1/app1.log, /apps/app1/app1-json.log
          # Note: __ (double underscore) = internal Promtail label

  # ==========================================
  # NGINX APP1 ACCESS LOGS
  # ==========================================
  - job_name: nginx-app1-access
    static_configs:
      - targets:
          - localhost
        labels:
          job: nginx-app1
          # job: NGINX logs ke liye
          # Query: {job="nginx-app1"}
          
          app: app1
          # app: Kis app ke logs hain
          
          log_type: access
          # log_type: Access vs error logs distinguish karne ke liye
          # Query: {job="nginx-app1", log_type="access"}
          
          __path__: /nginx-logs/app1_access.log
          # __path__: Single file path (no glob)
          # /nginx-logs/: Mounted NGINX logs directory

  # ==========================================
  # NGINX APP1 ERROR LOGS
  # ==========================================
  - job_name: nginx-app1-error
    static_configs:
      - targets:
          - localhost
        labels:
          job: nginx-app1
          app: app1
          log_type: error
          # log_type: Error logs
          # Query: {job="nginx-app1", log_type="error"}
          
          __path__: /nginx-logs/app1_error.log

  # ==========================================
  # JSON LOGS WITH PIPELINE
  # ==========================================
  - job_name: uvicorn
    static_configs:
      - targets:
          - localhost
        labels:
          job: uvicorn
          __path__: /apps/app*/*-json.log
          # Glob pattern: Saare apps ke JSON logs
          # Matches: /apps/app1/app1-json.log, /apps/app2/app2-json.log, etc.
    
    pipeline_stages:
      # pipeline_stages: Log processing steps
      
      - json:
          # json: JSON logs ko parse karta hai
          expressions:
            # expressions: JSON fields ko extract karta hai
            
            timestamp: asctime
            # timestamp: JSON ka "asctime" field extract karo
            # Input: {"asctime": "2025-10-09 11:22:19", ...}
            # Output: timestamp = "2025-10-09 11:22:19"
            
            level: levelname
            # level: Log level extract
            # Input: {"levelname": "INFO", ...}
            
            message: message
            # message: Log message extract
            
            app: name
            # app: Application name extract
            # Input: {"name": "app1", ...}
      
      - labels:
          # labels: Extracted fields ko labels mein convert
          app:
          # app field ko label banao
          # Result: {job="uvicorn", app="app1"}
      
      - timestamp:
          # timestamp: Parsed timestamp ko use karo (not current time)
          source: timestamp
          # source: Kon sa field use karna hai
          format: RFC3339
          # format: Timestamp format
          # RFC3339: 2025-10-09T11:22:19Z
```

**Promtail Label Explanation:**

**1. Internal Labels (start with __):**
```yaml
__path__: /apps/app1/*.log  # File path pattern (Promtail use karta hai)
```
- `__` prefix = Promtail internal
- Loki mein nahi jaate
- Sirf file selection ke liye

**2. External Labels (sent to Loki):**
```yaml
job: app1        # {job="app1"}
app: application1 # {app="application1"}
log_type: access  # {log_type="access"}
```
- Loki mein queryable
- Filtering aur grouping ke liye

**3. Label Queries:**
```logql
{job="app1"}                          # App1 logs
{job="nginx-app1"}                    # NGINX logs for app1
{job="nginx-app1", log_type="access"} # NGINX access logs only
{job="uvicorn", app="app1"}           # JSON logs for app1
```

---

## Loki Configuration

### File: `monitoring/loki/loki-config.yml`

```yaml
# ============================================
# AUTHENTICATION
# ============================================
auth_enabled: false
# auth_enabled: Multi-tenancy authentication
# false: Single tenant mode (no auth required)
# true: Har request mein X-Scope-OrgID header chahiye

# ============================================
# SERVER SETTINGS
# ============================================
server:
  http_listen_port: 3100
  # http_listen_port: Loki API port
  # 3100: Main API endpoint
  # Endpoints: /loki/api/v1/push (ingestion), /loki/api/v1/query (querying)
  
  grpc_listen_port: 9096
  # grpc_listen_port: gRPC server port
  # 9096: Internal communication (distributors, ingesters)

# ============================================
# COMMON CONFIGURATION
# ============================================
common:
  path_prefix: /loki
  # path_prefix: Base directory for Loki data
  # /loki: Container mein path (volume mounted)
  
  storage:
    # storage: Storage backend configuration
    
    filesystem:
      # filesystem: Local disk storage (single-node setup)
      # Production mein: S3, GCS, Azure Blob
      
      chunks_directory: /loki/chunks
      # chunks_directory: Compressed log chunks ka storage
      # /loki/chunks: Log data stored here
      
      rules_directory: /loki/rules
      # rules_directory: Alerting rules ka storage
  
  replication_factor: 1
  # replication_factor: Data copies ki count
  # 1: No replication (single node)
  # 3: Production mein recommended (high availability)
  
  ring:
    # ring: Distributed hash ring configuration
    
    instance_addr: 127.0.0.1
    # instance_addr: Is Loki instance ka address
    # 127.0.0.1: Localhost (single node)
    
    kvstore:
      # kvstore: Key-value store for ring state
      
      store: inmemory
      # store: Storage backend type
      # inmemory: RAM mein store (restart par data lost)
      # Production: consul, etcd (persistent)

# ============================================
# SCHEMA CONFIGURATION
# ============================================
schema_config:
  # schema_config: Index aur chunk storage schema
  
  configs:
    - from: 2020-10-24
      # from: Schema start date (YYYY-MM-DD)
      # 2020-10-24: Schema effective date
      # Why? Schema changes ke liye different dates use kar sakte hain
      
      store: boltdb-shipper
      # store: Index storage backend
      # boltdb-shipper: Embedded database (single-node friendly)
      # Production: cassandra, bigtable
      
      object_store: filesystem
      # object_store: Chunk storage backend
      # filesystem: Local disk
      # Production: s3, gcs
      
      schema: v11
      # schema: Index schema version
      # v11: Latest stable schema
      
      index:
        # index: Index configuration
        
        prefix: index_
        # prefix: Index files ka prefix
        # index_: Files named as index_XXXXXX
        
        period: 24h
        # period: Har kitne time baad new index file
        # 24h: Daily rotation
        # Options: 24h, 168h (weekly)

# ============================================
# RULER (ALERTING)
# ============================================
ruler:
  alertmanager_url: http://localhost:9093
  # alertmanager_url: Prometheus Alertmanager ka URL
  # http://localhost:9093: Alerts yahan send honge
  # Note: Hamare setup mein Alertmanager nahi hai (optional)

# ============================================
# LIMITS CONFIGURATION
# ============================================
limits_config:
  # limits_config: Resource limits aur retention
  
  retention_period: 168h
  # retention_period: Logs kitni der store rahenge
  # 168h: 7 days (1 week)
  # Options: 24h (1 day), 720h (30 days)
  # Old logs automatically delete honge
  
  ingestion_rate_mb: 10
  # ingestion_rate_mb: Maximum ingestion rate per tenant
  # 10: 10 MB/second maximum
  # Limit cross karne par 429 error
  
  ingestion_burst_size_mb: 20
  # ingestion_burst_size_mb: Burst capacity
  # 20: Short bursts mein 20 MB/s allow
  # Sustained load ingestion_rate_mb se zyada nahi hona chahiye
```

**Loki Storage Architecture:**

```
Logs Flow:
  Promtail → Loki → Distributor → Ingester → Chunks
                                           ↓
                                     /loki/chunks/
                                           ↓
                                  compressed files
```

**Index vs Chunks:**
```
INDEX (/loki/index_*)
- Metadata: Labels, timestamps, chunk references
- Small files
- Fast querying ke liye

CHUNKS (/loki/chunks/*)
- Actual log data (compressed)
- Large files
- Efficient storage ke liye
```

**Retention Example:**
```
retention_period: 168h (7 days)

Day 1: Logs ingested → stored
Day 2: Logs ingested → stored
...
Day 7: Logs ingested → stored
Day 8: Day 1 logs deleted (7 days crossed)
Day 9: Day 2 logs deleted
```

---

## Grafana Configuration

### File: `monitoring/grafana/provisioning/datasources/datasources.yml`

```yaml
# ============================================
# DATASOURCES PROVISIONING
# ============================================
apiVersion: 1
# apiVersion: Provisioning API version
# 1: Current version

datasources:
  # datasources: Data source definitions ki list
  
  - name: Loki
    # name: Datasource ka naam (Grafana UI mein dikhega)
    # Loki: Dashboard queries mein use hoga
    
    type: loki
    # type: Datasource type
    # loki: Grafana Loki datasource plugin
    # Other types: prometheus, elasticsearch, mysql, etc.
    
    access: proxy
    # access: Data access method
    # proxy: Grafana server se data fetch karega (recommended)
    # direct: Browser se directly data fetch (CORS issues ho sakte hain)
    
    url: http://loki:3100
    # url: Loki server ka endpoint
    # http://loki:3100: Container name as hostname (Docker network)
    # /loki/api/v1/query: API endpoint (auto-appended)
    
    uid: P8E80F9AEF21F6940
    # uid: Unique identifier (dashboard JSON mein use hoga)
    # P8E80F9AEF21F6940: Random unique string
    # Why? Dashboard import/export mein consistency ke liye
    
    isDefault: true
    # isDefault: Default datasource
    # true: New panels mein automatically select hoga
    
    editable: true
    # editable: UI se edit kar sakte hain?
    # true: Settings changeable
    # false: Read-only (production mein recommended)
```

### File: `monitoring/grafana/provisioning/dashboards/dashboards.yml`

```yaml
# ============================================
# DASHBOARD PROVISIONING
# ============================================
apiVersion: 1

providers:
  # providers: Dashboard providers ki list
  
  - name: 'Default'
    # name: Provider ka naam
    # 'Default': Default provider (multiple ho sakte hain)
    
    orgId: 1
    # orgId: Grafana organization ID
    # 1: Default organization
    # Multi-org setups mein different IDs
    
    folder: ''
    # folder: Dashboards kis folder mein store honge
    # '': Root level (no folder)
    # 'App Dashboards': Custom folder name
    
    type: file
    # type: Provider type
    # file: JSON files se load karega
    # Other: database, cloud
    
    disableDeletion: false
    # disableDeletion: UI se delete kar sakte hain?
    # false: Deletable
    # true: Read-only (accidental deletion prevent)
    
    updateIntervalSeconds: 10
    # updateIntervalSeconds: File changes check interval
    # 10: Har 10 seconds mein check karega
    # File update hone par dashboard auto-reload
    
    allowUiUpdates: true
    # allowUiUpdates: UI se edit kar sakte hain?
    # true: Editable
    # false: Read-only
    
    options:
      # options: Provider-specific settings
      
      path: /var/lib/grafana/dashboards
      # path: Dashboard JSON files ka directory
      # /var/lib/grafana/dashboards: Container mein mounted path
      # Saare .json files yahan se load honge
      
      foldersFromFilesStructure: false
      # foldersFromFilesStructure: Subdirectories ko folders banao?
      # false: Saare dashboards root level mein
      # true: Directory structure preserve karega
```

---

## Dashboard JSON Explanation

### File: `monitoring/grafana/dashboards/app1-loki-enhanced.json`

Ab main **har word** explain karta hoon step by step:

### Top-Level Structure

```json
{
  "annotations": {
    "list": []
  },
```
**Explanation:**
- `annotations`: Dashboard par overlays/markers
- `list`: Annotation definitions ka array
- `[]`: Empty = No annotations configured
- **Use Case**: Deployment markers, incident indicators

```json
  "editable": true,
```
- `editable`: Dashboard ko edit kar sakte hain?
- `true`: Edit mode available
- `false`: Read-only dashboard

```json
  "fiscalYearStartMonth": 0,
```
- `fiscalYearStartMonth`: Financial year kis month se start hota hai
- `0`: January (0-indexed)
- **Use Case**: Business reporting, financial dashboards

```json
  "graphTooltip": 1,
```
- `graphTooltip`: Tooltip display mode
- `0`: Default (hover par individual panel)
- `1`: Shared crosshair (saare panels synchronized)
- `2`: Shared tooltip (same time par saare values)

```json
  "id": null,
```
- `id`: Dashboard ka database ID
- `null`: Auto-generated on import
- **Number**: Existing dashboard (e.g., `42`)

```json
  "links": [],
```
- `links`: Dashboard navigation links
- `[]`: No external links
- **Example**: Link to other dashboards, documentation

```json
  "liveNow": true,
```
- `liveNow`: Real-time data updates
- `true`: Latest data continuously fetch
- `false`: Time range fixed rahega

---

### Panel 1: Request Rate (Time Series)

```json
  "panels": [
    {
      "datasource": {"type": "loki", "uid": "P8E80F9AEF21F6940"},
```
**Explanation:**
- `panels`: Dashboard panels ka array
- `datasource`: Data source configuration
  - `type`: `"loki"` = Loki datasource
  - `uid`: `"P8E80F9AEF21F6940"` = Datasource unique ID (datasources.yml se match)

```json
      "fieldConfig": {
        "defaults": {
```
- `fieldConfig`: Field/column configuration
- `defaults`: Default settings (saare fields ke liye)

```json
          "color": {"mode": "palette-classic"},
```
- `color`: Color scheme
- `mode`:
  - `"palette-classic"`: Grafana ka classic color palette
  - `"thresholds"`: Threshold-based colors
  - `"fixed"`: Single color

```json
          "custom": {
            "axisCenteredZero": false,
```
- `custom`: Visualization-specific settings
- `axisCenteredZero`: Y-axis zero par centered ho?
  - `false`: Auto-scale (data range ke hisab se)
  - `true`: Zero hamesha center mein

```json
            "axisColorMode": "text",
```
- `axisColorMode`: Axis color scheme
  - `"text"`: Normal text color
  - `"series"`: Data series ke colors

```json
            "axisLabel": "Requests/sec",
```
- `axisLabel`: Y-axis ka label
- `"Requests/sec"`: Display text

```json
            "axisPlacement": "auto",
```
- `axisPlacement`: Y-axis position
  - `"auto"`: Automatic
  - `"left"`: Left side
  - `"right"`: Right side

```json
            "barAlignment": 0,
```
- `barAlignment`: Bar chart alignment
- `0`: Center aligned
- `-1`: Left aligned
- `1`: Right aligned

```json
            "drawStyle": "line",
```
- `drawStyle`: Graph drawing style
  - `"line"`: Line graph
  - `"bars"`: Bar chart
  - `"points"`: Scatter plot

```json
            "fillOpacity": 20,
```
- `fillOpacity`: Line ke neeche fill transparency
- `20`: 20% opaque (80% transparent)
- `0-100`: 0=invisible, 100=solid

```json
            "gradientMode": "opacity",
```
- `gradientMode`: Gradient effect
  - `"opacity"`: Transparency gradient
  - `"hue"`: Color gradient
  - `"none"`: No gradient

```json
            "hideFrom": {"tooltip": false, "viz": false, "legend": false},
```
- `hideFrom`: Kahan hide karna hai
  - `tooltip: false`: Tooltip mein show karo
  - `viz: false`: Graph mein show karo
  - `legend: false`: Legend mein show karo

```json
            "lineInterpolation": "smooth",
```
- `lineInterpolation`: Line drawing method
  - `"smooth"`: Curved/smooth lines
  - `"linear"`: Straight lines
  - `"stepBefore"`: Step graph

```json
            "lineWidth": 2,
```
- `lineWidth`: Line thickness (pixels)
- `2`: 2px thick line

```json
            "pointSize": 5,
```
- `pointSize`: Data point size
- `5`: 5px radius circles

```json
            "scaleDistribution": {"type": "linear"},
```
- `scaleDistribution`: Y-axis scale type
  - `"linear"`: Normal scale
  - `"log"`: Logarithmic scale

```json
            "showPoints": "never",
```
- `showPoints`: Data points visibility
  - `"never"`: Hide points (only lines)
  - `"always"`: Always show
  - `"auto"`: Auto (zoomed in par show)

```json
            "spanNulls": false,
```
- `spanNulls`: Null values ko skip karo?
  - `false`: Break line at nulls
  - `true`: Connect lines across nulls

```json
            "stacking": {"group": "A", "mode": "none"},
```
- `stacking`: Stacking configuration
  - `group`: Stacking group name
  - `mode`:
    - `"none"`: No stacking
    - `"normal"`: Stack values
    - `"percent"`: Stack as percentages

```json
            "thresholdsStyle": {"mode": "off"}
```
- `thresholdsStyle`: Threshold lines visibility
  - `"off"`: Hide threshold lines
  - `"line"`: Show as lines
  - `"area"`: Show as filled areas

```json
          "mappings": [],
```
- `mappings`: Value transformations
- `[]`: No mappings
- **Example**: `1` → `"Running"`, `0` → `"Stopped"`

```json
          "thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": null}]},
```
- `thresholds`: Color thresholds
  - `mode`:
    - `"absolute"`: Fixed values
    - `"percentage"`: Percentage-based
  - `steps`: Threshold levels
    - `color`: `"green"` = Color to use
    - `value`: `null` = Default (all values)

```json
          "unit": "reqps"
```
- `unit`: Value unit/format
- `"reqps"`: Requests per second
- **Other units**: `"bytes"`, `"percent"`, `"ms"` (milliseconds)

```json
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
```
- `gridPos`: Panel position aur size
  - `h`: Height (grid units) - `8`
  - `w`: Width (grid units) - `12` (half of 24 columns)
  - `x`: Horizontal position - `0` (left edge)
  - `y`: Vertical position - `0` (top)

```json
      "id": 1,
```
- `id`: Panel unique ID
- `1`: First panel

```json
      "options": {
        "legend": {
          "calcs": ["mean", "max", "lastNotNull"],
```
- `options`: Panel display options
- `legend`: Legend configuration
  - `calcs`: Calculated values to show
    - `"mean"`: Average value
    - `"max"`: Maximum value
    - `"lastNotNull"`: Latest non-null value

```json
          "displayMode": "table",
```
- `displayMode`: Legend display style
  - `"table"`: Table format
  - `"list"`: List format
  - `"hidden"`: Hide legend

```json
          "placement": "bottom",
```
- `placement`: Legend position
  - `"bottom"`: Below graph
  - `"right"`: Right side
  - `"top"`: Above graph

```json
          "showLegend": true
```
- `showLegend`: Legend visibility
  - `true`: Show
  - `false`: Hide

```json
        "tooltip": {"mode": "multi", "sort": "desc"}
```
- `tooltip`: Hover tooltip settings
  - `mode`:
    - `"multi"`: Multiple series show
    - `"single"`: Single series only
  - `sort`:
    - `"desc"`: Descending order
    - `"asc"`: Ascending order

```json
      "targets": [{
        "datasource": {"type": "loki", "uid": "P8E80F9AEF21F6940"},
```
- `targets`: Data queries ka array
- `datasource`: Query ka data source (same as panel datasource)

```json
        "editorMode": "code",
```
- `editorMode`: Query editor mode
  - `"code"`: Code/text mode
  - `"builder"`: Visual query builder

```json
        "expr": "sum(rate({job=\"nginx-app1\"}[1m]))",
```
**CRITICAL - LogQL Query:**
- `expr`: LogQL query expression

**Query Breakdown:**
```logql
sum(rate({job="nginx-app1"}[1m]))
│   │    │                  │
│   │    │                  └─ Time window (1 minute)
│   │    └──────────────────── Label filter
│   └───────────────────────── Rate function
└───────────────────────────── Sum aggregation
```

**Step-by-step:**
1. `{job="nginx-app1"}` - NGINX app1 logs select karo
2. `[1m]` - Last 1 minute ka data
3. `rate(...)` - Per-second rate calculate karo
   - Formula: `(current_count - previous_count) / time_difference`
   - Example: 60 requests in 1 min = 1 req/sec
4. `sum(...)` - Total sum (saare streams combine)

```json
        "legendFormat": "Request Rate",
```
- `legendFormat`: Legend mein label text
- `"Request Rate"`: Display name
- **Variables**: `{{label_name}}` use kar sakte hain

```json
        "queryType": "range",
```
- `queryType`: Query type
  - `"range"`: Time range query (graphs ke liye)
  - `"instant"`: Instant query (single value)

```json
        "refId": "A"
```
- `refId`: Query reference ID
- `"A"`: First query (multiple queries: A, B, C...)

```json
      "title": "App1 - Request Rate (per second)",
```
- `title`: Panel title (top mein display)

```json
      "type": "timeseries"
```
- `type`: Panel visualization type
  - `"timeseries"`: Time series graph
  - `"gauge"`: Gauge meter
  - `"stat"`: Single stat
  - `"table"`: Data table
  - `"logs"`: Log viewer

---

### Panel 5: Top 20 Endpoints (Table)

**Most Complex Query - Word by Word:**

```json
"expr": "topk(20, sum by (path) (count_over_time({job=\"nginx-app1\"} | regexp `\"[A-Z]+ (?P<path>/[^ ]*) HTTP` [15m])))"
```

**Complete Breakdown:**

```logql
topk(20, sum by (path) (count_over_time({job="nginx-app1"} | regexp `"[A-Z]+ (?P<path>/[^ ]*) HTTP` [15m])))
│      │                │               │                    │                                │
│      │                │               │                    │                                └─ Time: 15 min
│      │                │               │                    └──────────────────────────────── Regex parse
│      │                │               └───────────────────────────────────────────────────── Label filter
│      │                └────────────────────────────────────────────────────────────────────── Count logs
│      └──────────────────────────────────────────────────────────────────────────────────────── Group by path
└─────────────────────────────────────────────────────────────────────────────────────────────── Top 20
```

**Step 1: Label Filter**
```logql
{job="nginx-app1"}
```
- Select: NGINX app1 access logs

**Step 2: Regex Parsing**
```logql
| regexp `"[A-Z]+ (?P<path>/[^ ]*) HTTP`
```
- `|`: Pipe operator (log line processing)
- `regexp`: Regular expression parser
- Backticks: Regex pattern

**Regex Pattern Explanation:**
```regex
"[A-Z]+ (?P<path>/[^ ]*) HTTP"
 │      │        │       │
 │      │        │       └─ Literal: " HTTP"
 │      │        └───────── Capture: /[^ ]* (slash + non-space chars)
 │      └────────────────── Named group: (?P<path>...)
 └───────────────────────── HTTP method: [A-Z]+ (GET, POST, etc.)
```

**Input Line:**
```
172.25.25.140 - - [09/Oct/2025:11:22:19 +0500] "GET /app1/api/app-info HTTP/1.1" 200 1269
```

**Regex Match:**
```
"GET /app1/api/app-info HTTP/1.1"
     └──────────────────┘
            ↓
     path = "/app1/api/app-info"
```

**Step 3: Count Over Time**
```logql
count_over_time(...[15m])
```
- `count_over_time`: Function jo log lines count karta hai
- `[15m]`: Last 15 minutes ka window
- **Output**: Har matched line = 1, total = count

**Step 4: Group By Path**
```logql
sum by (path) (...)
```
- `sum by (path)`: Same path wale logs ko group karo
- **Example Output**:
  ```
  {path="/app1/"} → 1245
  {path="/app1/api/app-info"} → 892
  {path="/app1/health"} → 189
  ```

**Step 5: Top K**
```logql
topk(20, ...)
```
- `topk(20, ...)`: Top 20 results (descending order)
- **Final Output**: 20 most popular endpoints

**Complete Example:**
```
Input Logs (15 min):
  "GET /app1/ HTTP/1.1"           → 1245 times
  "GET /app1/api/app-info HTTP/1.1" → 892 times
  "GET /app1/health HTTP/1.1"       → 189 times
  ...

After Regex Parse:
  path="/app1/"         → 1245
  path="/app1/api/app-info" → 892
  path="/app1/health"   → 189

After topk(20):
  Top 20 endpoints with hit counts
```

---

### Panel Transformations

```json
      "transformations": [
        {
          "id": "organize",
```
- `transformations`: Data transformation steps
- `id`: Transformation type
  - `"organize"`: Column organization
  - `"merge"`: Merge series
  - `"filterByValue"`: Filter rows

```json
          "options": {
            "excludeByName": {"Time": true},
```
- `options`: Transformation settings
- `excludeByName`: Columns to hide
  - `"Time": true`: Time column hide karo

```json
            "renameByName": {"Value": "Total Hits", "path": "Endpoint"}
```
- `renameByName`: Column names change karo
  - `"Value"` → `"Total Hits"`
  - `"path"` → `"Endpoint"`

---

### Panel Color Overrides

```json
      "fieldConfig": {
        "overrides": [
          {
            "matcher": {"id": "byName", "options": "Total Hits"},
```
- `overrides`: Specific field customizations
- `matcher`: Kis field ko target karna hai
  - `id: "byName"`: Column name se match
  - `options: "Total Hits"`: Column name

```json
            "properties": [
              {"id": "custom.displayMode", "value": "gradient-gauge"},
```
- `properties`: Field properties
- `custom.displayMode`: Display style
  - `"gradient-gauge"`: Gradient bar with value

```json
              {"id": "color", "value": {"mode": "continuous-GrYlRd"}}
```
- `color`: Color configuration
  - `mode: "continuous-GrYlRd"`: Green → Yellow → Red gradient
  - **Low values**: Green
  - **Medium values**: Yellow
  - **High values**: Red

---

### Dashboard Global Settings

```json
  "refresh": "1s",
```
- `refresh`: Auto-refresh interval
- `"1s"`: Har 1 second mein data refresh
- **Options**: `"5s"`, `"10s"`, `"1m"`, `"5m"`, `""` (off)

```json
  "schemaVersion": 38,
```
- `schemaVersion`: Dashboard JSON schema version
- `38`: Current Grafana schema version

```json
  "style": "dark",
```
- `style`: Dashboard theme
  - `"dark"`: Dark theme
  - `"light"`: Light theme

```json
  "tags": ["app1", "loki", "logs", "nginx", "endpoints"],
```
- `tags`: Dashboard tags (search/categorization ke liye)
- Array of strings

```json
  "time": {"from": "now-15m", "to": "now"},
```
- `time`: Default time range
  - `from: "now-15m"`: 15 minutes ago se
  - `to: "now"`: Current time tak
  - **Options**: `"now-1h"`, `"now-24h"`, `"now-7d"`

```json
  "timezone": "",
```
- `timezone`: Time zone setting
- `""`: Browser default
- **Options**: `"UTC"`, `"Asia/Karachi"`, `"America/New_York"`

```json
  "title": "App1 - Enhanced Loki Dashboard",
```
- `title`: Dashboard name (top bar mein)

```json
  "uid": "app1-loki-enhanced",
```
- `uid`: Unique identifier
- Dashboard URL: `/d/app1-loki-enhanced/`

```json
  "version": 0
```
- `version`: Dashboard version number
- Save karne par increment hota hai

---

## Summary - Complete Pipeline

### 1. Application Layer
```
FastAPI (main.py)
  ↓ Generates
Logs (app1.log + app1-json.log)
```

### 2. Web Server Layer
```
NGINX (nginx.conf + app1-routing.conf)
  ↓ Generates
Access Logs (app1_access.log)
```

### 3. Collection Layer
```
Promtail (promtail-config.yml)
  ↓ Reads files using __path__
  ↓ Adds labels (job, app, log_type)
  ↓ Parses JSON (pipeline_stages)
  ↓ Sends to Loki
```

### 4. Storage Layer
```
Loki (loki-config.yml)
  ↓ Stores in /loki/chunks
  ↓ Indexes in /loki/index_*
  ↓ Retains for 168h (7 days)
```

### 5. Visualization Layer
```
Grafana (datasources.yml + dashboards.yml)
  ↓ Queries Loki (LogQL)
  ↓ Displays in Panels
  ↓ Dashboard (app1-loki-enhanced.json)
```

### Key Terminology

**LogQL Functions:**
- `rate()`: Per-second rate
- `count_over_time()`: Count log lines
- `sum()`: Aggregate values
- `topk()`: Top K results
- `regexp`: Extract fields with regex

**Labels:**
- `job`: Primary grouping
- `app`: Application identifier
- `log_type`: Log category
- `path`: Extracted endpoint path
- `status`: HTTP status code

**Panel Types:**
- `timeseries`: Line/bar graphs
- `gauge`: Meter/speedometer
- `stat`: Single numeric value
- `table`: Tabular data
- `piechart`: Pie/donut chart
- `logs`: Log viewer

**Units:**
- `reqps`: Requests per second
- `short`: Generic number
- `bytes`: Data size
- `ms`: Milliseconds
- `percent`: Percentage

---

**Document Created:** October 9, 2025  
**Purpose:** Complete word-by-word explanation of entire monitoring pipeline  
**Total Coverage:** 7 configuration files + 1 dashboard JSON = Full system documentation
