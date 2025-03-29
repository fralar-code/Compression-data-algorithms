# Compression Data Algorithms

## Introduction

This repository contains implementations of various **data compression algorithms**, aiming to analyze their efficiency and understand their mathematical and computational foundations. Data compression is crucial in multiple applications, from efficient data transmission to storage optimization.

The presented algorithms are **lossless compression techniques**, ensuring perfect reconstruction of the original data. Each algorithm is analyzed in terms of **computational complexity** and **compression ratio**.

## Implemented Algorithms

### 1. Huffman Coding

Huffman coding is a fundamental **lossless data compression algorithm**, widely used for text compression. It efficiently encodes a given text using **variable-length binary codes**, where more frequent symbols receive **shorter codes** and less frequent ones receive **longer codes**, minimizing the overall space required.

The implementation includes:

- **Building a discrete source** from text, associating words with their empirical probabilities.
- Constructing the **Huffman tree** using a **min-heap** data structure.
- Generating **prefix codes** by traversing the tree.

Huffman's algorithm generates an **optimal prefix code** for discrete sources with known probability distributions.

**Time Complexity**: $O(n \log n)$, where $n$ is the number of distinct symbols.

---

### 2. Burrows-Wheeler Transform (BWT)

BWT is a transformation that **enhances compression** by rearranging the input into blocks with high redundancy, making it easier to apply other compression techniques like **Move-to-Front (MTF)** and **Run-Length Encoding (RLE)**.

This project implements **Burrows-Wheeler Transform (BWT)** using two approaches:

- **BWT via rotations**: Computes all cyclic rotations of the input string, sorts them lexicographically, and extracts the last column.
- **BWT via suffix array**: Uses the **SA-IS** recursive algorithm to build the suffix array and derive the BWT.

#### **SA-IS Algorithm (Suffix Array Induced Sorting)**
- Classifies characters as **L-type**, **S-type**, or **LMS-type** (leftmost S-type character in a group).
- Identifies **LMS substrings** and sorts them using **induced sorting**.
- Recursively reduces the problem when LMS factors are not unique.
- Constructs the **full suffix array** from LMS suffixes.

**Time Complexity**: 
- Naive BWT construction: $O(n^2)$
- Using suffix arrays $O(n)$
---

### 3. Lempel-Ziv Algorithms (LZ77 & LZ78)

LZ77 and LZ78 are **dictionary-based compression techniques**, replacing repeated substrings with references to previous occurrences in the data stream.

- **LZ77**: Uses **sliding windows** to detect repetitions dynamically.
- **LZ78**: Builds an **incremental dictionary** based on input sequences.
The implementation evaluates the relationship between the number of triplets (𝑧) produced by LZ77 (or LZSS) encoding and the number of equal-letter runs (𝑟) in the Burrows-Wheeler Transform (BWT) of a given text, to validate the theoretical relations:

$r = O(z (\log n)^2)$

$z = O(r \log n)$

---

### 4. Integer Encoding Methods

This project implements various **integer encoding schemes**, including:

- **Gamma Encoding**
- **Delta Encoding**
- **Rice Encoding**
- **Fibonacci Encoding**

The goal is to compare their **bit-length efficiency** across different integers.

---

### 5. Sardinas-Patterson Algorithm

A method used to **verify whether a code is uniquely decodable**, meaning if a **prefix-free** exists. It constructs successive sets of suffixes to detect ambiguities.


---

## Repository Structure

- `/src/` - Contains Python implementations of the algorithms.
- `README.md` - This documentation file.

---

## How to Use

1. Clone the repository:
   ```sh
   git clone https://github.com/fralar-code/Compression-data-algorithms.git
   cd Compression-data-algorithms
2. Run one of the scripts in the `src/` folder:
   ```sh
   python src/Huffman/huffman.py
   
## Contributions 

If you want to improve or add other compression algorithms, feel free to open a pull request!

