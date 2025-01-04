#!/bin/bash

# 启动 nginx
service nginx start

# 启动 Django 后端
cd /app && exec python manage.py runserver 0.0.0.0:8000
