import copy
from oslo_config import cfg

from .base import database_opts

ccnet_init_opts = copy.deepcopy(database_opts) + [
    cfg.PortOpt('listen',
                default=10001,
                help='ccent server internal port'),
    cfg.StrOpt('name',
               required=True,
               regex=r'^[a-zA-Z0-9_\-]{3,15}$',
               help='Seafile server name'),
    cfg.HostAddressOpt('host',
                       default='127.0.0.1',
                       regex=r'^[^.].+\..+[^.]$',
                       help='Seafile server ip or domain name'),
]

cfg.set_defaults(ccnet_init_opts, user='ccnet')
