from collections import Counter
from heapq import heapify, heappop, heappush
from math import log2


# Huffman Node
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Function to build the Huffman tree
def build_huffman_tree(freq_map):
    heap = [Node(char, freq) for char, freq in freq_map.items()]
    heapify(heap)  # Sử dụng heapify để tạo heap từ danh sách ban đầu

    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heappush(heap, merged)

    return heappop(heap)


# Function to generate Huffman codes
def huffman_encoding(root, prefix="", code_map={}):
    if root is None:
        return
    if root.char is not None:
        code_map[root.char] = prefix
    huffman_encoding(root.left, prefix + "0", code_map)
    huffman_encoding(root.right, prefix + "1", code_map)
    return code_map

# Function to calculate metrics for Huffman coding
def calculate_metrics(data, code_map):
    freq_map = Counter(data)
    total_chars = len(data)
    probabilities = {char: freq / total_chars for char, freq in freq_map.items()}

    # Average code length
    avg_code_length = sum(probabilities[char] * len(code_map[char]) for char in probabilities)

    # Entropy
    entropy = -sum(probabilities[char] * log2(probabilities[char]) for char in probabilities)

    # Compression ratio
    initial_bits_per_char = log2(len(probabilities))  # Fixed bits per character
    compression_ratio = initial_bits_per_char / avg_code_length

    # Optimality ratio
    optimality_ratio = entropy / avg_code_length

    return avg_code_length, entropy, compression_ratio, optimality_ratio

# Example Huffman coding
data = "ly thuyet thong tin"
freq_map = Counter(data)
root = build_huffman_tree(freq_map)
huffman_map = huffman_encoding(root)
encoded_data = "".join(huffman_map[char] for char in data)
avg_code_length, entropy, compression_ratio, optimality_ratio = calculate_metrics(data, huffman_map)

print("Huffman Encoded:", encoded_data)
print("Huffman Code Map:", huffman_map)
print(f"Average Code Length: {avg_code_length:.4f}")
print(f"Entropy: {entropy:.4f}")
print(f"Compression Ratio: {compression_ratio:.4f}")
print(f"Optimality Ratio: {optimality_ratio:.4f}")
