import sys
import os
import pwd
from oslo_config import cfg
from stevedore import driver
from seafutils.config import base

cfg.CONF.register_opts(base.base_opts)


def run_user():
    return pwd.getpwuid(os.getpid()).pw_name


def run(app: str):
    if run_user() != 'seafile':
        print("run user not seafile", file=sys.stderr)
        sys.exit(1)

    mgr = driver.DriverManager('seafutils.app ', app,
                               warn_on_missing_entrypoint=False)
    return mgr.driver()


def launch(app: str):
    if run_user() != 'seafile':
        print("run user not seafile", file=sys.stderr)
        sys.exit(1)

    cfg.CONF.register_cli_opt(base.launch_opts)
    mgr = driver.DriverManager('seafutils.launcher ', app,
                               warn_on_missing_entrypoint=False)
    return mgr.driver()
