from rf import *
from time import *
from random import *
from crypt import *
from nfc import *
import RPi.GPIO as GPIO

class VH:
    def __init__(self):
        self.vh_rf = VH_RF()
        self.vh_rf.receiver_setup()
        self.database = self.vh_rf.database

        self.RSADriver = RSADriver()
        self.AESDriver = AESDriver()
        self.nfc = NFC()

#        self.nfc_uid = [37, 28, 22, 203, 228]
#        self.key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
#        self.sector = 4

    def string_to_int_list(self, listed_string):
        l = list(listed_string)
        l.remove('[')
        l.remove(']')
        temp = ""
        new_list = []
        for i in l:
            if i == ",":
                new_list.append(int(temp, 10))
                temp = ""
                continue
            if i != " ":
                temp += i
        new_list.append(int(temp, 10))
        return new_list

    def activate(self):
        while True:
            received_data = self.vh_rf.reliable_data_transfer_receive()
            received_data = self.vh_rf.get_data_from_packet(received_data)

            vacs_accessible = self.database.select_query("*", "vacs_accessible", "vac_no = " + str(received_data[1]))
            if vacs_accessible == []:
                print "You can not go here"

            # if inside, just continue going inYung ineedit ba nating file kahapon l
            vacs_accessible = vacs_accessible[0]
            if bool(vacs_accessible[2]):
                continue

            # get NFC info from database
            nfc_uid = self.string_to_int_list(vacs_accessible[4])
            key = self.string_to_int_list(vacs_accessible[5])
            sector = vacs_accessible[6]

            # Check NFC
            hexed_symmetric_key = self.nfc.read(key, sector, nfc_uid)

            # turn hexed list symmetric key into string
            symmetric_key = ""
            for hex_key in hexed_symmetric_key:
                symmetric_key += unichr(hex_key)

            # turn nonce into string
            string_data = ""
            int_data = received_data[2]
            data_extractor = 2 ** 8 - 1
            for i in range(0, 16):
                string_data += unichr(data_extractor & int_data)
                int_data = int_data >> 8
            string_data = string_data[::-1]

            # Encrypt nonce
            encrypted_data = self.AESDriver.encrypt_data(string_data, symmetric_key, 16)
            print encrypted_data
            encrypted_data = self.AESDriver.base64decode(encrypted_data)

            # turn encrypted data to integer for sending
            int_encrypted_data = 0
            for i in range(0, len(encrypted_data)):
                int_encrypted_data += (ord(encrypted_data[i]) << ((len(encrypted_data) - i - 1) * 8))

            print encrypted_data, int_encrypted_data

            # transmit integer
            sleep(2)
            self.vh_rf.send(received_data[1], int_encrypted_data)
            return

    def end(self):
        self.vh_rf.end_session()

v = VH()
while True:
    v.activate()
v.end()
