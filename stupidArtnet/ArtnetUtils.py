"""Provides common functions byte objects."""


def shift_this(number, high_first=True):
    """Utility method: extracts MSB and LSB from number.

    Args:
    number - number to shift
    high_first - MSB or LSB first (true / false)

    Returns:
    (high, low) - tuple with shifted values

    """
    low = (number & 0xFF)
    high = ((number >> 8) & 0xFF)
    if high_first:
        return((high, low))
    return((low, high))


def clamp(number, min_val, max_val):
    """Utility method: sets number in defined range.

    Args:
    number - number to use
    range_min - lowest possible number
    range_max - highest possible number

    Returns:
    number - number in correct range
    """
    return max(min_val, min(number, max_val))


def set_even(number):
    """Utility method: ensures number is even by adding.

    Args:
    number - number to make even

    Returns:
    number - even number
    """
    if number % 2 != 0:
        number += 1
    return number


def put_in_range(number, range_min, range_max, make_even=True):
    """Utility method: sets number in defined range.
    DEPRECATED: this will be removed from the library

    Args:
    number - number to use
    range_min - lowest possible number
    range_max - highest possible number
    make_even - should number be made even

    Returns:
    number - number in correct range

    """
    number = clamp(number, range_min, range_max)
    if make_even:
        number = set_even(number)
    return number


def make_address_mask(universe, sub=0, net=0, is_simplified=True):
    """Returns the address bytes for a given universe, subnet and net.

    Args:
    universe - Universe to listen
    sub - Subnet to listen
    net - Net to listen
    is_simplified - Whether to use nets and subnet or universe only,
    see User Guide page 5 (Universe Addressing)

    Returns:
    bytes - byte mask for given address

    """
    address_mask = bytearray()

    if is_simplified:
        # Ensure data is in right range
        universe = clamp(universe, 0, 32767)

        # Make mask
        msb, lsb = shift_this(universe)  # convert to MSB / LSB
        address_mask.append(lsb)
        address_mask.append(msb)
    else:
        # Ensure data is in right range
        universe = clamp(universe, 0, 15)
        sub = clamp(sub, 0, 15)
        net = clamp(net, 0, 127)

        # Make mask
        address_mask.append(sub << 4 | universe)
        address_mask.append(net & 0xFF)

    return address_mask
