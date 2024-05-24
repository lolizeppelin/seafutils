import os
from distutils.spawn import find_executable
from oslo_config import cfg

from seafutils.config.cmd import fsck_opts
from seafutils.config.cmd import dump_opts
from seafutils.config.cmd import gc_opts
from .initialize import initialized

FSCK = find_executable("seaf-fsck")
GC = find_executable("seafserv-gc")


def fsck():
    cfg.CONF.register_cli_opts(fsck_opts)
    cfg.CONF(project='seafile-fsck', description="seafile fsck tool")
    initialized()

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


def dump():
    cfg.CONF.register_cli_opts(dump_opts)
    cfg.CONF(project='seafile-dump', description="seafile dump tool")
    initialized()

    args = [
        FSCK,
        '-F', cfg.CONF.central,
        '-c', cfg.CONF.config,
        '-d', cfg.CONF.datadir,
        '--export', cfg.CONF.export,
    ]

    if cfg.CONF.repos:
        for r in cfg.CONF.repos:
            args.append(str(r))
    os.execv(FSCK, args)


def gc():
    """
    追加seahub的清理调用
    :return:
    """
    cfg.CONF.register_cli_opts(gc_opts)
    cfg.CONF(project='seafile-gc', description="seafile gc tool")
    initialized()

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
