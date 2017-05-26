import crypt

#f = open("key.txt", "w")
print "================= START OF RSA ============================"
# ================= START OF RSA ============================
rsa = crypt.RSADriver()

# Generate keys
# the first parameter here specifies the length of the key (in bits)
rsa_key = rsa.generate_keys(1024)

# Retrieve private and public key
# If the 2nd parameter is not specified, the default representation of the key would be PEM (more readable)
string = str(rsa.get_public_key(rsa_key)) + "\n"
print rsa.get_private_key(rsa_key)
print rsa.get_public_key(rsa_key)

# Example where output is DER representation
print rsa.get_private_key(rsa_key, "DER")
print rsa.get_public_key(rsa_key, "DER")

plain_text = "Sample Message"
# Encrypting message using public key
enc_message = rsa.encrypt_data(plain_text, rsa_key)
# This is encoded in ASCII thus the \x prefix. The value here is a tuple. You only need the first element of this tuple.
# For the length of encrypted message in bits, it must match the size of the key. Try to see if it does match.
print enc_message[0]
print "Length of encrypted message in bits: ", enc_message[0]

# Decrypting message using private key
decrypted_text = rsa.decrypt_data(enc_message, rsa_key)
# Let's see if it matches
print plain_text, decrypted_text
print "Does plain-text and decrypted message match? ", plain_text == decrypted_text

# Signing message
signature = rsa.sign_message(enc_message[0], rsa_key)
print signature
# Verifying signature
print rsa.verify_message(enc_message[0], signature, rsa_key)

# ================= END OF RSA ==============================

print "================= START OF AES ============================"
# ================= START OF AES ============================
aes = crypt.AESDriver()

# Example 1 --- Encrypting and decrypting without specifying IV
# Generate key of with byte length 16. (16 bytes = 128 bits)
print "Printing generated key: "
#key = aes.generate_key(16)
key = "abcdefghijklmnop"
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
string += key

# Encrypting
message = "Sample Message"
print "Plain text: ", message
ciphertext = aes.encrypt_data(message, key, 16, iv)
print ciphertext

# Decrypting
decrypted_data = aes.decrypt_data(ciphertext, key, 16, iv)
print "Decrypted message: ", decrypted_data
print "Does it match? ", message == decrypted_data

print "================= END OF AES =============================="

message = "vh_no" + str(5892689) + "key" + key + "expire" + str("2017/7/14")
print "Token: ", message

signed_message = rsa.sign_message(message, rsa_key)
string += str(signed_message[0])
print "Signed_Token: ", signed_message

#f.write(string)
#f.close()
