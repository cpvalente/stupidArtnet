from lib.StupidArtnet import StupidArtnet
import time

# THESE ARE MOST LIKELY THE VALUES YOU WILL BE NEEDING
target_ip = '127.0.0.1'  # localhost for testing, Artnet IPs typically on the 2.x or 10.x range
universe = 1            # see docs
packet_size = 100       # it is not necessary to send whole universe

# CREATING A STUPID ARTNET OBJECT
a = StupidArtnet()

# SETUP NEEDS FEW SKIPPABLE ELEMENTS
# TARGET_IP   = DEFAULT 127.0.0.1
# UNIVERSE    = DEFAULT 0
# PACKET_SIZE = DEFAULT 512
a.setup(target_ip, universe, packet_size)

# MORE ADVANCED CAN BE SET WITH SETTERS IF NEEDED
# SEQUENCE    = DEFAULT 0
# NET         = DEFAULT 0
# SUBNET      = DEFAULT 0

# CHECK INIT
print(a)

# YOU CAN CREATE YOUR OWN BYTE ARRAY
# OF PACKET_SIZE AND SEND IT
packet = bytearray(packet_size)  # create packet for Artnet
for i in range(packet_size):     # fill packet with sequential values
    packet[i] = (i % 256)

a.send(packet)                  # send packet

# OR USE STUPIDARTNET FUNCTIONS

for i in range(10):
    a.flash_all()       # set all to high
    time.sleep(100)     # wait

    a.blackout()        # set all to low
    time.sleep(100)     # wait
