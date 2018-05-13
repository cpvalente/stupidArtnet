from lib.StupidArtnet import StupidArtnet
import time
import random

# THESE ARE MOST LIKELY THE VALUES YOU WILL BE NEEDING
target_ip = '192.168.1.10'		# typically in 2.x or 10.x range
universe = 0 					# see docs
packet_size = 100				# it is not necessary to send whole universe

# CREATING A STUPID ARTNET OBJECT
# SETUP NEEDS A FEW ELEMENTS
# TARGET_IP   = DEFAULT 127.0.0.1
# UNIVERSE    = DEFAULT 0
# PACKET_SIZE = DEFAULT 512
# FRAME_RATE  = DEFAULT 30
a = StupidArtnet(target_ip, universe, packet_size)

# MORE ADVANCED CAN BE SET WITH SETTERS IF NEEDED
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
a.set_single_value(1, 255)			# set channel 1 to 255

# ... AND SEND
a.show()							# send data

# OR USE STUPIDARTNET FUNCTIONS
a.flash_all()						# send single packet with all channels at 255

time.sleep(1)						# wait a bit, 1 sec

a.blackout()						# send single packet with all channels at 0

# ALL THE ABOVE EXAMPLES SEND A SINGLE DATAPACKET
# STUPIDARTNET IS ALSO THREADABLE
# TO SEND PERSISTANT SIGNAL YOU CAN START THE THREAD
a.start()							# start continuos sendin

# AND MODIFY THE DATA AS YOU GO
for x in range(100):
	for i in range(packet_size):  	# Fill buffer with random stuff
		packet[i] = random.randint(0, 255)
	a.set(packet)
	time.sleep(.2)

# ... REMEMBER TO CLOSE THE THREAD ONCE YOU ARE DONE
a.stop()

# CLOSE THE SOCKET IN THE END, JUST TO BE SURE
a.close()
