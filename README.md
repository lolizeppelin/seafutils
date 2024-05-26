# Seafile 服务端工具

```text
seafile不提供rpm包
seafile没有使用标准服务管理(systemd)
seafile命令行不统一且使用多个脚本
seafile初始化配置比较麻烦

于是基于编seafile7.0.0写了一套seafile管理工具

1. 标准rpm包
2. 统一命令行
3. 标准systemd服务管理
4. 简洁的配置文件(单文件)
```

--- 

# seafile安装

```shell
# seafile(seafile 基础库)
dnf install libsearpc-3.1.11*
# ccnet(seafile RPC服务)
dnf install ccnet-7.0.2* ccnet-server-7.0.2*
# seafile(seafile 数据服务)
dnf install seafile-7.0.2* seafile-server-7.0.2*
# seahub(seafile 前端)
dnf install seahub-7.0.2*
# 管理工具
dnf install seafutils-2.0*
# 安装memcached 用于存储session
dnf install memcached
```

# memcached配置

```ini
# systemctl edit memcached.service
[Service]
RuntimeDirectoryMode = 0777
RuntimeDirectoryPreserve = no
RuntimeDirectory = memcached
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

---

#### 所有命令必须使用seafile用户或者root执行

#### root执行时会自动切换为seafile用户,不可访问root权限文件

#### 所有命令支持 -h 查看参数

---

## seafutils init

#### 初始化只有三个必要参数

1. 服务名
2. 域名
3. 数据库管理员密码

#### 一个最简化的初始化命令如下

```shell
# 如果需要使用memcache,可以再加一个参数-m /run/memcached/memcached.sock
# init执行过程失败会自动清理
seafutils init -n mynas -d mynas.my-domain.com -p db_admin_pass
```

### 全初始化参数如下

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

secret          seahub所用的加密key(默认使用uuid4.hex前20个字符)
memcache        memcache地址(默认不配置,不使用memcache缓存session)
```

---

## seafutils relocate

### seafile数据文件夹修改重定向(修改配置文件后执行)

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

---

### seafile数据删除

1. 删除配置指向的ccnet配置文件夹(默认/var/lib/seafile/config)
2. 删除配置指向的seafile数据文件夹(默认/var/lib/seafile/data)
3. 删除配置指向配置文件夹下的所有文件(默认/etc/seafile/central)
4. 删除数据库

```sql
drop database seafile;
drop database ccnet;
drop database seahub;
drop owned by seafile cascade;
drop owned by ccnet cascade;
drop owned by seahub cascade;
drop role seafile;
drop role ccnet;
drop role seahub;
```