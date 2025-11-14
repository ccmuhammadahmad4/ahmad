# 📊 Complete Monitoring & Deployment Guide

## 🎯 Overview

This document provides complete information about the 5 FastAPI applications deployment with NGINX reverse proxy and Prometheus + Grafana monitoring setup.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        LAN Network                               │
│                   (IP: 172.25.25.140)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   NGINX (Port 80) │
                    │  Reverse Proxy    │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │         │           │           │         │
    ┌───▼───┐ ┌──▼───┐ ┌────▼────┐ ┌───▼───┐ ┌───▼───┐
    │ App1  │ │ App2 │ │  App3   │ │ App4  │ │ App5  │
    │:5001  │ │:5002 │ │  :5003  │ │:5004  │ │:5005  │
    └───┬───┘ └──┬───┘ └────┬────┘ └───┬───┘ └───┬───┘
        │        │           │          │         │
        └────────┴───────────┴──────────┴─────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Prometheus       │
                    │   (Port 9090)      │
                    │   Docker Container │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │    Grafana         │
                    │   (Port 3000)      │
                    │   Docker Container │
                    └────────────────────┘
```

---

## 📁 Directory Structure

```
c:\Users\muhammadahmad4\applications\
│
├── app1/
│   ├── main.py                    # FastAPI app with Prometheus metrics
│   ├── static/                    # Static files
│   └── templates/                 # HTML templates
│
├── app2/ ... app5/                # Similar structure for all apps
│
├── monitoring/
│   ├── docker-compose.yml         # Prometheus + Grafana containers
│   ├── prometheus.yml             # Prometheus scrape configuration
│   └── grafana/
│       └── dashboards/
│           ├── app1-dashboard.json
│           ├── app2-dashboard.json
│           ├── app3-dashboard.json
│           ├── app4-dashboard.json
│           └── app5-dashboard.json
│
└── .venv/                         # Python virtual environment
    └── Lib/site-packages/
        └── prometheus_client/      # Metrics library

C:\nginx\
├── nginx.exe                      # NGINX executable
├── conf/
│   ├── nginx.conf                 # Main NGINX config
│   └── apps/
│       ├── nginx-port80-base.conf # Port 80 server block
│       ├── app1-routing.conf      # App1 routing
│       ├── app2-routing.conf      # App2 routing
│       ├── app3-routing.conf      # App3 routing
│       ├── app4-routing.conf      # App4 routing
│       ├── app5-routing.conf      # App5 routing
│       └── proxy-headers.conf     # Common proxy headers
└── logs/                          # NGINX logs
```

---

## 🚀 Components

### 1. **FastAPI Applications (5 Apps)**

**Location:** `c:\Users\muhammadahmad4\applications\app1` through `app5`

**Ports:** 5001, 5002, 5003, 5004, 5005

**Key Features:**
- FastAPI web framework
- Prometheus metrics instrumentation
- Custom metrics tracked:
  - `app{N}_request_count_total` - Total requests with labels (method, endpoint, status)
  - `app{N}_request_latency_seconds` - Request latency histogram
  - `app{N}_active_users` - Unique active users (by IP)
  - `app{N}_endpoint_hits_total` - Total hits per endpoint

**Metrics Endpoint:** `http://localhost:500{N}/metrics`

**Sample Prometheus Metrics:**
```python
# HELP app1_request_count_total App1 Request Count
# TYPE app1_request_count_total counter
app1_request_count_total{endpoint="/metrics",http_status="200",method="GET"} 5243.0

# HELP app1_active_users App1 Active Users
# TYPE app1_active_users gauge
app1_active_users 1.0

# HELP app1_request_latency_seconds App1 Request latency
# TYPE app1_request_latency_seconds histogram
app1_request_latency_seconds_bucket{endpoint="/metrics",le="0.005"} 5000.0
```

---

### 2. **NGINX Reverse Proxy**

**Location:** `C:\nginx`

**Port:** 80

**Configuration Files:**
- `C:\nginx\conf\nginx.conf` - Main configuration
- `C:\nginx\conf\apps\nginx-port80-base.conf` - Server block
- `C:\nginx\conf\apps\app{N}-routing.conf` - Individual app routing

**Routing Configuration:**
```nginx
# app1-routing.conf
location /app1/ {
    proxy_pass http://localhost:5001/;
    include apps/proxy-headers.conf;
}
```

