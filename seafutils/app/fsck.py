# seafile 修复 seafutils-fsck
import os
from distutils.spawn import find_executable
from oslo_config import cfg

from seafutils.config.seafile import fsck_opts

FSCK = find_executable("seaf-fsck")


def run():
    """
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


    :return:
    """
    cfg.CONF.register_cli_opts(fsck_opts)
    cfg.CONF(project='seafile-fsck', description="seafile fsck tool")

    args = [
        FSCK,
        '-F', cfg.CONF.central,
        '-c', cfg.CONF.config,
        '-d', cfg.CONF.datadir,
    ]

    if cfg.CONF.repair:
        args.append('--repair')
    if cfg.CONF.repos:
        for r in cfg.CONF.repos:
            args.append(str(r))
    os.execv(FSCK, args)
