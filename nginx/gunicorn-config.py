# Error-Free Gunicorn Configuration
import multiprocessing

# Server socket
bind = "127.0.0.1:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/gunicorn/threat_analyzer_access.log"
errorlog = "/var/log/gunicorn/threat_analyzer_error.log"
loglevel = "info"

# Process naming
proc_name = "threat_analyzer_web"

# Server mechanics
daemon = False
user = "abdulrehman"
group = "abdulrehman"

# Preload app for better performance
preload_app = True

# Graceful shutdown timeout
graceful_timeout = 30