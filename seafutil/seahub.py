import os
import shutil
import contextlib
from oslocfg import cfg
from seafutil.command import SeafCommand
from seafutil.seafile import SeafileCommand


CONF = cfg.CONF
NAME = 'seahub'
FILENAME = 'seahub_settings.py'


template = '''\
# -*- coding: utf-8 -*-\n
SECRET_KEY = %(key)s\n
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%(engine)s',
        'NAME': '%(name)s',
        'USER': '%(username)s',
        'PASSWORD': '%(password)s',
        'HOST': '%(host)s',
        'PORT': '%(port)s'
    }
}'''

def make_symlink(source, target):
    # get symlink
    pwd = os.getcwd()

    os.chdir(os.path.dirname(target))
    symlink = os.path.realpath(source)
    os.chdir(pwd)
    os.symlink(symlink, target)
    # return symlink



class SeahubCommand(SeafCommand):

    def generate_conf(self):

        conf = CONF[NAME]

        cfile = os.path.join(CONF.cfgdir, FILENAME)
        text = template % dict(key=CONF.hubkey,
                               name=conf.dbname,
                               engine=conf.engine,
                               username=conf.dbuser,
                               password=conf.dbpass,
                               host=conf.dbhost,
                               port=conf.dbport)
        with open(cfile, 'w') as f:
            f.write(text)

    @contextlib.contextmanager
    def prepare_avatar_dir(self):
        media_dir = os.path.join(CONF, 'seahub', 'media')
        orig_avatar_dir = os.path.join(media_dir, 'avatars')
        orig_avatar_dir_default = os.path.join(media_dir, 'avatars.default')

        seahub_data_dir = os.path.join(CONF.datadir, SeafileCommand.DATADIR)
        dest_avatar_dir = os.path.join(seahub_data_dir, 'avatars')

        # backup avatars
        shutil.move(orig_avatar_dir, orig_avatar_dir_default)
        # copy to dst
        shutil.copy(orig_avatar_dir_default, dest_avatar_dir)
        # change owner
        os.chown(dest_avatar_dir, self.user.pw_uid, self.user.pw_gid)
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
                pass