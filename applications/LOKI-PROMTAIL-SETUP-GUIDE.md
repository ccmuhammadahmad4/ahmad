# 📝 Promtail + Loki Logging Setup Guide

## 🎯 Overview

**Loki** is a log aggregation system designed to store and query logs efficiently. **Promtail** is the agent that collects logs and sends them to Loki.

Together they provide:
- ✅ Centralized log aggregation
- ✅ Real-time log streaming
- ✅ Label-based querying (like Prometheus)
- ✅ Grafana integration for visualization
- ✅ Low resource usage (compared to ELK stack)

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Application Layer                         │
├──────────────┬──────────────┬──────────────┬─────────────────┤
│   App1       │   App2       │   App3       │   App4   App5   │
│   :5001      │   :5002      │   :5003      │   :5004  :5005  │
│              │              │              │                  │
│   Writes logs to files:                                       │
│   - app1.log (human-readable)                                 │
│   - app1-json.log (structured JSON)                           │
└──────────────┴──────────────┴──────────────┴─────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                        Promtail                               │
│                   (Log Collector)                             │
│                                                               │
│   Monitors log files:                                         │
│   - /apps/app*/*.log                                          │
│   - /nginx-logs/*.log                                         │
│   - Parses JSON logs                                          │
│   - Adds labels (app, job, level)                            │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                          Loki                                 │
│                   (Log Aggregation)                           │
│                       Port: 3100                              │
│                                                               │
│   Stores logs with:                                           │
│   - Label indexing                                            │
│   - 31-day retention                                          │
│   - Compression                                               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                        Grafana                                │
│                   (Visualization)                             │
│                       Port: 3000                              │
│                                                               │
│   Queries logs via:                                           │
│   - LogQL (Loki Query Language)                               │
│   - Dashboards                                                │
│   - Explore interface                                         │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Components Added

### 1. **Loki** (Port 3100)

**Purpose**: Log aggregation server

**Features**:
- Stores logs with labels (like Prometheus for metrics)
- 31-day retention period
- Built-in compression
- Low resource usage

**Configuration**: `monitoring/loki/loki-config.yml`

**Access**: http://localhost:3100

### 2. **Promtail** (Port 9080)

**Purpose**: Log collection agent

**Features**:
- Watches log files
- Parses JSON logs
- Adds labels automatically
- Ships logs to Loki

**Configuration**: `monitoring/promtail/promtail-config.yml`

**Monitors**:
- App logs: `/apps/app{1-5}/*.log`
- NGINX logs: `/nginx-logs/*.log`
- JSON structured logs

### 3. **Application Logging**

**Added to all 5 apps:**

**Features**:
- Dual logging (human + JSON)
- Structured log format
- Request/response tracking
- Error logging
- Performance metrics in logs

**Log Files**:
- `app1.log` - Human-readable
- `app1-json.log` - JSON structured (for Loki)

---

## 🚀 Setup Instructions

### Step 1: Start Monitoring Stack

```powershell
cd c:\Users\muhammadahmad4\applications\monitoring
docker-compose down -v  # Clean restart
docker-compose up -d
```

**Expected Output**:
```
✓ Container loki-apps       Started
✓ Container promtail-apps   Started
✓ Container prometheus-apps Started
✓ Container grafana-apps    Started
```

### Step 2: Verify Containers

```powershell
docker-compose ps
```

**Expected**:
```
NAME              STATUS
grafana-apps      Up
loki-apps         Up
prometheus-apps   Up
promtail-apps     Up
```

### Step 3: Check Loki is Running

```powershell
curl http://localhost:3100/ready
```

**Expected**: `ready`

### Step 4: Restart Applications

Apps need restart to create log files:

```powershell
# Stop any running apps first (Ctrl+C in each terminal)

# Start app1
cd c:\Users\muhammadahmad4\applications\app1
..\.venv\Scripts\python.exe main.py

# Repeat for app2-5 in separate terminals
```

### Step 5: Verify Logs are Being Created

```powershell
# Check if log files exist
Get-ChildItem c:\Users\muhammadahmad4\applications\app*\*.log

# View recent logs
Get-Content c:\Users\muhammadahmad4\applications\app1\app1.log -Tail 10
```

### Step 6: Check Promtail is Collecting Logs

```powershell
# Check Promtail targets
curl http://localhost:9080/targets
```

---

## 📊 Using Loki in Grafana

### Access Grafana Explore

1. Open: http://localhost:3000
2. Click "Explore" (compass icon)
3. Select "Loki" datasource from dropdown

### LogQL Queries

**Show all logs from App1**:
```logql
{job="app1"}
```

**Show all logs from all apps**:
```logql
{app=~"application.*"}
```

**Show only ERROR logs**:
```logql
{job="app1"} |= "ERROR"
```

**Show logs from specific endpoint**:
```logql
{job="app1"} |= "/api/app-info"
```

**Show NGINX errors**:
```logql
{job="nginx", log_type="error"}
```

**Count errors per second**:
```logql
sum(rate({job="app1"} |= "ERROR" [5m]))
```

**Show requests by status code**:
```logql
{job="app1"} | json | status_code="200"
```

---

## 🎨 Create Log Dashboard

### Example Panel Configuration:

**Panel 1: Recent Application Logs**
```
Query: {app=~"application.*"}
Type: Logs
Time range: Last 15 minutes
```

**Panel 2: Error Rate**
```
Query: sum(rate({job=~"app.*"} |= "ERROR" [5m])) by (job)
Type: Time series
```

**Panel 3: Request Count by Endpoint**
```
Query: sum by (endpoint) (rate({job="app1"} | json [5m]))
Type: Bar chart
```

**Panel 4: Top Error Messages**
```
Query: topk(10, sum by (message) (rate({job=~"app.*"} |= "ERROR" [5m])))
Type: Table
```

---

## 📝 Log Format

### Human-Readable Log (app1.log):
```
2025-10-09 10:30:15 - app1 - INFO - Incoming request: GET /api/app-info from 172.25.25.1
2025-10-09 10:30:15 - app1 - INFO - App info requested
2025-10-09 10:30:15 - app1 - INFO - GET /api/app-info - 200 - 15.32ms
```

### JSON Structured Log (app1-json.log):
```json
{
  "timestamp": "2025-10-09T10:30:15.123456",
  "level": "INFO",
  "logger": "app1",
  "message": "GET /api/app-info - 200 - 15.32ms",
  "app": "app1",
  "port": 5001,
  "endpoint": "/api/app-info",
  "method": "GET",
  "status_code": 200,
  "duration_ms": 15.32
}
```

---

## 🔍 LogQL Examples

### Basic Queries

**All logs from App1**:
```logql
{job="app1"}
```

**Logs with "error" in message**:
```logql
{job="app1"} |= "error"
```

**Logs WITHOUT "metrics" in message**:
```logql
{job="app1"} != "metrics"
```

**Regex search**:
```logql
{job="app1"} |~ "ERROR|CRITICAL"
```

### JSON Parsing

**Extract and filter by status code**:
```logql
{job="app1"} | json | status_code="500"
```

**Filter by duration**:
```logql
{job="app1"} | json | duration_ms > 100
```

**Extract specific field**:
```logql
{job="app1"} | json | line_format "{{.endpoint}} took {{.duration_ms}}ms"
```

### Aggregations

**Count logs per second**:
```logql
sum(rate({job="app1"}[5m]))
```

**Count by log level**:
```logql
sum by (level) (rate({job="app1"} | json [5m]))
```

**Average request duration**:
```logql
avg by (endpoint) (
  rate({job="app1"} | json | duration_ms > 0 [5m])
)
```

**Top 5 slowest endpoints**:
```logql
topk(5,
  sum by (endpoint) (rate({job="app1"} | json | duration_ms > 0 [5m]))
)
```

---

## 🎯 Use Cases

### 1. Debug Production Issues

**Find all errors in last hour**:
```logql
{app=~"application.*"} |= "ERROR" | json
```

**Trace specific request**:
```logql
{job="app1"} | json | endpoint="/api/checkout"
```

### 2. Monitor Performance

**Slow requests (> 100ms)**:
```logql
{job="app1"} | json | duration_ms > 100
```

**Count slow requests**:
```logql
sum(rate({job="app1"} | json | duration_ms > 100 [5m]))
```

### 3. Security Monitoring

**Failed authentication attempts**:
```logql
{job=~"app.*"} |= "401"
```

**Unusual traffic patterns**:
```logql
{job="nginx", log_type="access"} | json | status_code="404"
```

### 4. Business Analytics

**API usage by endpoint**:
```logql
sum by (endpoint) (count_over_time({job="app1"} | json [1h]))
```

**Active users over time**:
```logql
count by (user_ip) (rate({job="app1"} | json [5m]))
```

---

## 🔧 Troubleshooting

### Logs Not Appearing in Loki

**Check 1: Are log files being created?**
```powershell
Get-ChildItem c:\Users\muhammadahmad4\applications\app1\*.log
Get-Content c:\Users\muhammadahmad4\applications\app1\app1-json.log -Tail 5
```

**Check 2: Is Promtail running?**
```powershell
docker logs promtail-apps --tail 20
```

**Check 3: Is Loki running?**
```powershell
docker logs loki-apps --tail 20
curl http://localhost:3100/ready
```

**Check 4: Check Promtail targets**
```powershell
curl http://localhost:9080/targets | ConvertFrom-Json
```

### Promtail Not Finding Log Files

**Issue**: Volume mount path incorrect

**Fix**: Check docker-compose.yml volumes:
```yaml
volumes:
  - C:/Users/muhammadahmad4/applications:/apps:ro
```

**Verify**:
```powershell
docker exec promtail-apps ls /apps/app1
```

### Loki Query Returns No Results

**Issue**: Labels don't match

**Solution**: Check available labels
```powershell
curl http://localhost:3100/loki/api/v1/labels | ConvertFrom-Json
```

**Check label values**:
```powershell
curl "http://localhost:3100/loki/api/v1/label/job/values" | ConvertFrom-Json
```

---

## 📊 Integration with Existing Dashboards

### Add Log Panel to App Dashboards

**Panel Configuration**:
```json
{
  "type": "logs",
  "title": "App1 Recent Logs",
  "datasource": "Loki",
  "targets": [
    {
      "expr": "{job=\"app1\"}",
      "refId": "A"
    }
  ],
  "options": {
    "showTime": true,
    "showLabels": false,
    "wrapLogMessage": true
  }
}
```

### Combined Metrics + Logs Dashboard

**Use Case**: See metrics AND logs together

**Panel 1**: Request Rate (Prometheus)
```promql
rate(app1_request_count_total[5m])
```

**Panel 2**: Request Logs (Loki)
```logql
{job="app1"} | json | line_format "{{.method}} {{.endpoint}} - {{.status_code}} ({{.duration_ms}}ms)"
```

---

## 📈 Performance Considerations

### Loki Storage

**Current Setup**:
- Retention: 31 days
- Storage: Docker volume `loki-data`
- Compression: Enabled

**Estimate**:
```
Average log rate: 100 lines/sec
Line size: 200 bytes
Daily: 100 * 200 * 86400 = 1.7 GB/day
Monthly: ~50 GB (compressed ~10 GB)
```

### Promtail Resource Usage

**Typical**:
- CPU: < 5%
- Memory: 50-100 MB
- Disk I/O: Minimal

### Query Performance

**Fast Queries**:
- Label filtering: `{job="app1"}`
- Recent time range: Last 15 minutes

**Slow Queries** (avoid):
- No label filters: `{}`
- Very long time ranges: Last 30 days
- Complex regex on log content

---

## 🎓 Best Practices

### 1. Use Structured Logging (JSON)

✅ **Good**:
```json
{"level": "ERROR", "endpoint": "/api", "status": 500}
```

❌ **Bad**:
```
Something went wrong
```

### 2. Add Meaningful Labels

✅ **Good**:
```yaml
labels:
  app: app1
  environment: production
  level: error
```

❌ **Bad** (too many labels):
```yaml
labels:
  request_id: abc123
  user_id: user456
  timestamp: 2025-10-09
```

### 3. Keep Log Volume Reasonable

**Guidelines**:
- Log important events: Errors, auth, transactions
- Don't log: Every debug message, sensitive data
- Use log levels: INFO, WARN, ERROR, CRITICAL

### 4. Use Time Ranges Wisely

✅ **Good**: Last 15 minutes, Last 1 hour
❌ **Slow**: Last 30 days

### 5. Create Alerts from Logs

**Example**: Alert on high error rate
```logql
sum(rate({job=~"app.*"} |= "ERROR" [5m])) > 10
```

---

## 🔐 Security Notes

### Current Setup (Development):

⚠️ **No Authentication**: Loki/Promtail don't require auth
⚠️ **File Permissions**: Log files readable by Promtail
⚠️ **Network**: Services on localhost only

### Production Recommendations:

1. **Enable Loki Authentication**
2. **Encrypt logs in transit** (TLS)
3. **Restrict network access** (firewall rules)
4. **Redact sensitive data** from logs
5. **Set proper file permissions**

---

## 📞 Quick Reference

### Ports:
- **Loki**: 3100
- **Promtail**: 9080
- **Grafana**: 3000 (existing)

### URLs:
- **Loki API**: http://localhost:3100
- **Promtail Targets**: http://localhost:9080/targets
- **Grafana Explore**: http://localhost:3000/explore

### Common Commands:

```powershell
# Restart monitoring stack
docker-compose restart

# View Loki logs
docker logs loki-apps

# View Promtail logs
docker logs promtail-apps

# Test Loki query
curl "http://localhost:3100/loki/api/v1/query?query={job=\"app1\"}"

# Check log files
Get-ChildItem c:\Users\muhammadahmad4\applications\app*\*.log
```

---

## 🎉 Success Criteria

Your Loki + Promtail setup is working when:

- [✅] All 4 containers running (loki, promtail, prometheus, grafana)
- [✅] Log files created in each app directory
- [✅] Promtail shows targets in /targets endpoint
- [✅] Grafana Explore shows logs from Loki datasource
- [✅] Can query logs by app: `{job="app1"}`
- [✅] JSON logs parsed correctly
- [✅] Can filter by log level, endpoint, etc.

---

**🚀 You now have complete observability: Metrics (Prometheus) + Logs (Loki) + Dashboards (Grafana)!**

**Last Updated**: October 9, 2025  
**Version**: 1.0
