# seafile 导出 seafutils-dump
import os
from distutils.spawn import find_executable
from oslo_config import cfg

from seafutils.config.seafile import dump_opts

FSCK = find_executable("seaf-fsck")


def run():
    """
    参数 top_export_path 是放置导出文件的目录。每个资料库将导出为导出目录的子目录。如果不指定资料库的ID，将导出所有库。

    目前只能导出未加密的资料库，加密资料库将被跳过。

        -c "${default_ccnet_conf_dir}" -d "${seafile_data_dir}" \
        -F "${default_conf_dir}" \

    cd seafile-server-latest
    ./seaf-fsck.sh --export top_export_path [library-id1] [library-id2] ...


    :return:
    """

    cfg.CONF.register_cli_opts(dump_opts)
    cfg.CONF(project='seafile-dump', description="seafile dump tool")

    args = [
        FSCK,
        '-F', cfg.CONF.central,
        '-c', cfg.CONF.config,
        '-d', cfg.CONF.datadir,
        '--export', cfg.CONF.export,
    ]

    if cfg.CONF.repos:
        for r in cfg.CONF.repos:
            args.append(str(r))
    os.execv(FSCK, args)
