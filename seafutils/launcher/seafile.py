import os

from oslo_config import cfg
from distutils.spawn import find_executable

from seafutils.config.cmd import launch_opts

SEAFILE = find_executable("seaf-server")


def run():
    """
    启动seafile
    :return:
    """
    cfg.CONF.register_cli_opts(launch_opts)
    cfg.CONF(project='seafile')

    args = (
        SEAFILE,
        '-F', cfg.CONF.central,
        '-c', cfg.CONF.config,
        '-d', cfg.CONF.datadir,
        '-l', os.path.join(cfg.CONF.logdir, "seafile-server.log"),
        '-P', cfg.CONF.pidfile,  # pid
    )
    os.execv(SEAFILE, args)
