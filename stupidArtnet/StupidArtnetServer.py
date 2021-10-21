"""(Very) Simple Implementation of Artnet.

Python Version: 3.6
Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf


NOTES
- For simplicity: NET and SUBNET not used by default but optional

"""

import socket
from threading import Thread
from stupidArtnet.ArtnetUtils import make_address_mask


class StupidArtnetServer():
    """(Very) simple implementation of an Artnet Server."""

    UDP_PORT = 6454
    s = None
    ARTDMX_HEADER = b'Art-Net\x00\x00P\x00\x0e'
    listeners = list()

    def __init__(self):
        """Initializes Art-Net server."""

        # server active flag
        self.listen = True

        self.th = Thread(target=self.__init_socket, daemon=True)
        self.th.start()

    def __init_socket(self):
        # Bind to UDP on the correct PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', self.UDP_PORT))  # Listen on any valid IP

        while self.listen:

            data, addr = self.s.recvfrom(1024)

            # only dealing with Art-Net DMX
            if self.validate_header(data):

                # check if this address is in any registered listener
                for listener in self.listeners:

                    # is it the address we are listening to
                    if (listener['address_mask'] == data[14:16]):
                        listener['buffer'] = list(data)[18:]

                        # check for registered callbacks
                        if (listener['callback'] != None):
                            listener['callback'](listener['buffer'])

    def __del__(self):
        """Graceful shutdown."""
        self.listeners.clear()
        self.close()

    def __str__(self):
        """Printable object state."""
        s = "===================================\n"
        s += "Stupid Artnet Listening\n"
        return s

    def register_listener(self, universe=0, sub=0, net=0, is_simplified=True, callback_function=None):
        """Adds a listener to an Art-Net Universe.

        Args:
        universe - Universe to listen
        sub - Subnet to listen
        net - Net to listen
        is_simplified - Wheter to use nets and subnet or simpler definition for universe only, see User Guide page 5 (Universe Addressing)
        callback_function - Function to call when new packet is received

        Returns:
        id - id of listener, used to delete listener if required
        """

        listener_id = len(self.listeners)
        new_listener = {
            'id': listener_id,
            'simplified': is_simplified,
            'address_mask': make_address_mask(universe, sub, net, is_simplified),
            'callback': callback_function,
            'buffer': []
        }

        self.listeners.append(new_listener)

        return listener_id

    def delete_listener(self, listener_id):
        """Deletes a registered listener.

        Args:
        listener_id - Id of listener to delete

        Returns:
        None
        """
        self.listeners = [
            i for i in self.listeners if not (i['id'] == listener_id)]

        return None

    def delete_all_listener(self):
        """Deletes all registered listeners.

        Returns:
        None
        """
        self.listeners = []
        return None

    def see_buffer(self, listener_id):
        """Show buffer values."""
        for listener in self.listeners:
            if (listener.get('id') == listener_id):
                print(listener.get('buffer'))

        return "Listener not found"

    def get_buffer(self, listener_id):
        """Return buffer values."""
        for listener in self.listeners:
            if (listener.get('id') == listener_id):
                return(listener.get('buffer'))

        return None

    def clear_buffer(self, listener_id):
        """Clear buffer in listener."""
        for listener in self.listeners:
            if (listener.get('id') == listener_id):
                listener['buffer'] = []

    def set_callback(self, listener_id, callback_function):
        """Add / change callback to a given listener."""
        for listener in self.listeners:
            if (listener.get('id') == listener_id):
                listener['callback'] = callback_function

    def set_address_filter(self, listener_id, universe, sub=0, net=0, is_simplified=True):
        """Add / change filter to existing listener."""
        # make mask bytes
        address_mask = make_address_mask(
            universe, sub, net, is_simplified)

        # find listener
        for listener in self.listeners:
            if (listener.get('id') == listener_id):
                listener['simplified'] = is_simplified
                listener['address_mask'] = address_mask
                listener['buffer'] = []

    def close(self):
        """Close UDP socket."""
        self.listen = False         # Set flag
        self.th.join()              # Terminate thread once jobs are complete

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

    # Initilize server, this starts a server in the Art-Net port
    a = StupidArtnetServer()

    # For every universe we would like to receive,
    # add a new listener with a optional callback
    # the return is an id for the listener
    u1_listener = a.register_listener(
        universe, callback_function=test_callback)

    # print object state
    print(a)

    # giving it some time for the demo
    time.sleep(3)

    # use the listener address to get data without a callback
    buffer = a.get_buffer(u1_listener)

    # Cleanup when you are done
    del a
