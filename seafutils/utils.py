import os

if os.name == 'nt':

    def getuser(uid):
        return "seafile"


    def switch_to_seafile():
        """
        do nothing
        :return:
        """
        return True


else:
    import pwd


    def switch_to_seafile():
        """
        do nothing
        :return:
        """
        user = pwd.getpwnam("seafile")
        uid = os.getuid()
        if uid == user.pw_uid:
            return True
        if uid != 0:
            return False
        os.setgid(user.pw_gid)
        os.setuid(user.pw_uid)
        return True


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
    return args
