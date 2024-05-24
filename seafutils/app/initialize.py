import os
import stat
import random
import string
import psycopg
import contextlib
import subprocess
from distutils.spawn import find_executable
from oslo_config import cfg

from seafutils.utils import getuser
from seafutils.config import templates
from seafutils.config.initialize import init_opts, ccnet_init_opts, seahub_init_opts, seafile_init_opts

CCNET = find_executable("ccnet-init")
SEAFILE = find_executable("seaf-server-init")
PSQL = find_executable("psql")


def password(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def verify(path):
    try:
        st = os.stat(path)
    except OSError:
        raise ValueError("path %s not exist or not readable" % path)
    if not stat.S_ISDIR(st.st_mode):
        raise ValueError("path %s not directory" % path)
    if not os.access(path, os.R_OK | os.W_OK | os.X_OK):
        raise ValueError("path %s can not be write or enter")
    if getuser(st.st_uid) != 'seafile':
        raise ValueError("path %s owner is not seafile" % path)
    for _ in os.scandir(path):
        raise ValueError("path %s is not empty" % path)


@contextlib.contextmanager
def connect(**kwargs):
    c = psycopg.connect(connect_timeout=3, **kwargs)
    try:
        yield c
    finally:
        c.close()


@contextlib.contextmanager
def create_database(conf):
    admin = cfg.CONF.admin or conf.user
    admin_passwd = cfg.CONF.admin_passwd or conf.passwd
    if not admin_passwd:
        raise ValueError("admin password not found")
    with connect(host=conf.host, port=conf.port, user=admin, password=admin_passwd,
                 dbname='postgres') as conn:
        conn.autocommit = True
        conn.execute("""CREATE DATABASE %s ENCODING 'UTF8' LC_COLLATE = 'zh_CN.UTF-8' LC_CTYPE = 'zh_CN.UTF-8'""")
        conn.autocommit = False

        cursor = conn.cursor()
        with conn.transaction("create"):
            cursor.execute("""CREATE ROLE "%s" WITH LOGIN PASSWORD '%s'""" % (conf.user, conf.passwd))
            cursor.execute('ALTER DATABASE "%s" OWNER TO "%s"' % (conf.db, conf.user))
            cursor.execute('GRANT ALL ON SCHEMA PUBLIC TO "%s"' % conf.user)
    try:
        yield
    except Exception:
        with connect(host=conf.host, port=conf.port,
                     user=admin, password=admin_passwd,
                     dbname='postgres') as conn:
            cursor = conn.cursor()
            with conn.transaction("drop"):
                cursor.execute('DROP OWNED by "%s" CASCADE' % conf.user)
                cursor.execute('DROP ROLE IF EXISTS "%s"' % conf.user)

            conn.autocommit = True
            conn.execute('DROP DATABASE IF EXISTS "%s"' % conf.db)
        raise


@contextlib.contextmanager
def cfile(path):
    if os.path.exists(path):
        raise ValueError('path %s already exist' % path)
    failed = False
    with open(path, 'w') as f:
        try:
            yield f
        except Exception:
            failed = True
    if failed:
        os.remove(path)


@contextlib.contextmanager
def init_seafile():
    """
    创建seafile配置文件与数据库,调用seafile初始化命令
    :return:
    """
    with cfile(os.path.join(cfg.CONF.central, 'seafile.conf')) as f:
        config = templates.seafile()
        config.write(f)
        f.flush()

        args = [
            SEAFILE,
            '-F', cfg.CONF.central,
            '--seafile-dir', cfg.CONF.datadir,
            '--fileserver-port', str(cfg.CONF.seafile.eport),
        ]

        with create_database(cfg.CONF.seafile):
            with cfile(os.path.join(cfg.CONF.config, 'seafile.ini')) as fi:
                fi.write(cfg.CONF.datadir)
                fi.flush()
                sub = subprocess.Popen(args, executable=SEAFILE, shell=False)
                if sub.wait() != 0:
                    raise ValueError("seafile initialize failed")
                yield


@contextlib.contextmanager
def init_ccnet():
    """
    创建ccnet配置文件与数据库,调用ccnet初始化命令
    :return:
    """
    with cfile(os.path.join(cfg.CONF.central, 'seafile.conf')) as f:
        config = templates.ccnet()
        config.write(f)
        f.flush()

        args = [
            CCNET,
            '-F', cfg.CONF.central,
            '--config-dir', cfg.CONF.config,
            '--name', cfg.CONF.ccent.name,
            '--host', cfg.CONF.ccent.domain,
        ]

        with create_database(cfg.CONF.ccnet):
            sub = subprocess.Popen(args, executable=CCNET, shell=False)
            if sub.wait() != 0:
                raise ValueError("ccnet initialize failed")
            yield


def init_seahub():
    """
    创建seahub配置文件与数据库
    :return:
    """
    sql = os.path.join(cfg.CONF.website, "sql", "postgres.sql")
    if not os.path.exists(sql):
        raise ValueError("seahub sql file %s not exist")
    conf = cfg.CONF.seahub
    with cfile(os.path.join(cfg.CONF.central, 'seahub_settings.py')) as f:
        content = templates.seahub()
        f.write(content)
        with create_database(cfg.CONF.seahub):
            args = [
                PSQL,
                '-U', conf.user,
                '-h', conf.host,
                '-p', str(conf.port),
                '-f', sql,
                '-w',
                conf.db,
            ]
            sub = subprocess.Popen(args, executable=PSQL, shell=False, env=dict(PGPASSWORD=conf.passwd))
            if sub.wait() != 0:
                raise ValueError("seahub load sql failed")


def init():
    # 默认密码使用随机密码
    cfg.set_defaults(ccnet_init_opts, passwd=password(10))
    cfg.set_defaults(seahub_init_opts, passwd=password(10))
    cfg.set_defaults(seafile_init_opts, passwd=password(10))

    cfg.CONF.register_cli_opts(init_opts)
    cfg.CONF.register_cli_opts(ccnet_init_opts, 'ccnet')
    cfg.CONF.register_cli_opts(seahub_init_opts, 'seahub')
    cfg.CONF.register_cli_opts(seafile_init_opts, 'seafile')
    cfg.CONF(project='seafile-init', description="seafile initialize")

    verify(cfg.CONF.central)
    verify(cfg.CONF.config)
    verify(cfg.CONF.datadir)

    # ------------ seafile ------------
    with init_seafile():
        with init_ccnet():
            init_seahub()


def relocate():
    cfg.CONF(project='seafile-relocate', description="seafile relocate data dir")
    initialized()
    if not os.path.exists(cfg.CONF.datadir) or not os.path.isdir(cfg.CONF.datadir):
        raise ValueError("%s is not exist or not directory" % cfg.CONF.datadir)
    cfile = os.path.join(cfg.CONF.config, "seafile.ini")
    if not os.path.exists(cfile) or not os.path.isfile(cfile):
        raise ValueError("%s not exist or not file" % cfile)
    with open(cfile, "w") as f:
        f.write(cfg.CONF.datadir)


def initialized():
    """issuer seafile initialized"""
    for conf in (
            os.path.join(cfg.CONF.central, 'ccnet.conf'),
            os.path.join(cfg.CONF.central, 'seafile.conf'),
            os.path.join(cfg.CONF.central, 'seahub_settings.py'),
    ):
        try:
            st = os.stat(conf)
            if not stat.S_ISREG(st.st_mode):
                raise ValueError("config %s is not file" % conf)
            if getuser(st.st_uid) != 'seafile':
                raise ValueError("config %s owner not seafile" % conf)
            if not os.access(conf, os.R_OK):
                raise ValueError("config %s not readable" % conf)
        except OSError:
            raise ValueError("seafile not initialized or config path error")
