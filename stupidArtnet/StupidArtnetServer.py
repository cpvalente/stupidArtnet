"""(Very) Simple Implementation of Artnet.

Python Version: 3.6
Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf


NOTES
- For simplicity: NET and SUBNET not used by default but optional

"""

import socket
from threading import Thread
# from .StupidArtnet import StupidArtnet # works with the test file
from StupidArtnet import StupidArtnet  # works locally


class StupidArtnetServer():
    """(Very) simple implementation of an Artnet Server."""

    UDP_PORT = 6454
    s = None
    ARTDMX_HEADER = b'Art-Net\x00\x00P\x00\x0e'
    callback = None

    def __init__(self, universe=0, sub=0, net=0, setSimplified=True, callback_function=None):
        """Initializes Art-Net server.

        Args:
        universe - Universe to listen
        sub - Subnet to listen
        net - Net to listen
        setSimplified - Wheter to use nets and subnet or simpler definition for universe only, see User Guide page 5 (Universe Addressing)

        Returns:
        None

        """
        # server active flag
        self.listen = True

        self.universe = universe
        self.subnet = sub
        self.net = net
        self.buffer = []
        self.callback = callback_function

        # simplify use of universe, net and subnet
        self.bIsSimplified = setSimplified
        self.address_mask = self.__make_address_mask()

        self.th = Thread(target=self.__init_socket, daemon=True)
        self.th.start()

    def __init_socket(self):
        # Bind to UDP on the correct PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', 6454))  # Listen on any IP valid

        while self.listen:

            data, addr = self.s.recvfrom(1024)

            # only dealing with Art-Net DMX
            if self.validate_header(data):

                # is it the address we are listening to
                if (data[14:16] == self.address_mask):
                    self.buffer = list(data)[18:]

                    # check for registered callbacks
                    if (self.callback != None):
                        self.callback(self.buffer)

    def __make_address_mask(self):

        address_mask = bytearray()

        if (self.bIsSimplified):
            a = StupidArtnet.shift_this(self.universe)  # convert to MSB / LSB
            address_mask.append(a[1])
            address_mask.append(a[0])

        else:
            address_mask.append(self.subnet << 4 | self.universe)
            address_mask.append(self.net & 0xFF)

        return address_mask

    def __del__(self):
        """Graceful shutdown."""
        self.close()

    def __str__(self):
        """Printable object state."""
        s = "===================================\n"
        s += "Stupid Artnet Listening\n"
        s += "Universe: %i \n" % self.universe
        if not (self.bIsSimplified):
            s += "Subnet: %i \n" % self.subnet
            s += "Net: %i \n" % self.net
        if (self.callback != None):
            s += "Callback function active"
        s += "\n"
        return s

    def see_buffer(self):
        """Show buffer values."""
        print(self.buffer)

    def get_buffer(self):
        """Return buffer values."""
        return self.buffer

    def set_callback(self, callback_function):
        """Utility function to easily set callback for receivind data."""
        self.callbacks = callback_function

    def set_universe(self, universe):
        """Setter for universe (0 - 15 / 256).

        Mind if protocol has been simplified
        """

        if (self.bIsSimplified):
            self.universe = StupidArtnet.put_in_range(universe, 0, 255, False)
        else:
            self.universe = StupidArtnet.put_in_range(universe, 0, 15, False)

        # recalculate address mask
        self.__make_address_mask()

    def set_subnet(self, subnet):
        """Setter for subnet address (0 - 15).

        Set simplify to false to use
        """
        self.subnet = StupidArtnet.put_in_range(subnet, 0, 15, False)
        self.__make_address_mask()

    def set_net(self, net):
        """Setter for net address (0 - 127).

        Set simplify to false to use
        """
        self.net = StupidArtnet.put_in_range(net, 0, 127, False)
        self.__make_address_mask()

    def close(self):
        """Close UDP socket."""
        self.listen = False         # Set flag
        self.th.join()              # Terminate thread once jobs are complete

    def clear(self):
        """Clear internal DMX Buffer."""
        self.buffer = []

    @staticmethod
    def validate_header(header):
        """Validates packet header as Art-Net packet.

        - The packet header spells Art-Net
        - The definition is for DMX Artnet (OPCode 0x50)
        - The protocol version is 15

        Args:
        header - Packet header as bytearray

        Returns:
        boolean - comparison value

        """

        return (header[:12] == StupidArtnetServer.ARTDMX_HEADER)


def test_callback(data):
    print('Received new data \n', data)


if __name__ == '__main__':

    import time

    print("===================================")
    print("Namespace run")

    # Art-Net 4 definition specifies nets and subnets
    # Please see README and Art-Net user guide for details
    # Here we use the simplified default
    universe = 1

    # Initilize server with a universe to listen to
    # And set a callback
    a = StupidArtnetServer(universe, callback_function=test_callback)

    # print object state
    print(a)

    # giving it some time for the demo
    time.sleep(3)

    # the latest DMX packet is available as an array
    buffer = a.get_buffer()

    # Cleanup when you are done
    del a
