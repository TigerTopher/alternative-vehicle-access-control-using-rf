from Database import *
from random import *

class Hasher():
    def __init__(self):
        self.database = Database("central_authority", "avracardabra", "localhost", "password")
        self.max_bits = 24
        self.modulo = 2 ** 24 - 1

    def hash_function(self, message):
        hash = self.database.select_query("hash", "hashed_messages", "message = '" + message + "'")
        if hash != []:
            return hash[0][0]
        hash_1 = int(random() * 100000) % self.modulo
        for i in message:
            index = (hash_1 ^ ord(i)) % self.modulo
            hash_1 = self.database.select_query("hash", "hashes", "id = " + str(index))[0][0]

        # Linear Probing with Chaining
        other_messages = self.database.select_query("message", "hashed_messages", "hash = " + str(hash_1))
        if other_messages != []:
            for i in range(index + 1, self.modulo + 1):
                hash_2 = self.database.select_query("hash", "hashes", "id = " + str(i))
                other_messages = self.database.select_query("message", "hashed_messages", "hash = " + str(hash_2))
                if other_messages == []:
                    self.database.insert_query("hash, message", str(hash_2) + "," + message, "hashed_messages")
                    return hash_2
            for i in range(0, index):
                hash_2 = self.database.select_query("hash", "hashes", "id = " + str(i))
                other_messages = self.database.select_query("message", "hashed_messages", "hash = " + str(hash_2))
                if other_messages == []:
                    self.database.insert_query("hash, message", str(hash_2) + "," + message, "hashed_messages")
                    return hash_2

        self.database.insert_query("hash, message", str(hash_1) + "," + message, "hashed_messages")
        return hash_2

    def end_session(self):
        self.database.disconnect()
