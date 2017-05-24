#!/bin/sh

ip link del edge1 type veth peer name coreb1
ip link del coreb2 type veth peer name corec1
ip link del corec2 type veth peer name cored1
ip link del cored2 type veth peer name coree1
ip link del coree2 type veth peer name coref1
ip link del coref2 type veth peer name edge2
