import string

# Gets the discrete source from the text: for each word, the observed probability in the text
def discrete_source(text):
    # punctuation is the list of punctuation characters like ,.;!
    punctuation = string.punctuation
    # Separate punctuation from words
    for c in punctuation:
        text = text.replace(c, ' '+c+' ')
    # Convert text to lowercase
    text = text.lower()
    
    # Split text into words
    words = text.split()
    
    # Create a dictionary to count occurrences
    dictionary = {}
    
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    
    # Normalize values between 0 and 1 by dividing occurrences by the total number of words
    num_words = len(words)
    for word in dictionary:
        dictionary[word] = dictionary[word] / num_words
    
    return dictionary

# Node object to store the probability value and the corresponding text string
class Node:
    def __init__(self, value=None, string=None):
        self.value = value
        self.string = string
        self.left = None
        self.right = None
        
    # Returns the value of the current node
    def get_value(self):
        return self.value

# In an in-order traversal, from a given node:
# - When visiting the left child, append '0' to the current codeword
# - When visiting the right child, append '1'
# This way, when reaching a leaf node, we obtain the final codeword,
# which we can add to the encoding dictionary
def traverse_tree(root, current_codeword, Code):
    # Base case (leaf node): add the codeword to Code
    if root.left is None and root.right is None:
        Code[root.string] = current_codeword
        print('String: {:15} Codeword: {}'.format(root.string, current_codeword))
        return
    traverse_tree(root.left, current_codeword + '0', Code)
    traverse_tree(root.right, current_codeword + '1', Code)
    return 
    

def huffman_encoding(source):
    # Q is the priority queue that contains nodes sorted by probability value
    Q = MinHeap()
    
    # Initialize Q with the leaf nodes of the tree
    for word in source:
        Q.insert(Node(string=word, value=source[word]))
    
    # At each step, create a parent node for the two removed nodes with the smallest values,
    # and insert it back into the queue
    while Q.size() > 1:
        left = Q.extract_min()
        right = Q.extract_min()
        parent = Node(value=left.get_value() + right.get_value())
        parent.left = left
        parent.right = right
        Q.insert(parent)
    
    # Q contains the root of the Huffman tree    
    root = Q.extract_min()
    # Code is the dictionary that will contain the encoding
    Code = {}
    print('\t\t\tEncoding')
    # Traverse the tree to obtain word encodings
    traverse_tree(root, '', Code)
    
    return Code


def encode(text, Code):
    # Separate punctuation from words
    punctuation = string.punctuation
    for c in punctuation:
        text = text.replace(c, ' '+c+' ')
    # Convert text to lowercase
    text = text.lower()
    # Create an array of words
    words = text.split()
    encoded_text = ''
    for word in words: 
        # Concatenate encodings to create the encoded text
        encoded_text = encoded_text + Code[word]
    return encoded_text

# decode takes the encoded text and follows the code to decrypt it
def decode(encoded_text, Code):
    decoded_text = ''
    current_pos = 0
    
    while current_pos < len(encoded_text):
        temp_value = ''
        temp_key = '' 
        # Search for the corresponding codeword
        for text, codeword in Code.items():
            # Check if the prefix matches starting from the current position in the text
            if encoded_text.startswith(codeword, current_pos):
                temp_value = codeword
                temp_key = text 
        # If we have not decoded a punctuation symbol,
        # insert a space before the string
        punctuation = string.punctuation
        if temp_key not in punctuation:
            temp_key = ' ' + temp_key
        # Concatenate the decoded words to reconstruct the original text
        decoded_text = decoded_text + temp_key
        current_pos += len(temp_value)
    return decoded_text

class MinHeap:
    # The heap is represented as an array
    def __init__(self):
        self.heap = []
        
    def _parent(self, index):
        return (index - 1) // 2

    def _left_child(self, index):
        return 2 * index + 1
    
    def _right_child(self, index):
        return 2 * index + 2
    
    def _heapify_up(self, index):
        while index > 0 and self.heap[index].get_value() < self.heap[self._parent(index)].get_value():
            self.heap[index], self.heap[self._parent(index)] = self.heap[self._parent(index)], self.heap[index]
            index = self._parent(index)

    def _heapify_down(self, index):
        smallest = index
        left = self._left_child(index)
        right = self._right_child(index)

        if left < len(self.heap) and self.heap[left].get_value() < self.heap[smallest].get_value():
            smallest = left
        if right < len(self.heap) and self.heap[right].get_value() < self.heap[smallest].get_value():
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)
    
    def insert(self, element):
        self.heap.append(element)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if len(self.heap) == 0:
            print("Empty heap")
            return
        min_element = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop(-1)
        self._heapify_down(0)
        return min_element

    def size(self):
        return len(self.heap)


def main():
    text = """ The man sat on the chair and took the book from the table;
    then the man began to read the book with great interest, because the book contained stories
    that the man found fascinating."""
    print('Text: \n', text, '\n')
    source = discrete_source(text)
    Code = huffman_encoding(source)
    encoded_text = encode(text, Code)
    print("\nEncoding: ", encoded_text)
    decoded_text = decode(encoded_text, Code)
    print("Decoding: ", decoded_text)
    
if __name__ == '__main__':
    main()
