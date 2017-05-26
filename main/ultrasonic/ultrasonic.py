import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 17
ECHO = 27

class UltrasonicDriver:
    def __init__(self, max_distance=10, logging=False):
        self.max_distance = max_distance
        self.log = logging
        
    def is_car_near(self, num_samp=1, time_samp=0.01):
        # optional input
        # no. of sampling
        # intervals of sampling

        samplings = []
        if self.log:
            print "Target distance is:", self.max_distance

        for i in range(0, num_samp):
            read_distance = UltrasonicDriver.get_distance()
            if self.log:
                print "Sampling #", i + 1, "| Distance: ", read_distance, "cm | ",

            if read_distance <= self.max_distance:
                samplings.append(True)

                if self.log:
                    print "True"
            else:
                samplings.append(False)
                if self.log:
                    print "False"

            if num_samp > 1:
                time.sleep(time_samp)
                print "Slept for", time_samp, "seconds"

        if samplings.count(True) > len(samplings) / 2:
            if self.log:
                print "Verdict: True"
            return True

        if self.log:
            print "Verdict: False"
        return False

    @staticmethod
    def set_detect_distance():
        pass

    @staticmethod
    def setup():
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)

        GPIO.output(TRIG, False)
        time.sleep(2)

    #        print "Ultrasonic Sensor have settled. Ready to sense!"

    @staticmethod
    def cleanup():
        GPIO.cleanup()

    @staticmethod
    def get_distance():

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 5)

        return distance