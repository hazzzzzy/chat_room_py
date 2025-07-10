# 绑定地址和端口
bind = '0.0.0.0:10086'

# 日志级别
loglevel = 'info'

workers = 1  # ws型应用通常使用单个 worker
threads = 5  # 适合 I/O 密集型任务（数据库查询、网络请求）
worker_class = "eventlet"  # ws型 worker 适合 WebSocket 和长连接
timeout = 30  # 防止请求卡死
keepalive = 5  # 连接保持时间
max_requests = 1000
max_requests_jitter = 100


# 定义自定义的日志格式
access_log_format = '%(h)s - %(t)s %(r)s %(s)s'

# 配置日志
accesslog = '-'  # 将访问日志输出到 stdout
errorlog = '-'  # 将错误日志输出到 stdout
