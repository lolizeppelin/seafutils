# seafile 垃圾回收 seafutils-gc
import os
from distutils.spawn import find_executable
from oslo_config import cfg

from seafutils.config.seafile import gc_opts

GC = find_executable("seafserv-gc")


def run():
    """
    Seahub 过期清理
    清理 Session 表:
    cd <install-path>/seafile-server-latest
    ./seahub.sh python-env seahub/manage.py clearsessions
    文件活动 (Activity)
    要清理文件活动表，登录到 MySQL/MariaDB，然后使用以下命令:
    use seahub_db;
    DELETE FROM Event WHERE to_days(now()) - to_days(timestamp) > 90;

    Seafile 过期清理
    usage: seafserv-gc [-c config_dir] [-d seafile_dir] [repo_id_1 [repo_id_2 ...]]
    Additional options:
    -r, --rm-deleted: remove garbaged repos
    -D, --dry-run: report blocks that can be remove, but not remove them
    -V, --verbose: verbose output messages

    :return: 
    """
    cfg.CONF.register_cli_opts(gc_opts)
    cfg.CONF(project='seafile-gc', description="seafile gc tool")

    args = [
        GC,
        '-F', cfg.CONF.central,
        '-c', cfg.CONF.config,
        '-d', cfg.CONF.datadir,
    ]

    if cfg.CONF.verbose:
        args.append('-V')
    if cfg.CONF.remove:
        args.append('--rm-deleted')
    else:
        args.append('--dry-run')
    if cfg.CONF.repos:
        for r in cfg.CONF.repos:
            args.append(str(r))
    os.execv(GC, args)
