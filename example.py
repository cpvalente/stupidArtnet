from lib.StupidArtnet import StupidArtnet
import time

# THESE ARE MOST LIKELY THE VALUES YOU WILL BE NEEDING
target_ip = '192.168.1.10'		# typically in 2.x or 10.x range
universe = 0 					# see docs
packet_size = 100				# it is not necessary to send whole universe

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

# YOU CAN CREATE YOUR OWN BYTE ARRAY OF PACKET_SIZE
packet = bytearray(packet_size)		# create packet for Artnet
for i in range(packet_size):		# fill packet with sequential values
    packet[i] = (i % 256)

# ... AND SET IT TO STUPID ARTNET
a.set(packet)						# only on changes

# ALL PACKETS ARE SAVED IN THE CLASS, YOU CAN CHANGE SINGLE VALUES
a.set_single_value(1, 255)

# ... AND SEND
a.show()

# OR USE STUPIDARTNET FUNCTIONS
a.flash_all()

time.sleep(1)						# wait a bit

a.blackout()

# CLOSE THE SOCKET IN THE END, JUST TO BE SURE
a.close()
