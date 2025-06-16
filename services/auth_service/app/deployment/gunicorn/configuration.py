bind = "0.0.0.0:8080"

workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 7200
keepalive = 600

BASE_DIR = "/app"
pythonpath = BASE_DIR
chdir = BASE_DIR
limit_request_line=8000

# Uvicorn에 http_timeout 설정 추가
worker_arguments = ["--http-timeout", "7200"]

# 로그 수준 설정
loglevel = 'debug'

accesslog = '/var/log/uvicorn_access.log'
errorlog = '/var/log/uvicorn_error.log'
