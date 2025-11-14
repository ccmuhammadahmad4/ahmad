# Complete Loki + Grafana Logging Setup Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Configuration Details](#configuration-details)
5. [Dashboard Features](#dashboard-features)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance](#maintenance)

---

## Architecture Overview

### System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    User Traffic (Port 80)                    │
│                  http://172.25.25.140/app1-5/                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    NGINX     │
                    │   Port 80    │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌────────┐         ┌────────┐        ┌────────┐
   │ App1   │         │ App2   │   ...  │ App5   │
   │ :5001  │         │ :5002  │        │ :5005  │
   └───┬────┘         └───┬────┘        └───┬────┘
       │                  │                  │
       │  Generates Logs  │                  │
       ▼                  ▼                  ▼
   ┌────────────────────────────────────────────┐
   │        Application Log Files               │
   │  app1.log, app1-json.log                  │
   │  app2.log, app2-json.log                  │
   │         ... (per app)                      │
   └────────────────┬───────────────────────────┘
                    │
                    ▼
            ┌───────────────┐
            │   NGINX Logs  │
            │ (Separate)    │
            │ app1_access   │
            │ app2_access   │
            │    ...        │
            └───────┬───────┘
                    │
                    │ Monitored by
                    ▼
            ┌───────────────┐
            │   Promtail    │
            │  (Collector)  │
            │   Port 9080   │
            └───────┬───────┘
                    │
                    │ Sends logs to
                    ▼
            ┌───────────────┐
            │     Loki      │
            │ (Log Storage) │
            │   Port 3100   │
            └───────┬───────┘
                    │
                    │ Queried by
                    ▼
            ┌───────────────┐
            │   Grafana     │
            │ (Dashboards)  │
            │   Port 3000   │
            └───────────────┘
```

### Data Flow
1. **User Request** → NGINX (Port 80)
2. **NGINX** → Routes to App1-5 (Ports 5001-5005)
3. **Apps** → Generate logs (text + JSON)
4. **NGINX** → Generates separate access logs per app
5. **Promtail** → Monitors log files (apps + NGINX)
6. **Promtail** → Sends logs to Loki
7. **Loki** → Stores and indexes logs
8. **Grafana** → Queries Loki and displays dashboards

---

## Prerequisites

### Software Requirements
- **Windows 10/11**
- **Docker Desktop** (for Loki, Promtail, Grafana containers)
- **Python 3.8+** with virtual environment
- **NGINX** (Windows version)
- **PowerShell 5.1+**

### Network Requirements
- Port 80: NGINX
- Port 3000: Grafana
- Port 3100: Loki
- Port 9080: Promtail
- Ports 5001-5005: FastAPI Applications

### Directory Structure
```
C:\Users\muhammadahmad4\applications\
├── app1/
│   ├── main.py
│   ├── app1.log
│   └── app1-json.log
├── app2/
│   ├── main.py
│   ├── app2.log
│   └── app2-json.log
├── app3-5/ (similar structure)
├── monitoring/
│   ├── docker-compose.yml
│   ├── loki/
│   │   └── loki-config.yml
│   ├── promtail/
│   │   └── promtail-config.yml
│   └── grafana/
│       ├── provisioning/
│       │   ├── datasources/
│       │   └── dashboards/
│       └── dashboards/
│           ├── app1-loki-enhanced.json
│           ├── app2-loki-enhanced.json
│           └── app3-5-loki-enhanced.json
└── .venv/ (Python virtual environment)

C:\nginx\
├── conf/
│   ├── nginx.conf
│   └── apps/
│       ├── nginx-port80-base.conf
│       ├── app1-routing.conf
│       ├── app2-routing.conf
│       └── app3-5-routing.conf
└── logs/
    ├── app1_access.log
    ├── app1_error.log
    ├── app2_access.log
    └── ... (per app)
```

---

## Step-by-Step Setup

### Phase 1: Application Setup

#### Step 1.1: Create Virtual Environment
```powershell
cd C:\Users\muhammadahmad4\applications
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Step 1.2: Install Dependencies
```powershell
pip install fastapi uvicorn python-json-logger
```

#### Step 1.3: Configure Application Logging
Each FastAPI application (app1-5) has dual logging:

**File: `app1/main.py`** (similar for app2-5)
```python
import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI

# Text Logger
text_handler = logging.FileHandler('app1.log')
text_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

# JSON Logger
json_handler = logging.FileHandler('app1-json.log')
json_handler.setFormatter(jsonlogger.JsonFormatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(text_handler)
logger.addHandler(json_handler)

app = FastAPI()

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to App1"}

@app.get("/api/app-info")
async def app_info():
    logger.info("App info endpoint accessed")
    return {"app": "app1", "port": 5001, "theme": "blue"}
```

**Why Dual Logging?**
- **Text logs**: Human-readable for debugging
- **JSON logs**: Structured data for parsing and analysis

#### Step 1.4: Start Applications
```powershell
# Terminal 1 - App1
cd C:\Users\muhammadahmad4\applications
.\.venv\Scripts\Activate.ps1
cd app1
python main.py

# Terminal 2 - App2
cd C:\Users\muhammadahmad4\applications
.\.venv\Scripts\Activate.ps1
cd app2
python main.py

# Repeat for app3, app4, app5
```

**Verification:**
```powershell
# Check if apps are running
for ($i=1; $i -le 5; $i++) {
    try {
        Invoke-WebRequest -Uri "http://localhost:500$i" -UseBasicParsing
        Write-Host "✓ App$i is running"
    } catch {
        Write-Host "✗ App$i not running"
    }
}
```

---

### Phase 2: NGINX Configuration

#### Step 2.1: NGINX Base Configuration
**File: `C:\nginx\conf\nginx.conf`**
```nginx
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    
    sendfile        on;
    keepalive_timeout  65;
    
    # Include port 80 configuration
    include apps/nginx-port80-base.conf;
}
```

#### Step 2.2: Port 80 Base Configuration
**File: `C:\nginx\conf\apps\nginx-port80-base.conf`**
```nginx
server {
    listen 80;
    server_name localhost 172.25.25.140 _;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # Include individual app configurations
    include apps/app1-routing.conf;
    include apps/app2-routing.conf;
    include apps/app3-routing.conf;
    include apps/app4-routing.conf;
    include apps/app5-routing.conf;
    
    # Health check
    location /health {
        access_log off;
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
```

#### Step 2.3: Per-App Routing Configuration
**File: `C:\nginx\conf\apps\app1-routing.conf`**
```nginx
# APP1 ROUTING CONFIGURATION
# Blue theme FastAPI application
# Port: 5001

# Static files for app1
location ~ ^/app1/static/(.*)$ {
    proxy_pass http://127.0.0.1:5001/static/$1;
    proxy_set_header Host $host;
}

# App 1 main routing - Blue theme
location /app1/ {
    # IMPORTANT: Logs MUST be first in location block
    access_log C:/nginx/logs/app1_access.log combined;
    error_log C:/nginx/logs/app1_error.log warn;
    
    rewrite ^/app1/(.*)$ /$1 break;
    proxy_pass http://127.0.0.1:5001;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
```

**Repeat for app2-5** with respective ports and log files.

**Critical Configuration Points:**
1. `access_log` and `error_log` MUST be at the TOP of location block
2. Each app has separate log files (app1_access.log, app2_access.log, etc.)
3. Use forward slashes (/) even on Windows: `C:/nginx/logs/`
4. `combined` log format provides detailed information

#### Step 2.4: Start NGINX
```powershell
cd C:\nginx
.\nginx.exe
```

**Verify NGINX:**
```powershell
# Test configuration
cd C:\nginx
.\nginx.exe -t

# Check if NGINX is running
Get-Process nginx

# Test access
Invoke-WebRequest http://172.25.25.140/app1/
```

**Check Log Files:**
```powershell
# Should show separate files per app
Get-ChildItem C:\nginx\logs\app*_access.log | Select-Object Name, Length, LastWriteTime
```

---

### Phase 3: Docker Monitoring Stack

#### Step 3.1: Docker Compose Configuration
**File: `C:\Users\muhammadahmad4\applications\monitoring\docker-compose.yml`**
```yaml
version: '3.8'

services:
  # Grafana Loki - Log Aggregation System
  loki:
    image: grafana/loki:latest
    container_name: loki-apps
    restart: unless-stopped
    ports:
      - "3100:3100"
    volumes:
      - ./loki/loki-config.yml:/etc/loki/local-config.yaml:ro
      - loki-data:/loki
    command: -config.file=/etc/loki/local-config.yaml
    networks:
      - monitoring-network

  # Promtail - Log Shipper (collects logs and sends to Loki)
  promtail:
    image: grafana/promtail:latest
    container_name: promtail-apps
    restart: unless-stopped
    volumes:
      - ./promtail/promtail-config.yml:/etc/promtail/config.yml:ro
      - /var/log:/var/log:ro
      - C:/Users/muhammadahmad4/applications:/apps:ro
      - C:/nginx/logs:/nginx-logs:ro
    command: -config.file=/etc/promtail/config.yml
    depends_on:
      - loki
    extra_hosts:
      - "host.docker.internal:host-gateway"
    networks:
      - monitoring-network

  # Grafana - Visualization & Dashboards
  grafana:
    image: grafana/grafana:latest
    container_name: grafana-apps
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
      - GF_AUTH_DISABLE_LOGIN_FORM=true
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_SERVER_ROOT_URL=http://localhost:3000
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    depends_on:
      - loki
    networks:
      - monitoring-network

networks:
  monitoring-network:
    driver: bridge

volumes:
  loki-data:
  grafana-data:
```

**Key Volume Mounts:**
- `C:/Users/muhammadahmad4/applications:/apps:ro` - Application logs
- `C:/nginx/logs:/nginx-logs:ro` - NGINX logs
- `:ro` means read-only (security best practice)

#### Step 3.2: Loki Configuration
**File: `C:\Users\muhammadahmad4\applications\monitoring\loki\loki-config.yml`**
```yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

ruler:
  alertmanager_url: http://localhost:9093

# Limits configuration
limits_config:
  retention_period: 168h  # 7 days
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20
```

**Configuration Explanation:**
- `auth_enabled: false` - No authentication (local setup)
- `retention_period: 168h` - Logs retained for 7 days
- `ingestion_rate_mb: 10` - Max 10MB/sec ingestion rate
- `filesystem` storage - Stores logs on disk (suitable for single-node)

#### Step 3.3: Promtail Configuration
**File: `C:\Users\muhammadahmad4\applications\monitoring\promtail\promtail-config.yml`**
```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # Application Logs - App1
  - job_name: app1
    static_configs:
      - targets:
          - localhost
        labels:
          job: app1
          app: application1
          __path__: /apps/app1/*.log

  # Application Logs - App2
  - job_name: app2
    static_configs:
      - targets:
          - localhost
        labels:
          job: app2
          app: application2
          __path__: /apps/app2/*.log

  # Repeat for app3, app4, app5...

  # NGINX App1 Access Logs
  - job_name: nginx-app1-access
    static_configs:
      - targets:
          - localhost
        labels:
          job: nginx-app1
          app: app1
          log_type: access
          __path__: /nginx-logs/app1_access.log

  # NGINX App1 Error Logs
  - job_name: nginx-app1-error
    static_configs:
      - targets:
          - localhost
        labels:
          job: nginx-app1
          app: app1
          log_type: error
          __path__: /nginx-logs/app1_error.log

  # Repeat NGINX configs for app2-5...

  # JSON Logs with Parsing
  - job_name: uvicorn
    static_configs:
      - targets:
          - localhost
        labels:
          job: uvicorn
          __path__: /apps/app*/*-json.log
    pipeline_stages:
      - json:
          expressions:
            timestamp: asctime
            level: levelname
            message: message
            app: name
      - labels:
          app:
      - timestamp:
          source: timestamp
          format: RFC3339
```

**Promtail Configuration Breakdown:**
1. **positions.yaml** - Tracks file read positions (avoids re-reading)
2. **clients** - Points to Loki server
3. **scrape_configs** - Defines what logs to collect
4. **labels** - Metadata for querying (job, app, log_type)
5. **__path__** - Glob pattern for log files
6. **pipeline_stages** - Parses JSON logs

#### Step 3.4: Start Docker Stack
```powershell
cd C:\Users\muhammadahmad4\applications\monitoring
docker-compose up -d
```

**Verify Containers:**
```powershell
docker ps
# Should show: loki-apps, promtail-apps, grafana-apps

# Check logs
docker logs loki-apps --tail 20
docker logs promtail-apps --tail 20
docker logs grafana-apps --tail 20
```

**Test Loki API:**
```powershell
# Get all job labels
Invoke-WebRequest -Uri "http://localhost:3100/loki/api/v1/label/job/values" -UseBasicParsing

# Query logs
$query = '{job="nginx-app1"}'
Invoke-WebRequest -Uri "http://localhost:3100/loki/api/v1/query_range?query=$query&limit=10" -UseBasicParsing
```

---

### Phase 4: Grafana Dashboard Setup

#### Step 4.1: Grafana Provisioning
**File: `C:\Users\muhammadahmad4\applications\monitoring\grafana\provisioning\datasources\datasources.yml`**
```yaml
apiVersion: 1

datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    uid: P8E80F9AEF21F6940
    isDefault: true
    editable: true
```

**File: `C:\Users\muhammadahmad4\applications\monitoring\grafana\provisioning\dashboards\dashboards.yml`**
```yaml
apiVersion: 1

providers:
  - name: 'Default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: false
```

#### Step 4.2: Enhanced Dashboard Structure
Each dashboard (`app1-loki-enhanced.json` through `app5-loki-enhanced.json`) contains:

**Panel 1: Request Rate Timeline**
- Query: `sum(rate({job="nginx-app1"}[1m]))`
- Type: Time Series Graph
- Shows: Requests per second over time
- Features: Mean, Max, Current values

**Panel 2: Total Requests Gauge**
- Query: `sum(count_over_time({job="nginx-app1"}[5m]))`
- Type: Gauge
- Shows: Total requests in last 5 minutes
- Thresholds: Green (0-100), Yellow (100-500), Orange (500-1000), Red (1000+)

**Panel 3: Quick Stats - 1 Min**
- Query: `sum(count_over_time({job="nginx-app1"}[1m]))`
- Type: Stat
- Shows: Requests in last 1 minute
- Background color based on value

**Panel 4: App Logs Count**
- Query: `sum(count_over_time({job="app1"}[1m]))`
- Type: Stat
- Shows: Application log entries in last minute

**Panel 5: Top 20 Endpoints Table**
- Query: `topk(20, sum by (path) (count_over_time({job="nginx-app1"} | regexp "\"[A-Z]+ (?P<path>/[^ ]*) HTTP" [15m])))`
- Type: Table
- Shows: Endpoint path and hit count
- Features: 
  - Color-coded hit counts (gradient gauge)
  - Sorted by popularity
  - Auto-width columns

**Panel 6: Top 10 Endpoints Pie Chart**
- Query: `topk(10, sum by (path) (count_over_time({job="nginx-app1"} | regexp "\"[A-Z]+ (?P<path>/[^ ]*) HTTP" [5m])))`
- Type: Donut Chart
- Shows: Percentage distribution of top endpoints
- Features:
  - Legend with values and percentages
  - Color-coded sections

**Panel 7: HTTP Status Codes**
- Query: `sum by (status) (count_over_time({job="nginx-app1"} | regexp "HTTP/[0-9.]+ (?P<status>[0-9]{3})" [1m]))`
- Type: Bar Chart (Stacked)
- Shows: 2xx, 3xx, 4xx, 5xx codes over time
- Color coding:
  - 2xx: Green (Success)
  - 3xx: Blue (Redirect)
  - 4xx: Yellow (Client Error)
  - 5xx: Red (Server Error)

**Panel 8: Real-time NGINX Logs**
- Query: `{job="nginx-app1"}`
- Type: Logs Panel
- Shows: Live log streaming
- Features:
  - Timestamp
  - Full log message
  - Descending order (newest first)

**Panel 9: Application Logs**
- Query: `{job="app1"}`
- Type: Logs Panel
- Shows: Application-level logs

**Panel 10: Application Log Rate**
- Query: `sum(count_over_time({job="app1"}[1m]))`
- Type: Time Series
- Shows: Application log volume over time

**Dashboard Settings:**
- Refresh: 1 second (real-time)
- Time Range: Last 15 minutes
- Timezone: Browser default
- Live Now: Enabled

#### Step 4.3: Import Dashboards Programmatically
```powershell
cd C:\Users\muhammadahmad4\applications\monitoring\grafana\dashboards

for ($i=1; $i -le 5; $i++) {
    $dashboard = Get-Content "app${i}-loki-enhanced.json" -Raw | ConvertFrom-Json
    $body = @{
        dashboard = $dashboard
        overwrite = $true
    } | ConvertTo-Json -Depth 100
    
    Invoke-RestMethod -Uri "http://localhost:3000/api/dashboards/db" `
                      -Method Post `
                      -Body $body `
                      -ContentType "application/json"
    
    Write-Host "✓ Imported App${i} Dashboard"
}
```

---

## Configuration Details

### Log Parsing Explained

#### NGINX Log Format (Combined)
```
172.25.25.140 - - [09/Oct/2025:11:22:19 +0500] "GET /app1/ HTTP/1.1" 200 1269 "-" "Mozilla/5.0..."
```

**Fields:**
- `172.25.25.140` - Client IP
- `-` - Remote user (not used)
- `-` - Auth user (not used)
- `[09/Oct/2025:11:22:19 +0500]` - Timestamp
- `"GET /app1/ HTTP/1.1"` - HTTP method, path, protocol
- `200` - HTTP status code
- `1269` - Response size (bytes)
- `"-"` - Referer
- `"Mozilla/5.0..."` - User agent

#### LogQL Queries Breakdown

**Basic Query:**
```
{job="nginx-app1"}
```
- Selects all logs with label `job="nginx-app1"`

**Rate Query:**
```
sum(rate({job="nginx-app1"}[1m]))
```
- `rate()` - Calculate per-second rate
- `[1m]` - Over 1 minute window
- `sum()` - Total across all streams

**Count Query:**
```
sum(count_over_time({job="nginx-app1"}[5m]))
```
- `count_over_time()` - Count log lines
- `[5m]` - In last 5 minutes
- `sum()` - Total count

**Regex Extraction:**
```
{job="nginx-app1"} | regexp `"[A-Z]+ (?P<path>/[^ ]*) HTTP"`
```
- `regexp` - Apply regular expression
- `(?P<path>...)` - Named capture group
- Extracts URL path from log line

**Aggregation by Label:**
```
sum by (path) (count_over_time({job="nginx-app1"} | regexp `...` [15m]))
```
- `sum by (path)` - Group by extracted path
- Counts hits per unique endpoint

**Top K:**
```
topk(10, sum by (path) (...))
```
- `topk(10, ...)` - Get top 10 results
- Sorted by value descending

### Why Promtail Restart Was Needed

**Issue:**
When NGINX log files were created AFTER Promtail started, Promtail had already scanned the log directory and recorded file positions. The new files weren't being monitored.

**Solution:**
```powershell
docker-compose restart promtail
```

**What Happens:**
1. Promtail stops
2. Position file (`/tmp/positions.yaml`) remains
3. Promtail restarts
4. Rescans log directories
5. Discovers new files (app1-5_access.log)
6. Starts tailing from current position
7. New logs are sent to Loki

**Alternative Solution:**
Delete position file before restart:
```powershell
docker exec promtail-apps rm /tmp/positions.yaml
docker-compose restart promtail
```

This forces Promtail to re-scan all files from the beginning.

---

## Dashboard Features

### Interactive Elements

**Time Range Selector:**
- Quick ranges: 5m, 15m, 1h, 6h, 24h
- Custom range picker
- Refresh button

**Panel Interactions:**
- Click legend to toggle series
- Hover for detailed tooltips
- Zoom in on time series (drag selection)
- Click on table rows to filter

**Log Panel Features:**
- Search/filter logs
- Click to expand full log entry
- Copy log content
- View parsed fields (for JSON logs)

### Query Examples

**Find errors in last hour:**
```
{job="app1"} |= "ERROR" 
```

**Count 404 errors:**
```
sum(count_over_time({job="nginx-app1"} |= "404" [1h]))
```

**Find slow responses:**
```
{job="nginx-app1"} | regexp `\d{3,} \d+ms`
```

**Filter by IP:**
```
{job="nginx-app1"} |= "172.25.25.140"
```

**Combine filters:**
```
{job="nginx-app1"} |= "POST" |= "/api/" != "200"
```

---

## Troubleshooting

### Common Issues

#### 1. Dashboards Not Showing Data

**Symptom:** Empty graphs, "No data" message

**Diagnosis:**
```powershell
# Check if Loki has data
curl http://localhost:3100/loki/api/v1/label/job/values

