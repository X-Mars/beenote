# beenote

### 项目介绍
1. 基于django rest framework + vue 的笔记软件
2. 前端基于 https://github.com/PanJiaChen/vue-element-admin
3. 支持**富文本**和**markdown**
4. 仅完成了 **新建笔记** 和 **我的文件夹** 功能
5. 近期会开放完成功能
6. 欢迎star、watch

### qq群
欢迎加入beenote-笔记与知识仓库，群聊号码：702860714
<img src="https://github.com/X-Mars/beenote/blob/master/images/qrcode_1546360555884.jpg?raw=true" width="70%" height="70%">

### 截图展示

<img src="https://github.com/X-Mars/beenote/blob/master/images/1.jpg?raw=true" width="70%" height="70%">
<img src="https://github.com/X-Mars/beenote/blob/master/images/2.jpg?raw=true" width="70%" height="70%">

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
密码： Admin123456
```
