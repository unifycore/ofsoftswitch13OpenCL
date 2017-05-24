#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo 'Dont forget to use sudo ;-)'
    exit 1
fi
#FWD_ROOT="/home/michal-dp/Dokumenty/ofsoftswitch13"
FWD_ROOT="/home/michal-dp/Dokumenty/ofsoftswitchNewNew/ofsoftswitch13"
CNT_SCRIPT="/home/michal-dp/ryu/ryu/app/dp_controller_net1_3_iperf.py"
#CNT_SCRIPT="/home/michal-dp/ryu/ryu/app/dp_controller_net1_3.py"

CONTROLLER="tcp:127.0.0.1:6633"

function start_fwd() {
	SOCKET="unix:/tmp/dp$1.socket"
	$FWD_ROOT/udatapath/ofdatapath -i "$3" -d "$2" "p$SOCKET" -v --no-slicing > /tmp/dp$1.log 2>&1 &
	$FWD_ROOT/secchan/ofprotocol "$SOCKET" "$CONTROLLER" --fail=closed  > /tmp/of$1.log 2>&1 &
}

function debug_fwd() {
	SOCKET="unix:/tmp/dp$1.socket"
	$FWD_ROOT/secchan/ofprotocol "$SOCKET" "$CONTROLLER" --fail=closed  > /tmp/of$1.log 2>&1 &
	gdb --args $FWD_ROOT/udatapath/ofdatapath -i "$3" -d "$2" "p$SOCKET" -v 
}

function start_cnt() {
	#screen -d -m -S "controller" ryu-manager $CNT_SCRIPT --observe-links --verbose > /tmp/controller.log 2>&1
	ryu-manager $CNT_SCRIPT --observe-links --verbose > /tmp/controller.log 2>&1 &
}

function do_start() {
  	start_fwd a 00000000000a 'eth0,corea'
	start_fwd aa 0000000000aa 'coreb,eth2'

	start_cnt
	sleep 0.5
	
}

function do_stop() {
	# forwarder
	killall ofprotocol
	killall ofdatapath

	# and controller
	killall ryu-manager
}

case $1 in
	start)
		do_start
		;;
	stop)
		do_stop
		;;
	restart)
		do_stop
		do_start
		;;
esac