# Check Promtail is running
docker logs promtail-apps --tail 50

# Verify log files exist
Get-ChildItem C:\nginx\logs\app*_access.log
```

**Solutions:**
- Restart Promtail: `docker-compose restart promtail`
- Generate traffic to create logs
- Check Promtail config for correct paths
- Verify Docker volume mounts

#### 2. NGINX Logs Not Separating

**Symptom:** All apps logging to same file

**Diagnosis:**
```powershell
# Check NGINX config
cd C:\nginx
.\nginx.exe -T | Select-String "access_log"
```

**Solution:**
- Ensure `access_log` directive is FIRST in location block
- Use forward slashes: `C:/nginx/logs/` not `C:\nginx\logs\`
- Reload NGINX: `.\nginx.exe -s reload`

#### 3. Promtail Not Collecting Logs

**Symptom:** Loki shows some jobs but not all

**Diagnosis:**
```powershell
# Check Promtail logs for errors
docker logs promtail-apps | Select-String "error"

# Verify file permissions
docker exec promtail-apps ls -la /nginx-logs/
docker exec promtail-apps ls -la /apps/app1/
```

**Solution:**
- Ensure files are readable (`:ro` in docker-compose)
- Check glob patterns in promtail-config.yml
- Restart Promtail

#### 4. Container Won't Start

**Diagnosis:**
```powershell
docker ps -a
docker logs loki-apps
docker logs promtail-apps
docker logs grafana-apps
```

**Common Causes:**
- Port already in use
- Invalid YAML syntax
- Volume mount path doesn't exist

**Solutions:**
- Stop conflicting services
- Validate YAML: `docker-compose config`
- Create missing directories

#### 5. Grafana Dashboard Import Fails

**Symptom:** "Dashboard title cannot be empty"

**Cause:** UTF-8 BOM encoding issue

**Solution:**
```powershell
cd C:\Users\muhammadahmad4\applications\monitoring\grafana\dashboards

