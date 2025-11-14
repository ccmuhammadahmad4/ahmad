# ✅ Complete Loki + Promtail + Grafana Setup - VERIFIED

## 🎯 **Setup Status: WORKING** ✅

---

## 📊 Architecture Flow

```
┌──────────────────────────────────────────┐
│         5 FastAPI Applications           │
│    (App1-5 on ports 5001-5005)          │
│                                          │
│  Generates logs:                         │
│  → app1.log (human-readable)            │
│  → app1-json.log (structured JSON)      │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│          Promtail (Agent)                │
│   Container: promtail-apps               │
│                                          │
│  Collects logs from:                     │
│  → /apps/app1/*.log                      │
│  → /apps/app2/*.log                      │
│  → /apps/app3/*.log                      │
│  → /apps/app4/*.log                      │
│  → /apps/app5/*.log                      │
│  → /nginx-logs/*.log                     │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│         Loki (Log Storage)               │
│   Container: loki-apps                   │
│   Port: 3100                             │
│                                          │
│  Stores logs with labels:                │
│  → {job="app1", app="application1"}     │
│  → {job="app2", app="application2"}     │
│  → ... etc                               │
│                                          │
│  Retention: 744 hours (31 days)         │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│       Grafana (Visualization)            │
│   Container: grafana-apps                │
│   Port: 3000                             │
│                                          │
│  Datasource: Loki                        │
│  UID: P8E80F9AEF21F6940                 │
│  URL: http://loki:3100                   │
│                                          │
│  Query Language: LogQL                   │
└──────────────────────────────────────────┘
```

---

## ✅ Verified Components

### 1. **Applications** ✓
```powershell
# All 5 apps running
App1: http://127.0.0.1:5001
App2: http://127.0.0.1:5002
App3: http://127.0.0.1:5003
App4: http://127.0.0.1:5004
App5: http://127.0.0.1:5005
```

**Logs Generated**:
- `C:\Users\muhammadahmad4\applications\app1\app1.log`
- `C:\Users\muhammadahmad4\applications\app1\app1-json.log`
- (Same for app2-5)

### 2. **Docker Containers** ✓
```
NAME              STATUS        PORTS
loki-apps         Up           3100:3100
promtail-apps     Up           (internal)
grafana-apps      Up           3000:3000
prometheus-apps   Up           9090:9090
```

### 3. **Loki** ✓
```powershell
# Test Loki is running
curl http://localhost:3100/ready
# Response: ready

# Check available labels
curl http://localhost:3100/loki/api/v1/labels
# Response: ["filename","job","log_type","service_name"]

# Check job values
curl http://localhost:3100/loki/api/v1/label/job/values
# Response: ["app1","app2","app3","app4","app5","nginx","uvicorn"]
```

### 4. **Promtail** ✓
**Config**: `monitoring/promtail/promtail-config.yml`

**Scrape Jobs**:
- app1 → `/apps/app1/*.log`
- app2 → `/apps/app2/*.log`
- app3 → `/apps/app3/*.log`
- app4 → `/apps/app4/*.log`
- app5 → `/apps/app5/*.log`
- nginx-access → `/nginx-logs/all_apps_access.log`
- nginx-error → `/nginx-logs/all_apps_error.log`
- uvicorn-logs → `/apps/app*/*.log` (JSON parsing)

### 5. **Grafana Datasource** ✓
```
Name: Loki
Type: loki
UID: P8E80F9AEF21F6940
URL: http://loki:3100
Access: proxy
Status: ✅ Working
```

---

## 🔍 Query Examples

### Basic Queries

**1. All logs from App1**:
```logql
{job="app1"}
```

**2. All logs from App2**:
```logql
{job="app2"}
```

**3. All logs from all apps**:
```logql
{job=~"app.*"}
```

**4. Only ERROR level logs**:
```logql
{job="app1"} |= "ERROR"
```

**5. Logs from specific endpoint**:
```logql
{job="app1"} |= "/api/app-info"
```

### Advanced Queries

**6. Count logs per second**:
```logql
sum(rate({job="app1"}[5m]))
```

**7. Top 5 apps by log volume**:
```logql
topk(5, sum by (job) (rate({job=~"app.*"}[5m])))
```

**8. JSON parsing**:
```logql
{job="app1"} | json | level="INFO"
```

---

## 🎯 How to Use

### Step 1: Open Grafana
```
URL: http://localhost:3000/explore
Username: admin
Password: admin123
```

### Step 2: Select Loki Datasource
- Top dropdown → Select **"Loki"**

### Step 3: Write Query
- Query field → Enter: `{job="app1"}`
- Click **"Run Query"**

### Step 4: View Logs
- Logs appear in table below
- Can filter, search, expand
- Time range adjustable

---

## 📊 Sample Queries for Each App

### App1 Logs:
```logql
{job="app1"}
```

### App2 Logs:
```logql
{job="app2"}
```

### App3 Logs:
```logql
{job="app3"}
```

### App4 Logs:
```logql
{job="app4"}
```

