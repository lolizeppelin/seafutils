import os
import glob
import shutil
import contextlib
import subprocess
from ConfigParser import ConfigParser
from oslocfg import cfg
from seafutil.command import SeafCommand
from seafutil.ccnet import CcnetCommand


CONF = cfg.CONF
NAME = 'seafile'
FILENAME = 'seafile.conf'
FILENAME3 = 'seafile.ini'

class SeafileCommand(SeafCommand):


    EXECFILE = '/usr/bin/seaf-server-init'

    DATADIR = 'seafile-data'

    DOCPATH = '/usr/share/doc/seafile'

    def execute(self):
        with self.database.prepare():
            sub = subprocess.Popen(executable=self.EXECFILE, args=self.generate_cmd(),  preexec_fn=self.pre_exec)
            code = sub.wait()
            if code != 0:
                raise ValueError('execute seaf-server-init fail')
            template_dir = os.path.join(CONF.datadir, self.DATADIR, 'library-template')
            os.makedirs(template_dir)
            self.chown(template_dir)
            for filename in os.listdir(self.DOCPATH):
                if filename.endswith('.doc'):
                    src = os.path.join(self.DOCPATH, filename)
                    dst = os.path.join(template_dir, filename)
                    if os.path.isfile(src):
                        shutil.copy(src, dst)
                        self.chown(dst)


    def generate_cmd(self):

        conf = CONF
        argv = [
            self.EXECFILE,
            '-F', CONF.cfgdir,
            '--seafile-dir', os.path.join(CONF.datadir, self.DATADIR),
            '--fileserver-port', str(conf.port),
        ]

        return argv

    @contextlib.contextmanager
    def generate_conf(self):

        if os.path.exists(os.path.join(CONF.cfgdir, FILENAME)):
            raise Exception('config file exist!')

        ccdatadir = os.path.join(CONF.datadir, CcnetCommand.DATADIR)
        if not os.path.exists(ccdatadir) or not os.path.isdir(ccdatadir):
            raise Exception('Ccnet not init finish?')
        if os.stat(ccdatadir).st_uid != self.user.pw_uid or os.stat(ccdatadir).st_gid != self.user.pw_gid:
            raise Exception('Dir %s is not owner by %s' % (ccdatadir, self.user.pw_name))
        if os.path.exists(os.path.join(ccdatadir, FILENAME3)):
            raise Exception('Config seafie.ini exist')

        with self.prepare_datadir():
            conf = CONF
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
            self.chown(cfile)

            cfile3 = os.path.join(CONF.datadir, CcnetCommand.DATADIR, FILENAME3)
            with open(cfile3, 'w') as fp:
                fp.write(os.path.join(CONF.datadir, self.DATADIR))
            self.chown(cfile3)

            try:
                yield
            except Exception as e:
                os.remove(cfile)
                os.remove(cfile3)
                raise e