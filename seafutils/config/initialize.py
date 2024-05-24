import copy
import itertools
from oslo_config import cfg
from .base import database_opts

init_opts = [
    cfg.StrOpt('admin',
               default='postgres',
               help='Database(global) admin user name'),
    cfg.StrOpt('admin_passwd', short='p',
               secret=True,
               help='Database(global) admin user password'),
]

ccnet_init_opts = copy.deepcopy(database_opts) + [
    cfg.PortOpt('listen',
                default=10001,
                help='ccent server internal port'),
    cfg.StrOpt('name',
               required=True,
               regex=r'^[a-zA-Z0-9_\-]{3,15}$',
               help='Seafile server name, e.g: mynas'),
    cfg.StrOpt('domain',
               default='127.0.0.1',
               regex=r'^[^.].+\..+[^.]$',
               help='Seafile server ip or domain name, e.g: nas.my-domain.com'),
]

seafile_init_opts = copy.deepcopy(database_opts) + [
    cfg.PortOpt('eport',
                default=8082,
                help='Seafile file server external port'),
    cfg.PortOpt('listen',
                default=12001,
                choices=[12001],
                help='Seafile server internal port'),
    cfg.PortOpt('backdoor',
                default=8080,
                help='Seafile development port'),
    cfg.BoolOpt('debug',
                default=False,
                help='Seafile enable development api'),
]

seahub_init_opts = copy.deepcopy(database_opts) + [
    cfg.StrOpt('secret',
               required=True,
               max_length=20,
               help='secret key'),
    cfg.StrOpt('memcache',
               help='memcache connection address, e.g /run/memcached.sock'),
]

cfg.set_defaults(ccnet_init_opts, user='ccnet', db='ccnet')
cfg.set_defaults(seafile_init_opts, user='seafile', db='seafile')
cfg.set_defaults(seahub_init_opts, user='seahub', db='seahub')


def list_opts():
    return [
        ('DEFAULT', itertools.chain(init_opts)),
        ('ccnet', itertools.chain(ccnet_init_opts)),
        ('seafile', itertools.chain(seafile_init_opts)),
        ('seahub', itertools.chain(seahub_init_opts)),
    ]
