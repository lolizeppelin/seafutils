import os

from oslo_config import cfg
from distutils.spawn import find_executable

from seafutils.config.cmd import launch_opts, launch_seahub_opts

PYTHON = find_executable("python2")


def run():
    """
    启动seahub
    :return:
    """
    cfg.CONF.register_cli_opts(launch_opts)
    cfg.CONF.register_cli_opts(launch_seahub_opts)
    cfg.CONF(project='seahub')

    third_part = os.path.join(cfg.CONF.website, 'thirdpart')
    gunicorn = os.path.join(third_part, 'gunicorn')
    access_log = os.path.join(cfg.CONF.logdir, 'access.log')
    error_log = os.path.join(cfg.CONF.logdir, 'error.log')

    env = {
        "DJANGO_SETTINGS_MODULE": "seahub.settings",
        "CCNET_CONF_DIR": cfg.CONF.config,
        "SEAFILE_CONF_DIR": cfg.CONF.datadir,
        "SEAFILE_CENTRAL_CONF_DIR": cfg.CONF.central,
        "SEAHUB_LOG_DIR": cfg.CONF.logdir,
    }

    if cfg.CONF.unix_socket:
        bind = 'unix:%s' % cfg.CONF.unix_socket
    else:
        bind = '%s:%d' % (cfg.CONF.listen, cfg.CONF.port)

    args = (
        PYTHON, gunicorn, "seahub.wsgi:application", '--preload',
        '--log-level=%s' % ('debug' if cfg.CONF.debug else 'error'),
        '--workers', str(cfg.CONF.workers),
        '--bind', bind,
        "--access-logfile=%s" % access_log,
        "--error-logfile=%s" % error_log,
        "--pid=%s" % cfg.CONF.pidfile,
    )
    os.chdir(cfg.CONF.website)
    os.execve(PYTHON, args, env)
