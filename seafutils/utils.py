import os

if os.name == 'nt':

    def getuser(uid):
        return "seafile"

else:
    import pwd


    def getuser(uid=None):
        if uid is None:
            uid = os.getuid()
        return pwd.getpwuid(uid).pw_name


def get_py2path(*args):
    args = list(args)
    # 写死python2.7 路径
    args.extend([
        '/usr/lib64/python2.7/site-packages',
        '/usr/lib/python2.7/site-packages',
    ])
    return ':'.join(args)
