import os
import sys
import pwd
import grp
import contextlib
from oslocfg import cfg
CONF = cfg.CONF


class SeafCommand(object):

    DATADIR = 'unkonwn'

    def __init__(self, environ_file):
        if not os.path.exists(environ_file):
            raise ValueError('environ file not exist')
        if not os.path.isfile(environ_file):
            raise ValueError('environ file not is not a file')
        if os.path.getsize(environ_file) > 4096:
            raise ValueError('environ file over size')

        if CONF.datadir == '/':
            raise ValueError('Datadir value error')
        if '.' in CONF.datadir:
            raise ValueError('Datadir value error')
        if not os.path.exists(CONF.datadir):
            raise ValueError('Path %s not exist' % CONF.datadir)
        self.user = None
        self.group = None
        with open(environ_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                kvlist = line.strip().split("=")
                if len(kvlist) != 2:
                    raise ValueError('environ is not a key value ini file')
                key = kvlist[0].strip()
                value = kvlist[1].strip()
                if key.lower() == 'user':
                    if value == 'root':
                        raise ValueError('Seafile user is root!')
                    self.user = value
                if key.lower() == 'group':
                    if value == 'root':
                        raise ValueError('Seafile group is root!')
                    self.group = value
                if self.user and self.group:
                    break
            else:
                raise ValueError('Can not find user and group in environ file')
        try:
            self.user = pwd.getpwnam(self.user)
            self.group = grp.getgrnam(self.group)
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