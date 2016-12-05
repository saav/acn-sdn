"""
4.2.1 Hub Controller
Adapted from /misc/of_tutorial.py
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class HubController (object):

    def __init__ (self, connection):
        # keeps track of connection
        self.connection = connection
        # binds the event listener
        connection.addListeners(self)
        # key-value store (keys are MACs, values are ports).
        self.mac_to_port = {}

    def resend_packet (self, packet_in, out_port):
        """
        resends packet to the network
        """
        msg = of.ofp_packet_out()
        msg.data = packet_in

        # Add an action to send to the specified port
        action = of.ofp_action_output(port = out_port)
        msg.actions.append(action)

        # Send message to switch
        self.connection.send(msg)

    def act_like_hub (self, packet, packet_in):
        """
        resend to all ports except the incoming port
        """
        self.resend_packet(packet_in, of.OFPP_ALL)

    def _handle_PacketIn (self, event):
        """
        Handles packet in messages from the switch.
        """
        packet = event.parsed # This is the parsed packet data.
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp # The actual ofp_packet_in message.

        self.act_like_hub(packet, packet_in)

def launch ():
    """
    starts the HubController
    """
    def start_switch (event):
        log.debug("Controlling %s" % (event.connection,))
        HubController(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
