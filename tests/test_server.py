import time
import socket
import unittest

from stupidArtnet import StupidArtnetServer


class Test(unittest.TestCase):
    """Test class for Artnet server."""

    artnet_header = b'Art-Net\x00\x00P\x00\x0e\x00\x00\x00\x00\x00\x08'
    dmx_packet = [1, 2, 3, 4, 5, 6, 7, 8]
    dmx_packet_bytes = b'\x01\x02\x03\x04\x05\x06\x07\x08'

    def setUp(self):
        """Creates UDP Client."""
        # Create a dummy UDP Client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Instanciate StupidArtnetServer
        self.stupid = StupidArtnetServer()

        print(self.stupid)

        # register listener on universe 0
        self.listener = self.stupid.register_listener()

        # make an artnet packet on universe 0
        artnet_data = bytearray()
        artnet_data.extend(self.artnet_header)
        artnet_data.extend(self.dmx_packet_bytes)

        time.sleep(0.5)

        # send artnet data
        self.sock.sendto(artnet_data, ('localhost', 6454))

        time.sleep(0.2)

        # send random stuff
        self.sock.sendto(b'Hello world', ('localhost', 6454))

    def tearDown(self):
        """Destroy Objects."""
        # destroy UDP Server
        self.sock.close()

        # destroy artnet instance
        del self.stupid

    def test_buffer(self):
        """Assert that server received data and filtered correctly."""
        buffer = self.stupid.get_buffer(self.listener)

        # Test with a artnet header
        self.assertEqual(buffer, self.dmx_packet)

    def test_header(self):
        """Assert Art-Net header."""
        artdmx = b'Art-Net\x00\x00P\x00\x0e'
        typo = b'Art-Net\x00\x00\x00\x0e'

        # Test with a artnet header
        self.assertTrue(StupidArtnetServer.validate_header(artdmx))

        # Test header with typo on OP code
        self.assertFalse(StupidArtnetServer.validate_header(typo))


if __name__ == '__main__':
    unittest.main()
