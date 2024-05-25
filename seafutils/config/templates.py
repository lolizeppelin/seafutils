# 配置文件模板
from oslo_config import cfg
from configparser import ConfigParser


class AllowUppercaseConf(ConfigParser):
    def optionxform(self, optionstr):
        return optionstr



# setting 模板
TEMPLATE = '''\
# -*- coding: utf-8 -*-\n
SECRET_KEY = '%(key)s'\n
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%(name)s',
        'USER': '%(username)s',
        'PASSWORD': '%(password)s',
        'HOST': '%(host)s',
        'PORT': '%(port)s'
    }
}\n
ENABLE_RESUMABLE_FILEUPLOAD = False\n
SEND_EMAIL_ON_ADDING_SYSTEM_MEMBER  = False\n
'''

MEMCACHED = '''\
\n
CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': '%(conn)s',
    },
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}\n
COMPRESS_CACHE_BACKEND = 'locmem'\n
THUMBNAIL_IMAGE_SIZE_LIMIT = 100\n
ENABLE_VIDEO_THUMBNAIL = False\n
FILE_PREVIEW_MAX_SIZE = 30 * 1024 * 1024\n
'''


def seafile():
    """
    seafile config
    :return:
    """
    conf = cfg.CONF.seafile

    config = AllowUppercaseConf()
    section = 'database'
    config.add_section(section)
    config.set(section, 'type', "pgsql")
    config.set(section, 'host', conf.host)
    config.set(section, 'port', str(conf.port))
    config.set(section, 'user', conf.user)
    config.set(section, 'password', conf.passwd)
    config.set(section, 'db_name', conf.db)
    config.set(section, 'connection_charset', 'utf8')
    return config


def ccnet():
    """
    ccnet config
    :return:
    """
    conf = cfg.CONF.ccnet
    section = 'Database'
    config = AllowUppercaseConf()
    config.add_section(section)
    config.set(section, 'ENGINE', "pgsql")
    config.set(section, 'HOST', conf.host)
    config.set(section, 'PORT', str(conf.port))
    config.set(section, 'USER', conf.user)
    config.set(section, 'PASSWD', conf.passwd)
    config.set(section, 'DB', conf.db)
    config.set(section, 'CONNECTION_CHARSET', 'utf8')
    return config


def seahub():
    """
    seahub config
    :return:
    """
    conf = cfg.CONF.seahub
    content = TEMPLATE % dict(key=conf.secret,
                              name=conf.db,
                              username=conf.user,
                              password=conf.passwd,
                              host=conf.host,
                              port=conf.port)
    if conf.memcache:
        content += (MEMCACHED % dict(conn=conf.memcache))
    return content
