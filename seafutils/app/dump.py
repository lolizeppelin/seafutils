# seafile 导出 seafutils-dump
import os
from distutils.spawn import find_executable
from oslo_config import cfg

from seafutils.config.cmd import dump_opts

FSCK = find_executable("seaf-fsck")


def run():
    cfg.CONF.register_cli_opts(dump_opts)
    cfg.CONF(project='seafile-dump', description="seafile dump tool")

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
