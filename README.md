[![.github/workflows/publish-to-pypi.yml](https://github.com/cpvalente/stupidArtnet/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/cpvalente/stupidArtnet/actions/workflows/publish-to-pypi.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# StupidArtnet

(Very) Simple Art-Net implementation in Python

#### Table of Contents
- [Installing from github](#installing-from-github)
- [Installing from Pip](#installing-from-pip)
- [Server Basics](#receiving-data)
- [Client Basics](#basics)
- [Persistent sending](#persistent-sending)
- [Example code](#example-code)
- [Notes](#notes)
- [Art-Net](#art-net)
- [Nets and Subnets](#nets-and-subnets)
- [License](#license)

### Installing from github
You can get up and running quickly cloning from github.
Run the example file to make sure everything is up to scratch
```bash
$ git clone https://github.com/cpvalente/stupidArtnet.git
$ cd stupidArtnet
$ python3 examples/example.py
```
### Installing from Pip
The project is now available in [Pip](https://pypi.org/project/stupidArtnet/) and can be installed with
```pip install stupidartnet```

### Receiving Data
You can use the server module to receive Art-Net data
```python
# a StupidArtnetServer can listen to a specific universe
# and return new data to a user defined callback
a = StupidArtnetServer(universe=0, callback_function=test_callback)

# if you prefer, you can also inspect the latest
# received data yourself
buffer = a.get_buffer()

```
### Persistent sending
Usually Artnet devices (and DMX in general) transmit data at a rate of no less than 30Hz.
You can do this with StupidArtnet by using its threaded abilities

```python
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
### Example code
See examples folder inside the package directory
- [x] Use with Tkinter
- [x] Send Art-Net (client)
- [x] Receive Art-Net (server)

### Notes

Artnet libraries tend to be complicated and hard to get off the ground. Sources were either too simple and didn't explain the workings or become too complex by fully implementing the protocol. <br />
This is meant as an implementation focusing on DMX over Artnet only (ArtDMX).

I am also doing my best to comment the sections where the packets is build. In an effort to help you understand the protocol and be able to extend it for a more case specific use.

Users looking to send a few channels to control a couple of LEDs, projectors or media servers can use this as reference.

Are you running several universes with different fixture types? I would recommend [ArtnetLibs](https://github.com/OpenLightingProject/libartnet) or the [Python Wrapper for Artnet Libs](https://github.com/haum/libartnet)

### Art-Net

Getting things running with protocol is pretty simple. just shove the protocol header into your data array and send it to the right place.
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

Note: This is true for the current version of Artnet 4 (v14), as [defined here](https://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf)

### Nets and Subnets

Artnet uses the concept of Universes and Subnets for data routing. I simplified here defaulting to use a 256 value universe. This will then be divided into low and high uint8 and look correct either way (Universe 17 will be Universe 1 of Subnet 2). In this case the net will always be 0.
This will look correct and behave fine for smaller networks, wanting to be able to specify Universes, Subnets and Nets you can disable simplification and give values as needed. <br />
The spec for Artnet 4 applies here: 128 Nets contain 16 Subnets which contain 16 Universes. 128 * 16 * 16 = 32 768 Universes

```python
# Create a StupidArtnet instance with the relevant values

# By default universe is simplified to a value between 0 - 255
# this should suffice for anything not using subnets
# on sending universe will be masked to two values
# making the use of subnets invisible

universe = 17	# equivalent to universe 1 subnet 1
a = StupidArtnet(target_ip, universe, packet_size)


#############################################

# You can also disable simplification
a.set_simplified(False)

# Add net and subnet value
# Values here are 0 based
a.set_universe(15)
a.set_subnet(15)
a.set_net(127)
```

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