for ($i=1; $i -le 5; $i++) {
    $content = [System.IO.File]::ReadAllText("app${i}-loki-enhanced.json")
    [System.IO.File]::WriteAllText("app${i}-loki-enhanced.json", 
                                    $content, 
                                    [System.Text.UTF8Encoding]::new($false))
}
```

---

## Maintenance

### Daily Operations

**Check System Health:**
```powershell
# Check all containers
docker ps

# Check disk usage
docker system df

# View recent logs
docker logs grafana-apps --since 1h
docker logs loki-apps --since 1h
docker logs promtail-apps --since 1h
```

**Generate Test Traffic:**
```powershell
for ($i=1; $i -le 5; $i++) {
    Invoke-WebRequest "http://172.25.25.140/app$i/" -UseBasicParsing
    Invoke-WebRequest "http://172.25.25.140/app$i/api/app-info" -UseBasicParsing
}
```

### Weekly Maintenance

**Clean Old Logs:**
```powershell
# NGINX logs older than 7 days
Get-ChildItem C:\nginx\logs\*.log | 
    Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | 
    Remove-Item

# Application logs
Get-ChildItem C:\Users\muhammadahmad4\applications\app*\*.log | 
    Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | 
    Remove-Item
```

**Docker Cleanup:**
```powershell
# Remove unused volumes
docker volume prune -f

