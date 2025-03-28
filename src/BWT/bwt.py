import matplotlib.pyplot as plt

def BWT_rotations(text):
    rotations = []
    length = len(text)
    # Compute all rotations of the string
    for i in range(length):
        rotation = text[i:] + text[:i]
        rotations.append(rotation)
    # Sort rotations in lexicographic order
    rotations.sort()
    I = 0
    L = ''
    # Extract the last column and the index of the original text
    for i in range(length):
        L += (rotations[i][-1])
        if rotations[i] == text:
            I = i
    return L, I


def define_type(text):
    # Types array stores the type (L, S, *) for each character in the text
    types = [0] * len(text)
    # Initialize the dollar sign type as S*
    types[-1] = '*'
    # Track initial indices of LMS factors
    lms_indices = []
    lms_indices.append(len(text) - 1)
    
    for i in range(len(text) - 2, -1, -1):
        if (text[i] < text[i+1]) or ((text[i] == text[i+1]) and ((types[i+1] == 'S') or (types[i+1] == '*'))):
            if (i > 0 and (text[i-1] > text[i])):
                types[i] = '*'
                lms_indices.insert(0, i)
            else:
                types[i] = 'S'
        elif (text[i] > text[i+1]) or ((text[i] == text[i+1]) and (types[i+1] == 'L')):
            types[i] = 'L'
    
    # Assign both start and end indices for LMS factors
    for i in range(len(lms_indices) - 1):
        lms_indices[i] = [lms_indices[i], lms_indices[i+1]]
    lms_indices[-1] = [lms_indices[-1], lms_indices[-1]]
    
    return types, lms_indices
    
# Identify bucket ranges for each character in the alphabet of the text
def bucket_range(string):
    # Sort characters of the string
    sorted_string = sorted(string)
    
    # Initialize a dictionary to store index ranges
    range_indices = {}
    
    # Track the current index and previous character
    current_index = 0
    previous_char = None
    
    for i, char in enumerate(sorted_string):
        if char != previous_char:
            if previous_char is not None:
                range_indices[previous_char] = [current_index, i - 1, 0]
            current_index = i
            previous_char = char
    
    # Add range for the last character
    if previous_char is not None:
        range_indices[previous_char] = [current_index, len(sorted_string) - 1, 0]
    
    return range_indices

# Perform induced sorting on the text
def induce_sorting(text, lms_indices, types):
    # {'character': (start, end, num_elements_in_bucket)}
    buckets = bucket_range(text)
    # Store LMS suffixes in SA
    SA = [None] * len(text)
    # Insert LMS elements at the end of their corresponding buckets in input order
    lms_indices.reverse()
    for start, _ in lms_indices:
        _, end, num_elements = buckets[text[start]]
        SA[end - num_elements] = start
        buckets[text[start]][2] += 1
    
    buckets = bucket_range(text)
    # Place L-type suffixes at the beginning of their buckets
    for i in range(len(SA) - 1):
        if SA[i] is not None:
            j = SA[i] - 1
            if types[j] == 'L':
                start_range = buckets[text[j]][0]
                num_elements = buckets[text[j]][2]
                SA[start_range + num_elements] = j
                buckets[text[j]][2] += 1

    # Place S-type suffixes at the end of their buckets
    for i in range(len(SA) - 1, 1, -1):
        if SA[i] is not None:
            j = SA[i] - 1
            if j >= 0 and (types[j] == 'S' or types[j] == '*'):
                end_range = buckets[text[j]][1]
                SA[end_range] = j
                buckets[text[j]][1] -= 1
    return SA

# Check if two LMS factors are equal
def are_equal(a, b, text, types):
    (start_a, end_a, _) = a
    (start_b, end_b, _) = b
    # Two LMS factors are equal if they reference the same string and have the same type for each character
    if text[start_a: end_a+1] == text[start_b: end_b+1]:
        if types[start_a: end_a+1] == types[start_b: end_b+1]:
            return True
    return False

