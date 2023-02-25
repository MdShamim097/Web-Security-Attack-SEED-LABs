import AES_algo as aes
import RSA_algo as rsa

print("--------------------------------")
print("Wlcome To Hybrid Crypto System!")
print("--------------------------------")

#Genering RSA public and Privite keys
public_key,private_key=rsa.keyGeneration(64)

#Taking Key & Message
key = input("Enter key(128) bits:")
plain_text = input("Enter the message: ")
if len(plain_text)>16:
    plain_text=plain_text[0:16]

elif len(plain_text)<16:
    for i in range(len(plain_text),16):
        plain_text=plain_text+' '

round_key = aes.scheduleKey(key)        

#Encrypting the message with AES Encryption
cipher_text=aes.encrypt(plain_text,round_key)
print("AES cipher text: "+cipher_text)

#Encrypting the AES key with RSA Public key
encrypted_key=rsa.encrypt(key,public_key)
print("Encrypted Key:",encrypted_key)

#Sending.........

#Decrypting the AES key using RSA Private Key
decrypted_key=''.join(rsa.decrypt(encrypted_key,private_key))
print("AES Symmetric Key:",decrypted_key)

#Decrypting the message using the AES symmetric key
dec_round_key=aes.scheduleKey(decrypted_key)
decrypted_text=aes.decrypt(cipher_text,dec_round_key)
print("Decrypted message: "+decrypted_text)