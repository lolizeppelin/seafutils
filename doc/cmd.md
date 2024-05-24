### 启动ccnet

```c
char *argv[] = {
"ccnet-server",
"-F", ctl->central_config_dir,
"-c", ctl->config_dir,
"-f", logfile,
"-d",
"-P", ctl->pidfile[PID_CCNET],
NULL};
```

### 启动seafile

```c
char *argv[] = {
"seaf-server",
"-F", ctl->central_config_dir,
"-c", ctl->config_dir,
"-d", ctl->seafile_dir,
"-l", logfile,
"-P", ctl->pidfile[PID_SERVER],
NULL};

```

---

### 启动seahub(gunicorn)

```shell

env = CCNET_CONF_DIR=%(datadir)/ccnet-data
env = SEAFILE_CONF_DIR=%(datadir)/seafile-data
env = SEAFILE_CENTRAL_CONF_DIR=/etc/seafile
env = SEAHUB_LOG_DIR=/var/log/seafile
env = PYTHONPATH=%(seahubpath):%(seahubpath)/thirdpart
env = DJANGO_SETTINGS_MODULE=seahub.settings

DJANGO_WSGI_MODULE=seahub.wsgi:application # WSGI module name

gunicorn ${DJANGO_WSGI_MODULE} --workers $NUM_WORKERS --log-level=debug
--access-logfile=/tmp/gunicorn-access.log
--error-logfile=/tmp/gunicorn-error.log --pid=${PID_FILE} --daemon --preload

```

---

### seaf-fsck.sh

```text

    执行 seaf-fsck.sh 不加任何参数将以只读方式检查所有资料库的完整性。

    cd seafile-server-latest
    ./seaf-fsck.sh


    如果你想检查指定资料库的完整性，只需将要检查的资料库 ID 作为参数即可：

    cd seafile-server-latest
    ./seaf-fsck.sh [library-id1] [library-id2] ...


    fsck 修复损坏的资料库有如下两步流程:

    如果记录在数据库中的资料库当前状态无法在数据目录中找出，fsck 将会在数据目录中找到最近可用状态。
    检查第一步中可用状态的完整性。如果文件或目录损坏，fsck 将会将其置空并报告损坏的路径，用户便可根据损坏的路径来进行恢复操作。
    执行如下命令来修复所有资料库：

    cd seafile-server-latest
    ./seaf-fsck.sh --repair


    大多数情况下我们建议你首先以只读方式检查资料库的完整性，找出损坏的资料库后，执行如下命令来修复指定的资料库：
    cd seafile-server-latest
    ./seaf-fsck.sh --repair [library-id1] [library-id2] ...

    参数 top_export_path 是放置导出文件的目录。每个资料库将导出为导出目录的子目录。如果不指定资料库的ID，将导出所有库。

    目前只能导出未加密的资料库，加密资料库将被跳过。

        -c "${default_ccnet_conf_dir}" -d "${seafile_data_dir}" \
        -F "${default_conf_dir}" \

    cd seafile-server-latest
    ./seaf-fsck.sh --export top_export_path [library-id1] [library-id2] ...



```

### seafserv-gc.sh

```text
    Seafile 过期清理
    usage: seafserv-gc [-c config_dir] [-d seafile_dir] [repo_id_1 [repo_id_2 ...]]
    Additional options:
    -r, --rm-deleted: remove garbaged repos
    -D, --dry-run: report blocks that can be remove, but not remove them
    -V, --verbose: verbose output messages



```

### seahub

```text

    清理 Session 表:
    cd <install-path>/seafile-server-latest
    ./seahub.sh python-env seahub/manage.py clearsessions
    文件活动 (Activity)
    要清理文件活动表，登录到 MySQL/MariaDB，然后使用以下命令:
    use seahub_db;
    DELETE FROM Event WHERE to_days(now()) - to_days(timestamp) > 90;


    export CCNET_CONF_DIR=${default_ccnet_conf_dir}
    export SEAFILE_CONF_DIR=${seafile_data_dir}
    export SEAFILE_CENTRAL_CONF_DIR=${central_config_dir}
    export PYTHONPATH=${INSTALLPATH}/seafile/lib/python2.6/site-packages:${INSTALLPATH}/seafile/lib64/python2.6/site-packages:${INSTALLPATH}/seahub:${INSTALLPATH}/seahub/thirdpart:$PYTHONPATH
    export PYTHONPATH=${INSTALLPATH}/seafile/lib/python2.7/site-packages:${INSTALLPATH}/seafile/lib64/python2.7/site-packages:$PYTHONPATH

    manage_py=${INSTALLPATH}/seahub/manage.py
    exec "$PYTHON" "$manage_py" createsuperuser


```