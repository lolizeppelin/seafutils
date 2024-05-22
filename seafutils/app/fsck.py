# seafile 修复 seafutils-fsck
import os
from distutils.spawn import find_executable
from oslo_config import cfg

from seafutils.config.cmd import fsck_opts

FSCK = find_executable("seaf-fsck")


def run():
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
