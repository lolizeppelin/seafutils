# Seafile 服务端部署工具

### 使用说明
seafile-init-* 是对应程序初始化脚本,必须由root执行
如果需要后续程序以非seafile用户运行,需要在init阶段指定用户
否则需要手动修改生成的文件夹权限
seafutil-luanch 是服务器启动的代理脚本,用于启动和关闭seafile-controller,由systemd调用


### 配置说明
1. lucach启动配置
```text
默认systemd.service设置EnvironmentFile=/etc/sysconfig/seafile
环境变量文件/etc/sysconfig/seafile文件内容为
CONFIGFILE=/etc/seafile.conf            # seafutil-luanch启动所用配置文件

如果需要修改启动
标准做法是通过systemctl edit sefile.service修改
EnvironmentFile的方式变更环境变量配置文件的指向
```

2. seafile.conf内容
```text
具体参考seafutil.conf模块中的各个opts
无默认值的必要配置为
name      seafile servername
external  seafile server对外IP/域名
datadir   seafile存放数据的文件夹,sefile、seahub、ccent的数据文件夹都在这个文件夹下
seahub    seahub程序文件根目录,seahub是一个python网站,没有打rpm包,通过这个配置指定seahub的网站根目录
hubkey    seahub所用的加密key,建议参考官网的key生成方式用随机算法生成
```


### DOC
```text
conf目录是seahub的uwsgi配置参考
第script目录从seafile官网的部署包中复制,作为制作本包的参考
seafile-freebsd-init.sh从freebsd的seafile-server包中提取
spec目录中的spec文件是对应rpm打包规则文件
pylibmc.tar.gz是启用memcached的必要插件
```


### 其他命令

```text
Firewall 能将不同的网络连接归类到不同的信任级别，Zone 提供了以下几个级别
drop: 丢弃所有进入的包，而不给出任何响应
block: 拒绝所有外部发起的连接，允许内部发起的连接
public: 允许指定的进入连接
external: 同上，对伪装的进入连接，一般用于路由转发
dmz: 允许受限制的进入连接
work: 允许受信任的计算机被限制的进入连接，类似 workgroup
home: 同上，类似 homegroup
internal: 同上，范围针对所有互联网用户
trusted: 信任所有连接

```

### memcached设置
需要uwsgi在memcached启动后启动,systemctl edit uwsgi.service
```text
[Unit]
Description=uWSGI Emperor Service
After=syslog.target memcached.service
```
或使用uwsig管理memecached,未测试此做法,具体参考uwsgi官方文档
```test
[uwsgi]
master = true
socket = /run/seafile/seahub-uwsgi.sock
attach-daemon = memcached -s /run/seafile/memcached.sock -a 0666 -u seafile
```


firewall-cmd --get-default-zone

firewall-cmd --zone=public --add-masquerade
firewall-cmd --zone=external --remove-masquerade
firewall-cmd --zone=public --add-forward-port=port=22:proto=tcp:toport=3753
firewall-cmd --zone=public --add-forward-port=port=22:proto=tcp:toaddr=192.168.1.100
firewall-cmd --zone=public --add-forward-port=port=22:proto=tcp:toport=2055:toaddr=192.168.1.100