**Access URLs:**
- App1: http://172.25.25.140/app1/
- App2: http://172.25.25.140/app2/
- App3: http://172.25.25.140/app3/
- App4: http://172.25.25.140/app4/
- App5: http://172.25.25.140/app5/

---

### 3. **Prometheus (Metrics Collection)**

**Type:** Docker Container

**Image:** `prom/prometheus:latest`

**Port:** 9090

**Configuration:** `c:\Users\muhammadahmad4\applications\monitoring\prometheus.yml`

**Scrape Configuration:**
```yaml
scrape_configs:
  - job_name: 'app1'
    scrape_interval: 1s
    static_configs:
      - targets: ['host.docker.internal:5001']
        labels:
          app: 'app1'
          app_name: 'Application 1'
  # ... similar for app2-5
```

**Key Settings:**
- Scrape interval: 1 second
- Targets: All 5 apps via `host.docker.internal`
- Storage: Persistent volume `monitoring_prometheus-data`

**Access URLs:**
- Web UI: http://localhost:9090
- Targets: http://localhost:9090/targets
- Graph: http://localhost:9090/graph

**Sample Queries:**
```promql
# Request rate per second
rate(app1_request_count_total[1m])

# Active users
app1_active_users

# 95th percentile latency
histogram_quantile(0.95, rate(app1_request_latency_seconds_bucket[5m]))

# Total endpoint hits
sum(app1_endpoint_hits_total)
```

---

### 4. **Grafana (Visualization)**

**Type:** Docker Container

**Image:** `grafana/grafana:latest`

**Port:** 3000

**Authentication:** Anonymous (No login required)

**Datasource:**
- Name: Prometheus
- Type: prometheus
- URL: http://prometheus:9090
- UID: cf0arwg9nsqgwc

**Dashboard Configuration:**

Each app has a dedicated dashboard with 5 panels:

1. **Request Rate** (Time Series)
   - Query: `rate(app{N}_request_count_total[5m])`
   - Shows: Requests per second over time

2. **Active Users** (Gauge)
   - Query: `app{N}_active_users`
   - Shows: Current number of unique users

3. **Total Endpoint Hits** (Stat Panel)
   - Query: `sum(app{N}_endpoint_hits_total)`
   - Shows: Cumulative total hits

4. **Endpoint Distribution** (Pie Chart)
   - Query: `app{N}_endpoint_hits_total`
   - Shows: Distribution of hits across endpoints

5. **Request Latency p95** (Time Series)
   - Query: `histogram_quantile(0.95, rate(app{N}_request_latency_seconds_bucket[5m]))`
   - Shows: 95th percentile response time

**Dashboard URLs:**
- App1: http://localhost:3000/d/app1-dashboard/app1-dashboard
- App2: http://localhost:3000/d/app2-dashboard/app2-dashboard
- App3: http://localhost:3000/d/app3-dashboard/app3-dashboard
- App4: http://localhost:3000/d/app4-dashboard/app4-dashboard
- App5: http://localhost:3000/d/app5-dashboard/app5-dashboard

**Settings:**
- Auto-refresh: 5 seconds
- Time range: Last 5 minutes (configurable)
- Anonymous access: Enabled (Admin role)

---

## 🔧 Setup & Configuration

### Prerequisites

1. **Python 3.13.7** with virtual environment
2. **Docker Desktop** (for Prometheus & Grafana)
3. **NGINX** installed at `C:\nginx`
4. **Required Python packages:**
   ```
   fastapi
   uvicorn
   prometheus-client==0.23.1
   ```

### Installation Steps

#### 1. Python Environment Setup

```powershell
# Navigate to applications directory
cd c:\Users\muhammadahmad4\applications

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install packages (if needed)
pip install fastapi uvicorn prometheus-client==0.23.1
```

#### 2. Start Applications

```powershell
# Terminal 1 - App1
cd c:\Users\muhammadahmad4\applications\app1
..\..venv\Scripts\python.exe main.py

# Terminal 2 - App2
cd c:\Users\muhammadahmad4\applications\app2
..\..venv\Scripts\python.exe main.py

# Repeat for app3, app4, app5 in separate terminals
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### 3. Start NGINX

```powershell
# Navigate to NGINX directory
cd C:\nginx

# Start NGINX
Start-Process nginx.exe -WindowStyle Hidden

# Verify running
Get-Process nginx
```

#### 4. Start Monitoring Stack

```powershell
# Navigate to monitoring directory
cd c:\Users\muhammadahmad4\applications\monitoring

# Start Docker containers
docker-compose up -d

