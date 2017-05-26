from Database import *
from random import *

d = Database("central_authority", "avracardabra", "localhost", "password")
max_bits = 24
l = range(0, 2 ** max_bits)
shuffle(l)
iterator = 0
for i in l:
    d.insert_query("hash", str(i), "hashes")
    print iterator
    iterator += 1
d.disconnect()
