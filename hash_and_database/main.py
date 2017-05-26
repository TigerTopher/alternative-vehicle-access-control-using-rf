from Hasher import *

h = Hasher()
for i in range(0, 10):
    hashed = h.hash_function(str(i))
    print i, hashed
h.end_session()
