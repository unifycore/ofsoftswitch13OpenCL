#!/bin/sh

ip link add edge1 type veth peer name coreb1
ip link add coreb2 type veth peer name corec1
ip link add corec2 type veth peer name cored1
ip link add cored2 type veth peer name coree1
ip link add coree2 type veth peer name coref1
ip link add coref2 type veth peer name edge2

for INT in eth0 eth2 edge1 edge2 coreb1 coreb2 corec1 corec2 cored1 cored2 coree1 coree2 coref1 coref2; do
	ip link set $INT mtu 1500
done
