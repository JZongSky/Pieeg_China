# 使用官方Python 3.12镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=src.main
ENV FLASK_ENV=production

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p src/static/uploads/products src/static/uploads/temp

# 设置权限
RUN chmod +x init_db.py

# 暴露端口
EXPOSE 5000

# 创建启动脚本
RUN echo '#!/bin/bash\n\
echo "等待数据库连接..."\n\
sleep 10\n\
echo "初始化数据库..."\n\
python init_db.py\n\
echo "启动Flask应用..."\n\
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 src.main:app\n\
' > start.sh && chmod +x start.sh

# 启动命令
CMD ["./start.sh"] 