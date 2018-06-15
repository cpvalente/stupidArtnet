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
This is meant as an implementation focusing on DMX over Artnet only (ArtDMX).

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
| 9      | 0x500  | OpCode High  (ArtDmx)         |
| 10     | 0x00   | Protocol V High               |
| 11     | 14     | Protocol V Low (currently 14) |
| 12     | 0x00   | Sequence** (0x00 to disable)  |
| 13     | int 8  | Physical     |
| 14     | int 8  | Sub + Uni ***                 |
| 15     | int 8  | Net ***      |
| 16     | int 8  | Length High (typically 512)   |
| 17     | int 8  | Length Low   |
| -      | -      | Append your packet here       |

** To allow the receiver to ensure packets are received in the right order <br />
*** By spec should look like this:
| Bit 15   | Bits 14-8  | Bits 7-4  | Bits 3-0  |
| :------- | :--------- | :-------- | :-------- |
| 0        | Net        | Subnet    | Universe  |

### Nets and Subnets

Artnet uses the concept of Universes and Subnets for data routing. I simplified here defaulting to use a 256 value universe. This will then be divided into low and high uint8 and look correct either way (Universe 17 will be Universe 1 of Subnet 2). In this case the net will always be 0.
This will look correct and behave fine for smaller networks, wanting to be able to specify Universes, Subnets and Nets you can disable simplification and give values as needed. <br />
The spec for Artnet 4 applies here: 128 Nets contain 16 Subnets which contain 16 Universes. 128 * 16 * 16 = 32 768 Universes

```
# Create a StupidArtnet instance with the relevant values

# By default universe is simplified to a value between 0 - 255
# on sending universe will be masked to two values
# making the use of subnets invisible

universe = 17
a = StupidArtnet(target_ip, universe, packet_size)


#############################################

# You can also disable simplification
a.set_simplified(False)

# Add net and subnet value
# Values here are 0 based
a.universe(15)
a.set_subnet(15)
a.set_net(127)
```

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
