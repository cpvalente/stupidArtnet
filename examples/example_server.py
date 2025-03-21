from stupidArtnet import StupidArtnetServer
import time


# create a callback to handle data when received
def test_callback(data):
    """Test function to receive callback data."""
    # the received data is an array
    # of the channels value (no headers)
    print('Received new data \n', data)


# a Server object initializes with the following data
# universe 			= DEFAULT 0
# subnet   			= DEFAULT 0
# net      			= DEFAULT 0
# setSimplified     = DEFAULT True
# callback_function = DEFAULT None

# You can use universe only
universe = 0

# By default, the server uses port 6454, no need to specify it.
# If you need to change the Art-Net port, ensure the port is within the valid range for UDP ports (1024-65535)
# Be sure that no other application is using the selected port on your network.
# To specify a different port, for example port 6455, you can do it like this:
# a = StupidArtnetServer(port=6455)  # Change 6455 to any valid port number between 1024 and 65535.

a = StupidArtnetServer() #Create a server with the default port 6454


# For every universe we would like to receive,
# add a new listener with a optional callback
# the return is an id for the listener
u1_listener = a.register_listener(
    universe, callback_function=test_callback)


# or disable simplified mode to use nets and subnets as per spec
# subnet = 1 (would have been universe 17 in simplified mode)
# net = 0
# a.register_listener(universe, sub=subnet, net=net,
#                    setSimplified=False, callback_function=test_callback)


# print object state
print(a)

# giving it some time for the demo
time.sleep(3)

# if you prefer not using callbacks, the channel data
# is also available in the method get_buffer()
# use the given id to access it
buffer = a.get_buffer(u1_listener)

# Remember to check the buffer size, as this may vary from 512
n_data = len(buffer)
if n_data > 0:
    # in which channel 1 would be
    print('Channel 1: ', buffer[0])

    # and channel 20 would be
    print('Channel 20: ', buffer[19])

# Cleanup when you are done
del a
