from Database import *
from NFC import *
import crypt

# read info
f = open("key.txt", "r")
public_key = f.readline()[0:-1]
symmetric_key = f.readline()[0:-1]
symmetric_key = "kJqwiO0#zNqU4Cv*"
print symmetric_key
vac = f.readline()[0:-1]
vh = f.readline()[0:-1]
token = f.readline()[0:-1]
f.close()

# seed vac
d = Database("vac", "avracardabra", "localhost", "password")
d.insert_query("self_vac_no, ca_public_key", vac + "," + "'" + public_key + "'", "vac_info")
d.insert_query("vin, public_key", vh + "," + "'" + symmetric_key + "'", "vehicles_registered")
d.disconnect()

# write on NFC
n = NFC()
nfc_sector = 4
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

# string to int and int to string encoding
'''
int_symmetric_key = 0
for i in range(0, len(symmetric_key)):
    int_symmetric_key += (ord(symmetric_key[i]) << ((len(symmetric_key) - i - 1) * 8))
    print int_symmetric_key, (len(symmetric_key) - i - 1) * 8

string = ""
data_extractor = 2 ** 8 - 1
for i in range(0, 16):
    string += unichr(data_extractor & int_symmetric_key)
    int_symmetric_key = int_symmetric_key >> 8
string = string[::-1]
print string
'''

# seed vh
nfc_uid = n.write(key, nfc_sector, [ord(c) for c in symmetric_key])
d = Database("vh", "avracardabra", "localhost", "password")
d.insert_query("self_vh_no", vh, "vh_info")
d.insert_query("vac_no, token, entered, inside, nfc_uid, nfc_key, nfc_sector, key_A", vac + "," + "'" + token + "'" + "," + "FALSE" + "," + "FALSE" + "," + "'" + str(nfc_uid) + "'" + "," + "'" + str(key) + "'" + "," + str(nfc_sector) + "," + "TRUE", "vacs_accessible")
d.disconnect()
