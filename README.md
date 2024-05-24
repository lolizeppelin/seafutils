# Seafile 服务端工具

#### 必须使用seafile用户或者root执行

#### root执行时会自动切换为seafile用户,不可读取root权限文件

--- 

## seafutils init

### 服务初始化

- #### DEFAULT

```text
admin         初始化时全局数据库管理员账户(默认postgres)
admin_passwd  初始化时全局数据库管理员密码
```

- #### ccnet

```text
db              数据库名(默认ccnet)
host            数据库host(默认127.0.0.1)
port            数据库端口(默认5432)
user            用户名(默认ccnet)
passwd          密码(默认生成随机密码)
admin           数据库管理员账户(默认使用全局数据库管理员账户)
admin_passwd    数据库管理员密码(默认使用全局数据库管理员密码)

listen          ccnet内部端口(默认10001)
name            seafile 服务名
host            seafile server对外IP/域名
```

- #### seafile

```text
db              数据库名(默认seafile)
host            数据库host(默认127.0.0.1)
port            数据库端口(默认5432)
user            用户名(默认seafile)
passwd          密码(默认生成随机密码)
admin           数据库管理员账户(默认使用全局数据库管理员账户)
admin_passwd    数据库管理员密码(默认使用全局数据库管理员密码)

eport           seafile对外服务端口(默认8082)
listen          无效参数
backdoor        无效参数
debug           无效参数

```

- #### seahub

```text
db              数据库名(默认seahub)
host            数据库host(默认127.0.0.1)
port            数据库端口(默认5432)
user            用户名(默认seahub)
passwd          密码(默认生成随机密码)
admin           数据库管理员账户(默认使用全局数据库管理员账户)
admin_passwd    数据库管理员密码(默认使用全局数据库管理员密码)

secret          seahub所用的加密key,建议参考官网的key生成方式用随机算法生成
memcache        memcache地址,不配置表示不使用memcache缓存session
```

---

## seafutils relocate

### seafile数据文件夹修改重定向

---

## seafutils gc

### 垃圾回收

---

## seafutils fsck

### 数据修复

---

## seafutils dump

### 数据导出

---

## seafutils reset

### 重置管理员密码

---

## seafutils clean

### seahub清理session

---

# memcached配置

```ini
# systemctl edit memcached.service
[Service]
RuntimeDirectoryMode=0777
RuntimeDirectoryPreserve=no
RuntimeDirectory=memcached
```

```shell
# vim /etc/sysconfig/memcached 
PORT="11211"
USER="memcached"
MAXCONN="1024"
CACHESIZE="128"
#OPTIONS="-l 127.0.0.1,::1"
OPTIONS="-l 127.0.0.1 -s /run/memcached/memcached.sock -a 0666"
```

# seafile启动与关闭

```shell

# 关闭
systemctl stop seahub.service
systemctl stop seafile.service
systemctl stop ccnet.service

# 启动
systemctl start ccnet.service
systemctl start seafile.service
systemctl start seahub.service


```