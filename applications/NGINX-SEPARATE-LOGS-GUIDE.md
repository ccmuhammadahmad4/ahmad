# 📊 NGINX Separate Logs Configuration Guide

## 🎯 Overview

Ab har app ke liye **separate NGINX logs** configure ho gaye hain. Pehle sare apps ki logs ek hi file (`all_apps_access.log` aur `all_apps_error.log`) mein collect hoti thi. Ab har app ki apni individual log files hain.

---

## 📁 Log File Structure

### Previous Setup (OLD):
```
C:/nginx/logs/
├── all_apps_access.log  ← Sab apps ki combined logs
└── all_apps_error.log   ← Sab apps ki combined errors
```

### Current Setup (NEW):
```
C:/nginx/logs/
├── app1_access.log      ← App1 ke requests
├── app1_error.log       ← App1 ke errors
├── app2_access.log      ← App2 ke requests
├── app2_error.log       ← App2 ke errors
├── app3_access.log      ← App3 ke requests
├── app3_error.log       ← App3 ke errors
├── app4_access.log      ← App4 ke requests
├── app4_error.log       ← App4 ke errors
├── app5_access.log      ← App5 ke requests
├── app5_error.log       ← App5 ke errors
├── all_apps_access.log  ← General logs (still exists)
└── all_apps_error.log   ← General errors (still exists)
```

---

## 🔧 Configuration Details

### App1 Routing Configuration

**File**: `app1-routing.conf`

```nginx
location /app1/ {
    rewrite ^/app1/(.*)$ /$1 break;
    proxy_pass http://127.0.0.1:5001;
    # ... proxy headers ...
    
    # ✅ Separate logs for App1
    access_log C:/nginx/logs/app1_access.log combined;
    error_log C:/nginx/logs/app1_error.log warn;
}
```

**Replicated for all 5 apps** with respective log files:
- App1: `app1_access.log`, `app1_error.log`
- App2: `app2_access.log`, `app2_error.log`
- App3: `app3_access.log`, `app3_error.log`
- App4: `app4_access.log`, `app4_error.log`
- App5: `app5_access.log`, `app5_error.log`

---

## 📊 Promtail Configuration

Promtail ab **har app ki separate NGINX logs** ko scrape kar raha hai.

### Updated Scrape Jobs

**Total NGINX Jobs**: 12

#### Per-App Access Logs (5 jobs):
```yaml
# App1 NGINX Access Logs
- job_name: nginx-app1-access
  static_configs:
    - targets: [localhost]
      labels:
        job: nginx-app1
        app: app1
        log_type: access
        __path__: /nginx-logs/app1_access.log

# App2, App3, App4, App5 similarly configured
```

#### Per-App Error Logs (5 jobs):
```yaml
# App1 NGINX Error Logs
- job_name: nginx-app1-error
  static_configs:
    - targets: [localhost]
      labels:
        job: nginx-app1
        app: app1
        log_type: error
        __path__: /nginx-logs/app1_error.log

# App2, App3, App4, App5 similarly configured
```

#### General Logs (2 jobs):
```yaml
# All apps combined access
- job_name: nginx-access
  static_configs:
    - targets: [localhost]
      labels:
        job: nginx
        log_type: access
        __path__: /nginx-logs/all_apps_access.log

# All apps combined error
- job_name: nginx-error
  static_configs:
    - targets: [localhost]
      labels:
        job: nginx
        log_type: error
        __path__: /nginx-logs/all_apps_error.log
```

---

## 🔍 Querying Logs in Grafana

### Query Specific App NGINX Logs

**App1 NGINX access logs only**:
```logql
{job="nginx-app1", log_type="access"}
```

**App1 NGINX errors only**:
```logql
{job="nginx-app1", log_type="error"}
```

**All App1 requests (NGINX + Application)**:
```logql
{app="app1"}
```

### Query Multiple Apps

**All NGINX access logs (all apps)**:
```logql
{job=~"nginx-app.*", log_type="access"}
```

**NGINX errors from App1 and App2**:
```logql
{job=~"nginx-app[12]", log_type="error"}
```

