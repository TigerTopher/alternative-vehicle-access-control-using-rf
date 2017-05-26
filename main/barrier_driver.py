import barrier
import time

# Don't forget to setup the GPIO by instantiating this
barr = barrier.BarrierDriver()

while True:
	barr.swing_up()
	time.sleep(1)
	barr.swing_down()
	time.sleep(1)
