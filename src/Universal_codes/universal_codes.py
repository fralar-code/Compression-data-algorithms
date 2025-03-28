import math
import matplotlib.pyplot as plt
import random
import numpy as np

def gamma_encoding(x):
    N = int(math.log2(x)) if x!=0 else 0
    binary= bin(x)[2:] #bin restitusice 0b in front of the conversion, we discard it
    zero= ''
    for i in range(0,N):
        zero += '0'
    return zero+binary

def gamma_decoding(code):
    decode = []
    i = 0
    while i < len(code):
        N = 0
        i = i
        while (i <len(code) and code[i] != '1'):
            i += 1
            N += 1
        decode.append(int(code[i: i+N+1], 2))
        i = (i+N+1)
    return decode


def delta_encoding(x):
    binary= bin(x)[3:] #we must exclude the first most significant bit
    N= int(math.log2(x)) if x!=0 else 0
    gamma = gamma_encoding(N+1)
    return gamma + binary

def delta_decoding(code):
    decode = []
    i = 0
    while i < len(code):
        L = 0
        i = i
        while (i <len(code) and code[i] != '1'):
            i += 1
            L += 1           
        
        N = int(code[i: i+L+1], 2) - 1
        tmp = "1" + code[i+L+1 : N+i+L+1]
        decode.append(int(tmp, 2))
        i = (N+i+L+1)
    return decode


def rice_encoding(x,k):
    q = int((x-1)/2**k)
    r = x-(2**k)*q-1
    unary = ('0'*q) + '1'
    binary = bin(r)[2:]
    zero = (k-len(binary))*'0'
    return unary + zero + binary

# We obtain the fibonacci sequence minor equal to N
def fibonacci_truncated(N, seq):
    if (seq[-1] > N ):
        return seq[:-1]
    else:
        seq.append(seq[-1] + seq[-2])
        return fibonacci_truncated(N, seq)


def fibonacci(n):
    if n == 0:
        return [0]
    elif n == 1:
        return [0,1]
    
    # recursive call
    seq = fibonacci(n - 1)
    # We concatenate in the sequence the last two words of lower size
    seq.append(seq[-1] + seq[-2])
    return seq


def fibonacci_encoding(N):
    seq = fibonacci_truncated(N, [0,1])
    # We construct the encoding of the number N by initializing the codeword string to 0.
    # To then insert a bit equal to 1 in the only positions that refer to the fibonacci numbers being considered for the sum
    # An integer- that is given by the sum of numbers in the fibonacci sequence- 
    # needing 'i' bits for its representation where i coincides with the i-th largest fibonacci taken into consideration.
    # To the codeword we append the symbol '1' indicating the termination of the encoding
    codeword = '0'*(len(seq)-2)+'1'
    codelist = list(codeword)
    for i in range(len(seq)-1,1,-1):
        r = N - seq[i]
        if r > 0:
            N = r
            codelist[i-2] = '1'
        if r == 0:
            codelist[i-2] = '1'
            break
    
    return ''.join(codelist)
        
  
def fibonacci_decoding(code): 
    decode = []
    i = 0
    while j < len(code):
        j = i
        # we increase 'i' until we reach two 1's
        while code[j] != '1' or code[j+1] !='1' :
            j += 1
        codeword = code[i:j+1]
        s = 0
        for k in range(len(codeword)):
            if codeword[k] == '1':
                s += fibonacci(k+2)[-1]
        decode.append(s)
        i = j+2
    return decode


def test():
    binary_len = []
    gamma_len = []
    delta_len = []
    fibonacci_len = []
    rice5_len = []
    rice7_len = []
    
    # We save the lengths of the various codes on the numbers 1 to 1000
    for i in range(1, 1001):
        binary_len.append(len(bin(i)[2:]))
        gamma_len.append(len(gamma_encoding(i)))
        delta_len.append(len(delta_encoding(i)))
        fibonacci_len.append(len(fibonacci_encoding(i)))
        rice5_len.append(len(rice_encoding(i,5)))
        rice7_len.append(len(rice_encoding(i,7)))

    # We compare in the plot the bits used for the representation 
    x = [i for i in range(1, 1001)]
    plt.figure(figsize=(10, 6))
    plt.plot(x, binary_len, label='binary')
    plt.plot(x, gamma_len, label='gamma')
    plt.plot(x, delta_len, label='delta')
    plt.plot(x, fibonacci_len, label='fibonacci')
    plt.plot(x, rice5_len, label='rice_5')
    plt.plot(x, rice7_len, label='rice_7')
    
    plt.title('Plot number of bits of numbers between 1 and 1000')
    plt.xlabel('integers')
    plt.ylabel('number of bits')
    plt.grid(True)
    plt.legend()
    plt.show()


