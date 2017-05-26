from nfc import *

n = NFC()

nfc_uid = [37, 28, 22, 203, 228]
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
sector = 4

data = n.read(key, sector)
print data

#data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#uid = n.write(key, sector, data)
#print uid

#data = n.read(key, sector, uid)
#print data
