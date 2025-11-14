# Script to create monitored versions of all apps

for ($i = 2; $i -le 5; $i++) {
    $appDir = "app$i"
    $port = 5000 + $i
    
    $content = @"
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
import uvicorn
import os
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

app = FastAPI(title="Application $i", description="Simple Application Number $i")

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'app${i}_request_count', 
    'App$i Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'app${i}_request_latency_seconds', 
    'App$i Request latency',
    ['endpoint']
)
ACTIVE_USERS = Gauge('app${i}_active_users', 'App$i Active Users')
ENDPOINT_HITS = Counter('app${i}_endpoint_hits', 'App$i Endpoint Hits', ['endpoint'])

# Simulated active users counter
active_users = set()

# Middleware for tracking
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Track unique users (using IP as identifier)
    user_ip = request.client.host
    active_users.add(user_ip)
    ACTIVE_USERS.set(len(active_users))
    
    # Track endpoint hits
    endpoint = request.url.path
    ENDPOINT_HITS.labels(endpoint=endpoint).inc()
    
    # Process request
    response = await call_next(request)
    
    # Record metrics
    process_time = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(process_time)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        http_status=response.status_code
    ).inc()
    
    return response

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/api/app-info")
async def get_app_info():
    return {
        "app_number": $i,
        "app_name": "Application $i",
        "port": $port,
        "message": "Welcome to Application Number $i!",
        "active_users": len(active_users)
    }

# Prometheus metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=$port)
"@
    
    $content | Set-Content -Path "$appDir\main.py" -Force
    Write-Host "Created monitored version for $appDir" -ForegroundColor Green
}

Write-Host "`nAll apps updated with Prometheus metrics!" -ForegroundColor Cyan
