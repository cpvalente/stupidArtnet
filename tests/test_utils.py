import unittest
from stupidArtnet.ArtnetUtils import shift_this, put_in_range, make_address_mask


class Test(unittest.TestCase):
    """Test class for Artnet Utilities."""

    def test_shift(self):
        """Test shift_this utility."""
        # send a 1
        self.assertEqual(shift_this(1), (0, 1))

        # send a 17
        self.assertEqual(shift_this(17), (0, 17))

        # send a 128
        self.assertEqual(shift_this(128), (0, 128))

        # send a 512
        self.assertEqual(shift_this(512), (2, 0))

        # send a 765
        self.assertEqual(shift_this(765), (2, 253))

        # send a 1024
        self.assertEqual(shift_this(1024), (4, 0))

        return True

    def test_range(self):
        """Test put_in_range utility."""
        # send a 1 from 0, 512, even
        self.assertEqual(put_in_range(1, 0, 512), (2))

        # send a 17 from 0, 18, even
        self.assertEqual(put_in_range(17, 0, 18), (18))

        # send a 128 from 0, 127
        self.assertEqual(put_in_range(128, 0, 127, False), (127))

        # send a 512 from 0, 512
        self.assertEqual(put_in_range(512, 0, 512), (512))

        # send a 1024 from 0, 512
        self.assertEqual(put_in_range(1024, 0, 512), (512))

        return True

    def test_mask(self):
        """Test mask and assert simplified mode."""
        self.assertEqual(make_address_mask(8), b'\x08\x00')
        self.assertEqual(make_address_mask(8, 0, 0, False), b'\x08\x00')

        self.assertEqual(make_address_mask(15), b'\x0f\x00')
        self.assertEqual(make_address_mask(15, 0, 0, False),  b'\x0f\x00')

        self.assertEqual(make_address_mask(16), b'\x10\x00')
        self.assertEqual(make_address_mask(0, 1, 0, False),  b'\x10\x00')

        self.assertEqual(make_address_mask(17), b'\x11\x00')
        self.assertEqual(make_address_mask(1, 1, 0, False),  b'\x11\x00')

        self.assertEqual(make_address_mask(18), b'\x12\x00')
        self.assertEqual(make_address_mask(2, 1, 0, False),  b'\x12\x00')
        self.assertEqual(2 + 1 * 16, 18)

        self.assertEqual(make_address_mask(99), b'c\x00')
        self.assertEqual(make_address_mask(3, 6, 0, False),  b'c\x00')
        self.assertEqual(3 + 6 * 16, 99)

        self.assertEqual(make_address_mask(255), b'\xff\x00')
        self.assertEqual(make_address_mask(15, 15, 0, False),  b'\xff\x00')
        self.assertEqual(15 + 15 * 16, 255)

        self.assertEqual(make_address_mask(256), b'\x00\x01')
        self.assertEqual(make_address_mask(0, 0, 1, False), b'\x00\x01')

        self.assertEqual(make_address_mask(257), b'\x01\x01')
        self.assertEqual(make_address_mask(1, 0, 1, False), b'\x01\x01')

        # with nets, it becomes difficult
        # to use the straight universe number
        self.assertEqual(make_address_mask(25736), b'\x88d')
        self.assertEqual(make_address_mask(8, 8, 100, False), b'\x88d')

        # Test clamp min
        self.assertEqual(make_address_mask(0), b'\x00\x00')
        self.assertEqual(make_address_mask(-15), b'\x00\x00')

        # Test clamp max
        self.assertEqual(make_address_mask(32767), b'\xff\x7f')
        self.assertEqual(make_address_mask(15, 15, 256, False), b'\xff\x7f')
        self.assertEqual(make_address_mask(999999), b'\xff\x7f')
        self.assertEqual(make_address_mask(99, 99, 300, False), b'\xff\x7f')

        return True


if __name__ == '__main__':
    unittest.main()
