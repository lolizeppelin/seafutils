# 更新配置
import os
from distutils.spawn import find_executable


def reset():
    """

    export CCNET_CONF_DIR=${default_ccnet_conf_dir}
    export SEAFILE_CONF_DIR=${default_seafile_data_dir}
    export SEAFILE_CENTRAL_CONF_DIR=${central_config_dir}
    export PYTHONPATH=${INSTALLPATH}/seafile/lib/python3/site-packages:${INSTALLPATH}/seafile/lib64/python3/site-packages:${INSTALLPATH}/seahub/thirdpart:$PYTHONPATH
    export SEAFILE_RPC_PIPE_PATH=${INSTALLPATH}/runtime
    export SEAHUB_DIR=$seahubdir

    if [[ -d ${INSTALLPATH}/pro ]]; then
        export PYTHONPATH=$PYTHONPATH:$pro_pylibs_dir
        export SEAFES_DIR=$seafesdir
        export SEAFILE_RPC_PIPE_PATH=${INSTALLPATH}/runtime
    fi

    manage_py=${INSTALLPATH}/seahub/manage.py
    exec "$PYTHON" "$manage_py" createsuperuser


    :return:
    """
