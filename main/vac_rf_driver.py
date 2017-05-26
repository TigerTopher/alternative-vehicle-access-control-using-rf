from rf import *

d = []

v = Vac_RF()
v.receiver_setup()
for i in range(0, 15):
    print i
    sleep(4)
    start_time = time()
    packet = v.send(-1, 24)
    end_time = time()
    d.append(end_time - start_time)
print d
print "Average: ", sum(d)/len(d)
v.end_session()
