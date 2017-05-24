#!/bin/sh

ip link add edgeb type veth peer name coreb1
ip link add coreb2 type veth peer name coreb3
ip link add coreb4 type veth peer name edge1
ip link add edgec type veth peer name corec1
ip link add corec2 type veth peer name corec3
ip link add corec4 type veth peer name edge2
ip link add edged type veth peer name cored1
ip link add cored2 type veth peer name cored3
ip link add cored4 type veth peer name edge3

for INT in eth0 eth2 edge1 edge2 edge3 edged edgeb edgec coreb1 coreb2 coreb3 coreb4 corec1 corec2 corec3 corec4 cored1 cored2 cored3 cored4; do
	ip link set $INT mtu 1500
done
