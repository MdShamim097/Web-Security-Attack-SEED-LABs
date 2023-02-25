import copy
import time
import bitvector as bv
from BitVector import *

int_mixer=[[0]*4 for i in range(4)]
int_invmixer=[[0]*4 for i in range(4)]
for r in range(4):
    for c in range(4):
        int_mixer[r][c]=int(bv.Mixer[r][c].get_bitvector_in_hex().upper(),16)
for r in range(4):
    for c in range(4):
        int_invmixer[r][c]=int(bv.InvMixer[r][c].get_bitvector_in_hex().upper(),16)

def hexadecimal1(a):
    a=ord(a)
    z=str(hex(a)).split('x')
    if len(z[1]) != 2 :
        z[1] = '0'+z[1]
    return z[1].upper()

def XOR(a, b):
    z = []
    for i in range(4):
        temp = str(hex(int(a[i],16)^int(b[i],16)).split('x')[-1]).upper()
        if len(temp) != 2 :
            temp = '0'+temp
        z.append(temp)
    return z
    
def scheduleKey(KEY):
    key_list = [hexadecimal1(i) for i in list(KEY)]
    round_key = []
    round_key.append(key_list)
    RC = ['01', '02', '04', '08', '10', '20', '40', '80', '1B', '36']
    rc = [int(i,16) for i in RC]
    for i in range(10):
        left_w3 = [round_key[-1][13], round_key[-1][14], round_key[-1][15], round_key[-1][12]]
        subtituteByte = []

        for j in range(4):
            b = BitVector(hexstring = left_w3[j])
            int_val = b.intValue()
            s = bv.Sbox[int_val]
            s = BitVector(intVal=s, size=8)
            subtituteByte.append(s.get_bitvector_in_hex().upper())

        subtituteByte[0] = str(hex(int(subtituteByte[0],16)^int(rc[i]))).split('x')[-1].upper()

        if len(subtituteByte[0]) != 2:
            subtituteByte[0]='0'+subtituteByte[0]

        #print(subtituteByte)
        w4 = XOR(round_key[-1][0:4],subtituteByte)
        w5 = XOR(round_key[-1][4:8],w4)
        w6 = XOR(round_key[-1][8:12],w5)
        w7 = XOR(round_key[-1][12:16],w6)
        w_final = w4 + w5 + w6 + w7
        round_key.append(w_final)
    return round_key

def XOR1(a, b):
    z = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    for i in range(4):
        for j in range(4):
            temp = str(hex(int(a[i][j],16)^int(b[i][j],16)).split('x')[-1]).upper()
            if(len(temp) != 2):
                temp = '0'+temp

            z[i][j] = temp
    return z

def leftShift(a):
    m = str(hex(int(a, 16)<<1)).split('x')[-1].upper()
    n = ''
    if len(m)==3:
        m = str(hex(int(m,16)^283)).split('x')[-1].upper()
    if len(m) != 2:
        m= '0'+m
    n=m[-2]+m[-1]
    return n

def hexadecimalXOR(a, b):
    z = str(hex(int(a, 16)^int(b, 16))).split('x')[-1].upper()
    if(len(z) != 2):
        z = '0'+z
    return z

def leftShiftXOR(a):
    m = leftShift(a)
    n = hexadecimalXOR(m ,a)
    return n

def mixColumns(mixer_mat,st_mat):
    z = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    for i in range(4):
        for j in range(4):
            m = '00'
            for k in range(4):
                if(mixer_mat[i][k] == 2):
                    a=leftShift(st_mat[k][j])
                    m = hexadecimalXOR(m,a)
                
                elif(mixer_mat[i][k] == 1):
                    m = hexadecimalXOR(m, st_mat[k][j])
                
                elif(mixer_mat[i][k] == 3):
                    m = hexadecimalXOR(m, leftShiftXOR(st_mat[k][j]))

                elif(mixer_mat[i][k] == 9):
                    a = leftShift(leftShift(leftShift(st_mat[k][j])))
                    b = hexadecimalXOR(a,st_mat[k][j])
                    m = hexadecimalXOR(m, b)

                elif(mixer_mat[i][k] == 11):
                    a = leftShift(leftShift(leftShift(st_mat[k][j])))
                    b = leftShift(st_mat[k][j])
                    c = hexadecimalXOR(a, b)
                    d = hexadecimalXOR(c, st_mat[k][j])
                    m = hexadecimalXOR(m, d)

                elif(mixer_mat[i][k] ==13):
                    a = leftShift(leftShift(leftShift(st_mat[k][j])))
                    b = leftShift(leftShift(st_mat[k][j]))
                    c = hexadecimalXOR(a, b)
                    d = hexadecimalXOR(c, st_mat[k][j])
                    m = hexadecimalXOR(m, d)

                elif(mixer_mat[i][k] == 14):
                    a = leftShift(leftShift(leftShift(st_mat[k][j])))
                    b = leftShift(leftShift(st_mat[k][j]))
                    c = leftShift(st_mat[k][j])
                    d = hexadecimalXOR(a, b)
                    e = hexadecimalXOR(c, d)
                    m = hexadecimalXOR(m, e)  

            z[i][j] = m
    return z

