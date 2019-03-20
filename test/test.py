
x = '''



        g_setenv ("CCNET_CONF_DIR", ctl->config_dir, TRUE);
    g_setenv ("SEAFILE_CONF_DIR", ctl->seafile_dir, TRUE);
    g_setenv ("SEAFILE_CENTRAL_CONF_DIR", ctl->central_config_dir, TRUE);

    char *seahub_dir = g_build_filename (installpath, "seahub", NULL);
    char *seafdav_conf = g_build_filename (ctl->central_config_dir, "seafdav.conf", NULL);
    g_setenv ("SEAHUB_DIR", seahub_dir, TRUE);
    g_setenv ("SEAFDAV_CONF", seafdav_conf, TRUE);

        char *argv[] = {
        "seaf-server",
        "-F", ctl->central_config_dir,
        "-c", ctl->config_dir,
        "-d", ctl->seafile_dir,
        "-l", logfile,
        "-P", ctl->pidfile[PID_SERVER],
        NULL};

    char *argv[] = {
        "ccnet-server",
        "-F", ctl->central_config_dir,
        "-c", ctl->config_dir,
        "-f", logfile,
        "-d",
        "-P", ctl->pidfile[PID_CCNET],
        NULL};



'''