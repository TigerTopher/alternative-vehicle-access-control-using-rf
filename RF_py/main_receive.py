from receiver import *

def receive_packets():
    PIN = 4

    if(wiringPiSetup() == -1):
        print "Error"
        return 0

    enableReceivePin(PIN)
    while True:
        if(available()):
            value = getReceivedValue()

            if(value == 0):
                print "Unknown encoding"
            else:
                print value

            resetAvailable()


receive_packets()
