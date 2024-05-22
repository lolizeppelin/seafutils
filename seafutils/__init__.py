import sys
from oslo_config import cfg
from stevedore import driver
from seafutils.config import cmd
from seafutils.config import base

from .utils import getuser

cfg.CONF.register_opts(base.base_opts)


def run(app: str):
    if getuser() != 'seafile':
        print("run user not seafile", file=sys.stderr)
        sys.exit(1)

    mgr = driver.DriverManager('seafutils.app ', app,
                               warn_on_missing_entrypoint=False)
    return mgr.driver()


def launch(app: str):
    if getuser() != 'seafile':
        print("run user not seafile", file=sys.stderr)
        sys.exit(1)

    cfg.CONF.register_cli_opt(cmd.launch_opts)
    mgr = driver.DriverManager('seafutils.launcher ', app,
                               warn_on_missing_entrypoint=False)
    return mgr.driver()
