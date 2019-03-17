import os
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

    def generate_db_conf(self):

        if os.path.exists(CONF.cfgdir, FILENAME):
            raise Exception('config file exist!')
        if os.path.exists(CONF.cfgdir, FILENAME2):
            raise Exception('config file2 exist!')
        if os.path.join(CONF.datadir, CcnetCommand.DATADIR, FILENAME2):
            raise Exception('config file3 exist!')

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

        cfile = os.path.join(CONF.cfgdir, FILENAME2)
        section = 'WEBDAV'
        config = ConfigParser()
        config.add_section(section)
        config.set(section, 'enabled', 'false')
        config.set(section, 'port', str(conf.devport))
        config.set(section, 'fastcgi', 'true')
        config.set(section, 'share_name', '/')

        with open(cfile, 'wb') as f:
            config.write(f)

        cfile = os.path.join(CONF.datadir, CcnetCommand.DATADIR, FILENAME3)
        with open(cfile, 'w') as fp:
            fp.write(os.path.join(CONF.datadir, self.DATADIR))