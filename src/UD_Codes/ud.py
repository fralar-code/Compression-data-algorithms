
#checks whether the codeword string is prefixed by any words in the Set set and returns all corresponding suffixes
def prefixes(codeword, Set):
    suffixes = []
    for el in Set:
        if el.startswith(codeword):
            suffixes.append(el[len(codeword):])
    return suffixes

def non_ud_codeword(Sets):
    # Position of the last set in Sets
    j = len(Sets) - 1
    # We proceed backwards to construct a non-UD message,
    # the string message can be encoded in two different ways.
    # Initialize the message by selecting the intersection between the last and first sets.
    # We then prepend the remaining parts of the message iteratively.
    message = Sets[0].intersection(Sets[j]).pop()
    # Among Si and S0, we consider common prefixes.
    # If the remaining suffix matches suffix_goal,
    # it indicates where we came from during construction to obtain that specific suffix.
    suffix_goal = message
    # Consider Si in reverse order, excluding the final set j.
    for i in range(j - 1, -1, -1):
        found = False
        # Look for prefixes of Si in S0
        for codeword2 in Sets[i]:  
            if found:
                break
            for codeword1 in Sets[0]:
                if found:
                    break
                # Check if they share the same prefix
                if codeword1.startswith(codeword2):   
                    # Check if the remaining suffix matches suffix_goal
                    if codeword1[len(codeword2):] == suffix_goal:
                        message = codeword2 + message
                        suffix_goal = codeword2
                        # Once suffix_goal is found, avoid further checks
                        found = True
                        break
        # Mirror case: search for prefixes of S0 in Si if suffix_goal was not found earlier
        if not found:
            for codeword2 in Sets[0]:
                if found:
                    break
                for codeword1 in Sets[i]:
                    if found:
                        break
                    if codeword1.startswith(codeword2):
                        if codeword1[len(codeword2):] == suffix_goal:
                            message = codeword2 + message
                            suffix_goal = codeword1
                            found = True
                            break
    
    print("Example of a non-UD message:", message)

def fill_sets(Sets, i):
    # Returns the set of suffixes obtained by comparing S[i-1] with S[0]
    Si = set()
    for codeword in Sets[i-1]:
        suffs = prefixes(codeword, Sets[0] - set([codeword]))
        Si.update(suffs)
    for codeword in Sets[0]:
        suffs = prefixes(codeword, Sets[i-1] - set([codeword]))
        Si.update(suffs)
    return Si

def sardinas_patterson(code):
    # The collection of sets Si
    Sets = []
    Sets.append(code)
    i = 0
    print('S[' + str(i) + '] =', Sets[i])
    
    # General case
    while True:
        i += 1
        # fill_sets generates the suffix set
        Si = fill_sets(Sets, i)
        Sets.append(Si)
        print('S[' + str(i) + '] =', Sets[i])
        
        # Conditions
        # If the i-th set is empty
        if len(Sets[i]) == 0:
            print("The code is UD")
            break
        # If the intersection between Si and S0 is not empty
        if len(Sets[0].intersection(Sets[i])) > 0:
            print("The code is not UD")
            # Generate a word that can be decoded in two ways
            non_ud_codeword(Sets)
            break
        # Check if the set Si is equal to any previous set
        flag = False
        for prev in Sets[0:i]:
            if Sets[i] == prev:
                flag = True
                break
        if flag:
            print("The code is UD")
            break

def main():
    C = {'012', '0123', '4', '310', '1024', '2402', '2401', '4013'}
    C1 = {'10', '010', '1', '1110'}
    C2 = {'0', '001', '101', '11'}
    C3 = {'0', '2', '03', '011', '104', '341', '11234'}
    C4 = {'01', '10', '001', '100', '000', '111'}
    C5 = {'0', '01', '011', '0111'}
    
    print('Test on C')
    sardinas_patterson(C)
    print('\nTest on C1')
    sardinas_patterson(C1)
    print('\nTest on C2')
    sardinas_patterson(C2)
    print('\nTest on C3')
    sardinas_patterson(C3)
    print('\nTest on C4')
    sardinas_patterson(C4)
    print('\nTest on C5')
    sardinas_patterson(C5)

if __name__ == '__main__':
    main()
