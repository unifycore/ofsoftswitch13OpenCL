
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

FIRST_EDGE_FORWARDER=[0x00000000000a]
FIRST_CORE_FORWARDER=[0x00000000000b]
SECOND_CORE_FORWARDER=[0x00000000000c]
THIRD_CORE_FORWARDER=[0x00000000000d]
LAST_EDGE_FORWARDER=[0x0000000000aa]

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

	if datapath.id in FIRST_EDGE_FORWARDER:		
		match = parser.OFPMatch(in_port=1,eth_type=0x800,ip_proto=6,ipv4_dst="172.16.0.2")
		actions = [parser.OFPActionSetField(ipv4_src="172.16.0.10"),parser.OFPActionOutput(2)]
		self.add_flow(datapath, 10, match, actions)
		match = parser.OFPMatch(in_port=1,eth_type=0x806)
		actions = [parser.OFPActionOutput(2)]
		self.add_flow(datapath, 20, match, actions)	
		match = parser.OFPMatch(in_port=2,eth_type=0x800,ip_proto=6)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 10, match, actions)
		match = parser.OFPMatch(in_port=2,eth_type=0x806)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 20, match, actions)
	
	if datapath.id in FIRST_CORE_FORWARDER:
		match = parser.OFPMatch(in_port=1,eth_type=0x800,ip_proto=6,ipv4_dst="172.16.0.2")
		actions = [parser.OFPActionDecNwTtl(),parser.OFPActionOutput(2)]
		self.add_flow(datapath, 10, match, actions)		
		match = parser.OFPMatch(in_port=1,eth_type=0x806)
		actions = [parser.OFPActionOutput(2)]
		self.add_flow(datapath, 20, match, actions)	
		match = parser.OFPMatch(in_port=2,eth_type=0x800,ip_proto=6)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 10, match, actions)
		match = parser.OFPMatch(in_port=2,eth_type=0x806)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 20, match, actions)

	if datapath.id in SECOND_CORE_FORWARDER:
		match = parser.OFPMatch(in_port=1,eth_type=0x800,ip_proto=6,ipv4_dst="172.16.0.2")
		actions = [parser.OFPActionDecNwTtl(),parser.OFPActionOutput(2)]
		self.add_flow(datapath, 10, match, actions)		
		match = parser.OFPMatch(in_port=1,eth_type=0x806)
		actions = [parser.OFPActionOutput(2)]
		self.add_flow(datapath, 20, match, actions)	
		match = parser.OFPMatch(in_port=2,eth_type=0x800,ip_proto=6)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 10, match, actions)
		match = parser.OFPMatch(in_port=2,eth_type=0x806)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 20, match, actions)

	if datapath.id in THIRD_CORE_FORWARDER:
		match = parser.OFPMatch(in_port=1,eth_type=0x800,ip_proto=6,ipv4_dst="172.16.0.2")
		actions = [parser.OFPActionDecNwTtl(),parser.OFPActionOutput(2)]
		self.add_flow(datapath, 10, match, actions)		
		match = parser.OFPMatch(in_port=1,eth_type=0x806)
		actions = [parser.OFPActionOutput(2)]
		self.add_flow(datapath, 20, match, actions)	
		match = parser.OFPMatch(in_port=2,eth_type=0x800,ip_proto=6)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 10, match, actions)
		match = parser.OFPMatch(in_port=2,eth_type=0x806)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 20, match, actions)
	
	if datapath.id in LAST_EDGE_FORWARDER:
		match = parser.OFPMatch(in_port=1,eth_type=0x800,ip_proto=6,ipv4_dst="172.16.0.2",ipv4_src="172.16.0.10")
		actions = [parser.OFPActionSetField(ipv4_src="172.16.0.1"),parser.OFPActionOutput(2)]
		self.add_flow(datapath, 10, match, actions)
		match = parser.OFPMatch(in_port=1,eth_type=0x806)
		actions = [parser.OFPActionOutput(2)]
		self.add_flow(datapath, 20, match, actions)
		match = parser.OFPMatch(in_port=2,eth_type=0x800,ip_proto=6)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 10, match, actions)
		match = parser.OFPMatch(in_port=2,eth_type=0x806)
		actions = [parser.OFPActionOutput(1)]
		self.add_flow(datapath, 20, match, actions)
	
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
