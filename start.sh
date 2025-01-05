#!/bin/bash

# 启动 nginx
service nginx start

# 同步数据库，并启动 Django 后端
cd /app && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
