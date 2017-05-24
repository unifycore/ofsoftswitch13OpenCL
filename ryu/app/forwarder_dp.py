# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

FIRST_EDGE_FORWARDER=[0xa]
LAST_EDGE_FORWARDER=[0xdd]

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
	nw_ttl = 85

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
	
#	match = parser.OFPMatch(in_port=1,eth_type=0x800,ip_proto=6,ipv4_src="172.16.0.1")
#	actions = [parser.OFPActionDecNwTtl(),parser.OFPActionOutput(2)]
#	self.add_flow(datapath, 1, match, actions)
#	match = parser.OFPMatch(in_port=1,eth_type=0x806)
#	actions = [parser.OFPActionOutput(2)]
#	self.add_flow(datapath, 2, match, actions)
	
#	match = parser.OFPMatch(in_port=2,eth_type=0x800,ip_proto=6)
#	actions = [parser.OFPActionOutput(1)]
#	self.add_flow(datapath, 1, match, actions)
#	match = parser.OFPMatch(in_port=2,eth_type=0x806)
#	actions = [parser.OFPActionOutput(1)]
#	self.add_flow(datapath, 2, match, actions)
	
	match = parser.OFPMatch(eth_type=0x806)
	actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
	self.add_flow(datapath, 100, match, actions)
	
	if datapath.id in FIRST_EDGE_FORWARDER:
		match = parser.OFPMatch(in_port=1,eth_type=0x800,ipv4_dst="172.16.0.2")
		actions = [parser.OFPActionDecNwTtl(),parser.OFPActionOutput(2)]
		self.add_flow(datapath, 50, match, actions)
		
		match = parser.OFPMatch(in_port=1,eth_type=0x800,ipv4_dst="172.16.0.3")
		actions = [parser.OFPActionDecNwTtl(),parser.OFPActionOutput(3)]
		self.add_flow(datapath, 50, match, actions)

		match = parser.OFPMatch(in_port=1,eth_type=0x800,ipv4_dst="172.16.0.4")
		actions = [parser.OFPActionDecNwTtl(),parser.OFPActionOutput(4)]
		self.add_flow(datapath, 50, match, actions)

		match = parser.OFPMatch(in_port=1,eth_type=0x800,ipv4_dst="172.16.0.5")
		actions = [parser.OFPActionDecNwTtl(),parser.OFPActionOutput(5)]
		self.add_flow(datapath, 50, match, actions)

		match = parser.OFPMatch(in_port=2,eth_type=0x800)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 50, match, actions)

		match = parser.OFPMatch(in_port=3,eth_type=0x800)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 50, match, actions)

		match = parser.OFPMatch(in_port=4,eth_type=0x800)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 50, match, actions)

		match = parser.OFPMatch(in_port=5,eth_type=0x800)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 50, match, actions)
	
	
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)    