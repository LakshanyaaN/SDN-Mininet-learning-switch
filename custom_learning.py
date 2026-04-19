from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# MAC address to block
BLOCKED_MAC = "00:00:00:00:00:03"


class LearningSwitch(object):
    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}

        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port

        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        src = packet.src
        dst = packet.dst

        # Learn MAC address
        self.mac_to_port[src] = in_port
        log.info(f"Learned MAC {src} on port {in_port}")

        # 🚫 BLOCK LOGIC (ALLOW ARP, BLOCK OTHER TRAFFIC)
        if str(src) == BLOCKED_MAC:
            if packet.type != packet.ARP_TYPE:
                log.info(f"Installing DROP rule for {src}")

                msg = of.ofp_flow_mod()
                msg.match.dl_src = src
                # No action = DROP

                self.connection.send(msg)
                return

        # If destination is known → install flow rule
        if dst in self.mac_to_port:
            out_port = self.mac_to_port[dst]

            log.info(f"Installing flow: {src} -> {dst} via port {out_port}")

            msg = of.ofp_flow_mod()
            msg.match.dl_src = src
            msg.match.dl_dst = dst
            msg.actions.append(of.ofp_action_output(port=out_port))
            msg.data = event.ofp

            self.connection.send(msg)

        else:
            # Flood if destination unknown
            log.info(f"Flooding packet from {src} to {dst}")

            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            msg.in_port = in_port

            self.connection.send(msg)


def launch():
    def start_switch(event):
        log.info("Custom Learning Switch Connected")
        LearningSwitch(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
