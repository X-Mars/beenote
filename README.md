# 密封笔记 beenote

## 项目介绍

1. 基于vue3 + django rest framework 的**markdown**笔记软件
2. 由cursor协助开发
3. 近期将进行频繁更新，欢迎star、watch

## 项目定位

1. **个人笔记** 和 **公司内部知识分享**

## demo

<http://beenote.huoxingxiaoliu.com:8000>
用户名：admin
密码：mifengbiji123

## qq群

欢迎加入beenote-笔记与知识仓库，群聊号码：702860714
<img src="https://github.com/X-Mars/beenote/blob/master/images/qrcode_1546360555884.jpg?raw=true" width="40%" height="40%">

## 截图展示

<img src="https://github.com/X-Mars/beenote/blob/master/images/1.jpg?raw=true" width="70%" height="70%">
<img src="https://github.com/X-Mars/beenote/blob/master/images/2.jpg?raw=true" width="70%" height="70%">

## 开发环境

```
python 3.12
sqlite
django 5.1.4
```

## 部署安装

1. 拉取代码

```
git clone https://github.com/X-Mars/beenote.git
```

2. 初始化后端

```
cd beenote/server
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```

3. 启动项目

```
python3 manage.py runserver
```

5. nginx 反向代理

```
location / {
  root /beenote/web/dist;
  index  index.html index.htm;
}

location /api {
  proxy_pass  http://localhost:8000;
  proxy_redirect     off;
  proxy_set_header   Host             $host;
  proxy_set_header   X-Real-IP        $remote_addr;
  proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
  proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
  proxy_max_temp_file_size 0;
  proxy_connect_timeout      90;
  proxy_send_timeout         900;
  proxy_read_timeout         900;
  proxy_buffer_size          34k;
  proxy_buffers              4 32k;
  proxy_busy_buffers_size    64k;
  proxy_temp_file_write_size 64k;
}
```

## 后台地址

```
<http://ip:8000/admin>
```

## 默认用户名密码

```
用户名：admin 
密码： mifengbiji
```

License
---
[996ICU License](LICENSE)  
