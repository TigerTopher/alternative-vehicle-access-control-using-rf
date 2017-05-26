from rf import *

d =[]

v = VH_RF()
v.receiver_setup()
for i in range(0, 15):
    print i
    start_time = time()
    packet = v.reliable_data_transfer_receive()
    data = v.get_data_from_packet(packet)
    print data
    end_time = time()
    d.append(end_time - start_time)
print d
print "Average: ", sum(d)/len(d)
v.end_session()
