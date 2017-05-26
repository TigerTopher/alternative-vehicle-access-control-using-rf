import ultrasonic 

ultra = ultrasonic.UltrasonicDriver()
# ultra = ultrasonic.UltrasonicDriver(max_distance=5, logging=True)

# this is required
ultra.setup()

print ultra.is_car_near(num_samp=1, time_samp=3)
# num_samp => number of sampling
# time_samp => time interval in seconds between every sampling

# this is required
ultra.cleanup()
