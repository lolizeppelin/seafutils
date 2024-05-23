## seafile rpm 打包文件

### 安装依赖

```shell
# rpmfusion 源安装
dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
# 不要装ffmpeg-free
dnf install ffmpeg
# openstack 基础库
dnf install python-oslo-config python-stevedore python-pbr
# python2
dnf install python2
# 数据库
dnf install postgresql15-server postgresql15-devel
# aria2
dnf install aria2
# seafile 依赖
dnf install pygobject2

```

---

## 编译

### 安装依赖

```shell
# 编译工具
dnf install gcc gcc-c++ cmake rpm-build automake autoconf
# seafile 依赖
dnf install libevent-devel libarchive-devel fuse-devel libcurl-devel libzdb-devel 
dnf install openssl-devel libuuid-devel sqlite-devel glib2-devel jansson-devel postgresql15-devel
dnf install vala libtool intltool

```

### 编译依赖

```shell
# su - builder 切换编译用户
cd ~
wget https://kojipkgs.fedoraproject.org//vol/fedora_koji_archive06/packages/python2-setuptools/41.2.0/4.fc34/src/python2-setuptools-41.2.0-4.fc34.src.rpm
rpm -ivh python2-setuptools-41.2.0-4.fc34.src.rpm
rpmbuild -ba rpmbuild/python2-setuptools.spec
# root 安装编译好的setuptools
wget https://kojipkgs.fedoraproject.org//vol/fedora_koji_archive06/packages/python-psycopg2/2.8.6/5.fc35/src/python-psycopg2-2.8.6-5.fc35.src.rpm
rpm -ivh python-psycopg2-2.8.6-5.fc35.src.rpm
# 将 BuildRequires: pkgconfig(libpq) 更改为 BuildRequires:  /usr/bin/pg_config
sed -i '0,/BuildRequires:.*pkgconfig(libpq)/s##BuildRequires:  /usr/bin/pg_config#' rpmbuild/SPECS/python-psycopg2.spec
rpmbuild -ba rpmbuild/SPECS/python-psycopg2.spec --without python3 --with python2 --without python3_debug --without tests
# root 安装编译好的psycopg2
rpmbuild -ba rpmbuild/SPECS/python2-simplejson.spec --without tests
# root 安装编译好的simplejson
rpmbuild -ba rpmbuild/SPECS/libsearpc.spec 
# root 安装编译好的libsearpc
rpmbuild -ba rpmbuild/SPECS/ccnet.spec 
# root 安装编译好的ccnet  ccnet-devel
rpmbuild -ba rpmbuild/SPECS/seafile.spec 
# root 安装编译好的seafile-server
rpmbuild -ba rpmbuild/SPECS/seafutils.spec 
```