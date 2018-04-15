# StupidArtnet

(Very) Simple Artnet implementation in Python


### Basics
Sending simple Artnet packets is pretty easy
```
# A StupidArtnet instance holds a target IP / universe and a buffer
a = StupidArtnet(target_ip, universe, packet_size)

# YOU CAN CREATE YOUR OWN BYTE ARRAY OF PACKET_SIZE
packet = bytearray(packet_size)
for i in range(packet_size):
	packet[i] = (i % 256)

# ... AND SET IT TO STUPID ARTNET
a.set(packet)

# YOU CAN CHANGE SINGLE VALUES
a.set_single_value(address, value)

# ... AND THE DATA
a.show()

# THE DATA IS SAVED IN THE INSTANCE BUFFER
# YOU CAN SEND THE LAST BUFFER AGAIN BY CALLING .show
a.show()

```
### Persistent sending
Usually Artnet devices (and DMX in general) transmit data at a rate of no less than 30Hz.
You can do this with StupidArtnet by using its threaded abilities

```
# TO SEND PERSISTENT SIGNAL YOU CAN START THE THREAD
a.start()

# AND MODIFY THE DATA AS YOU GO
for x in range(100):
	for i in range(packet_size):	# Fill buffer with random stuff
		packet[i] = random.randint(0, 255)
	a.set(packet)
	time.sleep(.2)

# ... REMEMBER TO CLOSE THE THREAD ONCE YOU ARE DONE
a.stop()

```


### Notes

Artnet libraries tend to be complicated and hard to get off the ground. Sources were either too simple and didn't explain the workings or become too complex by fully implementing the protocol. <br />
This is mean as an implementation focusing on DMX over Artnet only.

I am also doing my best to comment the sections where the packets is build. In an effort to help you understand the protocol and be able to extend it for a more case specific use.

Users looking to send a few channels to control a couple of LEDs, projectors or media servers can use this as reference.

Are you running several universes with different fixture types? I would recommend [ArtnetLibs](https://github.com/OpenLightingProject/libartnet) or the [Python Wrapper for Artnet Libs](https://github.com/haum/libartnet)

### Artnet

Really Artnet is really simple. just shove the protocol header into your data array and send it to the right place.
Usually Artnet devices are in the range of 2.x.x.x or 10.x.x.x. This is a convention however is not forcefully implemented.
I have filled the data to represent a ArtDmx packet


| Byte   | Value  | Description  |
| -----: | :----: | ------------ |
| 0      | A      | Header       |
| 1      | r      | "            |
| 2      | t      | "            |
| 3      | -      | "            |
| 4      | N      | "            |
| 5      | e      | "            |
| 6      | t      | "            |
| 7      | 0x00   | "            |
| 8      | 0x00   | OpCode Low   |
| 9      | 0x500  | OpCode High  |
| 10     | 0x00   | Protocol V High               |
| 11     | 14     | Protocol V Low (currently 14) |
| 12     | 0x00   | Sequence** (0x00 to disable)  |
| 13     | int 8  | Physical     |
| 14     | int 8  | Universe Low***               |
| 15     | int 8  | Universe High***              |
| 16     | int 8  | Lenght High (typically 512)   |
| 17     | int 8  | Lenght Low   |
| -      | -      | Append your packet here       |

** To allow the receiver to ensure packets are received in the right order <br />
*** Technically these is incorrect, Artnet uses the concept of Universes and Subnets for data routing. I simplified here

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
