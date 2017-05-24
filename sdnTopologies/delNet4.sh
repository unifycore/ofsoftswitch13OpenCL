#!/bin/sh

ip link del edgeb type veth peer name coreb1
ip link del coreb2 type veth peer name coreb3
ip link del coreb4 type veth peer name edge1
ip link del edgec type veth peer name corec1
ip link del corec2 type veth peer name corec3
ip link del corec4 type veth peer name edge2
ip link del edged type veth peer name cored1
ip link del cored2 type veth peer name cored3
ip link del cored4 type veth peer name edge3

