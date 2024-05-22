import os
from distutils.spawn import find_executable

from oslo_config import cfg
from seafutils.utils import get_py2path

PYTHON = find_executable("python2")


def run():
    """
    重置管理员
    :return:
    """
    cfg.CONF(project='reset')
    third_part = os.path.join(cfg.CONF.website, 'thirdpart')
    env = {
        "CCNET_CONF_DIR": cfg.CONF.config,
        "SEAFILE_CONF_DIR": cfg.CONF.datadir,
        "SEAFILE_CENTRAL_CONF_DIR": cfg.CONF.central,
        "PYTHONPATH": get_py2path(cfg.CONF.website, third_part),
    }
    args = [
        PYTHON,
        os.path.join(cfg.CONF.website, "manager.py"),
        'createsuperuser'
    ]
    os.execve(PYTHON, args, env)
