from Checksum import *

packet = 2147483647
c = Checksum()
packet_with_checksum = c.transmitter_checksum(packet)
print packet_with_checksum
if c.receiver_checksum(packet_with_checksum):
    print "Correct Message!"
else:
    print "Wrong!"
