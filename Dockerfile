# 使用 Python 3.12 基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Asia/Shanghai \
    PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ \
    PIP_TRUSTED_HOST=mirrors.aliyun.com

# 安装系统依赖和 nginx
RUN apt update && \
    apt install -y --no-install-recommends \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# 配置 nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# 复制前端构建产物
COPY web/dist/ /app/web/dist/

# 复制并安装后端依赖
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY server/ .

# 复制启动脚本
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 暴露端口
EXPOSE 80 8000

# 启动命令
ENTRYPOINT ["/start.sh"] 