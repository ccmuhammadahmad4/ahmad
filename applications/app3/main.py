from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
import uvicorn
import os
import logging
import json
from datetime import datetime
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app3.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("app3")

# JSON Logger for structured logs (Loki-friendly)
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "app": "app3",
            "port": 5003
        }
        if hasattr(record, 'endpoint'):
            log_data['endpoint'] = record.endpoint
        if hasattr(record, 'method'):
            log_data['method'] = record.method
        if hasattr(record, 'status_code'):
            log_data['status_code'] = record.status_code
        if hasattr(record, 'duration'):
            log_data['duration_ms'] = record.duration
        return json.dumps(log_data)

# Add JSON file handler
json_handler = logging.FileHandler('app3-json.log')
json_handler.setFormatter(JSONFormatter())
logger.addHandler(json_handler)

app = FastAPI(title="Application 3", description="Simple Application Number 1")

logger.info("Application 3 starting up...")

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'app3_request_count', 
    'app3 Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'app3_request_latency_seconds', 
    'app3 Request latency',
    ['endpoint']
)
ACTIVE_USERS = Gauge('app3_active_users', 'app3 Active Users')
ENDPOINT_HITS = Counter('app3_endpoint_hits', 'app3 Endpoint Hits', ['endpoint'])

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
    
    # Log incoming request
    logger.info(f"Incoming request: {request.method} {endpoint} from {user_ip}")
    
    # Process request
    response = await call_next(request)
    
    # Record metrics
    process_time = time.time() - start_time
    duration_ms = round(process_time * 1000, 2)
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(process_time)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        http_status=response.status_code
    ).inc()
    
    # Structured logging
    log_record = logger.makeRecord(
        logger.name, logging.INFO, "", 0, 
        f"{request.method} {endpoint} - {response.status_code} - {duration_ms}ms",
        (), None
    )
    log_record.endpoint = endpoint
    log_record.method = request.method
    log_record.status_code = response.status_code
    log_record.duration = duration_ms
    logger.handle(log_record)
    
    return response

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    logger.info("Serving homepage")
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/api/app-info")
async def get_app_info():
    logger.info("App info requested")
    return {
        "app_number": 1,
        "app_name": "Application 3",
        "port": 5003,
        "message": "Welcome to Application Number 1!",
        "active_users": len(active_users)
    }

# Prometheus metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    logger.info("Starting uvicorn server on port 5003")
    uvicorn.run(app, host="0.0.0.0", port=5003)
