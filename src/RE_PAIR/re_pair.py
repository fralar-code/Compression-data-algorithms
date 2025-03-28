from collections import defaultdict

# Returns the most frequent pair
def most_frequent_pair(sequence):
    # We create a dictionary that will have the symbol pair as the key and the value as the occurrences of the digram
    pair_count = defaultdict(int)
    i = 0

    while i < len(sequence) - 1:
        pair = (sequence[i], sequence[i+1])
        pair_count[pair] += 1
        # check if there is an overlap
        if (i+2)< len(sequence) and sequence[i] == sequence[i+1] and sequence[i+1] == sequence[i+2]:
            # We increase by 2 so that the overlap is considered only once
            i += 2  
        else:
            i += 1
            
    if not pair_count:
        return None
    # We return the pair with higher occurrence
    max_key = max(pair_count, key = pair_count.get)
    return (max_key, pair_count[max_key])


# Replaces the pair present in the sequence with the new non-terminal symbol
def replace_pair(sequence, pair, non_terminal_symbol):
    i = 0
    while i < len(sequence) - 1:
        if sequence[i] == pair[0] and sequence[i+1] == pair[1]:
            sequence = sequence[:i] + [non_terminal_symbol] + sequence[i+2:]    
        i += 1
    return sequence

def re_pair(sequence):
    sequence = list(sequence.lower())
    # The initial non-terminal symbol will be 'A'
    non_terminal_symbol = 'A'
    rules = []
    while True:
        # Get the most frequent pair of symbols
        pair, occurrence = most_frequent_pair(sequence)
        if occurrence <= 1:
            break
        # Replace the most frequent pair in the text with the new non-terminal symbol
        sequence = replace_pair(sequence, pair, non_terminal_symbol)
        # We add the new production rule
        rules.append((non_terminal_symbol, pair))
        # Create the new non-terminal symbol
        non_terminal_symbol = chr(ord(non_terminal_symbol) + 1)
    return sequence, rules

def re_pair_chomsky(sequence):
    sequence = sequence.lower()
    # The initial non-terminal symbol will be 'A'
    non_terminal_symbol = 'A'
    rules = []
    # We assign each terminal symbol a non-terminal symbol
    for char in set(sequence):
        rules.append((non_terminal_symbol, char))
        sequence = sequence.replace(char, non_terminal_symbol)
        non_terminal_symbol = chr(ord(non_terminal_symbol) + 1)
    sequence = list(sequence)
    while True:
        # We obtain the most frequent pair of symbols
        pair, occurrence = most_frequent_pair(sequence)
        if occurrence <= 1:
            # We transfrom S in CNF
            for i in range(len(sequence)-1):
                # At each step we use two non-terminal symbols head and tail
                # head is the symbol that produces the rule
                head = non_terminal_symbol
                non_terminal_symbol = chr(ord(non_terminal_symbol) + 1)
                # tail is the non-terminal symbol that replaces the sequence starting with the second symbol
                # if the sequence has two characters we do not use a new non-terminal symbol
                tail = non_terminal_symbol if len(sequence) != 2 else sequence[1]
                # if i = 0 we are considering the axiom, we keep track of it to return it in output
                if i == 0:
                    axiom = (head, (sequence[0],tail))
                # viceversa we add the new production rule in CNF
                else:
                    rules.append((head, (sequence[0],tail)))
                # we analyze the sequence from the second character onward, until we arrive at a sequence two characters long
                sequence = sequence[1:]
            break
        # We replace the most frquent pair in the text with the new non-terminal symbol
        sequence = replace_pair(sequence, pair, non_terminal_symbol)
        # We add the new production rule
        rules.append((non_terminal_symbol, pair))
        # Create the new non-terminal symbol
        non_terminal_symbol = chr(ord(non_terminal_symbol) + 1)
    return axiom, rules




def main():
    text = 'aaabcaabaaabcabdabd'
    compressed_text, rules = re_pair(text)
    print("Compressed text with re_pair(S):", compressed_text)
    print("Production rules:", rules)
    size = len(rules)*2 + len(compressed_text)
    print("Grammar size:", size)

    compressed_text, rules = re_pair_chomsky(text)
    print("\nCompressed text in Chomsky's normal form (S):", compressed_text[1])
    print("Production rules:", rules)
    size = 0
    for rule in rules:
        size += len(rule[1])
    print("Grammar size:", size)

if __name__=='__main__':
    main()
