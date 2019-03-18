# Seafile 服务端部署工具

### 使用说明
seafile-init-* 是对应程序初始化脚本
seafile-luanch 是服务器启动的代理脚本,用于启动和关闭seafile-controller,由systemd调用


### 配置说明
1. lucach启动配置
```text
默认systemd.service设置EnvironmentFile=/etc/sysconfig/seafile
环境变量文件/etc/sysconfig/seafile文件内容为
CONFIGFILE=/etc/seafile.conf            # seafile-luanch启动所用配置文件
PIDFILE=/run/seafile-controller.pid     # 提供给systemd的seafile-controller进程pid文件
TIMEOUT=5                               # systemd和seafile-luanch 共用的启动超时时间
User=seafile                            # systemd调用seafile-luanch所用用户
Group=seafile                           # systemd调用seafile-luanch所用组

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
第一层目录的脚本从seafile官网的部署包中复制,作为制作本包的参考
seafile-freebsd-init.sh从freebsd的seafile-server包中提取
spec目录中的spec文件是对应rpm打包规则文件
```