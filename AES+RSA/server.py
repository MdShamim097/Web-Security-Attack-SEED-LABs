import socket    
import os
import AES_algo as aes
import RSA_algo as rsa

s = socket.socket()        
print ("Socket successfully created")
 
port = 12345               
s.bind(('', port))        
print ("socket binded to %s" %(port))
 
s.listen(5)    
print ("socket is listening")           

print("--------------------------------")
print("Wlcome To Hybrid Crypto System!")
print("--------------------------------")

#Create a folder
#newpath = r'C:\Dont Open This' 
#if not os.path.exists(newpath):
#    os.makedirs(newpath)

directory=os.getcwd() +'/Don\'t Open This'
if not os.path.exists(directory):
   os.makedirs(directory)
   print("directory \'" +directory+ "\' created")

while True:
 
  # Establish connection with client.
  c, addr = s.accept()    
  print ('Got connection from', addr )
  c.send('Thank you for connecting'.encode())
  print(c.recv(1024).decode())
  #----------------------------------------
  #Genering RSA public and Privite keys
  public_key,private_key=rsa.keyGeneration(64)
  
  file_path =os.getcwd() +'/Don\'t Open This' +'\key.txt'
  if os.path.exists(file_path):
     print('file already exists')
  else:
     # create a file
     with open(file_path, 'w') as fp:
         # uncomment if you want empty file
         fp.write(str(private_key))
         fp.close() 
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
  #-----------------------------------------
  c.send(cipher_text.encode())
  print(c.recv(1024).decode())
  c.send(str(encrypted_key).encode())
  print(c.recv(1024).decode())
  c.send(str(public_key).encode())
  print(c.recv(1024).decode())
  
  c.close()
  break