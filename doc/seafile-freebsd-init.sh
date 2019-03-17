#!/bin/sh
#
# $FreeBSD: branches/2019Q1/net-mgmt/seafile-server/files/seafile.in 429506 2016-12-26 12:55:09Z riggs $
#

# PROVIDE: seafile
# REQUIRE: LOGIN cleanvar mysql
# KEYWORD: shutdown
#

#
# Add the following lines to /etc/rc.conf to enable seafile:
#
# seafile_enable (bool):	Set to "NO" by default.
#				Set it to "YES" to enable seafile.
# seafile_user (str):		User to run seafile as
#				Default to "seafile" created by the port
# seafile_group (str):		Group to run seafile as
#				Default to "seafile" created by the port
# seafile_path (str):		Set to "" by default will use the path
#				/usr/local/www/haiwen/seafile-server.
#				Set it to a different path.
# seafile_ccnet (str):		Set to "" by default will use the path
#				/usr/local/www/haiwen/ccnet.
#				Set it to a different path.
# seafile_conf (str):		Set to "" by default will use the path
#				/usr/local/www/haiwen/conf.
#				Set it to a different path.
# seafile_datadir (str):	Set to "" by default will use the path
#				in file /usr/local/www/haiwen/ccnet/seafile.ini.
#				Set it to a different path.
# seafile_logdir (str):		Set to "" by default will use the path
#				/usr/local/www/haiwen/logs
#				Set it to a different path.
# seafile_loglevel (str):	Set to "info" by default.
#				Possible values are debug, warning, info.

. /etc/rc.subr

name="seafile"
rcvar="seafile_enable"

load_rc_config $name

start_cmd="seafile_start"
restart_cmd="seafile_restart"
stop_cmd="seafile_stop"

: ${seafile_enable="NO"}
: ${seafile_user:="seafile"}
: ${seafile_group:="seafile"}
: ${seafile_path:="/usr/local/www/haiwen/seafile-server"}
: ${seafile_ccnet:="/usr/local/www/haiwen/ccnet"}
: ${seafile_conf:="/usr/local/www/haiwen/conf"}
: ${seafile_datadir:="`cat ${seafile_ccnet}/seafile.ini 2>/dev/null`"}
: ${seafile_logdir:="/usr/local/www/haiwen/logs"}
: ${seafile_loglevel:="info"}

command="/usr/local/www/haiwen/seafile-server/seafile/bin/seafile-controller"
command_args="-c \"${seafile_ccnet}\" -d \"${seafile_datadir}\" -F \"${seafile_conf}\" -l \"${seafile_logdir}\" -g \"${seafile_loglevel}\" -G \"${seafile_loglevel}\""

required_dirs="${seafile_ccnet} ${seafile_conf} ${seafile_datadir}"
required_files="${seafile_ccnet}/seafile.ini"

test_config() {
	if ! su -m ${seafile_user} -c "${command} -t ${command_args}" ; then
		exit 1;
	fi
}

check_component_running() {
	name=$1
	cmd=$2
	if pid=$(pgrep -f "$cmd" 2>/dev/null); then
		echo "{$name} is running, pid $pid. You can stop it by: "
		echo
		echo "        kill $pid"
		echo
		echo "Stop it and try again."
		echo
		exit
	fi
}

validate_already_running() {
	if pid=$(pgrep -f "seafile-controller -c ${seafile_ccnet}" 2>/dev/null); then
		echo "Seafile controller is already running, pid $pid"
		echo
		exit 1;
	fi

	check_component_running "ccnet-server" "ccnet-server -c ${seafile_ccnet}"
	check_component_running "seaf-server" "seaf-server -c ${seafile_ccnet}"
	check_component_running "fileserver" "fileserver -c ${seafile_ccnet}"
	check_component_running "seafdav" "wsgidav.server.run_server"
}

prepare_env() {
export PATH=${seafile_path}/seafile/bin:$PATH
export LD_LIBRARY_PATH=${seafile_path}/seafile/lib/:${seafile_path}/seafile/lib64:${LD_LIBRARY_PATH}
}

seafile_start() {
	check_required_before;
	validate_already_running;
	prepare_env;
	test_config;

	echo "Starting seafile server, please wait ..."

	su -m "${seafile_user}" -c "mkdir -p $seafile_logdir"
	su -m "${seafile_user}" -c "$command $command_args"

	sleep 3

	# check if seafile server started successfully
	if ! pgrep -f "seafile-controller -c ${seafile_ccnet}" 2>/dev/null 1>&2; then
	echo "Failed to start seafile server"
	exit 1;
	fi

	echo "Seafile server started"
	echo
}

seafile_stop() {
	if ! pgrep -f "seafile-controller -c ${seafile_ccnet}" 2>/dev/null 1>&2; then
		echo "Seafile is not running"
	return 1;
	fi

	echo "Stopping ${name}."
	pkill -SIGTERM -f "seafile-controller -c ${seafile_ccnet}"
	pkill -f "ccnet-server -c ${seafile_ccnet}"
	pkill -f "seaf-server -c ${seafile_ccnet}"
	pkill -f "fileserver -c ${seafile_ccnet}"
	pkill -f "soffice.*--invisible --nocrashreport"
	pkill -f  "wsgidav.server.run_server"
	return 0
}

seafile_restart() {
	seafile_stop;
	sleep 2
	seafile_start;
}

run_rc_command "$1"