### App5 Logs:
```logql
{job="app5"}
```

### All Apps Combined:
```logql
{job=~"app[1-5]"}
```

### NGINX Logs:
```logql
{job="nginx"}
```

---

## 🧪 Testing Commands

### Test Loki API:
```powershell
# Check Loki is ready
curl http://localhost:3100/ready

# Get labels
curl http://localhost:3100/loki/api/v1/labels

# Query app1 logs
$query = '{job="app1"}'
curl "http://localhost:3100/loki/api/v1/query_range?query=$query&limit=5"
```

### Generate Test Traffic:
```powershell
# Generate traffic to app1
1..10 | ForEach-Object { 
    curl http://172.25.25.140/app1/api/app-info -UseBasicParsing | Out-Null 
}

# Generate traffic to all apps
1..5 | ForEach-Object { 
    $app = $_
    curl "http://172.25.25.140/app$app/api/app-info" -UseBasicParsing | Out-Null
}
```

### Check Log Files:
```powershell
# List all log files
Get-ChildItem C:\Users\muhammadahmad4\applications\app*\*.log

# View app1 logs
Get-Content C:\Users\muhammadahmad4\applications\app1\app1.log -Tail 10
Get-Content C:\Users\muhammadahmad4\applications\app1\app1-json.log -Tail 5
```

---

## 🔧 Troubleshooting

### Issue: No logs in Grafana

**Check 1: Apps running?**
```powershell
1..5 | ForEach-Object { curl "http://127.0.0.1:500$_/api/app-info" }
```

**Check 2: Loki receiving logs?**
```powershell
curl http://localhost:3100/loki/api/v1/label/job/values
# Should show: app1, app2, app3, app4, app5
```

**Check 3: Promtail logs**
```powershell
docker logs promtail-apps --tail 20
```

**Check 4: Grafana datasource**
```powershell
# In Grafana UI:
# Settings → Data Sources → Loki → Test
# Should show: ✅ Data source is working
```

---

## 📁 Important Files

### Configuration Files:
```
monitoring/
├── docker-compose.yml              # Container orchestration
├── loki/
│   └── loki-config.yml            # Loki storage config
├── promtail/
│   └── promtail-config.yml        # Log collection config
└── grafana/
    └── provisioning/
        └── datasources/
            └── datasources.yml    # Grafana datasources
```

### Application Files:
```
app1/
├── main.py                         # App with logging
├── app1.log                        # Human-readable logs
└── app1-json.log                   # Structured JSON logs
```

---

## 🎉 Success Criteria

- [✅] All 5 apps running
- [✅] Loki container up (port 3100)
- [✅] Promtail collecting logs
- [✅] Grafana running (port 3000)
- [✅] Loki datasource configured in Grafana
- [✅] All 5 apps logs visible in Loki
- [✅] Can query logs in Grafana Explore
- [✅] JSON logs parsed correctly

---

## 🚀 Quick Start Commands

```powershell
# Start monitoring stack
cd C:\Users\muhammadahmad4\applications\monitoring
docker-compose up -d

# Start app1
cd C:\Users\muhammadahmad4\applications\app1
..\.venv\Scripts\python.exe main.py

# (Repeat for app2-5 in separate terminals)

# Generate traffic
1..5 | ForEach-Object {
    curl "http://172.25.25.140/app$_/api/app-info" -UseBasicParsing | Out-Null
}

# Open Grafana
Start-Process http://localhost:3000/explore
```

---

## 📊 Dashboard Ideas

### 1. Application Logs Dashboard
- Panel 1: Recent logs from all apps
- Panel 2: Error count by app
- Panel 3: Log rate per app
- Panel 4: Top error messages

### 2. Per-App Dashboard
- Panel 1: App1 recent logs
- Panel 2: App1 error rate
- Panel 3: App1 request count
- Panel 4: App1 log volume

---

## 🔐 Access Details

**Grafana**:
- URL: http://localhost:3000
- Username: `admin`
- Password: `admin123`

**Loki API**:
- URL: http://localhost:3100
- No auth required

**Apps**:
- App1: http://172.25.25.140/app1/
- App2: http://172.25.25.140/app2/
- App3: http://172.25.25.140/app3/
- App4: http://172.25.25.140/app4/
- App5: http://172.25.25.140/app5/

---

## ✅ Final Verification

Run this to verify everything:
```powershell
# Check containers
docker-compose ps

# Check Loki
curl http://localhost:3100/ready

# Check apps in Loki
1..5 | ForEach-Object {
    $query = "{job=`"app$_`"}"
    $result = curl "http://localhost:3100/loki/api/v1/query_range?query=$query&limit=1" | ConvertFrom-Json
    if($result.data.result.Count -gt 0) {
        Write-Host "✓ App$_ logs found"
    }
}

# Open Grafana
Start-Process http://localhost:3000/explore
```

---

**🎊 SETUP COMPLETE AND VERIFIED! 🎊**

**Date**: October 9, 2025  
**Status**: ✅ All systems operational  
**Components**: Apps (5) → Promtail → Loki → Grafana
