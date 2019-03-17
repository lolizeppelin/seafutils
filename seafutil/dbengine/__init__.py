from oslocfg import cfg
import contextlib
import sqlalchemy
import sqlalchemy.engine.url
from sqlalchemy.pool import NullPool

CONF = cfg.CONF


class DbEngineBase(object):

    ENGINEPREFIX = ''


    def __init__(self):
        self._engine = None


    @property
    def engine(self):
        if self._engine is None:
            self._engine = self._connect()
        return self._engine


    def _connect(self):
        url = '%(engine)s://%(user)s:%(passwd)s@%(host)s:%(port)s' % \
              dict(engine=self.ENGINEPREFIX,
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


    @contextlib.contextmanager
    def prepare(self):
        if CONF.create:
            with self._create():
                yield
        else:
            if self.tables():
                raise ValueError('Table in database %s' % CONF.dbname)
            yield


    def _create(self):
        raise NotImplementedError


    def tables(self):
        raise NotImplementedError


    def create_db(self):
        raise NotImplementedError


    def create_user(self):
        raise NotImplementedError