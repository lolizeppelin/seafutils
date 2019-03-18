import os
import contextlib
import subprocess
from ConfigParser import ConfigParser
from oslocfg import cfg
from seafutil.command import SeafCommand
from seafutil.ccnet import CcnetCommand


CONF = cfg.CONF
NAME = 'seafile'
FILENAME = 'seafile.conf'
FILENAME2 = 'seafdav.conf'
FILENAME3 = 'seafile.ini'

class SeafileCommand(SeafCommand):


    EXECFILE = '/usr/bin/seaf-server-init'

    DATADIR = 'seafile-data'

    def execute(self):

        def execute(self):
            with self.database.prepare():
                sub = subprocess.Popen(executable=self.EXECFILE, args=self.generate_cmd(),  preexec_fn=self.pre_exec)
                code = sub.wait()
                if code != 0:
                    raise ValueError('execute seaf-server-init fail')

    def generate_cmd(self):

        conf = CONF[NAME]
        argv = [
            self.EXECFILE,
            '-F', CONF.cfgdir,
            '--seafile-dir', os.path.join(CONF.datadir, self.DATADIR),
            '--fileserver-port', str(conf.port),
        ]

        return argv

    @contextlib.contextmanager
    def generate_conf(self):

        if os.path.exists(CONF.cfgdir, FILENAME):
            raise Exception('config file exist!')
        if os.path.exists(CONF.cfgdir, FILENAME2):
            raise Exception('config file2 exist!')
        if os.path.join(CONF.datadir, CcnetCommand.DATADIR, FILENAME2):
            raise Exception('config file3 exist!')
        ccdatadir = os.path.join(CONF.datadir, CcnetCommand.DATADIR)
        if not os.path.exists(ccdatadir) or not os.path.isdir(ccdatadir):
            raise Exception('Ccnet not init finish?')
        if os.stat(ccdatadir).st_uid != self.user.pw_uid or os.stat(ccdatadir).st_gid != self.user.pw_gid:
            raise Exception('Dir %s is not owner by %s' % (ccdatadir, self.user.pw_name))
        if os.path.exists(os.path.join(CONF.datadir, CcnetCommand.DATADIR, FILENAME3)):
            raise Exception('Config seafie.ini exist')

        with self.prepare_datadir():
            conf = CONF[NAME]
            cfile = os.path.join(CONF.cfgdir, FILENAME)
            section = 'database'
            config = ConfigParser()
            config.add_section(section)
            config.set(section, 'type', conf.engine)
            config.set(section, 'host', conf.dbhost or conf.unix_socket)
            config.set(section, 'port', str(conf.dbport))
            config.set(section, 'user', conf.dbuser)
            config.set(section, 'password', conf.dbpass)
            config.set(section, 'db_name', conf.dbname)
            config.set(section, 'connection_charset', 'utf8')
            with open(cfile, 'wb') as f:
                config.write(f)

            cfile2 = os.path.join(CONF.cfgdir, FILENAME2)
            section = 'WEBDAV'
            config = ConfigParser()
            config.add_section(section)
            config.set(section, 'enabled', 'false')
            config.set(section, 'port', str(conf.devport))
            config.set(section, 'fastcgi', 'true')
            config.set(section, 'share_name', '/')

            with open(cfile2, 'wb') as f:
                config.write(f)

            cfile3 = os.path.join(CONF.datadir, CcnetCommand.DATADIR, FILENAME3)
            with open(cfile3, 'w') as fp:
                fp.write(os.path.join(CONF.datadir, self.DATADIR))
            self.chown(cfile3)

            try:
                yield
            except Exception as e:
                os.remove(cfile)
                os.remove(cfile2)
                os.remove(cfile3)
                raise e