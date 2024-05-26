## seafile rpm 打包文件

### 安装依赖

```shell
# 标准英语环境安装
dnf install langpacks-core-en
# rpmfusion 源安装
dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
# 安装aria2
dnf install aria2
# ffmpeg (不要安装ffmpeg-free)
dnf install ffmpeg
# 安装jellyfin
dnf install jellyfin-server jellyfin-web
```