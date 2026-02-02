# gunicorn.conf.py
# Gunicorn configuration for authserver

# Socket
bind = "0.0.0.0:8000"

# Workers
workers = 2
worker_class = "sync"
worker_connections = 1000

# Timeout
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "authserver"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"
user = None
group = None

# Max requests
max_requests = 1000
max_requests_jitter = 50

# Preload application for better memory usage
# Loads app once before spawning workers to save memory
# and improve startup time
preload_app = True
