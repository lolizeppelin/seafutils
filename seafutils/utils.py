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
