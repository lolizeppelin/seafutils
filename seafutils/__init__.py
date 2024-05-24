import sys
from oslo_config import cfg
from stevedore import driver
from seafutils.config import cmd
from seafutils.config import base

from .utils import getuser
from .utils import switch_to_seafile

cfg.CONF.register_opts(base.base_opts)


def _run(namespace: str, app: str):
    mgr = driver.DriverManager(namespace, app,
                               warn_on_missing_entrypoint=False)
    try:
        return mgr.driver()
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


def execute(app: str):
    if not switch_to_seafile():
        print("run user not seafile or root", file=sys.stderr)
        sys.exit(1)
    _run('seafutils.app', app)


def launch(app: str):
    if getuser() != 'seafile':
        print("run user not seafile", file=sys.stderr)
        sys.exit(1)
    cfg.CONF.register_cli_opt(cmd.launch_opts)
    _run('seafutils.launcher', app)
