import socket
import unittest

from stupidArtnet import StupidArtnet


class Test(unittest.TestCase):
    """Test class for Artnet client."""

    # Art-Net stuff
    header_size = 18

    def setUp(self):
        """Creates UDP Server and Art-Net Client."""
        # Create dummy UDP Server
        self.sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind(('localhost', 6454))
        self.sock.settimeout(2000)

        # Instanciate stupidArtnet
        self.stupid = StupidArtnet(packet_size=24)

        # define a packet to send
        data = list(range(25))

        # send packet
        self.stupid.send(data)

        # confirm result
        self.received = self.sock.recv(512)

    def tearDown(self):
        """Destroy Objects."""
        # destroy UDP Server
        self.sock.close()

        # destroy artnet instance
        del self.stupid

    def test_header(self):
        """Assert Art-Net header."""
        # Art-Net header
        self.assertTrue(self.received.startswith(b'Art-Net'))

    def test_zero(self):
        """Check first data value, should be 0."""
        self.assertEqual(self.received[self.header_size], 0)

    def test_twelve(self):
        """Check twelfth data value, should be 12."""
        self.assertEqual(self.received[self.header_size] + 12, 12)

    def test_twentyfour(self):
        """Check twenty-fourth data value, should be 24."""
        self.assertEqual(self.received[self.header_size] + 24, 24)


if __name__ == '__main__':
    unittest.main()