# Verify containers
docker-compose ps

# Expected output:
# NAME              STATUS
# grafana-apps      Up
# prometheus-apps   Up
```

#### 5. Configure Grafana Datasource

**Method 1: Via API (Automated)**
```powershell
$body = @{
    name="Prometheus"
    type="prometheus"
    access="proxy"
    url="http://prometheus:9090"
    isDefault=$true
} | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri "http://localhost:3000/api/datasources" `
    -ContentType "application/json" -Body $body
```

**Method 2: Via Web UI (Manual)**
1. Open http://localhost:3000
2. Go to Configuration → Data Sources
3. Click "Add data source"
4. Select "Prometheus"
5. Enter URL: `http://prometheus:9090`
6. Click "Save & Test"

#### 6. Import Dashboards

```powershell
# Get datasource UID
$dsInfo = Invoke-RestMethod -Uri "http://localhost:3000/api/datasources"
$dsUid = $dsInfo[0].uid

# Import all dashboards
foreach($app in 1..5) {
    $dashboard = Get-Content "grafana\dashboards\app$app-dashboard.json" -Raw
    $dashboard = $dashboard -replace '"uid":\s*"[^"]*"', "`"uid`": `"$dsUid`""
    $dashObj = $dashboard | ConvertFrom-Json
    $dashObj.id = $null
    $dashObj.uid = "app$app-dashboard"
    $payload = @{dashboard=$dashObj; overwrite=$true} | ConvertTo-Json -Depth 20
    Invoke-RestMethod -Method POST -Uri "http://localhost:3000/api/dashboards/db" `
        -ContentType "application/json" -Body $payload
}
```

---

## 🎮 Operation & Maintenance

### Daily Operations

#### Start All Services

```powershell
# 1. Start Apps (5 terminals)
cd c:\Users\muhammadahmad4\applications
foreach($app in 1..5) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", `
        "cd app$app; ..\.venv\Scripts\python.exe main.py"
}

# 2. Start NGINX
cd C:\nginx
Start-Process nginx.exe -WindowStyle Hidden

# 3. Start Monitoring
cd c:\Users\muhammadahmad4\applications\monitoring
docker-compose up -d
```

#### Stop All Services

```powershell
# Stop Apps (close PowerShell windows or Ctrl+C in each terminal)

# Stop NGINX
cd C:\nginx
.\nginx.exe -s quit

# Stop Monitoring
cd c:\Users\muhammadahmad4\applications\monitoring
docker-compose down
```

#### Restart Services

```powershell
# Restart Apps (stop and start individually)

# Restart NGINX
cd C:\nginx
.\nginx.exe -s reload  # Reload config without downtime

# Restart Monitoring
cd c:\Users\muhammadahmad4\applications\monitoring
docker-compose restart
```

### Health Checks

```powershell
# Check Apps
foreach($port in 5001..5005) {
    $app = $port - 5000
    try {
        $response = Invoke-WebRequest "http://localhost:$port" -UseBasicParsing
        Write-Host "App$app (Port $port): OK - Status $($response.StatusCode)"
    } catch {
        Write-Host "App$app (Port $port): FAILED"
    }
}

# Check NGINX
$nginx = Get-Process nginx -ErrorAction SilentlyContinue
if($nginx) { Write-Host "NGINX: Running" } else { Write-Host "NGINX: Stopped" }

# Check Prometheus
try {
    $prom = Invoke-RestMethod "http://localhost:9090/-/healthy"
    Write-Host "Prometheus: Healthy"
} catch {
    Write-Host "Prometheus: Down"
}

