#!/usr/bin/python2.7
import os
import sys
from oslocfg import cfg
from seafutil import config
from seafutil.ccnet import CcnetCommand
import ccnet

CONF = cfg.CONF


class RPC(object):
    def __init__(self):
        ccdatadir = os.path.join(CONF.datadir, CcnetCommand.DATADIR)
        self.rpc_client = ccnet.CcnetThreadedRpcClient(
            ccnet.ClientPool(ccdatadir, central_config_dir=CONF.cfgdir))

    def get_db_email_users(self):
        return self.rpc_client.get_emailusers('DB', 0, 1)

    def create_admin(self):
        return self.rpc_client.add_emailuser(CONF.email, CONF.passwd, 1, 1)

    @property
    def noadmin(self):
        users = self.get_db_email_users()
        return len(users) == 0


def main():
    if os.getuid() != 0:
        sys.stderr.write('Init script run user not root\n')
        sys.stderr.flush()
        sys.exit(1)
    CONF.register_cli_opts(config.server_opts)
    CONF(project='seafile-init-admin', default_config_files=['/etc/seafile.conf', ])
    rpclient = RPC()
    if rpclient.noadmin:
        rpclient.create_admin()
    else:
        print 'Admin exist!'
        sys.exit(1)


if __name__ == '__main__':
    main()