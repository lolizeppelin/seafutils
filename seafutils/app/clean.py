import os
from distutils.spawn import find_executable

from oslo_config import cfg
from seafutils.utils import get_py2path

PYTHON = find_executable("python2")


def run():
    """
    清理session
    :return:
    """
    cfg.CONF(project='clean')
    env = {
        "CCNET_CONF_DIR": cfg.CONF.config,
        "SEAFILE_CONF_DIR": cfg.CONF.datadir,
        "SEAFILE_CENTRAL_CONF_DIR": cfg.CONF.central,
        "PYTHONPATH": get_py2path(cfg.CONF.website,
                                  os.path.join(cfg.CONF.website, 'thirdpart')),
    }
    args = [
        PYTHON,
        os.path.join(cfg.CONF.website, "manager.py"),
        'clearsessions'
    ]
    os.execve(PYTHON, args, env)
