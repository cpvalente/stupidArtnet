""" Simple Implementation of Artnet.

	06.04.18
	Python Version: 3.6
	Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf
			http://art-net.org.uk/wordpress/structure/streaming-packets/artdmx-packet-definition/

	NOTES
	- To make it super simple I have not implemented NET or SUBNET,
	these default to 0

"""

import socket       # how to stop this from being imported twice?


class StupidArtnet():
	"""(Very) simple implementation of Artnet."""

	UDP_PORT = 6454
	TARGET_IP = '127.0.0.1'

	SEQUENCE = 0
	PHYSICAL = 0
	UNIVERSE = 0
	NET = 0
	PACKET_SIZE = 512
	HEADER = bytearray()
	BUFFER = bytearray()

	_unL = 0x00
	_unH = 0x00

	_chL = 0x00
	_chH = 0x00

	def __init__(self):
		"""Initialize UDP here."""
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		pass

	def __str__(self):
		"""Printable object state."""
		s = "==================================="
		s = "Stupid Artnet initialized\n"
		s += "Target IP: %s:%i \n" % (self.TARGET_IP, self.UDP_PORT)
		s += "Universe: %i \n" % self.UNIVERSE
		s += "Packet Size: %i \n" % self.PACKET_SIZE

		return s

	def setup(self, targetIP='127.0.0.1', universe=0, packet_size=512):
		"""Setup class with network information."""
		self.TARGET_IP = targetIP
		self.UNIVERSE = universe
		self.PACKET_SIZE = self.put_in_range(packet_size, 2, 512)
		self.make_header()
		self.BUFFER = bytearray(self.PACKET_SIZE)

	def make_header(self):
		"""Setter for universe."""
		# 0 - id (8 x bytes)
		self.HEADER = bytearray()
		self.HEADER.extend(bytearray('Art-Net', 'utf8'))
		self.HEADER.append(0x0)
		# 8 - opcode low byte first  (int 16)
		self.HEADER.append(0x00)
		self.HEADER.append(0x50)  # ArtDmx data packet
		# 10 - proto ver high byte first (int 16)
		self.HEADER.append(0x0)
		self.HEADER.append(14)
		# 10 - sequence (int 8), not implemented
		# self.HEADER.append(self.SEQUENCE)
		self.HEADER.append(0x00)
		# physical port (int 8)
		self.HEADER.append(0x00)
		# 16bit universe, low bite first
		# not quite, good enough for now
		v = self.shift_this(self.UNIVERSE)			# convert to MSB / LSB
		self.HEADER.append(v[1])
		self.HEADER.append(v[0])

		# 16bit packet size, high byte first
		v = self.shift_this(self.PACKET_SIZE)		# convert to MSB / LSB
		self.HEADER.append(v[0])
		self.HEADER.append(v[1])

	def show(self):
		"""Finally send data."""
		packet = bytearray()
		packet.extend(self.HEADER)
		packet.extend(self.BUFFER)
		# self.SEQUENCE = (self.SEQUENCE + 1) % 256 # Not implemented
		self.s.sendto(packet, (self.TARGET_IP, self.UDP_PORT))

	def close(self):
		"""Close UDP socket."""
		self.s.close()

	##
	# SETTERS - HEADER
	##

	def set_universe(self, universe):
		"""Setter for universe."""
		self.UNIVERSE = universe
		v = self.shift_this(self.UNIVERSE)
		self._unL = v[1]
		self._unH = v[0]

		self.make_header()

	def set_packet_size(self, packet_size):
		"""Setter for packet size."""
		self.PACKET_SIZE = packet_size
		v = self.shift_this(self.UNIVERSE)
		self._chL = v[1]
		self._chH = v[0]

		self.make_header()

	def set_physical(self, physical):
		"""Setter for physical address.

		Not implemented
		"""
		self.PHYSICAL = physical  # not implemented
		self.make_header()

	def set_net(self, net):
		"""Setter for net address.

		Not implemented
		"""
		self.NET = net  # not implemented
		self.make_header()

	##
	# SETTERS - DATA
	##

	def clear(self):
		"""Clear DMX buffer."""
		self.BUFFER = bytearray(self.PACKET_SIZE)

	def set(self, p):
		"""Set buffer."""
		if len(self.BUFFER) != self.PACKET_SIZE:
			print("ERROR: packet does not match declared packet size")
			return
		self.BUFFER = p

	def set_single_value(self, address, value):
		"""Set single value in DMX buffer."""
		if address < 1 or address > 512:
			return
		self.BUFFER[address - 1] = value

	def set_single_rem(self, address, value):
		"""Set single value while blacking out others"""
		if address < 1 or address > 512:
			return
		self.clear()
		self.BUFFER[address - 1] = value

	def set_rgb(self, address, r, g, b):
		"""Set RGB from start address."""
		if address < 1 or address > 510:
			return
		self.BUFFER[address - 1] = r
		self.BUFFER[address    ] = g
		self.BUFFER[address + 1] = b

	##
	# AUX
	##

	def see_header(self):
		"""Show header values."""
		return self.HEADER

	def see_buffer(self):
		"""Show buffer values."""
		return self.BUFFER

	def blackout(self):
		"""Sends 0's all across"""
		self.clear()
		self.show()

	def flash_all(self):
		"""Sends 255's all across"""
		packet = bytearray(self.PACKET_SIZE)
		for i in range(self.PACKET_SIZE):
			packet[i] = 255
		self.set(packet)
		self.show()

	##
	# UTILS
	##

	@staticmethod
	def shift_this(number, high_first=True):
		"Utility method: extracts MSB and LSB from number"
		low 	= (number & 0xFF)
		high 	= ((number >> 8) & 0xFF)
		if (high_first):
			return((high, low))
		else:
			return((low, high))
		print("Something went wrong")
		return False

	@staticmethod
	def put_in_range(number, range_min, range_max, make_even=True):
		"Utility method: sets number in defined range."
		if (make_even and number % 2 != 0):
			number += 1
		if (number < range_min):
			number = range_min
		if (number > range_max):
			number = range_max
		return number
