# seafile 垃圾回收 seafutils-gc
import os
from distutils.spawn import find_executable
from oslo_config import cfg

from seafutils.config.cmd import gc_opts

GC = find_executable("seafserv-gc")


def run():
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
