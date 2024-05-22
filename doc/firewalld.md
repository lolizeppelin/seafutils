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

```shell

firewall-cmd --zone=public --add-forward-port=port=22:proto=tcp:toport=2055:toaddr=192.168.1.100
firewall-cmd --zone=external --add-forward-port=port=7901:proto=tcp:toport=22:toaddr=10.10.0.101

```