import copy
from oslo_config import cfg

from .base import database_opts

seahub_init_opts = copy.deepcopy(database_opts) + [
    cfg.StrOpt('secret',
               required=True,
               max_length=20,
               help='secret key'),
    cfg.StrOpt('memcache',
               help='memcache connection address, e.g /run/memcached.sock'),
]

launch_opts = [
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

cfg.set_defaults(seahub_init_opts, user='seahub')