def test2():
    binary_bits = []
    gamma_bits = []
    delta_bits = []
    fibonacci_bits = []
    rice5_bits = []
    rice7_bits = []
    
    # We save the lengths of the various codes on the numbers from 1 to 100000 with step 1010
    for i in range(1, 100001, 1010):
        binary_bits.append(len(bin(i)[2:]))
        gamma_bits.append(len(gamma_encoding(i)))
        delta_bits.append(len(delta_encoding(i)))
        fibonacci_bits.append(len(fibonacci_encoding(i)))
        rice5_bits.append(len(rice_encoding(i,5)))
        rice7_bits.append(len(rice_encoding(i,7)))

    x = [i for i in range(1, 100001, 1010)]
    plt.figure(figsize=(10, 6))
    plt.plot(x, binary_bits, label='binary')
    plt.plot(x, gamma_bits, label='gamma')
    plt.plot(x, delta_bits, label='delta')
    plt.plot(x, fibonacci_bits, label='fibonacci')
    plt.plot(x, rice5_bits, label='rice_5')
    plt.plot(x, rice7_bits, label='rice_7')
    
    plt.ylim(0, 50)
    plt.title('Plot number of bits of 100 numbers between 1 and 100000')
    plt.xlabel('integers')
    plt.ylabel('number of bits')
    plt.grid(True)
    plt.legend()
    plt.show()


def test3():
    binary_bits = []
    gamma_bits = []
    delta_bits = []
    fibonacci_bits = []
    rice5_bits = []
    rice7_bits = []
    
    random_numbers = []
    # We save the lengths of the various codes on the random numbers between 1 and 1000
    for i in range(100):
        random_numbers.append(random.randint(1, 1000))
    random_numbers.sort()

    for i in range(100):
        binary_bits.append(len(bin(random_numbers[i])[2:]))
        gamma_bits.append(len(gamma_encoding(random_numbers[i])))
        delta_bits.append(len(delta_encoding(random_numbers[i])))
        fibonacci_bits.append(len(fibonacci_encoding(random_numbers[i])))
        rice5_bits.append(len(rice_encoding(random_numbers[i],5)))
        rice7_bits.append(len(rice_encoding(random_numbers[i],7)))

    x = random_numbers
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, binary_bits, label='binary')
    plt.plot(x, gamma_bits, label='gamma')
    plt.plot(x, delta_bits, label='delta')
    plt.plot(x, fibonacci_bits, label='fibonacci')
    plt.plot(x, rice5_bits, label='rice_5')
    plt.plot(x, rice7_bits, label='rice_7')
    plt.title('Plot number of bits of 100 numbers between 1 and 1000')
    plt.xlabel('integers')
    plt.ylabel('number of bits')
    plt.grid(True)
    plt.legend()
    plt.show()


def test4():

    num_values = 1000
    # We generate num_values random numbers
    random_values = np.random.rand(num_values)
    # We normalize these values so that their sum is 1
    probabilities = random_values / sum(random_values)

    values = [i for i in range(1,1001)]
    # We generate 1000 random numbers with the specified probabilities
    random_numbers = np.random.choice(values, size=num_values, p=probabilities)

    binary_bits = []
    gamma_bits = []
    delta_bits = []
    fibonacci_bits = []
    rice5_bits = []
    rice7_bits = []

    random_numbers.sort()
    for i in range(1000):
        binary_bits.append(len(bin(random_numbers[i])[2:]))
        gamma_bits.append(len(gamma_encoding(random_numbers[i])))
        delta_bits.append(len(delta_encoding(random_numbers[i])))
        fibonacci_bits.append(len(fibonacci_encoding(random_numbers[i])))
        rice5_bits.append(len(rice_encoding(random_numbers[i],5)))
        rice7_bits.append(len(rice_encoding(random_numbers[i],7)))
 
    x = random_numbers
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, binary_bits, label='binary')
    plt.plot(x, gamma_bits, label='gamma')
    plt.plot(x, delta_bits, label='delta')
    plt.plot(x, fibonacci_bits, label='fibonacci')
    plt.plot(x, rice5_bits, label='rice_5')
    plt.plot(x, rice7_bits, label='rice_7')
    plt.title('Plot number of bits of 1000 numbers generated by a given distribution')
    plt.xlabel('integers')
    plt.ylabel('number of bits')
    plt.grid(True)
    plt.legend()
    plt.show()