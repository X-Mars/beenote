#!/bin/bash

# 检查必需的环境变量
if [ -z "$BEENOTE_SECRET_KEY" ]; then
    echo "错误: 环境变量 BEENOTE_SECRET_KEY 未设置"
    echo "请设置环境变量 BEENOTE_SECRET_KEY 后再运行程序"
    exit 1
fi

# 启动 nginx
service nginx start

# 同步数据库，并启动 Django 后端
cd /app && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
