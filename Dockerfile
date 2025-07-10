# 使用一个基础镜像，例如python:3.x
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将本地文件拷贝到容器中
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENV TZ=Asia/Shanghai

# 对外暴露的端口
EXPOSE 10086

# 启动应用
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
