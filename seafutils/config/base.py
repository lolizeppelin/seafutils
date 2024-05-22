import itertools
from oslo_config import cfg

base_opts = [
    cfg.StrOpt('central',
               default='/etc/seafile/central',
               help='Seafile central config path'),
    cfg.StrOpt('config',
               default='/var/lib/ccent/config',
               help='ccent config path'),
    cfg.StrOpt('datadir',
               default='/var/lib/seafile/data',
               help='Seafile server data path'),
    cfg.StrOpt('website',
               default='/usr/share/seahub/wsgi',
               help='seahub wsgi root path'),
    cfg.StrOpt('logdir',
               default='/var/log/seafile',
               help='Seafile log path'),
]

database_opts = [
    cfg.StrOpt('db',
               default="",
               help='Database name'),
    cfg.StrOpt('host',
               default='127.0.0.1',
               help='database host'),
    cfg.PortOpt('port',
                default=5432,
                help='database listen port'),
    cfg.StrOpt('user',
               required=True,
               help='Database user name'),
    cfg.StrOpt('passwd', short='p',
               secret=True,
               help='Database user password'),
    cfg.StrOpt('admin',
               help='Database admin user name'),
    cfg.StrOpt('admin_passwd',
               secret=True,
               help='Database admin password'),

]


def list_opts():
    return [
        ('DEFAULT', itertools.chain(base_opts))
    ]