# Check Grafana
try {
    $grafana = Invoke-RestMethod "http://localhost:3000/api/health"
    Write-Host "Grafana: $($grafana.database)"
} catch {
    Write-Host "Grafana: Down"
}
```

### Monitoring Metrics

```powershell
# View current metrics for all apps
foreach($app in 1..5) {
    Write-Host "`nApp$app Metrics:"
    $users = curl "http://localhost:9090/api/v1/query?query=app${app}_active_users" | 
        ConvertFrom-Json
    $requests = curl "http://localhost:9090/api/v1/query?query=app${app}_request_count_total" | 
        ConvertFrom-Json
    
    Write-Host "  Active Users: $($users.data.result[0].value[1])"
    Write-Host "  Total Requests: $($requests.data.result[0].value[1])"
}
```

### Troubleshooting

#### Apps Not Starting

**Check 1: Port already in use**
```powershell
netstat -ano | findstr ":5001"  # Check if port is busy
```

**Check 2: Virtual environment**
```powershell
.\.venv\Scripts\python.exe --version  # Should show Python 3.13.7
```

**Check 3: Dependencies**
```powershell
.\.venv\Scripts\pip list | findstr prometheus
```

#### NGINX Errors

**Check configuration:**
```powershell
cd C:\nginx
.\nginx.exe -t  # Test configuration
```

**View error logs:**
```powershell
Get-Content C:\nginx\logs\error.log -Tail 20
```

**Common issues:**
- Port 80 already in use: Stop IIS or other web server
- Config file BOM encoding: Recreate files with UTF-8 no BOM

#### Prometheus Not Scraping

**Check targets:**
```
http://localhost:9090/targets
```

**Verify app metrics endpoint:**
```powershell
curl http://localhost:5001/metrics
```

**Check Docker network:**
```powershell
docker exec prometheus-apps ping host.docker.internal
```

#### Grafana Dashboards Empty

**Check datasource:**
1. Go to http://localhost:3000/datasources
2. Click Prometheus
3. Scroll down and click "Save & Test"
4. Should show green "Data source is working"

**Check queries:**
1. Open any dashboard
2. Click panel title → Edit
3. Check if query returns data in "Query Inspector"

**Verify datasource UID:**
```powershell
# Get current datasource UID
$ds = Invoke-RestMethod "http://localhost:3000/api/datasources"
Write-Host "Datasource UID: $($ds[0].uid)"

# Dashboard should use this UID in datasource.uid field
```

---

## 📊 Metrics Reference

### App Metrics

Each application exposes the following metrics at `/metrics` endpoint:

| Metric Name | Type | Labels | Description |
|-------------|------|--------|-------------|
| `app{N}_request_count_total` | Counter | method, endpoint, http_status | Total HTTP requests |
| `app{N}_request_latency_seconds` | Histogram | endpoint | Request processing time |
| `app{N}_active_users` | Gauge | - | Current unique users (by IP) |
| `app{N}_endpoint_hits_total` | Counter | endpoint | Total hits per endpoint |

### Python Metrics (Auto-generated)

| Metric Name | Description |
|-------------|-------------|
| `python_gc_objects_collected_total` | Objects collected during GC |
| `python_gc_collections_total` | Number of GC collections |
| `python_info` | Python version information |
| `process_cpu_seconds_total` | Total CPU time |
| `process_resident_memory_bytes` | Resident memory size |

### Example PromQL Queries

```promql
# Request rate (requests per second)
rate(app1_request_count_total[1m])

# Error rate (4xx and 5xx responses)
sum(rate(app1_request_count_total{http_status=~"4..|5.."}[5m]))

# Average response time
rate(app1_request_latency_seconds_sum[5m]) / 
rate(app1_request_latency_seconds_count[5m])

# 95th percentile latency
histogram_quantile(0.95, 
  rate(app1_request_latency_seconds_bucket[5m]))

# Top endpoints by traffic
topk(5, sum by (endpoint) (app1_endpoint_hits_total))

# Total requests across all apps
sum(app1_request_count_total + app2_request_count_total + 
    app3_request_count_total + app4_request_count_total + 
    app5_request_count_total)
```

---

## 🔐 Security Considerations

### Current Setup (Development)

- **Grafana:** Anonymous admin access (no authentication)
- **Prometheus:** No authentication
- **NGINX:** No SSL/TLS
- **Apps:** HTTP only, no authentication

### Production Recommendations

1. **Enable Grafana Authentication:**
   ```yaml
   environment:
     - GF_AUTH_ANONYMOUS_ENABLED=false
     - GF_SECURITY_ADMIN_PASSWORD=<strong-password>
   ```

2. **Add SSL/TLS to NGINX:**
   - Generate certificates
   - Configure HTTPS listener
   - Redirect HTTP to HTTPS

3. **Secure Prometheus:**
   - Add basic authentication
   - Use reverse proxy with auth
   - Restrict network access

4. **Application Security:**
   - Add API authentication
   - Implement rate limiting
   - Use environment variables for secrets

5. **Network Security:**
   - Use firewall rules
   - Restrict Docker container access
   - Use Docker networks for isolation

---

## 🎯 Performance Tuning

### NGINX Optimization

```nginx
# nginx.conf
worker_processes auto;
worker_connections 1024;

