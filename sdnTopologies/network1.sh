#!/bin/sh

ip link add corea type veth peer name coreb

for INT in eth0 eth2 corea coreb; do
	ip link set $INT mtu 1500
done
