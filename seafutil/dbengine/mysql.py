import contextlib
from oslocfg import cfg

from seafutil.dbengine import DbEngineBase

CONF = cfg.CONF


class DbEngine(DbEngineBase):

    ENGINEPREFIX = 'mysql+mysqldb'


    def tables(self):
        tbs = []
        with self.engine.connect() as conn:
            r = conn.execute("show tables")
            for row in r:
                tbs.append(row[0])
            r.close()
        return tbs

    def databases(self):
        dbs = []
        with self.engine.connect() as conn:
            r = conn.execute("show databases")
            for row in r:
                dbs.append(row[0])
            r.close()
        return dbs

    def create_db(self):
        sql = "CREATE DATABASE %s default character set utf8" % CONF.dbname
        with self.engine.connect() as conn:
            r = conn.execute(sql)
            r.close()


    def create_user(self):
        _auth = {'schema': CONF.dbname,
                 'user': CONF.dbuser,
                 'passwd': CONF.dbpass,
                 'source': CONF.scope,
                 'privileges': 'ALL'}
        sqls = ["GRANT %(privileges)s ON %(schema)s.* "
                "TO '%(user)s'@'%(source)s' IDENTIFIED by '%(passwd)s'" % _auth,
                'FLUSH PRIVILEGES']
        with self.engine.connect() as conn:
            for sql in sqls:
                r = conn.execute(sql)
                r.close()


    def drop_user(self):
        sqls = ["DROP USER '%s'@'%s'" % (CONF.dbuser, CONF.scope),
                'FLUSH PRIVILEGES']
        with self.engine.connect() as conn:
            for sql in sqls:
                r = conn.execute(sql)
                r.close()

    def drop_db(self):
        sql = "DROP DATABASE %s" % CONF.dbname
        with self.engine.connect() as conn:
            r = conn.execute(sql)
            r.close()


    @contextlib.contextmanager
    def _create(self):
        if CONF.dbname in self.databases():
            raise ValueError('Database already exist, try --nocreate')
        try:
            self.create_db()
            self.create_user()
            yield
        except Exception as e:
            self.drop_user()
            self.drop_db()
            raise e
