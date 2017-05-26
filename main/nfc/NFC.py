from RPi.GPIO import *
from MFRC522 import *

class NFC:
    def __init__(self):
        self.MIFAREReader = MFRC522()

    def authenticate(self, key, sector, nfc_uid):
        while True:
            # Scan for cards
            (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

            # Get the UID of the card
            (status,uid) = self.MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == self.MIFAREReader.MI_OK and (uid == nfc_uid or nfc_uid == 0):

                # Select the scanned tag
                self.MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = self.MIFAREReader.MFRC522_Auth(self.MIFAREReader.PICC_AUTHENT1A, sector, key, uid)

                # Check if authenticated
                if status == self.MIFAREReader.MI_OK:
                    return uid
                print "Authentication Error!"
                return False

    def read(self, key, sector, nfc_uid = 0):
        if self.authenticate(key, sector, nfc_uid):
            data = self.MIFAREReader.MFRC522_Read(sector)
            self.MIFAREReader.MFRC522_StopCrypto1()
            return data
        return False

    def write(self, key, sector, data, nfc_uid = 0):
        uid = self.authenticate(key, sector, nfc_uid)
        if uid:
            self.MIFAREReader.MFRC522_Write(sector, data)
            self.MIFAREReader.MFRC522_StopCrypto1()
            return uid
        return False
