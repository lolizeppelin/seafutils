import os
import sys
import pwd
import grp
import contextlib
from oslocfg import cfg
import sqlalchemy
import sqlalchemy.engine.url
from sqlalchemy.pool import NullPool

CONF = cfg.CONF


class SeafCommand(object):

    def __init__(self, environ_file):
        if not os.path.exists(environ_file):
            raise ValueError('environ file not exist')
        if not os.path.isfile(environ_file):
            raise ValueError('environ file not is not a file')
        if os.path.getsize(environ_file) > 4096:
            raise ValueError('environ file over size')

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
                    self.user = value
                if key.lower() == 'group':
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

    def pre_exec(self):
        os.setgid(self.group.gr_gid)
        os.setuid(self.user.pw_uid)


    def connect(self):
        url = '%(engine)s://%(user)s:%(passwd)s@%(host)s:%(port)s' % \
              dict(engine=self.ENGINEMAP[CONF.engine],
                   user=CONF.rname if CONF.create else CONF.dbuser,
                   passwd=CONF.rpass if CONF.create else CONF.dbpasswd,
                   host=CONF.dbhost, port=str(CONF.dbport))
        if CONF.create:
            url += '/%s' % CONF.dbname
        engine = sqlalchemy.create_engine(url,
                                          poolclass=NullPool, echo=CONF.debug,
                                          logging_name='init-%s' % CONF.dbname,
                                          encoding='utf-8')
        return engine


    def generate_cmd(self):
        pass

    def generate_conf(self):
        pass