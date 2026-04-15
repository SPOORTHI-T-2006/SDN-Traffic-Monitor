from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer

log = core.getLogger()

mac_to_port = {}

def _handle_ConnectionUp(event):
    log.info("Switch %s has connected", dpidToStr(event.dpid))

    # Request stats every 5 seconds
    Timer(5, request_stats, recurring=True, args=[event.connection])


def request_stats(connection):
    log.info("Requesting stats from switch...")
    connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))


def _handle_FlowStatsReceived(event):
    log.info("========== FLOW STATS ==========")

    for stat in event.stats:
        if stat.match.nw_src and stat.match.nw_dst:
            log.info("Flow: %s -> %s | Packets: %d | Bytes: %d",
                     stat.match.nw_src,
                     stat.match.nw_dst,
                     stat.packet_count,
                     stat.byte_count)


def _handle_PacketIn(event):
    packet = event.parsed
    dpid = event.dpid
    in_port = event.port

    # Initialize MAC table
    mac_to_port.setdefault(dpid, {})

    src = packet.src
    dst = packet.dst

    # Learn MAC
    mac_to_port[dpid][src] = in_port

    if dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][dst]
    else:
        out_port = of.OFPP_FLOOD

    # Install flow rule (IMPORTANT)
    if out_port != of.OFPP_FLOOD:
        match = of.ofp_match.from_packet(packet, in_port)
        msg = of.ofp_flow_mod()
        msg.match = match
        msg.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(msg)

    # Send packet
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))
    msg.in_port = in_port
    event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    core.openflow.addListenerByName("FlowStatsReceived", _handle_FlowStatsReceived)

    log.info("Traffic Monitoring Controller Started 🚀")
