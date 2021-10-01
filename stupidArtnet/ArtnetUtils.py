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
    if (high_first):
        return((high, low))
    else:
        return((low, high))


def put_in_range(number, range_min, range_max, make_even=True):
    """Utility method: sets number in defined range.

    Args:
    number - number to use
    range_min - lowest possible number
    range_max - highest possible number
    make_even - should number be made even

    Returns:
    number - number in correct range

    """

    number = max(range_min, min(number, range_max))
    if (make_even and number % 2 != 0):
        number += 1
    return number


def make_address_mask(universe, sub=0, net=0, is_simplified=True):
    """Returns the address bytes for a given universe, subnet and net.

    Args:
    universe - Universe to listen
    sub - Subnet to listen
    net - Net to listen
    is_simplified - Wheter to use nets and subnet or simpler definition for universe only, see User Guide page 5 (Universe Addressing)

    Returns:
    bytes - byte mask for given address

    """

    address_mask = bytearray()

    if (is_simplified):
        # Ensure data is in right range
        universe = max(0, min(universe, 15))

        # Make mask
        a = shift_this(universe)  # convert to MSB / LSB
        address_mask.append(a[1])
        address_mask.append(a[0])
    else:
        # Ensure data is in right range
        universe = max(0, min(universe, 15))
        sub = max(0, min(sub, 15))
        net = max(0, min(sub, 127))

        # Make mask
        address_mask.append(sub << 4 | universe)
        address_mask.append(net & 0xFF)

    return address_mask
