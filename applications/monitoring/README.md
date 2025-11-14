# 📊 Prometheus + Grafana Monitoring Setup

Complete monitoring solution for all 5 applications with individual dashboards.

---

## 🏗️ **Architecture**

```
Applications (Host Machine)          Docker Containers
┌─────────────────────┐             ┌──────────────────┐
│  App1 :5001         │────────────▶│   Prometheus     │
│  App2 :5002         │             │   :9090          │
│  App3 :5003         │◀────────────│                  │
│  App4 :5004         │             │   Scrapes        │
│  App5 :5005         │             │   Metrics        │
└─────────────────────┘             └──────────────────┘
        │                                    │
        │                                    ▼
        │                            ┌──────────────────┐
        └───────────────────────────▶│    Grafana       │
                                     │    :3000         │
                                     │                  │
                                     │  5 Dashboards    │
                                     └──────────────────┘
```

---

## 📋 **Prerequisites**

✅ Docker & Docker Compose installed  
✅ All 5 apps running on ports 5001-5005  
✅ Prometheus client installed in apps (`pip install prometheus-client`)

---

## 🚀 **Quick Start**

### 1. Install Prometheus Client in Apps

```powershell
cd c:\Users\muhammadahmad4\applications
.\.venv\Scripts\Activate.ps1
pip install prometheus-client
```

### 2. Start Monitoring Stack

```powershell
cd c:\Users\muhammadahmad4\applications\monitoring
docker-compose up -d
```

### 3. Access Dashboards

- **Grafana**: http://localhost:3000
  - Username: `admin`
  - Password: `admin123`
  
- **Prometheus**: http://localhost:9090

---

## 📊 **Dashboards**

Har app ka apna isolated dashboard hai:

| Dashboard | URL | Metrics |
|-----------|-----|---------|
| App1 | http://localhost:3000/d/app1-dashboard | Request rate, Active users, Endpoint hits, Latency |
| App2 | http://localhost:3000/d/app2-dashboard | Request rate, Active users, Endpoint hits, Latency |
| App3 | http://localhost:3000/d/app3-dashboard | Request rate, Active users, Endpoint hits, Latency |
| App4 | http://localhost:3000/d/app4-dashboard | Request rate, Active users, Endpoint hits, Latency |
| App5 | http://localhost:3000/d/app5-dashboard | Request rate, Active users, Endpoint hits, Latency |

### Dashboard Search

Grafana mein search box mein app name type karein:
- Search: "App1" → App1 Dashboard dikhega
- Search: "App2" → App2 Dashboard dikhega
- Tags bhi use kar sakte hain: `app1`, `app2`, etc.

---

## 📈 **Tracked Metrics**

Har app ke liye ye metrics track hote hain:

### 1. **Request Count**
```
app<N>_request_count
```
- Total HTTP requests by method, endpoint, status code

### 2. **Request Latency**
```
app<N>_request_latency_seconds
```
- Response time distribution per endpoint

### 3. **Active Users**
```
app<N>_active_users
```
- Unique users (by IP address)

### 4. **Endpoint Hits**
```
app<N>_endpoint_hits
```
- Individual endpoint usage tracking

---

## 🔧 **Management Commands**

### Start Monitoring
```powershell
cd c:\Users\muhammadahmad4\applications\monitoring
docker-compose up -d
```

### Stop Monitoring
```powershell
docker-compose down
```

### View Logs
```powershell
# Prometheus logs
docker logs prometheus-apps

# Grafana logs
docker logs grafana-apps
```

### Restart Services
```powershell
docker-compose restart
```

### Remove Everything (including data)
```powershell
docker-compose down -v
```

---

## 📁 **Directory Structure**

```
monitoring/
├── docker-compose.yml              # Main Docker Compose file
├── prometheus.yml                  # Prometheus config (all apps)
├── app1-prometheus.yml            # App1 specific config
├── app2-prometheus.yml            # App2 specific config
├── app3-prometheus.yml            # App3 specific config
├── app4-prometheus.yml            # App4 specific config
├── app5-prometheus.yml            # App5 specific config
└── grafana/
    ├── provisioning/
    │   ├── datasources/
    │   │   └── prometheus.yml     # Auto-configure Prometheus
    │   └── dashboards/
    │       └── dashboards.yml     # Auto-load dashboards
    └── dashboards/
        ├── app1-dashboard.json    # App1 isolated dashboard
        ├── app2-dashboard.json    # App2 isolated dashboard
        ├── app3-dashboard.json    # App3 isolated dashboard
        ├── app4-dashboard.json    # App4 isolated dashboard
        └── app5-dashboard.json    # App5 isolated dashboard
```

---

## 🎯 **Dashboard Features**

Har dashboard mein:

1. **Request Rate Graph** - Real-time request rate per endpoint
2. **Active Users Gauge** - Current active users
3. **Total Endpoint Hits** - 5-minute window stats
4. **Endpoint Distribution** - Pie chart showing usage
5. **Latency Graph** - 95th percentile response times

---

## 🔍 **Verify Setup**

### 1. Check Apps are exposing metrics
```powershell
curl http://localhost:5001/metrics
curl http://localhost:5002/metrics
curl http://localhost:5003/metrics
curl http://localhost:5004/metrics
curl http://localhost:5005/metrics
```

### 2. Check Prometheus Targets
Visit: http://localhost:9090/targets

All 5 apps should show as **UP**

### 3. Check Grafana Datasource
Visit: http://localhost:3000/datasources

Prometheus should be configured and working

---

## 🐛 **Troubleshooting**

### Apps not showing in Prometheus?
```powershell
# Check if apps are running
netstat -ano | findstr "5001 5002 5003 5004 5005"

# Check Docker can access host
docker exec prometheus-apps ping host.docker.internal
```

### Dashboards not loading?
```powershell
# Check Grafana logs
docker logs grafana-apps

# Restart Grafana
docker-compose restart grafana
```

### Metrics not updating?
```powershell
# Reload Prometheus config
docker exec prometheus-apps kill -HUP 1
```

---

## 🎨 **Customization**

### Change Scrape Interval
Edit `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s  # Change this
```

### Add More Metrics
Edit app's `main.py` and add custom Prometheus metrics

### Modify Dashboards
Grafana UI → Edit Dashboard → Save

---

## 📝 **Important Notes**

1. **Isolation**: Har app ka dashboard completely isolated hai
2. **Search**: Grafana search mein app name ya tags use karein
3. **Data Retention**: Default 15 days (customize in prometheus.yml)
4. **Auto-reload**: Dashboards automatically load on Grafana startup

---

## 🌐 **Access URLs**

- **Grafana**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090
- **App1 Metrics**: http://localhost:5001/metrics
- **App2 Metrics**: http://localhost:5002/metrics
- **App3 Metrics**: http://localhost:5003/metrics
- **App4 Metrics**: http://localhost:5004/metrics
- **App5 Metrics**: http://localhost:5005/metrics

---

**Setup Complete! 🎉**

Sab apps ab monitored hain with individual dashboards!