# Remove unused images
docker image prune -f
```

### Backup Procedures

**Backup Grafana Dashboards:**
```powershell
$date = Get-Date -Format "yyyy-MM-dd"
$backupDir = "C:\Backups\grafana\$date"
New-Item -ItemType Directory -Path $backupDir -Force

Copy-Item "C:\Users\muhammadahmad4\applications\monitoring\grafana\dashboards\*" `
          -Destination $backupDir `
          -Recurse
```

**Backup Docker Volumes:**
```powershell
docker run --rm -v loki-data:/source -v C:/Backups/loki:/backup `
    alpine tar czf /backup/loki-backup-$(Get-Date -Format 'yyyy-MM-dd').tar.gz -C /source .

docker run --rm -v grafana-data:/source -v C:/Backups/grafana:/backup `
    alpine tar czf /backup/grafana-backup-$(Get-Date -Format 'yyyy-MM-dd').tar.gz -C /source .
```

### Performance Optimization

**Loki Query Performance:**
- Use shorter time ranges when possible
- Add label filters before regex
- Use `|=` (contains) before complex parsing
- Limit result count with `limit N`

**Promtail Optimization:**
- Use specific file paths (avoid wildcards when possible)
- Configure appropriate `sync_period`
- Set reasonable `batch_wait` and `batch_size`

**Grafana Performance:**
- Increase refresh interval for less critical dashboards
- Use query result caching
- Limit number of panels per dashboard (max 10-12)

### Scaling Considerations

**When to Scale:**
- Log ingestion > 10 MB/s
- Query latency > 2 seconds
- Storage > 100 GB

**Horizontal Scaling:**
- Add more Loki instances
- Use distributed architecture (read/write separation)
- Configure query frontend for caching

**Vertical Scaling:**
- Increase Docker container memory limits
- Add more CPU cores
- Use SSD for faster disk I/O

---

## Advanced Features

### Custom Alerts (Future Enhancement)

Example alert rule:
```yaml
groups:
  - name: nginx_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate({job=~"nginx-app.*"} |= "500" [5m])) > 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High 500 error rate detected