http {
    # Enable compression
    gzip on;
    gzip_types text/plain application/json;
    
    # Connection pooling
    upstream app1_backend {
        server localhost:5001 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }
    
    # Caching
    proxy_cache_path /path/to/cache levels=1:2 keys_zone=my_cache:10m;
}
```

### Prometheus Optimization

```yaml
# prometheus.yml
global:
  scrape_interval: 15s  # Reduce from 1s for production
  evaluation_interval: 15s

storage:
  tsdb:
    retention.time: 15d  # Keep data for 15 days
    retention.size: 50GB  # Or limit by size
```

### Grafana Optimization

- Use query caching
- Set appropriate refresh intervals (5s for dev, 30s+ for prod)
- Limit time range for queries
- Use recording rules in Prometheus for complex queries

---

## 📝 Backup & Recovery

### Grafana Dashboards Backup

```powershell
# Export all dashboards
$dashboards = Invoke-RestMethod "http://localhost:3000/api/search"
foreach($dash in $dashboards) {
    $dashboard = Invoke-RestMethod "http://localhost:3000/api/dashboards/uid/$($dash.uid)"
    $dashboard | ConvertTo-Json -Depth 20 | 
        Out-File "backup\$($dash.uid).json"
}
```

### Prometheus Data Backup

```powershell
# Stop Prometheus
docker-compose stop prometheus

# Backup data directory
docker run --rm -v monitoring_prometheus-data:/data -v ${PWD}/backup:/backup `
    alpine tar czf /backup/prometheus-backup.tar.gz /data

# Restart Prometheus
docker-compose start prometheus
```

### Configuration Backup

```powershell
# Create backup directory
New-Item -ItemType Directory -Path "backup\configs" -Force

# Backup NGINX configs
Copy-Item C:\nginx\conf\* backup\configs\nginx\ -Recurse

# Backup monitoring configs
Copy-Item monitoring\* backup\configs\monitoring\ -Recurse

# Backup application code
Copy-Item app*\main.py backup\configs\apps\
```

---

## 🔄 Docker Compose Reference

### Full Configuration

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus-apps
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    extra_hosts:
      - "host.docker.internal:host-gateway"
    networks:
      - monitoring-network

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
    depends_on:
      - prometheus
    networks:
      - monitoring-network

networks:
  monitoring-network:
    driver: bridge

volumes:
  prometheus-data:
    driver: local
  grafana-data:
    driver: local
```

### Common Commands

```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes (clean restart)
docker-compose down -v

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f grafana

# Restart specific service
docker-compose restart prometheus

# Check status
docker-compose ps

# Execute command in container
docker exec -it grafana-apps /bin/bash
```

---

## 📞 Quick Reference

### Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Apps via NGINX** |
| App1 | http://172.25.25.140/app1/ | FastAPI App 1 |
| App2 | http://172.25.25.140/app2/ | FastAPI App 2 |
| App3 | http://172.25.25.140/app3/ | FastAPI App 3 |
| App4 | http://172.25.25.140/app4/ | FastAPI App 4 |
| App5 | http://172.25.25.140/app5/ | FastAPI App 5 |
| **Apps Direct** |
| App1 | http://localhost:5001 | Direct access |
| App2 | http://localhost:5002 | Direct access |
| App3 | http://localhost:5003 | Direct access |
| App4 | http://localhost:5004 | Direct access |
| App5 | http://localhost:5005 | Direct access |
| **Monitoring** |
| Prometheus | http://localhost:9090 | Metrics database |
| Grafana | http://localhost:3000 | Dashboards |
| **Dashboards** |
| App1 Dashboard | http://localhost:3000/d/app1-dashboard/app1-dashboard | |
| App2 Dashboard | http://localhost:3000/d/app2-dashboard/app2-dashboard | |
| App3 Dashboard | http://localhost:3000/d/app3-dashboard/app3-dashboard | |
| App4 Dashboard | http://localhost:3000/d/app4-dashboard/app4-dashboard | |
| App5 Dashboard | http://localhost:3000/d/app5-dashboard/app5-dashboard | |

### Port Mapping

| Port | Service | Protocol |
|------|---------|----------|
| 80 | NGINX | HTTP |
| 5001 | App1 | HTTP |
| 5002 | App2 | HTTP |
| 5003 | App3 | HTTP |
| 5004 | App4 | HTTP |
| 5005 | App5 | HTTP |
| 9090 | Prometheus | HTTP |
| 3000 | Grafana | HTTP |

### File Locations

| Component | Path |
|-----------|------|
| Python Apps | `c:\Users\muhammadahmad4\applications\app{1-5}\` |
| Virtual Env | `c:\Users\muhammadahmad4\applications\.venv\` |
| NGINX | `C:\nginx\` |
| NGINX Config | `C:\nginx\conf\nginx.conf` |
| App Routing | `C:\nginx\conf\apps\app{1-5}-routing.conf` |
| Monitoring | `c:\Users\muhammadahmad4\applications\monitoring\` |
| Dashboards | `c:\Users\muhammadahmad4\applications\monitoring\grafana\dashboards\` |

---

## 📚 Additional Resources

### Documentation Links

- **FastAPI:** https://fastapi.tiangolo.com/
- **Prometheus:** https://prometheus.io/docs/
- **Grafana:** https://grafana.com/docs/
- **NGINX:** https://nginx.org/en/docs/
- **Prometheus Client (Python):** https://github.com/prometheus/client_python

### Useful Commands Cheat Sheet

```powershell
# === Python Environment ===
# Activate venv
.\.venv\Scripts\Activate.ps1

