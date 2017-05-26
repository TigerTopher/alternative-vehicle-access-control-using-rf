import time
import wiringpi

BARRIER_PIN = 18

class BarrierDriver:
	def __init__(self):
		self.setup()

	def setup(self):
		# use 'GPIO naming'
		wiringpi.wiringPiSetupGpio()

		# set #18 to be a PWM output
		wiringpi.pinMode(BARRIER_PIN, wiringpi.GPIO.PWM_OUTPUT)
		# set the PWM mode to milliseconds stype
		wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

		# divide down clock
		wiringpi.pwmSetClock(192)
		wiringpi.pwmSetRange(2000)

	def swing_up(self):
		for pulse in range(30, 150, 1):
			print pulse
			wiringpi.pwmWrite(18, pulse)
			time.sleep(0.03)
		time.sleep(1)

	def swing_down(self):
		for pulse in range(30, 150, -1):
			print pulse
			wiringpi.pwmWrite(18, pulse)
			time.sleep(0.03)
		time.sleep(1)
