import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from BWT.bwt import BWT_rotations, count_runs

def LZ77_encoding(text, window_size):
    i = 0
    output = []
    # The index i iterates over the entire input text
    while i < len(text):
        offset = 0  # Difference between indices
        best_length = 0  # Length of the best matching prefix
        
        # Define the search buffer indices
        start_index = max(0, i - window_size)
        end_index = i
        
        # j iterates over the search buffer, while i scans the lookahead buffer
        for j in range(start_index, end_index):
            current_length = 0
            # While within the lookahead buffer and characters match, increase prefix length
            while i + current_length < len(text) and text[j + current_length] == text[i + current_length]:
                current_length += 1
            
            # Update best prefix found, prioritizing closer matches when lengths are equal
            if current_length >= best_length:
                offset = i - j
                best_length = current_length
        
        if best_length > 0:
            # Store the triplet: (offset, length, next character after prefix)
            output.append((offset, best_length, text[i + best_length]))
            i += best_length + 1  # Move past the prefix and the next character
        else:
            # If no prefix is found, store the current character as a single entry
            output.append((0, 0, text[i]))
            i += 1
    
    return output

def LZSS_encoding(text, window_size):
    i = 0
    output = []
    # The index i iterates over the entire input text
    while i < len(text):
        offset = 0
        best_length = 0
        
        # Define the search buffer indices
        start_index = max(0, i - window_size)
        end_index = i
        
        for j in range(start_index, end_index):
            current_length = 0
            # While within the lookahead buffer and characters match, increase prefix length
            while i + current_length < len(text) and text[j + current_length] == text[i + current_length]:
                current_length += 1
            
            # Update best prefix found
            if current_length >= best_length:
                offset = i - j
                best_length = current_length
        
        if best_length > 0:
            # Store the pair: (offset, length)
            output.append((offset, best_length))
            i += best_length  # Move past the prefix
        else:
            # If no prefix is found, store the current character
            output.append((0, text[i]))
            i += 1
    
    return output

import random

def random_string(length=10, alphabet='abcdefghijklmnopqrstuvwxyz'):
    """Generate a random string of given length from the specified alphabet."""
    return ''.join(random.choice(alphabet) for _ in range(length))

import math
import matplotlib.pyplot as plt

def test(n=8, iterations=66):
    """Test whether the theoretical relations between LZ77 encoding and BWT runs hold:
    r = O(z (log n)**2)
    z = O(r log n)
    """
    z = []  # Store the number of LZ77 triplets
    r = []  # Store the number of BWT runs
    
    for _ in range(iterations):
        string = random_string(length=n)
        z.append(len(LZ77_encoding(string + '$', len(string) + 1)))
        r.append(count_runs(BWT_rotations(string)[0]))
    
    # Theoretical validation
    plt.figure(figsize=(10, 6))
    
    plt.subplot(1, 2, 1)
    x = list(range(iterations))
    upper_bound_r = [val * (math.log(n) ** 2) for val in z]
    plt.plot(x, upper_bound_r, linestyle='-', color='b', label='upper_bound_r')
    plt.plot(x, r, linestyle='-', color='r', label='r')
    plt.title('Plot of upper bound for r')
    plt.xlabel('z')
    plt.ylabel('r')
    plt.grid(True)
    plt.legend()
    
    plt.subplot(1, 2, 2)
    upper_bound_z = [val * math.log(n) for val in r]
    plt.plot(x, upper_bound_z, linestyle='-', color='b', label='upper_bound_z')
    plt.plot(x, z, linestyle='-', color='r', label='z')
    plt.title('Plot of upper bound for z')
    plt.xlabel('r')
    plt.ylabel('z')
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    text = 'aacaacabcabaaac$'
    # text = 'aabbabab'
    window_size = 6
    encode_1 = LZ77_encoding(text, window_size)
    print('LZ77 encoding:', encode_1)
    encode_2 = LZSS_encoding(text, window_size)
    print('LZSS encoding:', encode_2)

if __name__ == '__main__':
    main()
