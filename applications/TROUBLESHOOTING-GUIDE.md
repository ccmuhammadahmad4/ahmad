# Troubleshooting Guide - Loki + Grafana Setup

## Table of Contents
1. [Quick Diagnostic Commands](#quick-diagnostic-commands)
2. [Common Issues & Solutions](#common-issues--solutions)
3. [Log Analysis](#log-analysis)
4. [Performance Issues](#performance-issues)
5. [Recovery Procedures](#recovery-procedures)

---

## Quick Diagnostic Commands

### System Health Check

**Check all services status:**
```powershell
# Docker containers
docker ps -a | Select-String "loki|promtail|grafana|prometheus"

# FastAPI apps
for ($i=1; $i -le 5; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:500$i" -UseBasicParsing -TimeoutSec 2
        Write-Host "✓ App$i running (Port 500$i)" -ForegroundColor Green
    } catch {
        Write-Host "✗ App$i NOT running (Port 500$i)" -ForegroundColor Red
    }
}

# NGINX
Get-Process nginx -ErrorAction SilentlyContinue
if ($?) {
    Write-Host "✓ NGINX running" -ForegroundColor Green
} else {
    Write-Host "✗ NGINX NOT running" -ForegroundColor Red
}

# Test NGINX routing
for ($i=1; $i -le 5; $i++) {
    try {
        Invoke-WebRequest "http://172.25.25.140/app$i/" -UseBasicParsing | Out-Null
        Write-Host "✓ NGINX routing to App$i working" -ForegroundColor Green
    } catch {
        Write-Host "✗ NGINX routing to App$i FAILED" -ForegroundColor Red
    }
}
```

### Log File Status

**Check log files:**
```powershell
# NGINX logs
Write-Host "`n=== NGINX Logs ===" -ForegroundColor Cyan
Get-ChildItem C:\nginx\logs\app*_access.log | 
    Select-Object Name, 
                  @{N='Size(KB)';E={[math]::Round($_.Length/1KB, 2)}}, 
                  LastWriteTime |
    Format-Table -AutoSize

# Application logs
Write-Host "`n=== Application Logs ===" -ForegroundColor Cyan
Get-ChildItem C:\Users\muhammadahmad4\applications\app*\*.log | 
    Select-Object Name, 
                  @{N='Size(KB)';E={[math]::Round($_.Length/1KB, 2)}}, 
                  LastWriteTime |
    Format-Table -AutoSize
```

### Loki & Promtail Status

**Check Loki API:**
```powershell
# Loki health
Invoke-WebRequest -Uri "http://localhost:3100/ready" -UseBasicParsing

# Available labels
$labels = Invoke-RestMethod -Uri "http://localhost:3100/loki/api/v1/labels"
Write-Host "`n=== Loki Labels ===" -ForegroundColor Cyan
$labels.data | Format-Table

# Available job values
$jobs = Invoke-RestMethod -Uri "http://localhost:3100/loki/api/v1/label/job/values"
Write-Host "`n=== Loki Jobs ===" -ForegroundColor Cyan
$jobs.data | Format-Table
```

**Check Promtail:**
```powershell
# Promtail logs
docker logs promtail-apps --tail 50

# Check if Promtail is tailing files
docker exec promtail-apps cat /tmp/positions.yaml
```

### Grafana Status

**Check Grafana:**
```powershell
# Grafana health
Invoke-WebRequest -Uri "http://localhost:3000/api/health" -UseBasicParsing

# List datasources
$datasources = Invoke-RestMethod -Uri "http://localhost:3000/api/datasources"
Write-Host "`n=== Grafana Datasources ===" -ForegroundColor Cyan
$datasources | Select-Object name, type, url | Format-Table

# List dashboards
$dashboards = Invoke-RestMethod -Uri "http://localhost:3000/api/search"
Write-Host "`n=== Grafana Dashboards ===" -ForegroundColor Cyan
$dashboards | Select-Object title, type, uid | Format-Table
```

---

## Common Issues & Solutions

### Issue 1: No Data in Grafana Dashboards

**Symptoms:**
- Panels show "No data"
- Empty graphs
- "0" in stat panels

**Diagnosis Steps:**

**Step 1: Check if Loki has data**
```powershell
# Query Loki directly
$query = '{job="nginx-app1"}'
$url = "http://localhost:3100/loki/api/v1/query_range?query=$query&limit=10"
$response = Invoke-RestMethod -Uri $url

if ($response.data.result.Count -gt 0) {
    Write-Host "✓ Loki has data for nginx-app1" -ForegroundColor Green
} else {
    Write-Host "✗ NO data in Loki for nginx-app1" -ForegroundColor Red
}
```

**Step 2: Check Promtail logs**
```powershell
docker logs promtail-apps --tail 100 | Select-String "error|failed|warn"
```

**Step 3: Verify log files exist and are updating**
```powershell
# Check last write time
Get-ChildItem C:\nginx\logs\app1_access.log | 
    Select-Object Name, Length, LastWriteTime
```

**Solutions:**

**Solution 1A: Log files not created**
```powershell
# Generate traffic to create logs
for ($i=1; $i -le 5; $i++) {
    Invoke-WebRequest "http://172.25.25.140/app$i/" -UseBasicParsing
}

# Check if logs created
Get-ChildItem C:\nginx\logs\app*_access.log
```

**Solution 1B: Promtail not collecting**
```powershell
# Restart Promtail to re-scan files
docker-compose -f C:\Users\muhammadahmad4\applications\monitoring\docker-compose.yml restart promtail

# Wait 10 seconds
Start-Sleep -Seconds 10

# Check Promtail logs
docker logs promtail-apps --tail 20
```

**Solution 1C: Wrong job label in query**
```powershell
# List available jobs
$jobs = Invoke-RestMethod -Uri "http://localhost:3100/loki/api/v1/label/job/values"
Write-Host "Available jobs:" -ForegroundColor Cyan
$jobs.data

# Update dashboard query to use correct job name
```

---

### Issue 2: NGINX Logs Not Separating

**Symptoms:**
- All apps logging to same file
- Only `access.log` exists, no `app1_access.log`
- Mixed logs from different apps

**Diagnosis:**
```powershell
# Check NGINX config
cd C:\nginx
.\nginx.exe -T | Select-String "access_log"
```

**Expected Output:**
```
access_log C:/nginx/logs/app1_access.log combined;
access_log C:/nginx/logs/app2_access.log combined;
access_log C:/nginx/logs/app3_access.log combined;
access_log C:/nginx/logs/app4_access.log combined;
access_log C:/nginx/logs/app5_access.log combined;
```

**Solution:**

**Fix Configuration:**
Edit each `appN-routing.conf` file:

```nginx
location /app1/ {
    # CRITICAL: access_log MUST be FIRST directive in location block
    access_log C:/nginx/logs/app1_access.log combined;
    error_log C:/nginx/logs/app1_error.log warn;
    
    # Then other directives...
    rewrite ^/app1/(.*)$ /$1 break;
    proxy_pass http://127.0.0.1:5001;
    # ...
}
```

**Common Mistakes:**
```nginx
# WRONG: Using backslashes
access_log C:\nginx\logs\app1_access.log;

# WRONG: Missing log format
access_log C:/nginx/logs/app1_access.log;

# WRONG: access_log not first
rewrite ^/app1/(.*)$ /$1 break;
access_log C:/nginx/logs/app1_access.log combined;  # TOO LATE!

# CORRECT: Forward slashes, format specified, first in block
access_log C:/nginx/logs/app1_access.log combined;
```

**Reload NGINX:**
```powershell
cd C:\nginx

# Test config first
.\nginx.exe -t

# If OK, reload
.\nginx.exe -s reload
```

---

### Issue 3: Applications Not Starting

**Symptoms:**
- `ImportError: No module named 'fastapi'`
- Apps exit immediately
- Connection refused on ports 5001-5005

**Diagnosis:**
```powershell
# Check if .venv exists
Test-Path C:\Users\muhammadahmad4\applications\.venv

# Check if packages installed
C:\Users\muhammadahmad4\applications\.venv\Scripts\pip.exe list
```

**Solution:**

**Activate Virtual Environment:**
```powershell
cd C:\Users\muhammadahmad4\applications
.\.venv\Scripts\Activate.ps1

# Verify activation (should show (.venv) in prompt)
# (.venv) PS C:\Users\muhammadahmad4\applications>

# Start app
cd app1
python main.py
```

**If .venv missing:**
```powershell
cd C:\Users\muhammadahmad4\applications
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn python-json-logger
```

**Start All Apps Script:**
```powershell
# Save as start-all-apps.ps1
cd C:\Users\muhammadahmad4\applications

for ($i=1; $i -le 5; $i++) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
        cd C:\Users\muhammadahmad4\applications
        .\.venv\Scripts\Activate.ps1
        cd app$i
        python main.py
"@
    Write-Host "Started App$i" -ForegroundColor Green
    Start-Sleep -Seconds 2
}
```

---

### Issue 4: Promtail Not Collecting NGINX Logs

**Symptoms:**
- `{job="app1"}` returns data
- `{job="nginx-app1"}` returns no data
- Promtail logs show "no targets" or "file not found"

**Diagnosis:**
```powershell
# Check Promtail can see files
docker exec promtail-apps ls -la /nginx-logs/

# Expected output:
# app1_access.log
# app1_error.log
# app2_access.log
# ...
```

**Solution:**

**If files not visible:**
```powershell
# Check docker-compose.yml volume mount
Get-Content C:\Users\muhammadahmad4\applications\monitoring\docker-compose.yml | 
    Select-String "nginx-logs"

# Should show:
# - C:/nginx/logs:/nginx-logs:ro

# If missing, add to promtail service:
volumes:
  - C:/nginx/logs:/nginx-logs:ro

# Restart container
docker-compose -f C:\Users\muhammadahmad4\applications\monitoring\docker-compose.yml restart promtail
```

**If files visible but not collected:**
```powershell
# Check promtail-config.yml
Get-Content C:\Users\muhammadahmad4\applications\monitoring\promtail\promtail-config.yml | 
    Select-String "__path__"

# Verify path matches:
# __path__: /nginx-logs/app1_access.log

# Force restart
docker-compose -f C:\Users\muhammadahmad4\applications\monitoring\docker-compose.yml down
docker-compose -f C:\Users\muhammadahmad4\applications\monitoring\docker-compose.yml up -d
```

---

### Issue 5: Dashboard Import Fails

**Symptoms:**
- Error: "Dashboard title cannot be empty"
- Error: "Invalid JSON"
- Dashboard not appearing in list

**Diagnosis:**
```powershell
# Check file encoding
Get-Content C:\Users\muhammadahmad4\applications\monitoring\grafana\dashboards\app1-loki-enhanced.json -Raw | 
    Out-File test.txt -Encoding utf8

# Check for BOM (Byte Order Mark)
$bytes = [System.IO.File]::ReadAllBytes("app1-loki-enhanced.json")
if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    Write-Host "✗ File has UTF-8 BOM" -ForegroundColor Red
} else {
    Write-Host "✓ File encoding OK" -ForegroundColor Green
}
```

**Solution:**

**Fix UTF-8 BOM:**
```powershell
cd C:\Users\muhammadahmad4\applications\monitoring\grafana\dashboards

for ($i=1; $i -le 5; $i++) {
    $file = "app${i}-loki-enhanced.json"
    
    # Read content
    $content = [System.IO.File]::ReadAllText($file)
    
    # Write without BOM
    $utf8NoBOM = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($file, $content, $utf8NoBOM)
    
    Write-Host "✓ Fixed $file" -ForegroundColor Green
}
```

**Import via API:**
```powershell
for ($i=1; $i -le 5; $i++) {
    $dashboard = Get-Content "app${i}-loki-enhanced.json" -Raw | ConvertFrom-Json
    
    $body = @{
        dashboard = $dashboard
        overwrite = $true
    } | ConvertTo-Json -Depth 100
    
    try {
        Invoke-RestMethod -Uri "http://localhost:3000/api/dashboards/db" `
                          -Method Post `
                          -Body $body `
                          -ContentType "application/json" | Out-Null
        Write-Host "✓ Imported App${i} Dashboard" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to import App${i}: $_" -ForegroundColor Red
    }
}
```

---

### Issue 6: Loki Container Won't Start

**Symptoms:**
- `docker ps` doesn't show `loki-apps`
- Error: "bind: address already in use"
- Container exits immediately

**Diagnosis:**
```powershell
# Check logs
docker logs loki-apps

# Check if port is in use
Get-NetTCPConnection -LocalPort 3100 -ErrorAction SilentlyContinue
```

**Solutions:**

**Solution 6A: Port conflict**
```powershell
# Find process using port
Get-NetTCPConnection -LocalPort 3100 | 
    Select-Object -ExpandProperty OwningProcess | 
    ForEach-Object { Get-Process -Id $_ }

# Stop the process or change Loki port in docker-compose.yml
# ports:
#   - "3101:3100"  # Use external port 3101
```

**Solution 6B: Invalid config**
```powershell
# Validate Loki config
docker run --rm -v C:\Users\muhammadahmad4\applications\monitoring\loki:/etc/loki `
    grafana/loki:latest `
    -config.file=/etc/loki/loki-config.yml -verify-config
```

**Solution 6C: Volume permission issue**
```powershell
# Remove volume and recreate
docker-compose -f C:\Users\muhammadahmad4\applications\monitoring\docker-compose.yml down -v
docker-compose -f C:\Users\muhammadahmad4\applications\monitoring\docker-compose.yml up -d
```

---

### Issue 7: Endpoint Analytics Showing "No Data"

**Symptoms:**
- Top 20 Endpoints table empty
- Pie chart shows "No data"
- Other panels work fine

**Diagnosis:**
```powershell
# Test regex query manually
$query = '{job="nginx-app1"} | regexp `"[A-Z]+ (?P<path>/[^ ]*) HTTP"`'
$url = "http://localhost:3100/loki/api/v1/query_range?query=$query&limit=10"

try {
    $response = Invoke-RestMethod -Uri $url
    if ($response.data.result.Count -gt 0) {
        Write-Host "✓ Regex extraction working" -ForegroundColor Green
        $response.data.result[0].values | Select-Object -First 5
    } else {
        Write-Host "✗ Regex not matching" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Query failed: $_" -ForegroundColor Red
}
```

**Solutions:**

**Solution 7A: No traffic**
```powershell
# Generate traffic
for ($i=1; $i -le 5; $i++) {
    for ($j=1; $j -le 10; $j++) {
        Invoke-WebRequest "http://172.25.25.140/app$i/" -UseBasicParsing | Out-Null
        Invoke-WebRequest "http://172.25.25.140/app$i/api/app-info" -UseBasicParsing | Out-Null
    }
}

# Wait 10 seconds for Promtail to collect
Start-Sleep -Seconds 10

# Refresh dashboard
```

**Solution 7B: Wrong log format**
```powershell
# Check NGINX log format
Get-Content C:\nginx\logs\app1_access.log -Tail 1

# Should contain: "GET /app1/ HTTP/1.1"
# If format different, adjust regex in dashboard query
```

**Solution 7C: Time range too short**
- Dashboard time range: Last 15 minutes
- If no traffic in last 15 min, no data shown
- Extend time range or generate new traffic

---

## Log Analysis

### Reading NGINX Logs

**Log Format (Combined):**
```
172.25.25.140 - - [09/Oct/2025:11:22:19 +0500] "GET /app1/ HTTP/1.1" 200 1269 "-" "Mozilla/5.0..."
```

**Field Breakdown:**
```
172.25.25.140           → Client IP
-                       → Remote user (usually -)
-                       → Auth user (usually -)
[09/Oct/2025:11:22:19]  → Timestamp
"GET /app1/ HTTP/1.1"   → Request line
200                     → HTTP status code
1269                    → Response size (bytes)
"-"                     → Referer
"Mozilla/5.0..."        → User agent
```

**Common Patterns:**

**Success:**
```
172.25.25.140 - - [09/Oct/2025:11:22:19 +0500] "GET /app1/ HTTP/1.1" 200 1269
```
Status: 200 = OK

**Not Found:**
```
172.25.25.140 - - [09/Oct/2025:11:22:20 +0500] "GET /app1/missing HTTP/1.1" 404 162
```
Status: 404 = Not Found

**Server Error:**
```
172.25.25.140 - - [09/Oct/2025:11:22:21 +0500] "POST /app1/api/data HTTP/1.1" 500 85
```
Status: 500 = Internal Server Error

**PowerShell Analysis:**
```powershell
# Count requests per endpoint
Get-Content C:\nginx\logs\app1_access.log | 
    ForEach-Object {
        if ($_ -match '"[A-Z]+ (/[^ ]*) HTTP') {
            $matches[1]
        }
    } | 
    Group-Object | 
    Sort-Object Count -Descending | 
    Select-Object Count, Name

# Count by status code
Get-Content C:\nginx\logs\app1_access.log | 
    ForEach-Object {
        if ($_ -match 'HTTP/[0-9.]+ ([0-9]{3})') {
            $matches[1]
        }
    } | 
    Group-Object | 
    Sort-Object Name

# Find errors (4xx, 5xx)
Get-Content C:\nginx\logs\app1_access.log | 
    Select-String 'HTTP/[0-9.]+ [45][0-9]{2}'
```

### Reading Application Logs

**Text Format:**
```
2025-10-09 11:22:19,123 - uvicorn.access - INFO - 127.0.0.1:52345 - "GET / HTTP/1.1" 200
```

**JSON Format:**
```json
{
  "asctime": "2025-10-09 11:22:19,123",
  "name": "app1",
  "levelname": "INFO",
  "message": "Root endpoint accessed"
}
```

**PowerShell Analysis:**
```powershell
# Count by log level (text logs)
Get-Content C:\Users\muhammadahmad4\applications\app1\app1.log | 
    ForEach-Object {
        if ($_ -match ' - ([A-Z]+) - ') {
            $matches[1]
        }
    } | 
    Group-Object | 
    Sort-Object Count -Descending

# Parse JSON logs
Get-Content C:\Users\muhammadahmad4\applications\app1\app1-json.log | 
    ForEach-Object {
        $_ | ConvertFrom-Json
    } | 
    Where-Object { $_.levelname -eq 'ERROR' } | 
    Select-Object asctime, message
```

---

## Performance Issues

### Slow Dashboard Loading

**Symptoms:**
- Panels take >5 seconds to load
- Timeouts
- Browser freezing

**Diagnosis:**

**Check Query Performance:**
1. Open dashboard in Grafana
2. Click panel title → Inspect → Query
3. Look at "Request duration"

**Solutions:**

**Solution 1: Reduce time range**
```json
// Change from 1 hour to 15 minutes
{
  "time": {
    "from": "now-15m",  // Was: "now-1h"
    "to": "now"
  }
}
```

**Solution 2: Optimize queries**
```logql
# SLOW: No label filter
{} |= "app1"

# FAST: Label filter first
{job="nginx-app1"}

# SLOW: Complex regex on all logs
{job="nginx-app1"} | regexp `very.*complex.*regex`

# FAST: Filter before regex
{job="nginx-app1"} |= "keyword" | regexp `simpler`
```

**Solution 3: Increase refresh interval**
```json
// Change from 1s to 5s for less critical dashboards
{
  "refresh": "5s"  // Was: "1s"
}
```

**Solution 4: Limit results**
```logql
# Add limit
topk(10, sum by (path) (...))  # Instead of topk(100, ...)
```

### High CPU Usage

**Diagnosis:**
```powershell
# Check container resource usage
docker stats loki-apps promtail-apps grafana-apps --no-stream
```

**Solutions:**

**Solution 1: Configure Loki limits**
Edit `loki-config.yml`:
```yaml
limits_config:
  max_query_parallelism: 4  # Limit concurrent queries
  max_entries_limit_per_query: 5000  # Limit result size
  max_streams_per_user: 10000  # Limit total streams
```

**Solution 2: Configure Promtail batch**
Edit `promtail-config.yml`:
```yaml
clients:
  - url: http://loki:3100/loki/api/v1/push
    batchwait: 1s      # Wait 1 sec before sending
    batchsize: 102400  # 100KB batch size
```

**Solution 3: Reduce Grafana refresh**
- Change dashboard refresh from 1s to 5s or 10s

### High Disk Usage

**Diagnosis:**
```powershell
# Check Loki volume size
docker exec loki-apps du -sh /loki

# Check log file sizes
Get-ChildItem C:\nginx\logs\*.log, C:\Users\muhammadahmad4\applications\app*\*.log | 
    Measure-Object -Property Length -Sum | 
    Select-Object @{N='TotalMB';E={[math]::Round($_.Sum/1MB, 2)}}
```

**Solutions:**

**Solution 1: Configure retention**
Edit `loki-config.yml`:
```yaml
limits_config:
  retention_period: 72h  # Keep only 3 days (was 7 days)
```

**Solution 2: Rotate NGINX logs**
Create `rotate-nginx-logs.ps1`:
```powershell
$logsDir = "C:\nginx\logs"
$archiveDir = "C:\nginx\logs\archive"

# Create archive directory
New-Item -ItemType Directory -Path $archiveDir -Force

# Move logs older than 3 days
Get-ChildItem "$logsDir\*.log" | 
    Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-3)} | 
    ForEach-Object {
        $date = $_.LastWriteTime.ToString('yyyy-MM-dd')
        $newName = "$($_.BaseName)-$date$($_.Extension).gz"
        
        # Compress and move
        Compress-Archive -Path $_.FullName -DestinationPath "$archiveDir\$newName"
        Remove-Item $_.FullName
    }
```

Schedule daily:
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-File C:\scripts\rotate-nginx-logs.ps1"

$trigger = New-ScheduledTaskTrigger -Daily -At 2am

Register-ScheduledTask -TaskName "RotateNginxLogs" `
    -Action $action -Trigger $trigger -Description "Rotate NGINX logs daily"
```

---

## Recovery Procedures

### Complete System Restart

**Step 1: Stop everything**
```powershell
# Stop Docker containers
cd C:\Users\muhammadahmad4\applications\monitoring
docker-compose down

# Stop NGINX
cd C:\nginx
.\nginx.exe -s quit

# Stop FastAPI apps (close terminals or Ctrl+C)
```

**Step 2: Start Docker stack**
```powershell
cd C:\Users\muhammadahmad4\applications\monitoring
docker-compose up -d

# Wait for containers to be healthy
Start-Sleep -Seconds 15

# Verify
docker ps
```

**Step 3: Start NGINX**
```powershell
cd C:\nginx

# Test config
.\nginx.exe -t

# Start
.\nginx.exe
```

**Step 4: Start applications**
```powershell
cd C:\Users\muhammadahmad4\applications

for ($i=1; $i -le 5; $i++) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
        cd C:\Users\muhammadahmad4\applications
        .\.venv\Scripts\Activate.ps1
        cd app$i
        python main.py
"@
    Start-Sleep -Seconds 2
}
```

**Step 5: Verify**
```powershell
# Test full stack
for ($i=1; $i -le 5; $i++) {
    Invoke-WebRequest "http://172.25.25.140/app$i/" -UseBasicParsing | Out-Null
}

# Check Loki
Start-Sleep -Seconds 10
Invoke-RestMethod "http://localhost:3100/loki/api/v1/label/job/values"

# Open Grafana
Start-Process "http://localhost:3000"
```

### Reset Loki Data

**Warning:** This deletes all log data!

```powershell
cd C:\Users\muhammadahmad4\applications\monitoring

# Stop Loki
docker-compose stop loki

# Remove volume
docker volume rm monitoring_loki-data

# Restart
docker-compose up -d loki

# Verify
docker logs loki-apps --tail 20
```

### Reset Grafana Dashboards

```powershell
# Delete all dashboards via API
$dashboards = Invoke-RestMethod "http://localhost:3000/api/search"
foreach ($dashboard in $dashboards) {
    Invoke-RestMethod -Uri "http://localhost:3000/api/dashboards/uid/$($dashboard.uid)" `
                      -Method Delete
    Write-Host "Deleted: $($dashboard.title)"
}

# Re-import
cd C:\Users\muhammadahmad4\applications\monitoring\grafana\dashboards
for ($i=1; $i -le 5; $i++) {
    $dashboard = Get-Content "app${i}-loki-enhanced.json" -Raw | ConvertFrom-Json
    $body = @{dashboard = $dashboard; overwrite = $true} | ConvertTo-Json -Depth 100
    Invoke-RestMethod -Uri "http://localhost:3000/api/dashboards/db" `
                      -Method Post -Body $body -ContentType "application/json"
}
```

### Rebuild Everything

**Nuclear option - complete reset:**

```powershell
# 1. Stop all services
cd C:\Users\muhammadahmad4\applications\monitoring
docker-compose down -v

cd C:\nginx
.\nginx.exe -s quit

# 2. Clear logs
Remove-Item C:\nginx\logs\*.log -Force
Remove-Item C:\Users\muhammadahmad4\applications\app*\*.log -Force

# 3. Restart Docker
docker-compose up -d

# 4. Restart NGINX
cd C:\nginx
.\nginx.exe

# 5. Restart apps
cd C:\Users\muhammadahmad4\applications
.\.venv\Scripts\Activate.ps1

for ($i=1; $i -le 5; $i++) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
        cd C:\Users\muhammadahmad4\applications
        .\.venv\Scripts\Activate.ps1
        cd app$i
        python main.py
"@
}

# 6. Generate traffic
Start-Sleep -Seconds 20
for ($i=1; $i -le 5; $i++) {
    for ($j=1; $j -le 10; $j++) {
        Invoke-WebRequest "http://172.25.25.140/app$i/" -UseBasicParsing | Out-Null
    }
}

# 7. Import dashboards
cd C:\Users\muhammadahmad4\applications\monitoring\grafana\dashboards
for ($i=1; $i -le 5; $i++) {
    $dashboard = Get-Content "app${i}-loki-enhanced.json" -Raw | ConvertFrom-Json
    $body = @{dashboard = $dashboard; overwrite = $true} | ConvertTo-Json -Depth 100
    Invoke-RestMethod -Uri "http://localhost:3000/api/dashboards/db" `
                      -Method Post -Body $body -ContentType "application/json"
}

Write-Host "`n✓ System rebuilt successfully!" -ForegroundColor Green
```

---

## Emergency Contacts & Resources

### Grafana Documentation
- **Loki Queries**: https://grafana.com/docs/loki/latest/logql/
- **Dashboard Variables**: https://grafana.com/docs/grafana/latest/variables/
- **Troubleshooting**: https://grafana.com/docs/loki/latest/operations/troubleshooting/

### Common Error Messages

**"too many outstanding requests"**
- **Cause**: Loki overloaded
- **Fix**: Reduce query parallelism or increase resources

**"context deadline exceeded"**
- **Cause**: Query timeout
- **Fix**: Reduce time range or simplify query

**"failed to tail file"**
- **Cause**: File permissions or path issue
- **Fix**: Check volume mounts and file permissions

**"entry out of order"**
- **Cause**: Log timestamps not monotonic
- **Fix**: Ensure system time is synchronized

---

**Document Version:** 1.0  
**Last Updated:** October 9, 2025  
**Related Documents:**
- LOKI-GRAFANA-COMPLETE-SETUP.md
- DASHBOARD-CONFIGURATION-GUIDE.md