def encrypt(plain_text,round_key):
    msg_list = [hexadecimal1(i) for i in list(plain_text)]
    state_matrix = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    key_matrix = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]

    i=0
    for r in range(4):
        for c in range(4):
            state_matrix[c][r]=msg_list[i]
            key_matrix[c][r]=round_key[0][i]
            i=i+1

    state_matrix=XOR1(state_matrix,key_matrix)

    for round in range(10):
        # Substitute Bytes
        for r in range(4):
            for c in range(4):
                b = BitVector(hexstring = state_matrix[r][c])
                int_val = b.intValue()
                s = bv.Sbox[int_val]
                s = BitVector(intVal=s, size=8)
                state_matrix[r][c]=s.get_bitvector_in_hex().upper()
        
        #Shift Rows
        temp_matrix=copy.deepcopy(state_matrix)  
        for r in range(4):
            for c in range(4):
                state_matrix[r][c]=temp_matrix[r][(r+c)%4]

        #Mix Columns
        if round!=9:
            state_matrix = mixColumns(int_mixer, state_matrix)

        #Add Round Key
        z=[['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
        i=0
        for r in range(4):
            for c in range(4):
                z[c][r]=round_key[round+1][i]
                i=i+1
        
        #print(z)        
        state_matrix = XOR1(state_matrix, z)     

    cipherText = ''
    for i in range(4):
        for j in range(4):
            cipherText += state_matrix[j][i]

    return cipherText                

def decrypt(cipherText, round_key):
    state_matrix = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    for i in range(4):
        for j in range(4):
            state_matrix[j][i] = cipherText[2*j+8*i:2*j+8*i+2]
  
    #Add Round Key
    z=[['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    round = 9
    i=0
    for r in range(4):
        for c in range(4):
            z[c][r]=round_key[round+1][i]
            i=i+1
           
    state_matrix = XOR1(state_matrix, z)  

    for i in range(8, -2, -1):

        #Inverse Shift Row
        temp = copy.deepcopy(state_matrix)

        for j in range(4):
            for k in range(4):
                state_matrix[j][k] = temp[j][(4+k-j)%4]

        #Inverse Substitution Bytes
        for r in range(4):
            for c in range(4):
                b = BitVector(hexstring = state_matrix[r][c])
                int_val = b.intValue()
                s = bv.InvSbox[int_val]
                s = BitVector(intVal=s, size=8)
                state_matrix[r][c]=s.get_bitvector_in_hex().upper()

        #Add Round Key
        z=[['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
        j=0
        for r in range(4):
            for c in range(4):
                z[c][r]=round_key[i+1][j]
                j=j+1
        
        state_matrix = XOR1(state_matrix, z)  

        #Inverse Mix Column
        if(i != -1):
            state_matrix = mixColumns(int_invmixer, state_matrix)
        
    decipher_list = []

    for i in range(4):
        for j in range(4):
            decipher_list.append(state_matrix[j][i])

    temp_text=[ chr(int(i,16)) for i in decipher_list]
    decipher_text= ''.join(temp_text)
    return decipher_text

#Main
def main():
    plain_text = input('Plain Text:')
    if len(plain_text)>16:
       plain_text=plain_text[0:16]

    elif len(plain_text)<16:
       for i in range(len(plain_text),16):
          plain_text=plain_text+' '

    KEY = input('Key(128 bits):')
    keyscheduling_time=time.time()
    round_key = scheduleKey(KEY)
    keyscheduling_time=time.time()-keyscheduling_time

    encryption_time=time.time()
    cipher_text = encrypt(plain_text, round_key)
    encryption_time=time.time()-encryption_time
    print("Cipher Text:"+cipher_text)

    decryption_time=time.time()
    decipher_text = decrypt(cipher_text, round_key)
    decryption_time=time.time()-decryption_time
    print("Decipherded Text:"+decipher_text)

    print("Key Scheduling Time:",keyscheduling_time)
    print("Encryption Time:",encryption_time)
    print("Decryption Time:",decryption_time)

if __name__=='__main__':
    main()