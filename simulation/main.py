# Programmed by: Christopher Ivan Vizcarra [TigerTopher]
# February 19, 2017
# Thesis simulation

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
import time
import random
import base64
import hashlib

CHALLENGE_RESPONSE_BYTES = 1000000
KEY_LENGTH = 4096
BS = 16

pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


class AESCipher:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))


def randomBytes(n):
    return bytearray(random.getrandbits(8) for i in range(n))


# Temporary Nonce
def gen_nonce(length=1000):  # length=1000):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


class TopherTimer:
    def __init__(self, verbose_param):
        self.elapsing = False
        self.verbose = verbose_param
        self.start_time = 0.0
        self.end_time = 0.0
        self.log_message = ""

    def startTimer(self, log_message_param):
        self.elapsing = True
        self.start_time = time.time()
        self.log_message = log_message_param
        if self.verbose:
            print "[LOG] Timer starts. Action: ", self.log_message

    def endTimer(self):
        self.elapsing = False
        self.end_time = time.time()
        if self.verbose:
            print "[LOG] Timer ends.   Action: ", self.log_message

        print "Duration is ", str(self.end_time - self.start_time), "seconds"

        self.log_message = ""


class VehicleAccessControl:
    def __init__(self, id=-1):  # initialization
        self.id = id
        self.name = ""
        self.registeredVHs = {}
        # id : [symmetric key, lifetime]

        tt.startTimer("Generating Public Private Keys for VAC [Key length: " + str(KEY_LENGTH) + " bits]")

        # self.keys contain the public and private key
        random_generator = Random.new().read
        self.keys = RSA.generate(KEY_LENGTH, random_generator)

        tt.endTimer()
        self.CA_pub = ""

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def broadcastVACinfo(self):
        return (self.id, gen_nonce(CHALLENGE_RESPONSE_BYTES))

    def getPublicKey(self):
        return self.keys.publickey().exportKey('DER')

    def setCAPublicKey(self, CA_pub):
        self.CA_pub = CA_pub

    def getCAPublicKey(self):
        return self.CA_pub

    def VACdecryptsMessage(self, VH_id, encrypted_message, iv, challenge):
        # find the key based on the VH_id

        tt.startTimer("VAC decrypts Message")
        decryptor = AES.new(self.registeredVHs[VH_id][0], AES.MODE_CFB, IV=iv)
        plain = decryptor.decrypt(encrypted_message)
        tt.endTimer()

        if (challenge == plain):
            return True
        return False

    def findVHbyID(self, VH_id):
        for key, value in self.registeredVHs.iteritems():
            if (key == VH_id):
                return self.registeredVHs[VH_id]
        return -1


class CentralAuthority:
    def __init__(self):
        self.VACs = {}
        self.VHs = {}
        self.VAC_count = 0
        self.VH_count = 0

        tt.startTimer("Generating Public Private Keys for CA [Key length: " + str(KEY_LENGTH) + " bits]")

        # self.keys contain the public and private key
        random_generator = Random.new().read
        self.keys = RSA.generate(KEY_LENGTH, random_generator)

        tt.endTimer()

    def getPublicKey(self):
        return self.keys.publickey().exportKey('DER')

    def generateVAC(self, name):
        VAC = VehicleAccessControl(self.VAC_count + 1)
        VAC.setName(name)
        VAC.setCAPublicKey(self.getPublicKey())
        self.registerVAC(VAC)
        self.VAC_count += 1
        return VAC

    def registerVAC(self, VAC):
        self.VACs.update({VAC.getId(): VAC})

    def generateVH(self, name):
        # Create Vehicle
        VH = Vehicle(self.VH_count + 1)
        VH.setName(name)

        # Register Vehicle
        self.registerVH(VH)
        self.VH_count += 1
        return VH

    def registerVH(self, VH):
        self.VHs.update({VH.getId(): VH})

    def grantToken(self, VH_id, VAC_id, lifetime_days):
        # Token format: Symmetric key, VH id, lifetime

        # Generate Symmetric Key
        new_symmetric_key = gen_nonce(32)
        # 24 bits + 128 bits +
        message = str(VH_id) + "|" + str(lifetime_days) + "|" + new_symmetric_key

        # Gather VAC
        VAC = self.VACs[VAC_id]

        # Signing message
        hashed_message = SHA256.new(message).digest()
        signature = self.keys.sign(hashed_message, '')

        # Encrypting message
        encrypted_message = VAC.keys.publickey().encrypt(message, 32)
        decrypted_message = VAC.keys.decrypt(encrypted_message)

        if self.keys.publickey().verify(hashed_message, signature):
            print "True"

        return (VAC_id, encrypted_message, signature,
                new_symmetric_key)  # Returns a tuple of VAC_id, encrypted message, signature, and symmetric key

    # decrypted_message = VAC.keys.decrypt(encrypted_message)
    # if self.keys.publickey().verify(hashed_message, signature_message):
    # 	print "True"

    def getVACIdbyName(self, name):
        for key, value in self.VACs.iteritems():
            if (value.getName() == name):
                return value.getId()

        print "Finding VAC named", name, "was found"
        return -1

    def getVHIdbyName(self, name):
        for key, value in self.VHs.iteritems():
            if (value.getName() == name):
                return value.getId()

        print "Finding VH named", name, "was found"
        return -1


