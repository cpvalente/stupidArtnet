"""(Very) Simple Implementation of Artnet.

Python Version: 3.6
Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf
		http://art-net.org.uk/wordpress/structure/streaming-packets/artdmx-packet-definition/


"""

import socket
from threading import Thread


class StupidArtnetServer():
    """(Very) simple implementation of Artnet."""

    UDP_PORT = 6454
    s = None
    ARTDMX_HEADER = b'Art-Net\x00\x00P\x00\x0e'
    callback = None

    def __init__(self, universe=0, callback_function=None):
        """Class Initialization."""

        self.listen = True

        self.universe = universe
        self.buffer = []
        self.callback = callback_function

        self.th = Thread(target=self.__initSocket, daemon=True)
        self.th.start()

    def __initSocket(self):
        # Bind to UDP on the correct PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', 6454))  # Listen on any IP valid

        while self.listen:

            data, addr = self.s.recvfrom(1024)

            # only dealing with Art-Net DMX
            if self.validateHeader(data):

                # is it the universe we are listening to
                if (data[14] == self.universe):
                    self.buffer = list(data)[18:]

                    # check for registered callbacks
                    if (self.callback != None):
                        self.callback(self.buffer)

    def __del__(self):
        """Graceful shutdown."""
        self.close()

    def __str__(self):
        """Printable object state."""
        s = "===================================\n"
        s += "Stupid Artnet Listening\n"
        s += "Universe: %i \n" % self.universe
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

    def setCallback(self, callback_function, universe=0):
        """Utility function to easily set callback on a given channel / universe."""
        self.callbacks = callback_function

    def close(self):
        """Close UDP socket."""

        self.listen = False         # Set flag
        self.th.join()              # Terminate thread once jobs are complete

    def clear(self):
        """Clear internal DMX Buffer."""
        self.buffer = []

    @staticmethod
    def validateHeader(header):
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


def testCallback(data):
    print('Received new data', data)


if __name__ == '__main__':

    import time

    print("===================================")
    print("Namespace run")

    universe = 1

    # Initilize server with a universe to listen to
    # And set a callback
    a = StupidArtnetServer(universe, testCallback)
    print(a)

    # giving it some time for the demo
    time.sleep(3)

    # the latest DMX packet is available as an array
    buffer = a.get_buffer()

    # Cleanup when you are done
    del a
