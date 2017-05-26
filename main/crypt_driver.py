import crypt


print "================= START OF AES ============================"
# ================= START OF AES ============================
aes = crypt.AESDriver()

# Example 1 --- Encrypting and decrypting without specifying IV
# Generate key of with byte length 16. (16 bytes = 128 bits)
print "Printing generated key: "
key = aes.generate_key(16)
print key

# Encrypting
message = "Sample Message"
print "Plain text: ", message
ciphertext = aes.encrypt_data(message, key, 16)

print "Cipher text", ciphertext
print "Len of cipher text", len(ciphertext)

print "Decoded: ", aes.base64decode(ciphertext)
print "Len of decoded: ", len(aes.base64decode(ciphertext))

print "encode the decoded", aes.base64encode(aes.base64decode(ciphertext))
print "len of encode the decoded", len(aes.base64encode(aes.base64decode(ciphertext)))

# Decrypting
decrypted_data = aes.decrypt_data(ciphertext, key, 16)
print "Decrypted message: ", decrypted_data
print "Does it match? ", message == decrypted_data

# Example 2 --- Encrypting and decrypting while specifying IV\
key = aes.generate_key(16)
iv = aes.generate_key(16)

# Encrypting
message = "Sample Message"
print "Plain text: ", message
ciphertext = aes.encrypt_data(message, key, 16, iv)

# Decrypting
decrypted_data = aes.decrypt_data(ciphertext, key, 16, iv)
print "Decrypted message: ", decrypted_data
print "Does it match? ", message == decrypted_data

# ================= END OF AES ==============================
print "================= END OF AES =============================="

print ciphertext

decoded_key = aes.base64decode(ciphertext)
print decoded_key

int_encrypted_data = 0
for i in range(0, len(decoded_key)):
    print decoded_key[i] == chr(ord(decoded_key[i]))
    int_encrypted_data += (ord(decoded_key[i]) << ((len(decoded_key) - i - 1) * 8))

string_data = ""
int_data = int_encrypted_data
data_extractor = 2 ** 8 - 1
for i in range(0, 16):
    string_data += chr(data_extractor & int_data)
    int_data = int_data >> 8
string_data = string_data[::-1]

print string_data

encoded_key = aes.base64encode(string_data)
print encoded_key



exit()

print "================= START OF RSA ============================"
# ================= START OF RSA ============================
rsa = crypt.RSADriver()

# Generate keys
# the first parameter here specifies the length of the key (in bits)
key = rsa.generate_keys(1024)

# Retrieve private and public key
# If the 2nd parameter is not specified, the default representation of the key would be PEM (more readable)
print rsa.get_private_key(key)
print rsa.get_public_key(key)

# Example where output is DER representation
print rsa.get_private_key(key, "DER")
print rsa.get_public_key(key, "DER")

plain_text = "Sample Message"
# Encrypting message using public key
enc_message = rsa.encrypt_data(plain_text, key)
# This is encoded in ASCII thus the \x prefix. The value here is a tuple. You only need the first element of this tuple.
# For the length of encrypted message in bits, it must match the size of the key. Try to see if it does match.
print enc_message[0]
print "Length of encrypted message in bits: ", enc_message[0]

# Decrypting message using private key
decrypted_text = rsa.decrypt_data(enc_message, key)
# Let's see if it matches
print plain_text, decrypted_text
print "Does plain-text and decrypted message match? ", plain_text == decrypted_text

# Signing message
signature = rsa.sign_message(enc_message[0], key)
# Verifying signature
print rsa.verify_message(enc_message[0], signature, key)

# ================= END OF RSA ==============================

print "================= START OF AES ============================"
# ================= START OF AES ============================
aes = crypt.AESDriver()

# Example 1 --- Encrypting and decrypting without specifying IV
# Generate key of with byte length 16. (16 bytes = 128 bits)
print "Printing generated key: "
key = aes.generate_key(16)
print key

# Encrypting
message = "Sample Message"
print "Plain text: ", message
ciphertext = aes.encrypt_data(message, key, 16)

# Decrypting
decrypted_data = aes.decrypt_data(ciphertext, key, 16)
print "Decrypted message: ", decrypted_data
print "Does it match? ", message == decrypted_data

# Example 2 --- Encrypting and decrypting while specifying IV\
key = aes.generate_key(16)
iv = aes.generate_key(16)

# Encrypting
message = "Sample Message"
print "Plain text: ", message
ciphertext = aes.encrypt_data(message, key, 16, iv)

# Decrypting
decrypted_data = aes.decrypt_data(ciphertext, key, 16, iv)
print "Decrypted message: ", decrypted_data
print "Does it match? ", message == decrypted_data

print "================= END OF AES =============================="

print key

decoded_key = aes.base64decode(key)
print decoded_key

encoded_key = aes.base64encode(decoded_key)
print encoded_key
