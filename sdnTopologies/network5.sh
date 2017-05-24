#!/bin/sh

ip link add edgeb type veth peer name coreb1
ip link add coreb2 type veth peer name coreb3
ip link add coreb4 type veth peer name coreb5
ip link add coreb6 type veth peer name edge1
ip link add edgec type veth peer name corec1
ip link add corec2 type veth peer name corec3
ip link add corec4 type veth peer name corec5
ip link add corec6 type veth peer name edge2
ip link add edged type veth peer name cored1
ip link add cored2 type veth peer name cored3
ip link add cored4 type veth peer name cored5
ip link add cored6 type veth peer name edge3
ip link add edgee type veth peer name coree1
ip link add coree2 type veth peer name coree3
ip link add coree4 type veth peer name coree5
ip link add coree6 type veth peer name edge4
ip link add edgef type veth peer name coref1
ip link add coref2 type veth peer name coref3
ip link add coref4 type veth peer name coref5
ip link add coref6 type veth peer name edge5
ip link add edgeg type veth peer name coreg1
ip link add coreg2 type veth peer name coreg3
ip link add coreg4 type veth peer name coreg5
ip link add coreg6 type veth peer name edge6
ip link add edgeh type veth peer name coreh1
ip link add coreh2 type veth peer name coreh3
ip link add coreh4 type veth peer name coreh5
ip link add coreh6 type veth peer name edge7
ip link add edgei type veth peer name corei1
ip link add corei2 type veth peer name corei3
ip link add corei4 type veth peer name corei5
ip link add corei6 type veth peer name edge8

for INT in eth0 eth2 edge1 edge2 edge3 edge4 edge5 edge6 edge7 edge8 edged edgeb edgec edgee edgef edgeg edgeh edgei coreb1 coreb2 coreb3 coreb4 coreb5 coreb6 corec1 corec2 corec3 corec4 corec5 corec6 cored1 cored2 cored3 cored4 cored5 cored6 coree1 coree2 coree3 coree4 coree5 coree6 coref1 coref2 coref3 coref4 coref5 coref6 coreg1 coreg2 coreg3 coreg4 coreg5 coreg6 coreh1 coreh2 coreh3 coreh4 coreh5 coreh6 corei1 corei2 corei3 corei4 corei5 corei6; do
	ip link set $INT mtu 1500
done