```

### Multi-Tenancy

Configure Loki for multiple tenants:
```yaml
auth_enabled: true

auth:
  type: jwt
  jwt:
    secret: your-secret-key
```

### Log Retention Policies

Configure different retention per tenant:
```yaml
limits_config:
  retention_period: 168h  # Default 7 days
  
table_manager:
  retention_deletes_enabled: true
  retention_period: 336h  # 14 days for old tables
```

---

## Summary

### Complete Tech Stack
- **Applications**: 5 FastAPI apps (Python)
- **Web Server**: NGINX (reverse proxy, load balancer)
- **Log Collector**: Promtail
- **Log Storage**: Loki
- **Visualization**: Grafana
- **Container Platform**: Docker

### Key Metrics
- **Log Sources**: 17 (5 apps × 2 logs + 5 NGINX access + 5 NGINX error + 2 general)
- **Dashboards**: 5 enhanced dashboards
- **Refresh Rate**: 1 second (real-time)
- **Retention**: 7 days
- **Panel Types**: 10 per dashboard (50 total)

### Best Practices Implemented
✅ Separate log files per application
✅ Structured logging (JSON + text)
✅ Centralized log aggregation
✅ Real-time monitoring
✅ Visual dashboards with multiple views
✅ Proper error handling and status code tracking
✅ Security headers in NGINX
✅ Docker container isolation
✅ Volume persistence for data
✅ Configuration as code

---

**Document Version:** 1.0  
**Last Updated:** October 9, 2025  
**Author:** System Documentation  
**Environment:** Windows 10, Docker Desktop, Python 3.x, NGINX 1.28
