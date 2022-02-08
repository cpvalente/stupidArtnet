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
        """Test mask."""
        # send universe 8, simplified
        self.assertEqual(make_address_mask(8), b'\x08\x00')

        # send universe 8, simplified
        self.assertEqual(make_address_mask(8), b'\x08\x00')

        # send universe 17, simplified
        self.assertEqual(make_address_mask(17), b'\x0f\x00')

        # send universe 8, sub 8, net 100
        self.assertEqual(make_address_mask(8, 8, 100, False), b'\x88\x08')

        return True


if __name__ == '__main__':
    unittest.main()
