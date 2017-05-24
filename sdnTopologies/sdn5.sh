#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo 'Dont forget to use sudo ;-)'
    exit 1
fi
#FWD_ROOT="/home/michal-dp/Dokumenty/ofsoftswitch13"
FWD_ROOT="/home/michal-dp/Dokumenty/ofsoftswitchNewNew/ofsoftswitch13"
CNT_SCRIPT="/home/michal-dp/ryu/ryu/app/dp_controller_net5_iperf.py"
#CNT_SCRIPT="/home/michal-dp/ryu/ryu/app/dp_controller_net5.py"

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
  	start_fwd a 00000000000a 'eth0,edgeb,edgec,edged,edgee,edgef,edgeg,edgeh,edgei'
	start_fwd b1 00000000000b 'coreb1,coreb2'
	start_fwd b2 0000000000bb 'coreb3,coreb4'
	start_fwd b3 000000000bbb 'coreb5,coreb6'
	start_fwd c1 00000000000c 'corec1,corec2'
	start_fwd c2 0000000000cc 'corec3,corec4'
	start_fwd c3 000000000ccc 'corec5,corec6'
	start_fwd d1 00000000000d 'cored1,cored2'
	start_fwd d2 0000000000dd 'cored3,cored4'
	start_fwd d3 000000000ddd 'cored5,cored6'
	start_fwd e1 00000000000e 'coree1,coree2'
	start_fwd e2 0000000000ee 'coree3,coree4'
	start_fwd e3 000000000eee 'coree5,coree6'
	start_fwd f1 00000000000f 'coref1,coref2'
	start_fwd f2 0000000000ff 'coref3,coref4'
	start_fwd f3 000000000fff 'coref5,coref6'
	start_fwd g1 00000000001a 'coreg1,coreg2'
	start_fwd g2 0000000001aa 'coreg3,coreg4'
	start_fwd g3 000000001aaa 'coreg5,coreg6'
	start_fwd h1 00000000001b 'coreh1,coreh2'
	start_fwd h2 0000000001bb 'coreh3,coreh4'
	start_fwd h3 000000001bbb 'coreh5,coreh6'
	start_fwd i1 00000000001c 'corei1,corei2'
	start_fwd i2 0000000001cc 'corei3,corei4'
	start_fwd i3 000000001ccc 'corei5,corei6'
	start_fwd aa 0000000000aa 'edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,eth2'

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
