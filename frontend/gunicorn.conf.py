# gunicorn.conf.py

# Socket
bind = "0.0.0.0:8000"

# Workers
workers = 3
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
proc_name = "frontend"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"
user = None
group = None

# SSL (если понадобится в будущем)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Max requests
max_requests = 1000
max_requests_jitter = 50

# Preload application for better memory usage
# Loads app once before spawning workers to save memory
# and improve startup time
preload_app = True
