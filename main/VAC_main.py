from rf import *
from time import *
from random import *
from ultrasonic import *
from crypt import *
from barrier import *
import string
import RPi.GPIO as GPIO

class Vac():
    def __init__(self):
        self.vac_rf = Vac_RF()
        self.vac_rf.receiver_setup()
        self.database = self.vac_rf.database
        self.data_length = 128

        self.ultrasonic_sensor = UltrasonicDriver()
        self.ultrasonic_sensor.setup()
        self.RSADriver = RSADriver()
        self.AESDriver = AESDriver()
        self.barrier = BarrierDriver()

    def activate(self):
        while True:
            if(self.ultrasonic_sensor.is_car_near()):
                # broadcast nonce
                nonce = ''.join(choice(string.letters + string.digits + string.punctuation) for _ in range(16))
                int_nonce = 0
                for i in range(0, len(nonce)):
                    int_nonce += (ord(nonce[i]) << ((len(nonce) - i - 1) * 8))
                print nonce, int_nonce
                self.vac_rf.send(-1, int_nonce)

                # Consider case na iniwan ni kotse si vac

                # receive data
                received_data = self.vac_rf.reliable_data_transfer_receive()
                received_data = self.vac_rf.get_data_from_packet(received_data)

                # get the public key for the vehicle
                public_key = self.database.select_query("public_key", "vehicles_registered", "vin = " + str(received_data[1]))

                # if there is no public key for the vehicle, he can't go in
                if(public_key == []):
                    print "Car can't go in."
                    sleep(5)
                    continue

                public_key = public_key[0][0]

                # convert data to string in order to decrypt it
                string_data = ""
                int_data = received_data[2]
                data_extractor = 2 ** 8 - 1
                for i in range(0, 16):
                    string_data += chr(data_extractor & int_data)
                    int_data = int_data >> 8
                string_data = string_data[::-1]

                print string_data, received_data[2]

                # decrypt data
                string_data = self.AESDriver.base64encode(string_data)
                print string_data
                decrypted_data = self.AESDriver.decrypt_data(string_data, public_key, 16)

                #print "D:", decrypted_data, "N:", nonce

                # if decrypted data is equal to nonce enter
                if decrypted_data == nonce:
                    self.barrier.swing_up()
                    print "Welcome!"
                    sleep(5)
                    self.barrier.swing_down()
                    continue

                # if it gets here, you can't go in
                print "You are not welcome here!"
                sleep(5)
            sleep(2)
            #self.vac_rf.send(data[1], self.crypt_driver.encrpyt(sign(data[2])))
            return

    def end(self):
        self.vac_rf.end_session()
        self.ultrasonic_sensor.cleanup()

v = Vac()
while True:
    v.activate()
v.end()
