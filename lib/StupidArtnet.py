""" Simple Implementation of Artnet.

    21.02.18
    Python Version: 3.6
    Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf

    TODO
    - Artnet should be implemented similarly to sockets
    - ie. there cant be multiple objects on the same port
    - Add some functions for clearing buffer
    - Test broadcast
    - Should UDP socket be part of class?

    NOTES
    - To make it super simple I have not implemented NET or SUBNET,
    this are default to 0

"""

import socket       # how to stop this from being imported twice?


class StupidArtnet():
    """(Very) simple implementation of Artnet."""

    UDP_PORT = 6454
    TARGET_IP = '127.0.0.1'
    UNIVERSE = 0
    PACKET_SIZE = 512
    PHYSICAL = 0
    SEQUENCE = 0

    _una = 0x00
    _unb = 0x00

    _cha = 0x00
    _chb = 0x00

    def __init__(self):
        """Iitialize UDP here."""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pass

    def __str__(self):
        """Printable object state."""
        s = "==================================="
        s = "Stupid Artnet initialized\n"
        s += "Target IP: %s:%i \n" % (self.TARGET_IP, self.UDP_PORT)
        s += "Universe: %i \n" % self.UNIVERSE
        s += "Packet Size: %i \n" % self.PACKET_SIZE

        return s

    def setup(self, targetIP='127.0.0.1', universe=0, packet_size=512):
        """Setup class with network information."""
        self.TARGET_IP = targetIP
        self.UNIVERSE = universe
        self.PACKET_SIZE = packet_size

        self._una = (self.UNIVERSE & 0xFF)
        self._unb = ((self.UNIVERSE >> 8) & 0xFF)

        self._cha = (self.PACKET_SIZE & 0xFF)
        self._chb = ((self.PACKET_SIZE >> 8) & 0xFF)

    def set_universe(self, universe):
        """Setter for universe."""
        self.UNIVERSE = universe

        self._una = (self.UNIVERSE & 0xFF)
        self._unb = ((self.UNIVERSE >> 8) & 0xFF)

    def set_physical(self, physical):
        """Setter for physical address."""
        self.PHYSICAL = physical  # not implemented

    def set_sequence(self, sequence):
        """Setter for sequence."""
        self.SEQUENCE = sequence  # NOT IMPLEMENTED

    def set_packet_size(self, packet_size):
        """Setter for packet size, should restrict."""
        self.PACKET_SIZE = packet_size

        self._cha = (self.PACKET_SIZE & 0xFF)
        self._chb = ((self.PACKET_SIZE >> 8) & 0xFF)

    def make_header(self):
        """Setter for universe."""
        # DMX Header
        header = bytearray()

        # id (8 x bytes)
        header.extend(bytearray('Art-Net', 'utf8'))
        header.append(0x0)
        # opcode low byte first  (int 16)
        header.append(0x00)
        header.append(0x50)  # ArtDmx data packet
        # proto ver high byte first (int 16)
        header.append(0x0)
        header.append(14)
        # sequence (int 8), not implemented
        header.append(0x00)
        # physical port (int 8)
        header.append(0x00)

        # add universe (int 16) and packet length (int 16)
        # packet data in the end (512 x bytes)
        return header

    def blackout(self):
        """Sends 0's all across"""
        packet = bytearray(self.PACKET_SIZE)

        self.send(packet)

    def flash_all(self):
        """Sends 255's all across"""
        packet = bytearray(self.PACKET_SIZE)
        for i in range(self.PACKET_SIZE):
            packet[i] = 255

        self.send(packet)

    def send(self, p):
        """Finally send data."""
        packet = self.make_header()

        # 16bit universe
        packet.append(self._una)
        packet.append(self._unb)

        # 16bit packet size
        packet.append(self._cha)
        packet.append(self._chb)

        packet.extend(p)

        self.s.sendto(packet, (self.TARGET_IP, self.UDP_PORT))