# Install package
pip install <package-name>

# List packages
pip list

# === NGINX ===
# Test config
nginx -t

# Reload config
nginx -s reload

# Stop
nginx -s quit

# View processes
Get-Process nginx

# === Docker ===
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Restart service
docker-compose restart <service>

# === Prometheus ===
# Query API
curl "http://localhost:9090/api/v1/query?query=<promql>"

# Check targets
curl http://localhost:9090/api/v1/targets

# === Grafana ===
# List datasources
curl http://localhost:3000/api/datasources

# Add datasource
Invoke-RestMethod -Method POST -Uri "http://localhost:3000/api/datasources" `
    -ContentType "application/json" -Body <json>

# Import dashboard
Invoke-RestMethod -Method POST -Uri "http://localhost:3000/api/dashboards/db" `
    -ContentType "application/json" -Body <json>
```

---

## ✅ Success Criteria

Your monitoring setup is working correctly if:

1. ✅ All 5 apps are accessible via NGINX at http://172.25.25.140/appX/
2. ✅ Each app exposes metrics at http://localhost:500X/metrics
3. ✅ Prometheus shows all 5 targets as "UP" at http://localhost:9090/targets
4. ✅ Grafana is accessible at http://localhost:3000 (no login required)
5. ✅ All 5 dashboards show data with graphs updating in real-time
6. ✅ Metrics visible: Request Rate, Active Users, Endpoint Hits, Latency

---

## 🎓 Learning Points

### What Was Implemented

1. **Reverse Proxy Pattern:** NGINX routing requests to backend FastAPI apps
2. **Metrics Instrumentation:** Custom Prometheus metrics in Python applications
3. **Pull-based Monitoring:** Prometheus scraping metrics from apps
4. **Time-Series Visualization:** Grafana dashboards with multiple panel types
5. **Containerization:** Docker Compose for monitoring infrastructure
6. **Service Discovery:** Static configuration with labeled targets

### Key Takeaways

- **Prometheus Client Library** automatically adds `_total` suffix to Counter metrics
- **Datasource UID** must match between Grafana datasource and dashboard JSON
- **Docker host.docker.internal** is used to access host machine from containers on Windows
- **NGINX location blocks** need trailing slash for proper proxy_pass behavior
- **Grafana provisioning** can fail silently; manual API import is more reliable
- **Anonymous auth** in Grafana simplifies development but must be disabled in production

---

## 📅 Maintenance Schedule

### Daily
- Check application logs for errors
- Monitor dashboard for anomalies
- Verify all targets are UP in Prometheus

### Weekly
- Review Grafana dashboards for insights
- Check Docker container resource usage
- Backup Grafana dashboards

### Monthly
- Update Prometheus/Grafana Docker images
- Clean up old Prometheus data if needed
- Review and optimize PromQL queries
- Update Python dependencies

### Quarterly
- Full system backup
- Security audit
- Performance review
- Update documentation

---

**Document Version:** 1.0  
**Last Updated:** October 7, 2025  
**Author:** Setup completed for Muhammad Ahmad  
**Status:** ✅ Production Ready (Development Configuration)

---

## 🎉 Congratulations!

You now have a complete, working monitoring system with:
- 5 FastAPI applications
- NGINX reverse proxy
- Prometheus metrics collection
- Grafana visualization dashboards

Everything is documented, working, and ready for further development!
