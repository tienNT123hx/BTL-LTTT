import heapq
import numpy as np
from PIL import Image
from math import log2



class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self,other):
        return self.freq < other.freq
    


#Bước 1: Tìm xem mỗi ký tự xuất hiện bao nhiêu lần
def makeFrequencyLibrary(text):
    frequency = {}
    for character in text:
        if (character not in frequency):
            frequency[character] = 0
        frequency[character] += 1
    return frequency

#Bước 2: Build a priority queue (dùng min-heap)
def makeHeap(frequency): 
    heap = []
    #Frequency library có dạng như sau: {'A': 3, 'B': 2}
    #Với mỗi một phần tử trong library, tạo ra 1 node, rồi đẩy hết bọn nó vào heap
    for key in frequency:
        node = Node(key, frequency[key])
        heapq.heappush(heap, node)
    heapq.heapify(heap)
    return heap

#Bước 3: Build a HuffmanTree by selecting 2 nodes and merging them. Returns the root of huffman tree
def makeHuffmanTreeFromHeap(heap):
    while (len(heap) > 1):
        node1 = heapq.heappop(heap);
        node2 = heapq.heappop(heap);

        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    return heap[0]

#Bước 4: Assign code to character (đi xuống cái tree từ cái root) / Tạo ra key để giải mã / Tao ra dictionary tu ma 
def generateHuffmanCodes(node, currentCode = '', HuffmanCodes = None):
    if HuffmanCodes is None:  # Initialize a new dictionary if not provided
        HuffmanCodes = {}
    if node is not None:
        if node.char is not None:
            HuffmanCodes[node.char] = currentCode;
        generateHuffmanCodes(node.left, currentCode + '0', HuffmanCodes)
        generateHuffmanCodes(node.right, currentCode + '1', HuffmanCodes)
    return HuffmanCodes

#Bước 5: Encode text
def encodeText(text, HuffmanCodes):
    encodedText = ''
    for character in text:
        encodedText += HuffmanCodes[character]
    return encodedText

#Bước 6: Decode text
def decodeText(undecodedText, HuffmanCodes):
    #reversing the HuffmanCodes dictionary
    decodedText = ''
    reverseHuffmanCodes = {}
    for key in HuffmanCodes:
        reverseHuffmanCodes[HuffmanCodes[key]] = key
    
    #decoding the things
    currentBits = ''
    for bits in undecodedText:
        currentBits += bits
        if currentBits in reverseHuffmanCodes:
            decodedText += reverseHuffmanCodes[currentBits]
            currentBits = ''
    return decodedText

def calculateMetrics(data, codeMap):
    freqMap = makeFrequencyLibrary(data)
    totalChars = len(data)
    probabilities = {char: freq / totalChars for char, freq in freqMap.items()}

    # Average code length
    avgCodeLength = sum(probabilities[char] * len(codeMap[char]) for char in probabilities)

    # Entropy
    entropy = -sum(probabilities[char] * log2(probabilities[char]) for char in probabilities)

    # Compression ratio
    initialBitsPerChar = log2(len(probabilities))  # Fixed bits per character
    compressionRatio = initialBitsPerChar / avgCodeLength

    # Optimality ratio
    optimalityRatio = entropy / avgCodeLength

    return avgCodeLength, entropy, compressionRatio, optimalityRatio

def encodeImage(imagePath):
    # Load the image
    img = Image.open(imagePath)
    imgArray = np.array(img)  # Convert to a NumPy array

    # Flatten the image array into a list of pixel tuples
    flatArray = imgArray.reshape(-1, imgArray.shape[-1])
    pixelTuples = [tuple(pixel) for pixel in flatArray]

    # Create a frequency library for the pixel tuples
    frequency = makeFrequencyLibrary(pixelTuples)
    print(frequency)

    # Build the min-heap
    heap = makeHeap(frequency)

    # Build the Huffman Tree
    huffmanTreeRoot = makeHuffmanTreeFromHeap(heap)

    # Generate Huffman codes
    huffmanCodes = {}
    generateHuffmanCodes(huffmanTreeRoot, "", huffmanCodes)
    print(huffmanCodes)

    # Encode the image
    encodedText = ""
    for pixel in pixelTuples:
        encodedText += huffmanCodes[pixel]
    print(encodedText)
    return encodedText, huffmanCodes, imgArray.shape

# Function to decode the encoded image
def decodeImage(encodedText, huffmanCodes, originalShape):
    # Reverse the Huffman codes dictionary
    reverse_huffman_codes = {code: value for value, code in huffmanCodes.items()}

    # Decode the text into pixel values
    decodedPixels = []
    currentBits = ""

    for bit in encodedText:
        currentBits += bit
        if currentBits in reverse_huffman_codes:
            decodedPixels.append(reverse_huffman_codes[currentBits])
            currentBits = ""

    # Reshape the decoded pixels into the original image shape
    decodedArray = np.array(decodedPixels).reshape(originalShape)
    decodedImg = Image.fromarray(decodedArray.astype('uint8'))
    return decodedImg


if __name__ == "__main__":
    # Encode the image
    encodedText, huffmanCodes, shape = encodeImage("D:\Code\python\huffman\example.jpg")
    print("Image successfully encoded!")

    # Decode the image

    decodedImage = decodeImage(encodedText, huffmanCodes, shape)
    decodedImage.show()
    decodedImage.save("decoded_image.jpg")
    print("Image successfully decoded!")