# 蜜蜂🐝笔记 beenote

## 项目介绍

1. 基于vue3 + django rest framework 的**markdown**笔记软件
2. 由**cursor**协助开发
3. 近期将进行频繁更新，欢迎star、watch

## 项目定位

1. **个人笔记** 和 **公司内部知识分享**

## demo（待上线）

<http://beenote.huoxingxiaoliu.com:8000>
用户名：admin
密码：mifengbiji

## 跟着火星小刘学运维开发

<https://space.bilibili.com/439068477>

## qq群

欢迎加入beenote-笔记与知识仓库，群聊号码：**702860714**  

<div style="display: flex; gap: 20px;">
  <img src="https://github.com/X-Mars/beenote/blob/master/images/qrcode.jpg?raw=true" alt="QR Code" width="40%" height="40%">
  <a href="https://space.bilibili.com/439068477" target="_blank">
    <img src="https://github.com/X-Mars/Zabbix-Alert-WeChat/blob/master/images/5.jpg?raw=true" alt="B站火星小刘" width="98.5%" height="98.5%">
  </a>
</div>

## 截图展示

![登录页](https://github.com/X-Mars/beenote/blob/master/images/1.png?raw=true)
![仪表盘](https://github.com/X-Mars/beenote/blob/master/images/2.png?raw=true)
![笔记管理](https://github.com/X-Mars/beenote/blob/master/images/3.png?raw=true)
![笔记授权](https://github.com/X-Mars/beenote/blob/master/images/4.png?raw=true)

## 开发环境

```shell
python 3.12
sqlite
django 5.1.4
node v22.12.0
```

## 部署安装

1. 拉取代码

```shell
git clone https://github.com/X-Mars/beenote.git
```

2. 初始化后端

```shell
cd beenote/server
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```

3. 启动项目

```shell
python3 manage.py runserver
```

4. nginx 反向代理

```conf
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

```url
<http://ip:8000/admin>
```

## 默认用户名密码

```conf
用户名：admin 
密码： mifengbiji
```

## License

[996ICU License](LICENSE)  
