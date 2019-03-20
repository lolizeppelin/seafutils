import os
import contextlib
from oslocfg import cfg
import subprocess
from seafutil.command import SeafCommand

from ConfigParser import ConfigParser


CONF = cfg.CONF
NAME = 'ccnet'
FILENAME = 'ccnet.conf'

class CcnetCommand(SeafCommand):


    EXECFILE = '/usr/bin/ccnet-init'

    DATADIR = 'ccnet-data'

    def execute(self):
        with self.database.prepare():
            sub = subprocess.Popen(executable=self.EXECFILE, args=self.generate_cmd(), preexec_fn=self.pre_exec)
            code = sub.wait()
            if code != 0:
                raise ValueError('execute ccnet-init fail')

    def generate_cmd(self):

        argv = [
            self.EXECFILE,
            '-F', CONF.cfgdir,
            '--config-dir', os.path.join(CONF.datadir, self.DATADIR),
            '--name', CONF.name,
            '--host', CONF.external,
        ]

        return argv

    @contextlib.contextmanager
    def generate_conf(self):
        if os.path.exists(os.path.join(CONF.cfgdir, FILENAME)):
            raise Exception('config file exist!')
        with self.prepare_datadir():
            conf = CONF
            cfile = os.path.join(CONF.cfgdir, FILENAME)
            section = 'Database'
            config = ConfigParser()
            config.add_section(section)
            config.set(section, 'ENGINE', conf.engine)
            config.set(section, 'HOST', conf.dbhost)
            config.set(section, 'PORT', str(conf.dbport))
            config.set(section, 'USER', conf.dbuser)
            config.set(section, 'PASSWD', conf.dbpass)
            config.set(section, 'DB', conf.dbname)
            config.set(section, 'CONNECTION_CHARSET', 'utf8')
            with open(cfile, 'wb') as f:
                config.write(f)
            self.chown(cfile)
            try:
                yield
            except Exception as e:
                os.remove(cfile)
                raise e

