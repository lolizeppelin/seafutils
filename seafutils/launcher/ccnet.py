import os

from oslo_config import cfg
from distutils.spawn import find_executable

from seafutils.config.cmd import launch_opts

CCNET = find_executable("ccnet-server")


def run():
    """
    启动ccnet
    :return:
    """
    cfg.CONF.register_cli_opts(launch_opts)
    cfg.CONF(project='ccnet')

    args = (
        CCNET,
        '-F', cfg.CONF.central,
        '-c', cfg.CONF.config,
        '-f', os.path.join(cfg.CONF.logdir, "ccnet-server.log"),
        '-P', cfg.CONF.pidfile,  # pid
        '-d'
    )
    os.execv(CCNET, args)