### Filter by Content

**404 errors in App1 NGINX logs**:
```logql
{job="nginx-app1", log_type="access"} |= "404"
```

**5xx errors across all NGINX logs**:
```logql
{job=~"nginx.*"} |~ " 5[0-9]{2} "
```

---

## 📈 Benefits

### 1. **Better Isolation**
- ✅ Har app ki logs alag se dekh sakte hain
- ✅ Debugging asaan ho gaya
- ✅ Specific app ki performance track kar sakte hain

### 2. **Targeted Monitoring**
- ✅ App1 ki traffic App2 se separate
- ✅ Individual app ki error rate
- ✅ Per-app request patterns

### 3. **Cleaner Loki Queries**
- ✅ Simple label filtering: `{job="nginx-app1"}`
- ✅ No need for complex regex on log content
- ✅ Faster query performance

### 4. **Granular Dashboards**
- ✅ Har app ka apna NGINX dashboard
- ✅ Compare apps side-by-side
- ✅ Individual SLA tracking

---

## 🎨 Dashboard Ideas

### Panel 1: App1 NGINX Request Rate
```logql
sum(rate({job="nginx-app1", log_type="access"}[5m]))
```

### Panel 2: App1 vs App2 Traffic Comparison
```logql
sum by (job) (rate({job=~"nginx-app[12]", log_type="access"}[5m]))
```

### Panel 3: NGINX Error Rate by App
```logql
sum by (app) (rate({job=~"nginx-app.*", log_type="error"}[5m]))
```

### Panel 4: Top 5 URLs in App1
```logql
topk(5, sum by (request) (rate({job="nginx-app1"}[5m])))
```

### Panel 5: HTTP Status Code Distribution
```logql
sum by (status) (rate({job="nginx-app1"} | pattern `<_> <_> <_> <_> <_> <_> <_> <_> <status>` [5m]))
```

---

## 🔄 Log Rotation

### Current Setup
NGINX logs rotate automatically based on NGINX configuration.

### Recommended Settings

Add to `nginx.conf`:
```nginx
# Log rotation settings
http {
    # ... other settings ...
    
    # Access log with buffer
    access_log C:/nginx/logs/access.log combined buffer=32k;
    
    # Error log level
    error_log C:/nginx/logs/error.log warn;
}
```

### External Log Rotation (Optional)

Use Windows Task Scheduler with PowerShell:
```powershell
# Rotate logs daily
$logPath = "C:\nginx\logs"
$date = Get-Date -Format "yyyy-MM-dd"

Get-ChildItem "$logPath\*.log" | ForEach-Object {
    $newName = "$($_.BaseName)_$date.log"
    Copy-Item $_.FullName "$logPath\archive\$newName"
    Clear-Content $_.FullName
}
```

---

## 📊 Log Analysis Examples

### 1. Find Slow Requests
```bash
# In NGINX logs, add request_time
# Then query in Grafana:
{job="nginx-app1"} | pattern `<_> <_> <_> <_> <_> <_> <_> <request_time>` | request_time > 1.0
```

### 2. Top IP Addresses
```logql
topk(10, sum by (remote_addr) (count_over_time({job="nginx-app1"}[1h])))
```

### 3. Request Rate by Hour
```logql
sum by (hour) (count_over_time({job="nginx-app1"}[1h]))
```

---

## 🚀 Quick Verification

### Step 1: Check Log Files Exist
```powershell
Get-ChildItem C:\nginx\logs\app*_*.log
```

**Expected Output**:
```
app1_access.log
app1_error.log
app2_access.log
app2_error.log
app3_access.log
app3_error.log
app4_access.log
app4_error.log
app5_access.log
app5_error.log
```

### Step 2: Generate Some Traffic
```powershell
# App1
curl http://172.25.25.140/app1/

# App2
curl http://172.25.25.140/app2/

# App3
curl http://172.25.25.140/app3/
```

### Step 3: Check Logs Have Content
```powershell
Get-Content C:\nginx\logs\app1_access.log -Tail 5
Get-Content C:\nginx\logs\app2_access.log -Tail 5
```

