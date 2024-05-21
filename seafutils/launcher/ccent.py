import os
import sys

from oslo_config import cfg
from distutils.spawn import find_executable

CCNET = find_executable("ccnet-server")


def run():
    """
    char *argv[] = {
    "ccnet-server",
    "-F", ctl->central_config_dir,
    "-c", ctl->config_dir,
    "-f", logfile,
    "-d",
    "-P", ctl->pidfile[PID_CCNET],
    NULL};
    :return:
    """
    cfg.CONF(project='ccnet')

    args = (
        CCNET,
        '-F', cfg.CONF.central,
        '-c', cfg.CONF.config,
        '-f', os.path.join(cfg.CONF.logdir, "ccnet-server.log"),
        '-P', cfg.CONF.pidfile,  # pid
        '-d'  # 以守护进程运行
    )
    os.execv(CCNET, *args)
