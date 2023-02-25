import socket     
import os    
import AES_algo as aes
import RSA_algo as rsa

s = socket.socket()        
port = 12345               
# connect to the server on local computer
s.connect(('127.0.0.1', port))
 
print (s.recv(1024).decode())
s.send('Welcome'.encode())
cipher_text=s.recv(1024).decode()
print("Cipher Text:"+cipher_text)
s.send('Ok'.encode())
encrypted_key=str(s.recv(1024*16).decode())
print("Encrypted Key:"+encrypted_key)
s.send('Ok'.encode())
public_key=str(s.recv(1024*2).decode())
print("Public Key:"+public_key)
s.send('Ok'.encode())
#------------------------------------------
my_file = os.path.join(os.getcwd() +'/Don\'t Open This' +'\key.txt')
with open(my_file) as f:
    # your code to work on the file goes here
    for line in f:
        private_key=line
        print("Reading key from the file...")
        print("Private Key:"+private_key)
    f.close()    
#------------------------------------------
encrypted_key=encrypted_key.replace(" ","")
encrypted_key=encrypted_key.replace("[","")
encrypted_key=encrypted_key.replace("]","")

encrypted_key=encrypted_key.split(',')
encrypted_key_list=[]
for i in range(len(encrypted_key)):
    encrypted_key_list.append(int(encrypted_key[i]))

#------------------------------------------
public_key=public_key.replace(" ","")
public_key=public_key.replace("(","")
public_key=public_key.replace(")","")

public_key=public_key.split(',')
public_key_tuple=()
for i in range(len(public_key)):
    public_key_tuple+=(int(public_key[i]),)
#------------------------------------------
private_key=private_key.replace(" ","")
private_key=private_key.replace("(","")
private_key=private_key.replace(")","")

private_key=private_key.split(',')
private_key_tuple=()
for i in range(len(private_key)):
    private_key_tuple+=(int(private_key[i]),)
#-----------------------------------------
decrypted_key=''.join(rsa.decrypt(encrypted_key_list,private_key_tuple))
print("AES Symmetric Key:",decrypted_key)

dec_round_key=aes.scheduleKey(decrypted_key)
decrypted_text=aes.decrypt(cipher_text,dec_round_key)
print("Decrypted message: "+decrypted_text)

s.close()      