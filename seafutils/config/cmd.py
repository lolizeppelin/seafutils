from oslo_config import types
from oslo_config import cfg

gc_opts = [
    cfg.BoolOpt('remove',
                default=False,
                help='remove garbaged repos or just to show'),
    cfg.BoolOpt('verbose',
                short='v',
                default=False,
                help='verbose output messages'),
    cfg.ListOpt('repos',
                short='r',
                item_type=types.Integer(),
                help='target repos id list'),
]

fsck_opts = [
    cfg.BoolOpt('repair',
                default=False,
                help='do repair'),
    cfg.ListOpt('repos',
                short='r',
                item_type=types.Integer(),
                help='target repos id list'),
]

dump_opts = [
    cfg.StrOpt('export',
               required=True,
               help='export files to directory'),
    cfg.ListOpt('repos',
                short='r',
                item_type=types.Integer(),
                help='target repos id list to dump'),
]


launch_opts = [
    cfg.StrOpt('pidfile',
               required=True,
               help='Process pid file'),
]

launch_seahub_opts = [
    cfg.BoolOpt('debug',
                default=False,
                help='gunicorn log level'),
    cfg.IntOpt('workers',
               default=4,
               min=1, max=128,
               help='gunicorn process number'),
    cfg.IPOpt('listen', short='l',
              default='0.0.0.0',
              help='wsgi server listen address'),
    cfg.PortOpt('port',
                default=8080,
                help='wsgi server listen port'),
    cfg.StrOpt('unix_socket', short='s',
               help='wsgi server listen on unix socket, e.g /tmp/seahub.sock'),
]
