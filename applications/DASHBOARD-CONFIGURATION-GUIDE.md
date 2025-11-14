# Grafana Dashboard Configuration - Complete Guide

## Table of Contents
1. [Dashboard Overview](#dashboard-overview)
2. [Panel Configurations](#panel-configurations)
3. [LogQL Query Explanations](#logql-query-explanations)
4. [Dashboard Customization](#dashboard-customization)
5. [Query Optimization](#query-optimization)

---

## Dashboard Overview

### Dashboard Structure

Each of the 5 dashboards (App1-5) has **identical structure** with different job labels:

```
App1 - Enhanced Loki Dashboard (UID: app1-loki-enhanced)
├── Panel 1: Request Rate (Time Series)
├── Panel 2: Total Requests (Gauge)
├── Panel 3: Quick Stats - 1min (Stat)
├── Panel 4: App Logs Count (Stat)
├── Panel 5: Top 20 Endpoints (Table)
├── Panel 6: Top 10 Endpoints (Pie Chart)
├── Panel 7: HTTP Status Codes (Bar Chart)
├── Panel 8: NGINX Access Logs (Logs)
├── Panel 9: Application Logs (Logs)
└── Panel 10: Application Log Rate (Time Series)
```

### Dashboard Settings

**Global Settings:**
```json
{
  "refresh": "1s",           // Auto-refresh every 1 second
  "time": {
    "from": "now-15m",       // Show last 15 minutes
    "to": "now"              // Until current time
  },
  "timezone": "browser",     // Use browser timezone
  "liveNow": true           // Enable real-time updates
}
```

**Layout:**
- Grid: 24 columns
- Panel height: Auto-adjusting
- Responsive design

---

## Panel Configurations

### Panel 1: Request Rate Timeline

**Purpose:** Show real-time request rate per second

**Configuration:**
```json
{
  "title": "Request Rate (per second)",
  "type": "timeseries",
  "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
}
```

**Query:**
```logql
sum(rate({job="nginx-app1"}[1m]))
```

**Explanation:**
- `{job="nginx-app1"}` - Filter logs by job label
- `rate([1m])` - Calculate per-second rate over 1-minute window
- `sum()` - Total across all log streams

**Why this query?**
- Shows traffic patterns
- Identifies peak usage times
- Detects sudden spikes/drops

**Panel Options:**
- **Graph Style**: Lines (smooth interpolation)
- **Line Width**: 2px
- **Fill Opacity**: 10%
- **Point Size**: 5px (on hover)
- **Axis**: Auto-scale
- **Legend**: Bottom, show values (Mean, Max, Current)

**Example Output:**
```
Time        Value
10:30:00    5.2 req/s
10:30:30    8.1 req/s
10:31:00    12.3 req/s  ← Spike detected
10:31:30    6.7 req/s
```

---

### Panel 2: Total Requests Gauge

**Purpose:** Show total requests in last 5 minutes with color-coded thresholds

**Configuration:**
```json
{
  "title": "Total Requests (Last 5 min)",
  "type": "gauge",
  "gridPos": {"h": 8, "w": 6, "x": 12, "y": 0}
}
```

**Query:**
```logql
sum(count_over_time({job="nginx-app1"}[5m]))
```

**Explanation:**
- `count_over_time([5m])` - Count log lines in 5-minute window
- `sum()` - Total count

**Color Thresholds:**
```json
{
  "thresholds": [
    {"value": 0,    "color": "green"},   // 0-100: Normal
    {"value": 100,  "color": "yellow"},  // 100-500: Busy
    {"value": 500,  "color": "orange"},  // 500-1000: High
    {"value": 1000, "color": "red"}      // 1000+: Critical
  ]
}
```

**Panel Options:**
- **Min**: 0
- **Max**: Auto
- **Show Threshold Labels**: Yes
- **Show Threshold Markers**: Yes

**Use Cases:**
- Quick health check
- Load assessment
- Capacity planning

---

### Panel 3: Quick Stats - 1 Minute

**Purpose:** Show requests in last minute with background color

**Configuration:**
```json
{
  "title": "Quick Stats - 1 min",
  "type": "stat",
  "gridPos": {"h": 4, "w": 3, "x": 18, "y": 0}
}
```

**Query:**
```logql
sum(count_over_time({job="nginx-app1"}[1m]))
```

**Panel Options:**
- **Graph Mode**: None
- **Color Mode**: Background
- **Text Size**: Auto
- **Orientation**: Horizontal

**Display Format:**
```
┌─────────────────┐
│                 │
│      142        │ ← Large number
│   Requests      │ ← Unit label
│                 │
└─────────────────┘
Background color changes based on value
```

---

### Panel 4: App Logs Count

**Purpose:** Monitor application-level logging activity

**Configuration:**
```json
{
  "title": "App Logs (Last 1 min)",
  "type": "stat",
  "gridPos": {"h": 4, "w": 3, "x": 21, "y": 0}
}
```

**Query:**
```logql
sum(count_over_time({job="app1"}[1m]))
```

**Difference from Panel 3:**
- Monitors `{job="app1"}` - application logs
- Panel 3 monitors `{job="nginx-app1"}` - NGINX logs

**Why separate?**
- Application logs = internal events (errors, debug messages)
- NGINX logs = HTTP requests/responses
- Different log volumes indicate different issues

---

### Panel 5: Top 20 Endpoints Table

**Purpose:** Show which endpoints are hit most frequently (exact counts)

**Configuration:**
```json
{
  "title": "Top 20 Endpoints (Last 15 min)",
  "type": "table",
  "gridPos": {"h": 10, "w": 12, "x": 0, "y": 8}
}
```

**Query:**
```logql
topk(20, sum by (path) (count_over_time({job="nginx-app1"} | regexp `"[A-Z]+ (?P<path>/[^ ]*) HTTP"` [15m])))
```

**Query Breakdown:**

**Step 1: Filter logs**
```logql
{job="nginx-app1"}
```
→ Select NGINX access logs for app1

**Step 2: Extract endpoint path**
```logql
| regexp `"[A-Z]+ (?P<path>/[^ ]*) HTTP"`
```
→ Parse HTTP request line:
```
Input:  "GET /app1/api/app-info HTTP/1.1"
Output: path = "/app1/api/app-info"
```

**Regex Explanation:**
- `"[A-Z]+` - Matches HTTP method (GET, POST, PUT, etc.)
- ` ` - Space
- `(?P<path>/[^ ]*)` - Named capture group for path
  - `(?P<path>...)` - Creates label named "path"
  - `/[^ ]*` - Matches "/" followed by any non-space characters
- ` HTTP"` - Matches end of request line

**Step 3: Count hits per path**
```logql
count_over_time(...[15m])
```
→ Count occurrences in 15-minute window

**Step 4: Group by path**
```logql
sum by (path) (...)
```
→ Aggregate counts for same path

**Step 5: Get top 20**
```logql
topk(20, ...)
```
→ Return top 20 results sorted descending

**Table Transformations:**
```json
{
  "transformations": [
    {
      "id": "organize",
      "options": {
        "renameByName": {
          "path": "Endpoint",
          "Value": "Total Hits"
        }
      }
    }
  ]
}
```

**Column Configuration:**
```json
{
  "fieldConfig": {
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "Total Hits"},
        "properties": [
          {
            "id": "custom.displayMode",
            "value": "gradient-gauge"
          },
          {
            "id": "color",
            "value": {"mode": "continuous-GrYlRd"}
          }
        ]
      }
    ]
  }
}
```

**Example Output:**
```
┌─────────────────────────────────────┬────────────┐
│ Endpoint                            │ Total Hits │
├─────────────────────────────────────┼────────────┤
│ /app1/                             │ 1245 ██████│
│ /app1/api/app-info                 │ 892  ████  │
│ /app1/static/css/main.css          │ 456  ██    │
│ /app1/api/users                    │ 234  █     │
│ /app1/health                       │ 189  █     │
└─────────────────────────────────────┴────────────┘
```

**Color Gradient:**
- Green: Low hits
- Yellow: Medium hits
- Red: High hits

---

### Panel 6: Top 10 Endpoints Pie Chart

**Purpose:** Visualize endpoint distribution as percentages

**Configuration:**
```json
{
  "title": "Top 10 Endpoints Distribution (Last 5 min)",
  "type": "piechart",
  "gridPos": {"h": 10, "w": 12, "x": 12, "y": 8}
}
```

**Query:**
```logql
topk(10, sum by (path) (count_over_time({job="nginx-app1"} | regexp `"[A-Z]+ (?P<path>/[^ ]*) HTTP"` [5m])))
```

**Difference from Panel 5:**
- **Time window**: 5 minutes (vs 15 min) - more recent data
- **Top K**: 10 (vs 20) - focus on most popular
- **Visualization**: Pie chart (vs Table) - shows proportions

**Panel Options:**
```json
{
  "pieType": "donut",
  "displayLabels": ["name", "percent"],
  "legendDisplayMode": "table",
  "legendPlacement": "right",
  "legendValues": ["value", "percent"]
}
```

**Example Output:**
```
        ┌────────────────────────────┐
        │   Endpoint Distribution     │
        ├────────────────────────────┤
        │  /app1/         45.2% (523)│
        │  /api/app-info  32.1% (372)│
        │  /static/...    12.4% (144)│
        │  /health         6.8% (79) │
        │  /api/users      3.5% (40) │
        └────────────────────────────┘
        
   45.2%                    32.1%
    ╱────╲                 ╱────╲
   │  /  │                │ API │
    ╲____╱                 ╲____╱
```

**Use Cases:**
- Identify most accessed endpoints
- Detect unusual traffic patterns
- Optimize caching for popular routes

---

### Panel 7: HTTP Status Codes

**Purpose:** Track HTTP response status codes over time

**Configuration:**
```json
{
  "title": "HTTP Status Codes (Last 1 min)",
  "type": "barchart",
  "gridPos": {"h": 8, "w": 24, "x": 0, "y": 18}
}
```

**Query:**
```logql
sum by (status) (count_over_time({job="nginx-app1"} | regexp `HTTP/[0-9.]+ (?P<status>[0-9]{3})` [1m]))
```

**Regex Explanation:**
```
Input:  HTTP/1.1 200 1269 "-" "Mozilla..."
                 ^^^
                 |
         Captured as "status"
```

Pattern: `HTTP/[0-9.]+ (?P<status>[0-9]{3})`
- `HTTP/[0-9.]+` - Matches HTTP version (1.0, 1.1, 2.0)
- ` ` - Space
- `(?P<status>[0-9]{3})` - Captures 3-digit status code

**Color Overrides:**
```json
{
  "overrides": [
    {
      "matcher": {"id": "byRegexp", "options": "2[0-9]{2}"},
      "properties": [{"id": "color", "value": {"fixedColor": "green"}}]
    },
    {
      "matcher": {"id": "byRegexp", "options": "3[0-9]{2}"},
      "properties": [{"id": "color", "value": {"fixedColor": "blue"}}]
    },
    {
      "matcher": {"id": "byRegexp", "options": "4[0-9]{2}"},
      "properties": [{"id": "color", "value": {"fixedColor": "yellow"}}]
    },
    {
      "matcher": {"id": "byRegexp", "options": "5[0-9]{2}"},
      "properties": [{"id": "color", "value": {"fixedColor": "red"}}]
    }
  ]
}
```

**Status Code Meanings:**
- **2xx (Green)**: Success
  - 200 OK
  - 201 Created
  - 204 No Content
- **3xx (Blue)**: Redirection
  - 301 Moved Permanently
  - 302 Found
  - 304 Not Modified
- **4xx (Yellow)**: Client Error
  - 400 Bad Request
  - 401 Unauthorized
  - 404 Not Found
- **5xx (Red)**: Server Error
  - 500 Internal Server Error
  - 502 Bad Gateway
  - 503 Service Unavailable

**Example Output:**
```
Count
 800 ┤
     │  ███
 600 ┤  ███
     │  ███
 400 ┤  ███  █
     │  ███  █
 200 ┤  ███  █  █
     │  ███  █  █  █
   0 └──200──404─500─502─
      (Green)(Yellow)(Red)
```

**Alerting Criteria:**
- **Warning**: 4xx > 10% of total
- **Critical**: 5xx > 1% of total

---

### Panel 8: NGINX Access Logs (Real-time)

**Purpose:** Live streaming of NGINX access logs

**Configuration:**
```json
{
  "title": "NGINX Access Logs (Real-time)",
  "type": "logs",
  "gridPos": {"h": 12, "w": 12, "x": 0, "y": 26}
}
```

**Query:**
```logql
{job="nginx-app1"}
```

**Panel Options:**
```json
{
  "showTime": true,
  "showLabels": false,
  "showCommonLabels": false,
  "wrapLogMessage": true,
  "prettifyLogMessage": false,
  "enableLogDetails": true,
  "sortOrder": "Descending",
  "dedupStrategy": "none"
}
```

**Display Format:**
```
2025-10-09 11:22:19  172.25.25.140 - - [09/Oct/2025:11:22:19 +0500] "GET /app1/ HTTP/1.1" 200 1269
2025-10-09 11:22:20  172.25.25.140 - - [09/Oct/2025:11:22:20 +0500] "GET /app1/api/app-info HTTP/1.1" 200 845
2025-10-09 11:22:21  172.25.25.140 - - [09/Oct/2025:11:22:21 +0500] "GET /app1/static/css/main.css HTTP/1.1" 200 2341
```

**Interactive Features:**
- Click on log line to expand details
- Copy log content
- Filter by text
- View parsed fields (if JSON)

**Use Cases:**
- Debugging specific requests
- Monitoring real-time activity
- Investigating errors
- Analyzing user behavior

---

### Panel 9: Application Logs

**Purpose:** Show application-level logs (errors, debug, info)

**Configuration:**
```json
{
  "title": "Application Logs",
  "type": "logs",
  "gridPos": {"h": 12, "w": 12, "x": 12, "y": 26}
}
```

**Query:**
```logql
{job="app1"}
```

**Log Levels:**
- **DEBUG**: Detailed diagnostic info
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error events
- **CRITICAL**: Critical issues

**Example Output:**
```
2025-10-09 11:22:19 INFO    Root endpoint accessed
2025-10-09 11:22:20 INFO    App info endpoint accessed
2025-10-09 11:22:21 WARNING Database connection slow (125ms)
2025-10-09 11:22:22 ERROR   Failed to process request: KeyError 'user_id'
```

**Filtering Examples:**
```logql
{job="app1"} |= "ERROR"           # Show only errors
{job="app1"} |= "database"        # Filter by keyword
{job="app1"} != "DEBUG"           # Exclude debug logs
{job="app1"} |~ "ERROR|CRITICAL"  # Regex filter
```

---

### Panel 10: Application Log Rate

**Purpose:** Monitor application logging volume over time

**Configuration:**
```json
{
  "title": "Application Log Rate",
  "type": "timeseries",
  "gridPos": {"h": 8, "w": 24, "x": 0, "y": 38}
}
```

**Query:**
```logql
sum(count_over_time({job="app1"}[1m]))
```

**Why Monitor Log Rate?**
- **Sudden spike**: Indicates errors or unusual activity
- **Drop to zero**: Application may have crashed
- **Gradual increase**: Growing user base or increasing errors
- **Pattern changes**: Deployment impact

**Example Patterns:**

**Normal Pattern:**
```
Logs/min
  100 ┤  ╭─╮    ╭─╮
   80 ┤ ╭╯ ╰╮  ╭╯ ╰╮
   60 ┤╭╯   ╰╮╭╯   ╰╮
   40 ┤╯     ╰╯     ╰
      └──────────────────
       Business hours pattern
```

**Error Spike:**
```
Logs/min
  500 ┤        ╱╲
  400 ┤       ╱  ╲
  300 ┤      ╱    ╲
  200 ┤─────╱      ╲────
      └──────────────────
       Error burst detected
```

**Application Crash:**
```
Logs/min
  100 ┤─────────
   80 ┤─────────╲
   60 ┤         ╲
    0 ┤          ╰──────
      └──────────────────
       Application stopped
```

---

## LogQL Query Explanations

### Query Structure

**Basic Structure:**
```logql
{label_selector} | filter | parser | aggregation
```

**Examples:**

**1. Simple Filter:**
```logql
{job="nginx-app1"} |= "ERROR"
```
- Select logs with `job="nginx-app1"`
- Filter lines containing "ERROR"

**2. Regex Parsing:**
```logql
{job="nginx-app1"} | regexp `pattern`
```
- Extract fields using regular expressions

**3. Aggregation:**
```logql
sum(count_over_time({job="app1"}[5m]))
```
- Count log lines over 5 minutes
- Sum total across streams

**4. Rate Calculation:**
```logql
rate({job="nginx-app1"}[1m])
```
- Calculate per-second rate

### Advanced Queries

**Count Unique Values:**
```logql
count(count by (path) (rate({job="nginx-app1"}[5m])))
```
- Count unique endpoint paths

**Calculate Percentage:**
```logql
(sum(count_over_time({job="nginx-app1"} |= "404" [5m])) / 
 sum(count_over_time({job="nginx-app1"}[5m]))) * 100
```
- Percentage of 404 errors

**Average Response Size:**
```logql
avg(sum by (bytes) (count_over_time({job="nginx-app1"} | 
    regexp `HTTP/[0-9.]+ [0-9]{3} (?P<bytes>[0-9]+)` [5m])))
```
- Extract bytes sent
- Calculate average

**Slow Requests:**
```logql
{job="app1"} | regexp `(?P<duration>[0-9]+)ms` | duration > 1000
```
- Extract duration from logs
- Filter requests > 1 second

### Query Optimization Tips

**1. Label Filtering First:**
```logql
# GOOD: Filter labels first
{job="nginx-app1", status="200"} |= "api"

# BAD: Parse before filtering
{job="nginx-app1"} | regexp `...` | status="200"
```

**2. Use Contains Before Regex:**
```logql
# GOOD: Simple filter first
{job="nginx-app1"} |= "POST" | regexp `pattern`

# BAD: Complex regex only
{job="nginx-app1"} | regexp `POST.*pattern`
```

**3. Limit Time Range:**
```logql
# GOOD: Short window for high-frequency queries
rate({job="nginx-app1"}[1m])

# BAD: Long window (slow)
rate({job="nginx-app1"}[1h])
```

**4. Use Appropriate Aggregation:**
```logql
# GOOD: Use topk for limited results
topk(10, sum by (path) (...))

# BAD: Return all results
sum by (path) (...)
```

---

## Dashboard Customization

### Adding New Panels

**Step 1: Determine Panel Type**
- **Time Series**: Trends over time (rates, counts)
- **Gauge**: Current value with thresholds
- **Stat**: Single numeric value
- **Table**: Structured data
- **Pie Chart**: Proportional distribution
- **Bar Chart**: Categorical comparison
- **Logs**: Raw log streaming

**Step 2: Write Query**
```logql
# Example: Track POST requests
sum(rate({job="nginx-app1"} |= "POST" [1m]))
```

**Step 3: Configure Panel**
- Set title
- Choose visualization
- Configure axes/thresholds
- Add transformations if needed

**Step 4: Position Panel**
```json
{
  "gridPos": {
    "h": 8,   // Height in grid units
    "w": 12,  // Width (max 24)
    "x": 0,   // Horizontal position
    "y": 0    // Vertical position
  }
}
```

### Custom Time Ranges

**Quick Ranges:**
```json
{
  "time": {
    "from": "now-5m",   // Last 5 minutes
    "from": "now-1h",   // Last hour
    "from": "now-24h",  // Last day
    "from": "now-7d",   // Last week
    "from": "now/d",    // Today (start of day)
  }
}
```

**Absolute Ranges:**
```json
{
  "time": {
    "from": "2025-10-09T00:00:00.000Z",
    "to": "2025-10-09T23:59:59.999Z"
  }
}
```

### Threshold Configuration

**Gauge Thresholds:**
```json
{
  "thresholds": {
    "mode": "absolute",
    "steps": [
      {"value": null, "color": "green"},
      {"value": 100, "color": "yellow"},
      {"value": 500, "color": "red"}
    ]
  }
}
```

**Percentage Thresholds:**
```json
{
  "thresholds": {
    "mode": "percentage",
    "steps": [
      {"value": 0, "color": "green"},
      {"value": 50, "color": "yellow"},
      {"value": 80, "color": "red"}
    ]
  }
}
```

### Variables (Template Variables)

**Create Variable:**
```json
{
  "templating": {
    "list": [
      {
        "name": "app",
        "type": "custom",
        "options": ["app1", "app2", "app3", "app4", "app5"],
        "current": {"value": "app1"}
      }
    ]
  }
}
```

**Use in Query:**
```logql
{job="nginx-$app"}
```

**Dynamic Variable:**
```json
{
  "name": "endpoint",
  "type": "query",
  "datasource": "Loki",
  "query": "{job=\"nginx-app1\"} | regexp `(?P<path>/[^ ]*)` | label_format path=$path"
}
```

---

## Query Optimization

### Performance Best Practices

**1. Use Shorter Time Windows for Real-time Panels:**
```logql
# Fast: 1-minute window
rate({job="nginx-app1"}[1m])

# Slower: 1-hour window
rate({job="nginx-app1"}[1h])
```

**2. Limit Results:**
```logql
# Returns top 10 only
topk(10, sum by (path) (...))

# Returns all (potentially thousands)
sum by (path) (...)
```

**3. Use Label Filters:**
```logql
# Fast: Label filtering (indexed)
{job="nginx-app1", status="200"}

# Slow: Log content filtering (not indexed)
{job="nginx-app1"} |= "200"
```

**4. Avoid Complex Regex in High-Frequency Queries:**
```logql
# Better: Simple contains
{job="nginx-app1"} |= "GET"

# Slower: Complex regex
{job="nginx-app1"} | regexp `GET.*api.*v[0-9]+`
```

### Caching Strategies

**Panel Caching:**
```json
{
  "cacheTimeout": "60",  // Cache for 60 seconds
}
```

**Query Caching:**
Configure in Loki:
```yaml
query_range:
  results_cache:
    cache:
      enable_fifocache: true
      fifocache:
        max_size_bytes: 1GB
        validity: 24h
```

### Troubleshooting Slow Queries

**Check Query Stats:**
1. Open Query Inspector (Grafana)
2. Look for:
   - Query duration
   - Bytes processed
   - Lines processed

**Optimize Based on Stats:**
- **High duration**: Reduce time range or use simpler regex
- **Many bytes**: Add label filters earlier
- **Many lines**: Use `|=` filter before parsing

---

## Summary

### Dashboard Capabilities

**Real-time Monitoring:**
- 1-second refresh rate
- Live log streaming
- Instant alerts on thresholds

**Traffic Analysis:**
- Request rate trends
- Endpoint popularity
- Status code distribution

**Performance Metrics:**
- Response times (if logged)
- Error rates
- Traffic patterns

**Log Management:**
- Centralized log viewing
- Advanced filtering
- Historical analysis

### Next Steps

**Enhancements to Consider:**
1. Add response time tracking
2. Configure alerting rules
3. Add user agent analysis
4. Implement geographic tracking (if using proxy headers)
5. Create comparison dashboards (app1 vs app2)
6. Add SLA monitoring panels

**Advanced Features:**
1. Multi-tenancy support
2. Log sampling for high-volume apps
3. Custom retention policies per job
4. Alert integration (Slack, email, PagerDuty)

---

**Document Version:** 1.0  
**Last Updated:** October 9, 2025  
**Related Documents:**
- LOKI-GRAFANA-COMPLETE-SETUP.md
- NGINX-COMPLETE-GUIDE.md
- TROUBLESHOOTING-GUIDE.md