# Reduce LMS factors
def reduce_lms(text, types, lms_indices, SA):
    # Extract LMS factors based on suffix array order, following the induced ordering 
    lms_sorted = []
    for i in range(len(SA)):
        for start, end in lms_indices:
            if SA[i] == start:
                lms_sorted.append([start, end, None])
    
    equal_lms = False
    # We assign a name to each lms following the induced ordering 
    # The names are characters that follow ascii encoding starting with character 0.
    c = ord('0')
    #the array lms_sorted contains tuples (index_start_lms, index_end_lms, encode_lms)
    lms_sorted[0][2] = chr(c)
    for i in range(1, len(lms_sorted)):
        # equal lms factor are encoded with the same character
        if are_equal(lms_sorted[i], lms_sorted[i-1], text, types):
            equal_lms = True
            lms_sorted[i][2] = chr(c)
        else:
            c += 1
            lms_sorted[i][2] = chr(c)
    
    # ---- base case of the recursione -----
    if not equal_lms:
        return SA
    else:
        # We sort by initial index 
        # so we take them in the order in which they appear in the text.
        lms_sorted.sort(key=lambda lms: lms[0])
        # We concatenate the encoding of the lms in the order they appear in the initial text obtaining the reduced string
        reduced_string = ''.join([code for _, _, code in lms_sorted])

        # ---- PASSO RICORSIVO ----
        #We get the suffix array of the lower size problem
        SA_i = SA_IS(reduced_string)
        # We follow the sorting returned by the suffix array of the recursive call.
        # by going to sort the lms 
        tmp_lms = [lms_sorted[i][:2] for i in SA_i]
        SA = induce_sorting(text, tmp_lms, types)
        return SA
    
def SA_IS(text):    
    types, lms_indices = define_type(text)
    SA = induce_sorting(text, lms_indices, types)
    return reduce_lms(text, types, lms_indices, SA)
    
# Compute BWT using suffixes
def BWT_suffixes(text):
    text += '$'
    SA = SA_IS(text)
    output = ''
    for i in range(len(SA)):
        if SA[i] > 0:
            output += text[SA[i]-1]
        else:
            Index = i
            output += '$'
    return output, Index

def count_runs(text):
    if len(text) < 1:
        return 0

    run_count = 1  
    # Assign the first element
    run_character = text[0]  

    for character in text[1:]:
        # If we find a character different from the current run, increment the counter
        if character != run_character:
            run_count += 1  
            # Update with the new character
            run_character = character 
    
    return run_count


import random
import string

def random_string(length):
    # Consider only letters
    characters = string.ascii_letters 
    
    # Generate a list of random characters
    random_characters = [random.choice(characters) for _ in range(length)]

    # Convert the list of characters into a string
    random_str = ''
    for character in random_characters:
        random_str += character
    
    return random_str


def test_run(num_strings=100000, string_length=4):
    print('Optimal strings of length', string_length, ':')
    for i in range(num_strings):
        # Generate a random string
        string = random_string(string_length)
        bwt_output, _ = BWT_rotations(string)
        # Calculate the number of runs in the BWT output
        p_bwt = count_runs(bwt_output)
        # Ideally, the BWT output is easily compressible when it contains only one run.
        # We define a qualitatively good string for compression when the ratio
        # between length and the number of runs in the string is greater than 0.5
        ratio = p_bwt / string_length 
        if ratio <= 0.5:
             print(bwt_output, 'ratio', ratio)
    

def fibonacci(size):
    if size == 0:
        return ['b']
    elif size == 1:
        return ['b', 'a']
    
    # Recursive call
    seq = fibonacci(size - 1)
    # Concatenate the last two words of smaller size in the sequence
    seq.append(seq[-1] + seq[-2])
    return seq


def test_fibonacci():
    sequences = fibonacci(18)
    print('Fibonacci sequences:', sequences)

    run_bwt_rot = []
    run_bwt_suff = []

    fibonacci_even_indices = sequences[::2]
    # Take Fibonacci words of even order
    for seq in fibonacci_even_indices:
        # Remove the last character from the Fibonacci words
        seq = seq[:-1]
        output_rot, _ = BWT_rotations(seq)
        output_suff, _ = BWT_suffixes(seq)
        run_bwt_rot.append(count_runs(output_rot))
        run_bwt_suff.append(count_runs(output_suff))
    
    plt.figure(figsize=(8, 6))
    x = [i for i in range(0, len(fibonacci_even_indices))]
    plt.plot(x, run_bwt_rot, label='run_rot')
    plt.plot(x, run_bwt_suff, label='run_suff')
    plt.title('Run Comparison')
    plt.xlabel('fibonacci_even_indices')
    plt.ylabel('number of runs')
    plt.grid(True)
    plt.legend()
    plt.show()
    # print('Number of runs BWT rotations: ', run_bwt_rot)
    # print('Number of runs BWT suffixes: ', run_bwt_suff)

def main():
    text = 'GTCCCGATGTCATGTCAGGA'
    # text = 'cbbcacbbcadacbadacb'
    L, I = BWT_rotations(text)
    print('BWT output with rotations:', L, '\tI:', I)
    output_sa, index = BWT_suffixes(text)
    print('BWT output with suffixes:', output_sa, '\tI:', index)


if __name__ == '__main__':
    main()