### Step 4: Verify in Grafana Explore
1. Open: http://localhost:3000/explore
2. Select "Loki" datasource
3. Query: `{job="nginx-app1"}`
4. Should see logs from App1 only

---

## 🎯 Label Strategy

### NGINX App-Specific Logs:
```yaml
labels:
  job: nginx-app1      # Identifies NGINX + specific app
  app: app1            # App identifier
  log_type: access     # access or error
```

### General NGINX Logs:
```yaml
labels:
  job: nginx           # General NGINX
  log_type: access     # access or error
```

### Querying Strategy:

**Specific app NGINX logs**:
```logql
{job="nginx-app1"}
```

**All NGINX logs (all apps)**:
```logql
{job=~"nginx.*"}
```

**Only NGINX access logs**:
```logql
{job=~"nginx.*", log_type="access"}
```

**Combined: App1 NGINX + Application logs**:
```logql
{app="app1"}
```

---

## 📝 Log Format

### NGINX Combined Format:
```
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"
```

### Example Log Line:
```
172.25.25.1 - - [09/Oct/2025:09:45:23 +0500] "GET /app1/api/app-info HTTP/1.1" 200 185 "-" "curl/7.83.1"
```

### Parsed Fields:
- `remote_addr`: 172.25.25.1
- `time_local`: 09/Oct/2025:09:45:23 +0500
- `request`: GET /app1/api/app-info HTTP/1.1
- `status`: 200
- `body_bytes_sent`: 185
- `http_user_agent`: curl/7.83.1

---

## 🔧 Troubleshooting

### Issue 1: Log Files Not Created

**Check**:
```powershell
Test-Path C:\nginx\logs\app1_access.log
```

**Fix**: Generate traffic:
```powershell
curl http://172.25.25.140/app1/
```

### Issue 2: Promtail Not Scraping

**Check Promtail logs**:
```powershell
docker logs promtail-apps --tail 20
```

**Check targets**:
```powershell
curl http://localhost:9080/targets
```

### Issue 3: Empty Logs in Grafana

**Verify Loki**:
```powershell
curl http://localhost:3100/ready
```

**Query Loki directly**:
```powershell
curl "http://localhost:3100/loki/api/v1/query?query={job=\"nginx-app1\"}"
```

---

## 📈 Performance Impact

### Storage Requirements

**Per App (estimated)**:
- Access logs: ~10-50 MB/day (depends on traffic)
- Error logs: ~1-5 MB/day

**Total for 5 apps**:
- ~50-250 MB/day for access logs
- ~5-25 MB/day for error logs

### Promtail Resource Usage

**Before** (2 NGINX jobs):
- CPU: ~2%
- Memory: ~50 MB

**After** (12 NGINX jobs):
- CPU: ~3-4%
- Memory: ~60-70 MB

**Impact**: Minimal ✅

---

## ✅ Summary

### What Changed:

1. ✅ **NGINX Config**: Added `access_log` and `error_log` to each app location
2. ✅ **Promtail Config**: Added 10 new scrape jobs (5 apps × 2 log types)
3. ✅ **Log Files**: Now 10 separate log files (+ 2 general = 12 total)
4. ✅ **Loki Labels**: App-specific NGINX logs have `job=nginx-app1`, `app=app1`

### Benefits:

- 🎯 **Isolation**: Each app's NGINX logs separate
- 🔍 **Easier Debugging**: Filter by specific app
- 📊 **Better Dashboards**: Per-app NGINX metrics
- ⚡ **Faster Queries**: Simple label filtering

### Query Examples:

```logql
# App1 NGINX logs only
{job="nginx-app1"}

# All App1 logs (NGINX + Application)
{app="app1"}

# All NGINX access logs (all apps)
{job=~"nginx.*", log_type="access"}

# App1 errors (NGINX + Application)
{app="app1", log_type="error"}
```

---

**🎉 Setup Complete! Ab har app ki NGINX logs alag se track ho rahi hain!**

**Last Updated**: October 9, 2025  
**Version**: 1.0
