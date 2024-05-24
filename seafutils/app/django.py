import os
from distutils.spawn import find_executable

from oslo_config import cfg
from seafutils.utils import get_py2path
from .initialize import initialized


PYTHON = find_executable("python2")


def run(project, method):
    cfg.CONF(project=project)
    initialized()
    third_part = os.path.join(cfg.CONF.website, 'thirdpart')
    env = {
        "CCNET_CONF_DIR": cfg.CONF.config,
        "SEAFILE_CONF_DIR": cfg.CONF.datadir,
        "SEAFILE_CENTRAL_CONF_DIR": cfg.CONF.central,
        "PYTHONPATH": get_py2path(cfg.CONF.website, third_part),
    }
    args = [
        PYTHON,
        os.path.join(cfg.CONF.website, "manage.py"),
        method
    ]
    os.execve(PYTHON, args, env)


def clean():
    """
    清理session
    :return:
    """
    run("clean", "clearsessions")


def reset():
    """
    重置管理员
    :return:
    """
    run("reset", "createsuperuser")
