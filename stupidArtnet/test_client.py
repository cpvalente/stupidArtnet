import unittest
from StupidArtnet import StupidArtnet
import socket


class Test(unittest.TestCase):

    def setUp(self):
        """Creates UDP Server and Art-Net Client."""

        # Create dummy UDP Server
        self.sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind(('localhost', 6454))

        # Instanciate stupidArtnet
        self.stupid = StupidArtnet(packet_size=24)

    def tearDown(self):
        """Destroy Objects."""

        # destroy UDP Server
        self.sock.close()

        # destroy artnet instance
        del(self.stupid)

    def test_client(self):
        """Sends data to server and asserts output."""

        # define a packet to send
        data = [x for x in range(25)]

        # send packet
        self.stupid.send(data)

        # assert result
        m = self.sock.recv(512)

        # Art-Net header
        self.assertTrue(m.startswith(b'Art-Net'))

        # Check a few random points
        header_size = 18

        self.assertEqual(m[header_size],        0)
        self.assertEqual(m[header_size] + 12,   12)
        self.assertEqual(m[header_size] + 24,   24)


if __name__ == '__main__':
    unittest.main()
