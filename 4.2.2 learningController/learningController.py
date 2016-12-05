"""
4.2.2 Learning Controller
Adapted from /misc/of_tutorial.py
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class LearningController (object):

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

    def act_like_switch (self, packet, packet_in):
        """
        Implement switch-like behavior that stores MACs
        """
        # Learn the port for the source MAC
        # log.debug('Src: %s Dst: %s Port: %s', packet.src, packet.dst, packet_in.in_port)

        if packet.src in self.mac_to_port: 
            log.debug('mac found in table')
            # check for change in port number
            if self.mac_to_port[packet.src] != packet_in.in_port:
                log.debug('updating port number in table')
                self.mac_to_port[packet.src] = packet_in.in_port
        else:
            log.debug('mac not found in table')
            self.mac_to_port[packet.src] = packet_in.in_port

        # if the port associated with the destination MAC of the packet is known:
        if packet.dst in self.mac_to_port:
            # Send packet out the associated port
            self.resend_packet(packet_in, self.mac_to_port[packet.dst])
        else:
            # Flood the packet out everything but the input port
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

        self.act_like_switch(packet, packet_in)

def launch ():
    """
    starts the LearningController
    """
    def start_switch (event):
        log.debug("Controlling %s" % (event.connection,))
        LearningController(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
