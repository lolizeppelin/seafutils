import os
import sys

from oslo_config import cfg
from distutils.spawn import find_executable

SEAFILE = find_executable("seaf-server")


def run():
    """
    char *argv[] = {
    "seaf-server",
    "-F", ctl->central_config_dir,
    "-c", ctl->config_dir,
    "-d", ctl->seafile_dir,
    "-l", logfile,
    "-P", ctl->pidfile[PID_SERVER],
    NULL};
    :return:
    """
    cfg.CONF(project='seafile')

    args = (
        SEAFILE,
        '-F', cfg.CONF.central,
        '-c', cfg.CONF.config,
        '-d', cfg.CONF.datadir,
        '-l', os.path.join(cfg.CONF.logdir, "seafile-server.log"),
        '-P', cfg.CONF.pidfile,  # pid
    )
    os.execv(SEAFILE, *args)
