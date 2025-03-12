"""(Very) Simple Implementation of Artnet.

Python Version: 3.6
Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf

NOTES
- For simplicity: NET and SUBNET not used by default but optional

"""

import socket
import _thread
from time import sleep
from stupidArtnet.ArtnetUtils import shift_this, put_in_range


class StupidArtnet():
    """(Very) simple implementation of Artnet."""

    def __init__(self, target_ip='127.0.0.1', universe=0, packet_size=512, fps=30,
                 even_packet_size=True, broadcast=False, source_address=None, artsync=False, port=6454):
        """Initializes Art-Net Client.

        Args:
        targetIP - IP of receiving device
        universe - universe to listen
        packet_size - amount of channels to transmit
        fps - transmition rate
        even_packet_size - Some receivers enforce even packets
        broadcast - whether to broadcast in local sub
        artsync - if we want to synchronize buffer
        port - UDP port used to send Art-Net packets (default: 6454)

        Returns:
        None

        """
        # Instance variables
        self.target_ip = target_ip
        self.sequence = 0
        self.physical = 0
        self.universe = universe
        self.subnet = 0
        self.if_sync = artsync
        self.net = 0
        self.packet_size = put_in_range(packet_size, 2, 512, even_packet_size)
        self.packet_header = bytearray()
        self.buffer = bytearray(self.packet_size)
        self.port = port  
        # Use provided port or default 6454
        # By default, the server uses port 6454, no need to specify it.
        # If you need to change the Art-Net port, ensure the port is within the valid range for UDP ports (1024-65535).
        # Be sure that no other application is using the selected port on your network.

        self.make_even = even_packet_size

        self.is_simplified = True		# simplify use of universe, net and subnet

        # UDP SOCKET
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if broadcast:
            self.socket_client.setsockopt(
                socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Allow speciying the origin interface
        if source_address:
            self.socket_client.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_client.bind(source_address)

        # Timer
        self.fps = fps
        self.__clock = None

        self.make_artdmx_header()
        
        if self.if_sync:
            self.artsync_header = bytearray()
            self.make_artsync_header()


    def __del__(self):
        """Graceful shutdown."""
        self.stop()
        self.close()


    def __str__(self):
        """Printable object state."""
        state = "===================================\n"
        state += "Stupid Artnet initialized\n"
        state += f"Target IP: {self.target_ip} : {self.port} \n"
        state += f"Universe: {self.universe} \n"
        if not self.is_simplified:
            state += f"Subnet: {self.subnet} \n"
            state += f"Net: {self.net} \n"
        state += f"Packet Size: {self.packet_size} \n"
        state += "==================================="

        return state


    def make_artdmx_header(self):
        """Make packet header."""
        # 0 - id (7 x bytes + Null)
        self.packet_header = bytearray()
        self.packet_header.extend(bytearray('Art-Net', 'utf8'))
        self.packet_header.append(0x0)
        # 8 - opcode (2 x 8 low byte first)
        self.packet_header.append(0x00)
        self.packet_header.append(0x50)  # ArtDmx data packet
        # 10 - prototocol version (2 x 8 high byte first)
        self.packet_header.append(0x0)
        self.packet_header.append(14)
        # 12 - sequence (int 8), NULL for not implemented
        self.packet_header.append(self.sequence)
        # 13 - physical port (int 8)
        self.packet_header.append(0x00)
        # 14 - universe, (2 x 8 low byte first)
        if self.is_simplified:
            # not quite correct but good enough for most cases:
            # the whole net subnet is simplified
            # by transforming a single uint16 into its 8 bit parts
            # you will most likely not see any differences in small networks
            msb, lsb = shift_this(self.universe)   # convert to MSB / LSB
            self.packet_header.append(lsb)
            self.packet_header.append(msb)
        # 14 - universe, subnet (2 x 4 bits each)
        # 15 - net (7 bit value)
        else:
            # as specified in Artnet 4 (remember to set the value manually after):
            # Bit 3  - 0 = Universe (1-16)
            # Bit 7  - 4 = Subnet (1-16)
            # Bit 14 - 8 = Net (1-128)
            # Bit 15     = 0
            # this means 16 * 16 * 128 = 32768 universes per port
            # a subnet is a group of 16 Universes
            # 16 subnets will make a net, there are 128 of them
            self.packet_header.append(self.subnet << 4 | self.universe)
            self.packet_header.append(self.net & 0xFF)
        # 16 - packet size (2 x 8 high byte first)
        msb, lsb = shift_this(self.packet_size)		# convert to MSB / LSB
        self.packet_header.append(msb)
        self.packet_header.append(lsb)


    def make_artsync_header(self):
        """Make ArtSync header"""
        self.artsync_header = bytearray()  # Initialize as empty bytearray
        # ID: Array of 8 characters, the final character is a null termination.
        self.artsync_header.extend(bytearray('Art-Net', 'utf8'))
        self.artsync_header.append(0x0)
        # OpCode: Defines the class of data within this UDP packet. Transmitted low byte first.
        self.artsync_header.append(0x00)
        self.artsync_header.append(0x52)
        # ProtVerHi and ProtVerLo: Art-Net protocol revision number. Current value =14.
        # Controllers should ignore communication with nodes using a protocol version lower than =14.
        self.artsync_header.append(0x0)
        self.artsync_header.append(14)
        # Aux1 and Aux2: Should be transmitted as zero.
        self.artsync_header.append(0x0)
        self.artsync_header.append(0x0)


    def send_artsync(self):
        """Send Artsync"""
        self.make_artsync_header()
        try:
            self.socket_client.sendto(self.artsync_header, (self.target_ip, self.port))
        except socket.error as error:
            print(f"ERROR: Socket error with exception: {error}")


    def show(self):
        """Finally send data."""
        packet = bytearray()
        packet.extend(self.packet_header)
        packet.extend(self.buffer)
        try:
            self.socket_client.sendto(packet, (self.target_ip, self.port))
            if self.if_sync:  # if we want to send artsync
                self.send_artsync()
        except socket.error as error:
            print(f"ERROR: Socket error with exception: {error}")
        finally:
            self.sequence = (self.sequence + 1) % 256


    def close(self):
        """Close UDP socket."""
        self.socket_client.close()

    # THREADING #

    def start(self):
        """Starts thread clock."""
        self.show()
        if not hasattr(self, "running"):
            self.running = True
        if self.running:
            sleep((1000.0 / self.fps) / 1000.0)
            _thread.start_new_thread(self.start, ())


    def stop(self):
        """Set flag so thread will exit."""
        self.running = False

    # SETTERS - HEADER #

    def set_universe(self, universe):
        """Setter for universe (0 - 15 / 256).

        Mind if protocol has been simplified
        """
        # This is ugly, trying to keep interface easy
        # With simplified mode the universe will be split into two
        # values, (uni and sub) which is correct anyway. Net will always be 0
        if self.is_simplified:
            self.universe = put_in_range(universe, 0, 255, False)
        else:
            self.universe = put_in_range(universe, 0, 15, False)
        self.make_artdmx_header()


    def set_subnet(self, sub):
        """Setter for subnet address (0 - 15).

        Set simplify to false to use
        """
        self.subnet = put_in_range(sub, 0, 15, False)
        self.make_artdmx_header()


    def set_net(self, net):
        """Setter for net address (0 - 127).

        Set simplify to false to use
        """
        self.net = put_in_range(net, 0, 127, False)
        self.make_artdmx_header()


    def set_packet_size(self, packet_size):
        """Setter for packet size (2 - 512, even only)."""
        self.packet_size = put_in_range(packet_size, 2, 512, self.make_even)
        self.make_artdmx_header()

    # SETTERS - DATA #

    def clear(self):
        """Clear DMX buffer."""
        self.buffer = bytearray(self.packet_size)


    def set(self, value):
        """Set buffer."""
        if len(value) != self.packet_size:
            print("ERROR: packet does not match declared packet size")
            return
        self.buffer = value


    def set_16bit(self, address, value, high_first=False):
        """Set single 16bit value in DMX buffer."""
        if address > self.packet_size:
            print("ERROR: Address given greater than defined packet size")
            return
        if address < 1 or address > 512 - 1:
            print("ERROR: Address out of range")
            return
        value = put_in_range(value, 0, 65535, False)

        # Check for endianess
        if high_first:
            self.buffer[address - 1] = (value >> 8) & 0xFF  # high
            self.buffer[address] = (value) & 0xFF 			# low
        else:
            self.buffer[address - 1] = (value) & 0xFF				# low
            self.buffer[address] = (value >> 8) & 0xFF  # high


    def set_single_value(self, address, value):
        """Set single value in DMX buffer."""
        if address > self.packet_size:
            print("ERROR: Address given greater than defined packet size")
            return
        if address < 1 or address > 512:
            print("ERROR: Address out of range")
            return
        self.buffer[address - 1] = put_in_range(value, 0, 255, False)


    def set_single_rem(self, address, value):
        """Set single value while blacking out others."""
        if address > self.packet_size:
            print("ERROR: Address given greater than defined packet size")
            return
        if address < 1 or address > 512:
            print("ERROR: Address out of range")
            return
        self.clear()
        self.buffer[address - 1] = put_in_range(value, 0, 255, False)


    def set_rgb(self, address, red, green, blue):
        """Set RGB from start address."""
        if address > self.packet_size:
            print("ERROR: Address given greater than defined packet size")
            return
        if address < 1 or address > 510:
            print("ERROR: Address out of range")
            return

        self.buffer[address - 1] = put_in_range(red, 0, 255, False)
        self.buffer[address] = put_in_range(green, 0, 255, False)
        self.buffer[address + 1] = put_in_range(blue, 0, 255, False)

    # AUX Function #

    def send(self, packet):
        """Set buffer and send straightaway.

        Args:
        array - integer array to send
        """
        self.set(packet)
        self.show()


    def set_simplified(self, simplify):
        """Builds Header accordingly.

        True - Header sends 16 bit universe value (OK but incorrect)
        False - Headers sends Universe - Net and Subnet values as protocol
        It is recommended that you set these values with .set_net() and set_physical
        """
        # avoid remaking header if there are no changes
        if simplify == self.is_simplified:
            return
        self.is_simplified = simplify
        self.make_artdmx_header()


    def see_header(self):
        """Show header values."""
        print(self.packet_header)


    def see_buffer(self):
        """Show buffer values."""
        print(self.buffer)


    def blackout(self):
        """Sends 0's all across."""
        self.clear()
        self.show()


    def flash_all(self, delay=None):
        """Sends 255's all across."""
        self.set([255] * self.packet_size)
        self.show()
        # Blackout after delay
        if delay:
            sleep(delay)
            self.blackout()


if __name__ == '__main__':
    print("===================================")
    print("Namespace run")
    TARGET_IP = '127.0.0.1'         # typically in 2.x or 10.x range
    UNIVERSE_TO_SEND = 15           # see docs
    PACKET_SIZE = 20                # it is not necessary to send whole universe

    a = StupidArtnet(TARGET_IP, UNIVERSE_TO_SEND, PACKET_SIZE, artsync=True)
    a.set_simplified(False)
    a.set_net(129)
    a.set_subnet(16)

    # Look at the object state
    print(a)

    a.set_single_value(13, 255)
    a.set_single_value(14, 100)
    a.set_single_value(15, 200)

    print("Sending values")
    a.show()
    a.see_buffer()
    a.flash_all()
    a.see_buffer()
    a.show()

    print("Values sent")

    # Cleanup when you are done
    del a
