# beenote

### 项目介绍
1. 基于django rest framework + vue 的笔记软件
2. 前端基于 https://github.com/PanJiaChen/vue-element-admin

### 开发环境
```
python 3.6
mysql 5.7.24
django 2.1.4
```

### 部署安装

1. 拉取代码
```
git clone https://github.com/X-Mars/beenote.git
```
2. 导入数据库文件
```
beenote/beenote/beenote.sql
```
3. 启动 django
```
pip3 install -r requirements.txt

python3 beenote/beenote/beenote/manage.py runserver 0.0.0.0 8000
```

4. nginx 反向代理
```
    location / {
	root /beenote/BeeNote-Web/dist;
	index  index.html index.htm;
    }

	location /api-v1 {
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
### 后台地址
```
http://ip:8000/admin
```
### 用户名密码
```
用户名：admin 
密码： mifengbiji
```