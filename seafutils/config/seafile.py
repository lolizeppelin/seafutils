import copy
from oslo_config import types
from oslo_config import cfg

from .base import database_opts

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
    cfg.BoolOpt('export',
                required=True,
                default=False,
                help='export files to directory'),
    cfg.ListOpt('repos',
                short='r',
                item_type=types.Integer(),
                help='target repos id list to dump'),
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

cfg.set_defaults(seafile_init_opts, user='seafile')