class Vehicle:
    def __init__(self, id=-1):  # initialization
        self.id = id
        self.name = ""
        self.tokens = {}  # token - CA signed vouchers to enter a VAC
        self.VACsAndKeys = {}  # VAC_id : symmetric key
        self.isRegisteredToVAC = {}

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def addToken(self, token):
        # token is a tuple of VAC_id, encrypted message, signature, and symmetric key
        # encrypted message contains:
        # message = str(VH_id) + "|" + str(lifetime_days)+ "|" + new_symmetric_key

        # The token is added in the db
        # The symmetric key is added in the db as well
        self.isRegisteredToVAC.update({token[0]: False})
        self.VACsAndKeys.update({token[0]: token[3]})  # VAC_id and symmetric key
        self.tokens.update({token[0]: token})

    def registerVAC(self, VAC_id):
        self.isRegisteredToVAC[VAC_id] = True

    def getToken(self, VAC_id):
        for key, value in self.tokens.iteritems():
            if (key == VAC_id):
                return self.tokens[VAC_id]
        return -1

    def isVACTokenrecognized(self, VAC_id):
        for key, value in self.tokens.iteritems():
            if (key == VAC_id):
                return self.tokens[VAC_id]
        return -1

    def isVACrecognized(self, VAC_id):
        for key, value in self.VACsAndKeys.iteritems():
            if (key == VAC_id):
                return self.VACsAndKeys[VAC_id]
        return -1

    def checkIfRegisteredToVAC(self, VAC_id):
        for key, value in self.isRegisteredToVAC.iteritems():
            if (key == VAC_id):
                return self.isRegisteredToVAC[VAC_id]  # True or False
        return -1

    def processVAC(self, VAC_id, challenge):
        print "VACs and Keys", self.VACsAndKeys
        print VAC_id
        print self.isVACrecognized(VAC_id)

        if (self.isVACrecognized(VAC_id) != -1):  # If recognized
            # Check if registered...
            print "Registered", self.checkIfRegisteredToVAC(VAC_id)

            if (self.checkIfRegisteredToVAC(VAC_id)):
                # encrypt challenge question
                tt.startTimer("VH encrypts challenge question")
                key = self.VACsAndKeys[VAC_id]
                iv = Random.new().read(AES.block_size)
                print "IV: ", type(iv)
                cipher = AES.new(key, AES.MODE_CFB, iv)
                encrypted_challenge = cipher.encrypt(challenge)
                tt.endTimer()
                return ("registered", (self.getId(), [encrypted_challenge, iv]))
            # return VH_id, [encrypted challenge, iv]
            # if token is available
            else:
                token = self.getToken(VAC_id)
                if (token == -1):
                    return ("no token found")
                else:
                    # return Token [a tuple of VAC_id, encrypted message, signature, and symmetric key]
                    return ("token", token)
        else:
            return ("no token found")


tt = TopherTimer(True)


def VHandVACinteraction(VH, VAC):
    # 1. VAC gives VAC_id + Challenge Response
    broadcast_id, challenge = VAC.broadcastVACinfo()

    # 2. VH checks for VAC id
    VH_response = VH.processVAC(int(broadcast_id), challenge)
    print VH_response[0]
    if (VH_response[0] == "no token found"):
        print "Fail: VH doesn't know VAC."
        return -1

    if (VH_response[0] == "token"):
        token = VH_response[1]

        # return Token [a tuple of VAC_id, encrypted message, signature, and symmetric key]
        # token is a tuple of VAC_id, encrypted message, signature, and symmetric key
        # encrypted message contains:
        # message = str(VH_id) + "|" + str(lifetime_days)+ "|" + new_symmetric_key

        # get the token and decrypt
        decrypted_message = VAC.keys.decrypt(token[1])
        message = decrypted_message.split("|", 2)

        # print decrypted_message[2]
        hashed_message = SHA256.new(decrypted_message).digest()
        # print "Decrypted: ", decrypted_message

        pubKeyObj = RSA.importKey(VAC.getCAPublicKey())

        # 3. VAC adds token to its database

        # tt.startTimer("Generating Public Private Keys for VAC [Key length: " + str(KEY_LENGTH) + " bits]")

        tt.startTimer("Verifying token. ")
        pubKeyObj.publickey().verify(hashed_message, token[2])
        tt.endTimer()

        if pubKeyObj.publickey().verify(hashed_message, token[2]):
            print "Token is verified."
            VAC.registeredVHs.update({int(message[0]): [message[2], [message[1]]]})
            VH.registerVAC(VAC.getId())
            print VAC.registeredVHs
        else:
            print "Fail: Token is not signed properly"
            return -1
        # Question: Should we already allow entrance after adding the token?

    # VH_response is now registered! [Either from token or VH_response[0] == "registered"]
    # VH needs to encrypt the challenge [This is done in VH.processVAC]
    # VAC needs only to decrypt the challenge
    # VH_response = (return VH_id, [encrypted challenge, iv])

    if (VH_response[0] == "registered"):
        if (VAC.VACdecryptsMessage(VH.getId(), VH_response[1][1][0], VH_response[1][1][1], challenge)):
            print "Access Granted"
        else:
            print "Access Denied"
    else:
        # This goes to this block when:
        pass


def main():
    # Initialize CA, VACs, VHs
    CA = CentralAuthority()
    VAC = CA.generateVAC("UP Diliman Gate 1")
    VAC2 = CA.generateVAC("UP Diliman Gate 2")
    VH = CA.generateVH("TigerTopher Bus")
    CA.getVACIdbyName("UP Diliman Gate 1")

    VH.addToken(CA.grantToken(VAC.getId(), 1, 3600))

    # Scenario 1. VAC sees VH.
    print "VAC sees VH 1st time"
    VHandVACinteraction(VH, VAC)

    print "VAC sees VH 2nd time"
    VHandVACinteraction(VH, VAC)


# 	print "VAC sees unregistered VH"
# 	VHandVACinteraction(VH, VAC2)

main()
