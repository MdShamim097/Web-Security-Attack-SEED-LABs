import time
import random
from BitVector import *

def generatePrime(key_size):
    while(1):
        x=random.randint(2**(key_size-1),2**key_size)
        bv=BitVector(intVal=x)
        check=bv.test_for_primality()
        if check!=0:
            return x
        

def keyGeneration(key_size):
    while(1):
      p=generatePrime(key_size)
      q=generatePrime(key_size)
      if p!=q:
          break 

    n=p*q
    #print("n=",n) 
    phi_n=(p-1)*(q-1)
    
    g=0
    while g!=1:
        e=random.randint(1,phi_n)
        bv1=BitVector(intVal=e)     
        bv2=BitVector(intVal=phi_n)  
        g=bv1.gcd(bv2)
        g=int(g)
    #print("g=",g,",","e=",e,",","phi_n=",phi_n) 

    d = pow(e, -1, phi_n)
    d=d % phi_n
    if(d < 0):
        d += phi_n
    #print("d=",d)  

    return ((e,n),(d,n))

def encrypt(plain_text,public_key):
    e,n=public_key
    cipher_text=[pow(ord(char),e,n) for char in plain_text]
    return cipher_text

def decrypt(cipher_text,private_key):
    d,n=private_key
    text=[chr(pow(char,d,n)) for char in cipher_text]
    return "".join(text)

#Main
def main():
    for i in range(4):
        k=input('Enter k:')
        print("---------k="+k+"--------------")
        keygeneration_time=time.time()
        public_key,private_key=keyGeneration(int(k))
        keygeneration_time=time.time()-keygeneration_time
        print("Public(e,n): ",public_key)
        print("Private(d,n): ",private_key)

        plain_text=input('Enter text:')
        encryption_time=time.time()
        cipher_text=encrypt(plain_text,public_key)
        encryption_time=time.time()-encryption_time
        print("Cipher text:",cipher_text)

        decryption_time=time.time()
        decipher_text=decrypt(cipher_text,private_key)
        decryption_time=time.time()-decryption_time
        print("decrypted =",decipher_text)

        print("Key Generation Time:",keygeneration_time)
        print("Encryption Time:",encryption_time)
        print("Decryption Time:",decryption_time)

if __name__=='__main__':
    main()