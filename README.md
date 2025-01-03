# 蜜蜂🐝笔记 beenote

## 项目介绍

1. 基于vue3 + django rest framework 的**markdown**笔记软件
2. 由**cursor**协助开发
3. 欢迎提意见和需求
4. 近期将进行频繁更新，欢迎star、watch

## 功能定位

1. **个人笔记** 和 **公司内部知识分享**
2. 用户分为**普通用户**、**管理员用户**、**超级管理员**三种角色
3. 用户角色可以创建**笔记和笔记分组**
4. 管理员可以看到全部用户的笔记和笔记分组，并可以为其他用户分配**笔记和笔记分组**权限
5. 超级管理员可以配置第三方登录
6. 用户只可以看到管理员授权的**笔记和笔记分组**

## demo（待上线）

<https://beenote.huoxingxiaoliu.com/login?username=admin&password=mifengbiji>  
用户名：admin  
密码：mifengbiji  

## 跟着火星小刘学运维开发

<https://space.bilibili.com/439068477>

## qq群

欢迎加入beenote-笔记与知识仓库。
<a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=a_y5qjuIfBYZHkhGg4JTZqGjTk3KUI5T&jump_from=webapi&authKey=qJpb8UQWFJcxKBdT/zq9kGBqiMxOm9k3TkfYeAtaVtHAbKbIfxMiGBolmP+aWa5b"><img border="0" src="https://pub.idqqimg.com/wpa/images/group.png" alt="vue+django+zabbix+grafana" title="vue+django+zabbix+grafana"></a>

<div style="display: flex; gap: 20px;">
  <a href="https://qm.qq.com/cgi-bin/qm/qr?k=a_y5qjuIfBYZHkhGg4JTZqGjTk3KUI5T&jump_from=webapi&authKey=qJpb8UQWFJcxKBdT/zq9kGBqiMxOm9k3TkfYeAtaVtHAbKbIfxMiGBolmP+aWa5b" target="_blank">
    <img src="https://github.com/X-Mars/beenote/blob/master/images/qrcode.jpg?raw=true" alt="QR Code" width="40%" height="40%">
  </a>
  <a href="https://space.bilibili.com/439068477" target="_blank">
    <img src="https://github.com/X-Mars/Zabbix-Alert-WeChat/blob/master/images/5.jpg?raw=true" alt="B站火星小刘" width="53.4%" height="53.4%">
  </a>
</div>

## 截图展示

![登录页](https://github.com/X-Mars/beenote/blob/master/images/1.png?raw=true)
![仪表盘](https://github.com/X-Mars/beenote/blob/master/images/2.png?raw=true)
![笔记管理](https://github.com/X-Mars/beenote/blob/master/images/3.png?raw=true)
![笔记授权](https://github.com/X-Mars/beenote/blob/master/images/4.png?raw=true)
![三方登录](https://github.com/X-Mars/beenote/blob/master/images/5.png?raw=true)

## 开发环境

```shell
python 3.12
sqlite 3
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
