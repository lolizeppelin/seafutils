import os
import shutil
import stat
import random
import string
import uuid

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


def verify(path, empty=False):
    try:
        st = os.stat(path)
    except OSError:
        raise ValueError("path %s not exist or not readable" % path)
    if not stat.S_ISDIR(st.st_mode):
        raise ValueError("path %s not directory" % path)
    if not os.access(path, os.R_OK | os.W_OK | os.X_OK):
        raise ValueError("path %s can not be write or enter" % path)
    if getuser(st.st_uid) != 'seafile':
        raise ValueError("path %s owner is not seafile" % path)
    if empty:
        for _ in os.scandir(path):
            raise ValueError("path %s is not empty" % path)


@contextlib.contextmanager
def connect(**kwargs):
    try:
        c = psycopg.connect(connect_timeout=3, **kwargs)
    except Exception as e:
        raise ValueError("psycopg connect failed: %s" % str(e))
    try:
        yield c
    finally:
        c.close()


@contextlib.contextmanager
def create_database(conf):
    admin = conf.admin or cfg.CONF.admin
    admin_passwd = conf.admin_passwd or cfg.CONF.admin_passwd
    with connect(host=conf.host, port=conf.port, user=admin, password=admin_passwd,
                 dbname='postgres') as conn:
        conn.autocommit = True
        conn.execute("""CREATE DATABASE %s ENCODING 'UTF8' 
        LC_COLLATE = 'zh_CN.UTF-8' LC_CTYPE = 'zh_CN.UTF-8'""" % conf.db)
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
                cursor.execute('ALTER DATABASE "%s" OWNER TO "%s"' % (conf.db, admin))
                cursor.execute('DROP OWNED by "%s" CASCADE' % conf.user)
                cursor.execute('DROP ROLE IF EXISTS "%s"' % conf.user)

            conn.autocommit = True
            conn.execute('DROP DATABASE IF EXISTS "%s"' % conf.db)
        raise


@contextlib.contextmanager
def clean(path):
    verify(os.path.dirname(path))
    if os.path.exists(path):
        raise ValueError('path %s already exist' % path)
    try:
        yield
    except Exception:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        raise


@contextlib.contextmanager
def init_seafile():
    """
    创建seafile配置文件与数据库,调用seafile初始化命令
    :return:
    """

    config = templates.seafile()
    path = os.path.join(cfg.CONF.central, 'seafile.conf')
    with clean(path):
        args = [
            SEAFILE,
            '-F', cfg.CONF.central,
            '--seafile-dir', cfg.CONF.datadir,
            '--fileserver-port', str(cfg.CONF.seafile.eport),
        ]

        with clean(cfg.CONF.datadir):
            with create_database(cfg.CONF.seafile):
                ini = os.path.join(cfg.CONF.config, 'seafile.ini')
                with clean(ini):
                    with open(ini, 'w') as f:
                        f.write(cfg.CONF.datadir)
                    sub = subprocess.Popen(args, executable=SEAFILE, shell=False)
                    if sub.wait() != 0:
                        raise ValueError("seafile initialize execute failed")
                    config.read(path)
                    with open(path, 'w') as f:
                        config.write(f)
                    yield


@contextlib.contextmanager
def init_ccnet():
    """
    创建ccnet配置文件与数据库,调用ccnet初始化命令
    :return:
    """
    config = templates.ccnet()
    path = os.path.join(cfg.CONF.central, 'ccnet.conf')
    with clean(path):
        args = [
            CCNET,
            '-F', cfg.CONF.central,
            '--config-dir', cfg.CONF.config,
            '--name', cfg.CONF.ccnet.name,
            '--host', cfg.CONF.ccnet.domain,
        ]

        with clean(cfg.CONF.config):
            with create_database(cfg.CONF.ccnet):
                sub = subprocess.Popen(args, executable=CCNET, shell=False)
                if sub.wait() != 0:
                    raise ValueError("ccnet initialize execute failed")
                config.read(path)
                with open(path, 'w') as f:
                    config.write(f)
                yield


def init_seahub():
    """
    创建seahub配置文件,导入数据库sql
    :return:
    """
    sql = os.path.join(cfg.CONF.website, "sql", "postgres.sql")
    if not os.path.exists(sql):
        raise ValueError("seahub sql file %s not exist")
    conf = cfg.CONF.seahub

    path = os.path.join(cfg.CONF.central, 'seahub_settings.py')
    with clean(path):
        with open(path, 'w') as f:
            content = templates.seahub()
            f.write(content)

        with create_database(cfg.CONF.seahub):
            args = [
                PSQL,
                '-w', '-q',
                '-U', conf.user,
                '-h', conf.host,
                '-p', str(conf.port),
                '-f', sql,
                conf.db,
            ]
            sub = subprocess.Popen(args, executable=PSQL, shell=False, env=dict(PGPASSWORD=conf.passwd))
            if sub.wait() != 0:
                raise ValueError("seahub load sql failed")


def init():
    # 数据库默认密码使用随机密码
    cfg.set_defaults(ccnet_init_opts, passwd=password(10))
    cfg.set_defaults(seafile_init_opts, passwd=password(10))
    # secret使用uuid4随机数
    cfg.set_defaults(seahub_init_opts, passwd=password(10), secret=uuid.uuid4().hex[:20])

    cfg.CONF.register_cli_opts(init_opts)
    cfg.CONF.register_cli_opts(ccnet_init_opts, 'ccnet')
    cfg.CONF.register_cli_opts(seahub_init_opts, 'seahub')
    cfg.CONF.register_cli_opts(seafile_init_opts, 'seafile')
    cfg.CONF(project='seafile-init', description="seafile initialize")

    verify(cfg.CONF.central, empty=True)

    # ------------ seafile ------------
    with init_ccnet():
        with init_seafile():
            init_seahub()


def relocate():
    cfg.CONF(project='seafile-relocate', description="seafile relocate data dir")
    initialized()
    if not os.path.exists(cfg.CONF.datadir) or not os.path.isdir(cfg.CONF.datadir):
        raise ValueError("%s is not exist or not directory" % cfg.CONF.datadir)
    ini = os.path.join(cfg.CONF.config, "seafile.ini")
    if not os.path.exists(ini) or not os.path.isfile(ini):
        raise ValueError("%s not exist or not file" % ini)
    with open(ini, "w") as f:
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
