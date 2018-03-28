""" Simple Implementation of Artnet.

    28.02.18
    Python Version: 3.6
    Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf

    TODO
    - Artnet should be implemented similarly to sockets
    - ie. there cant be multiple objects on the same port
    - Add some functions for clearing buffer

    NOTES
    - To make it super simple I have not implemented NET or SUBNET,
    these default to 0

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
    HEADER = bytearray()
    BUFFER = bytearray()

    _una = 0x00
    _unb = 0x00

    _cha = 0x00
    _chb = 0x00

    def __init__(self):
        """Initialize UDP here."""
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
        self.BUFFER = bytearray(self.PACKET_SIZE)

        self.set_packet_size(packet_size)
        self.set_universe(universe)
        self.make_header()

    def make_header(self):
        """Setter for universe."""
        # id (8 x bytes)
        self.HEADER = bytearray()
        self.HEADER.extend(bytearray('Art-Net', 'utf8'))
        self.HEADER.append(0x0)
        # opcode low byte first  (int 16)
        self.HEADER.append(0x00)
        self.HEADER.append(0x50)  # ArtDmx data packet
        # proto ver high byte first (int 16)
        self.HEADER.append(0x0)
        self.HEADER.append(14)
        # sequence (int 8), not implemented
        self.HEADER.append(0x00)
        # physical port (int 8)
        self.HEADER.append(0x00)

        # 16bit universe
        self.HEADER.append(self._una)
        self.HEADER.append(self._unb)

        # 16bit packet size
        self.HEADER.append(self._cha)
        self.HEADER.append(self._chb)

    def show(self):
        """Finally send data."""
        packet = bytearray()
        packet.extend(self.HEADER)
        packet.extend(self.BUFFER)

        self.s.sendto(packet, (self.TARGET_IP, self.UDP_PORT))

    ##
    # SETTERS
    ##

    def set_universe(self, universe):
        """Setter for universe."""
        self.UNIVERSE = universe

        self._una = (self.UNIVERSE & 0xFF)
        self._unb = ((self.UNIVERSE >> 8) & 0xFF)

        self.make_header()

    def set_packet_size(self, packet_size):
        """Setter for packet size, should restrict."""
        self.PACKET_SIZE = packet_size

        self._cha = (self.PACKET_SIZE & 0xFF)
        self._chb = ((self.PACKET_SIZE >> 8) & 0xFF)

        self.make_header()

    def set_physical(self, physical):
        """Setter for physical address."""
        self.PHYSICAL = physical  # not implemented
        self.make_header()

    def set_sequence(self, sequence):
        """Setter for sequence."""
        self.SEQUENCE = sequence  # NOT IMPLEMENTED
        self.make_header()

    def clear(self):
        """Clear DMX buffer."""
        self.BUFFER = bytearray(self.PACKET_SIZE)

    def set(self, p):
        """Set buffer."""
        self.BUFFER = p

    def set_single_value(self, address, value):
        """Set single value in DMX buffer."""
        if address < 1 or address > 512:
            return
        self.BUFFER[address - 1] = value

    def set_single_rem(self, address, value):
        """Set single value while blacking out others"""
        if address < 1 or address > 512:
            return
        self.BUFFER = bytearray(self.PACKET_SIZE)
        self.BUFFER[address - 1] = value

    def set_rgb(self, address, r, g, b):
        """Set RGB from start address."""
        if address < 1 or address > 510:
            return
        self.BUFFER[address - 1] = r
        self.BUFFER[address] = g
        self.BUFFER[address + 1] = b

    ##
    # AUX
    ##

    def see_header(self):
        """Show header values."""
        return self.HEADER

    def see_buffer(self):
        """Show buffer values."""
        return self.BUFFER

    def blackout(self):
        """Sends 0's all across"""
        packet = bytearray(self.PACKET_SIZE)

        self.set(packet)
        self.show()

    def flash_all(self):
        """Sends 255's all across"""
        packet = bytearray(self.PACKET_SIZE)
        for i in range(self.PACKET_SIZE):
            packet[i] = 255

        self.set(packet)
        self.show()
