from oslocfg import cfg


server_opts = [
    cfg.StrOpt('name',
               required=True,
               regex=r'^[a-zA-Z0-9_\-]{3,15}$',
               help='Seafile server name'),
    cfg.StrOpt('external',
               default='127.0.0.1',
               required=True,
               regex=r'^[^.].+\..+[^.]$',
               help='Seafile server ip or domain name'),
    cfg.StrOpt('cfgdir',
               default='/etc/seafile',
               help='Seafile config path'),
    cfg.StrOpt('logdir',
               default='/var/log/seafile',
               help='Seafile log path'),
    cfg.StrOpt('loglevel',
               default='info',
               choices=['info', 'notice', 'warning', 'debug'],
               help='Seafile log level'),
    cfg.StrOpt('datadir',
               required=True,
               regex='',
                help='Seafile server data path'),
    cfg.StrOpt('seahub',
               help='Seahub app root path'),
    cfg.StrOpt('hubkey',
               required=True,
               secret=True,
               max_length=20,
               help='Seahub secret key')
]

# options for server-luanch
luanch_opts = [
    cfg.StrOpt('action',
               required=True,
               choices=['start', 'stop'],
               help='Seafile luanch type'),
    cfg.StrOpt('config',
               short='c',
               required=True,
               help='Seafile luanch config file'),
    cfg.StrOpt('pid',
               short='p',
               required=True,
               help='Seafile controller process pid file'),
    cfg.IntOpt('timeout',
               short='t',
               default=5,
               min=1, max=10,
               help='Seafile controller luanch timeout'),

]

# options for init script
base_init_opts = [
    cfg.StrOpt('user',
               default='seafile',
               help='seafile process running user'),
    cfg.StrOpt('group',
               default='seafile',
               help='seafile process running group'),
]

database_init_opts = [
    cfg.StrOpt('engine',
               default='mysql',
               choices=['mysql'],
               # choices=['mysql', 'postgresql'],
               help='database engine'),
    cfg.StrOpt('dbhost',
               short='o',
               default='127.0.0.1',
               help='database host'),
    cfg.PortOpt('dbport',
                short='P',
                default=3306,
                help='database listen port'),
    # cfg.StrOpt('unix-socket', short='u',
    #            help='database unix socket'
    #            ),
    cfg.StrOpt('dbuser', short='u',
               required=True,
               help='Database user name'),
    cfg.StrOpt('dbpasswd', short='p',
               secret=True,
               required=True,
               help='Database user password'),
    cfg.StrOpt('scope',
               default='127.0.0.1',
               help='Database user name scope'),
    cfg.StrOpt('rname',
               default='root',
               help='Database root name'),
    cfg.StrOpt('rpass',
               secret=True,
               help='Database root password'),
    cfg.BoolOpt('create',
                default=True,
                help='create new database schema or use existing database schema'),
    cfg.BoolOpt('debug',
                default=False,
                help='connect database use debug mode'),
]

ccnet_init_opts = [
    cfg.PortOpt('port',
                default=10001,
                help='Ccnet server listen port'),
    cfg.StrOpt('dbname',
               default='ccnet',
               help='ccnet database name'),
]

seafile_init_opts = [
    cfg.PortOpt('port',
                default=8082,
                help='Seafile file server public port'),
    cfg.PortOpt('iport',
                default=12001,
                choices=[12001],
                help='Seafile server internal port'),
    cfg.StrOpt('dbname',
               default='seafile',
               help='Seafile database name'),
    cfg.BoolOpt('develop',
                default=False,
                help='Seafile enable development api'),
    cfg.PortOpt('devport',
                default=8080,
                help='Seafile development port')
]

seahub_init_opts = [
    cfg.StrOpt('dbname',
               default='seahub',
               help='seahub database name'),
]


def list_server_opts():
    return server_opts