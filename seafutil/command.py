import os
import sys
import pwd
import grp
import contextlib
from oslocfg import cfg
CONF = cfg.CONF


class SeafCommand(object):

    DATADIR = 'unkonwn'

    def __init__(self):

        if CONF.datadir == '/':
            raise ValueError('Datadir value error')
        if '.' in CONF.datadir:
            raise ValueError('Datadir value error')
        if not os.path.exists(CONF.datadir):
            raise ValueError('Path %s not exist' % CONF.datadir)

        try:
            self.user = pwd.getpwnam(CONF.user)
            self.group = grp.getgrnam(CONF.group)
        except KeyError:
            raise ValueError('Group or user can not be found')
        else:
            if self.user.pw_gid != self.group.gr_gid:
                raise ValueError('User gid not eq group id')

        import_str = 'seafutil.dbengine.%s' % CONF.engine
        __import__(import_str)
        module = sys.modules[import_str]
        cls = getattr(module, 'DbEngine')
        self.database = cls()

    def chown(self, path):
        os.chown(path, self.user.pw_uid, self.user.pw_gid)

    def pre_exec(self):
        os.setgid(self.user.pw_gid)
        os.setuid(self.user.pw_uid)

    @contextlib.contextmanager
    def prepare_datadir(self):
        datadir = os.path.join(CONF.datadir, self.DATADIR)
        if os.path.exists(datadir):
            for root, dirs, files in os.walk(datadir):
                if dirs or files:
                    raise Exception('Data dir is not empty')
                else:
                    break
        else:
            os.makedirs(datadir, mode=0755, exist_ok=False)
        self.chown(datadir)
        try:
            yield
        except Exception as e:
            try:
                os.removedirs(datadir)
            except Exception:
                pass
            raise e

    def generate_cmd(self):
        pass
    @contextlib.contextmanager
    def generate_conf(self):
        pass