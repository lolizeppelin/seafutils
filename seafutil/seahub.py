import os
import subprocess
import shutil
import contextlib
from oslocfg import cfg
from seafutil.command import SeafCommand
from seafutil.seafile import SeafileCommand


CONF = cfg.CONF
NAME = 'seahub'
FILENAME = 'seahub_settings.py'
FILENAME2 = 'memcached'


TEMPLATE = '''\
# -*- coding: utf-8 -*-\n
SECRET_KEY = '%(key)s'\n
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%(engine)s',
        'NAME': '%(name)s',
        'USER': '%(username)s',
        'PASSWORD': '%(password)s',
        'HOST': '%(host)s',
        'PORT': '%(port)s'
    }
}\n
ENABLE_RESUMABLE_FILEUPLOAD = True\n
SEND_EMAIL_ON_ADDING_SYSTEM_MEMBER  = False\n
'''

MEMCACHED = '''\
CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': '/run/seafile/memcached.sock',
    },
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}\n
COMPRESS_CACHE_BACKEND = 'locmem'\n
'''


MEMCACHE = '''\
PORT="11211"\n
USER="seafile"\n
MAXCONN="1024"\n
CACHESIZE="128"\n
OPTIONS="-s /run/seafile/memcache.sock -a 0666"\n
'''



def make_symlink(source, target):
    # get symlink
    pwd = os.getcwd()

    os.chdir(os.path.dirname(target))
    symlink = os.path.realpath(source)
    os.chdir(pwd)
    os.symlink(symlink, target)
    # return symlink



class SeahubCommand(SeafCommand):

    @contextlib.contextmanager
    def generate_conf(self):

        with self.prepare_datadir():
            conf = CONF
            cfile = os.path.join(CONF.cfgdir, FILENAME)
            text = TEMPLATE % dict(key=CONF.hubkey,
                                   name=conf.dbname,
                                   engine=conf.engine,
                                   username=conf.dbuser,
                                   password=conf.dbpass,
                                   host=conf.dbhost,
                                   port=conf.dbport)
            memconf = None
            if CONF.memcache:
                text += MEMCACHED
                memconf = os.path.join(CONF.cfgdir, FILENAME2)
                if not os.path.exists(memconf):
                    with open(memconf, 'w') as f:
                        f.write(MEMCACHE)
                else:
                    memconf = None

            with open(cfile, 'w') as f:
                f.write(text)

            self.chown(cfile)
            try:
                yield
            except Exception as e:
                os.remove(cfile)
                if memconf:
                    os.remove(memconf)
                raise e


    @contextlib.contextmanager
    def prepare_avatar_dir(self):
        media_dir = os.path.join(CONF.seahub, 'media')
        orig_avatar_dir = os.path.join(media_dir, 'avatars')
        orig_avatar_dir_default = os.path.join(media_dir, 'avatars.default')

        seahub_data_dir = os.path.join(CONF.datadir, SeafileCommand.DATADIR)
        dest_avatar_dir = os.path.join(seahub_data_dir, 'avatars')

        # backup avatars
        shutil.move(orig_avatar_dir, orig_avatar_dir_default)
        # copy to dst
        shutil.copytree(orig_avatar_dir_default, dest_avatar_dir)
        # change owner
        self.chown(dest_avatar_dir)
        # make symlink
        make_symlink(dest_avatar_dir, orig_avatar_dir)


        try:
            yield
        except Exception as e:
            # rollback
            os.unlink(orig_avatar_dir)
            shutil.rmtree(dest_avatar_dir)
            shutil.move(orig_avatar_dir_default, orig_avatar_dir)
            raise e

    def execute(self):
        with self.prepare_avatar_dir():
            with self.database.prepare():
                sqlfile = os.path.join(CONF.seahub, 'sql', 'mysql.sql')
                info = dict(user=CONF.dbuser, passwd=CONF.dbpass,
                            host=CONF.dbhost, port=CONF.dbport,
                            schema=CONF.dbname, sqlfile=sqlfile)
                command = 'mysql -u%(user)s -p%(passwd)s -h%(host)s -P %(port)d %(schema)s < %(sqlfile)s' % info
                sub = subprocess.Popen(command, shell=True)
                code = sub.wait()
                if code != 0:
                    raise ValueError('Run init sql fail')
                thumbdir = os.path.join(CONF.seahub, 'seahub', 'thumbnail', 'thumb')
                if not os.path.exists(thumbdir):
                    os.makedirs(thumbdir)
                self.chown(thumbdir)
