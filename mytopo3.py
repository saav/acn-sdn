"""
Assignment 7 - Custom Topology for Third Part
"""

from mininet.topo import Topo

class MyTopo(Topo):

    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        host1 = self.addHost('h1', ip='0.0.0.0')
        host2 = self.addHost('h2', ip='0.0.0.0')
        host3 = self.addHost('h3', ip='0.0.0.0')
        host4 = self.addHost('h4', ip='0.0.0.0')

        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')

        # Add links
        #Switch 1
        self.addLink(host1, switch1)
        self.addLink(host2, switch1)
        self.addLink(switch2, switch1)

        #Switch 2
        self.addLink(host3, switch2)
        self.addLink(host4, switch2)

        #Switch 3
        self.addLink(switch1, switch3)
        self.addLink(switch2, switch3)

topos = { 'mytopo': ( lambda: MyTopo() ) }
