import operator
import heapq
import os
import pickle


def read_binary_file(path):
    with open(path, "rb") as input_file:
        return input_file.read()


def write_binary_file(path, output):
    with open (path, 'wb+') as out:
        out.write(output)


def find_frequencies(bytesString):  # Return a dictionary containing bytes as keys and frequencies as values
    bytes_list = {}
    for byte in bytesString:
        if byte not in bytes_list:
            bytes_list[byte] = 0
        bytes_list[byte] += 1
    return bytes_list


class HeapNode:
    def __init__(self, freq, left=None, right=None, value=""):
        self.freq = freq
        self.left = left
        self.right = right
        self.value = value

    def __lt__(self, other):  # Overloading '<' operator for HeapNodes
        return self.freq < other.freq


def make_heap(frequencies): # return a heap constructed by frequencies dictionary
    heap = []
    for key in frequencies:
        node = HeapNode(freq=frequencies[key], value=key)
        heapq.heappush(heap, node)
    return heap


def merge_2nodes(heap):  # Pop then merge 2 smallest nodes of the heap. Then add this new node to heap
    a = heapq.heappop(heap)
    bytes_array = heapq.heappop(heap)
    merged = HeapNode(a.freq + bytes_array.freq, a, bytes_array, None)
    heapq.heappush(heap, merged)


def encoding(codes_list, node, code):  # Make a unique code for each byte by traversing the heap
    if node is None:
        return
    codes_list[node.value] = code
    encoding(codes_list, node.left, code + "0") # concatenate '0' to parent's code for left nodes
    encoding(codes_list, node.right, code + "1") # concatenate '1' to parent's code for right nodes


def preprocess():
    path = input("Enter the address --> ")
    bytesString = read_binary_file(path)
    orig_file_size = os.stat(path).st_size

    frequencies = find_frequencies(bytesString)
    heap = make_heap(frequencies)

    # Keep on merging nodes until
    # there is one (root) left
    while len(heap) > 1:
        merge_2nodes(heap)

    codes_list = {}
    encoding(codes_list, heap[0], "")  # Passing root of the heap that doesn't have any unique code
    del codes_list[None] # Deleting the useless key-value which is 'None'
    return bytesString, codes_list, orig_file_size


def huffman_compress(bytesString, codes_list, path="./compressed_file"):
    # Output is being concatenated
    # by each byte's unique code
    output = ""
    for byte in bytesString:
        output += codes_list[byte]

    bytes_array = bytearray()
    
    # Divide 'output' to sub-strings of
    # length 8 to be converted to bytes
    for i in range(0, len(output), 8):
        byte = output[i:i+8]
        bytes_array.append(int(byte, 2))

    write_binary_file(path, bytes_array)
    compressed_size = os.stat(path).st_size

    with open("./key_values.pkl", 'wb') as f: # Save the tree which will be used for decoding
        pickle.dump(codes_list, f, pickle.HIGHEST_PROTOCOL)
    del codes_list # Free the allocated space
    print("File's been compressed successfully :)")
    return compressed_size


def huffman_decompress(read_path='./compressed_file'):
    # Read the frequencies tree to begin decoding
    with open("./key_values.pkl", 'rb') as f:
        codes_list =  dict(pickle.load(f))

    # As we're decoding we do not need keys (bytes),
    # but also we need its values (unique-codes). So
    # we need to reverse the dictionary:
    # {byte: unique-code} --> {unique-code: byte}
    reverse_codes = dict([(val, key) for key, val in codes_list.items()])
    compressed_file = read_binary_file(read_path)
    extension = input('Input desired file extension (without ".")-> ')
    bits_string = ""

    # Convert each byte to string of 0's and 1's
    # with length of 8, then concat them
    for byte in compressed_file:
        bits = bin(byte)[2:].rjust(8, '0')
        bits_string += bits

    current_code = ""
    output = bytearray()
    for i in range(len(bits_string)):
        current_code += bits_string[i]

        # Check whether 'current_code' is in our list.
        # If it is, it means that this code used to be
        # a unique code in our tree. To decode, we only
        # need to replace reverse_codes[current_code]
        if current_code in reverse_codes.keys():
            output.append(reverse_codes[current_code])
            current_code = ""

    write_binary_file('./decompressed_file.' + extension, output)
    print("File's been decompressed successfully :)")


############### End of Functions ###############



mode = input("Do you need to compress or decompress?(c/d) ")
if mode == "c" or mode == "C":
    bytesString, codes_list, orig_size = preprocess()
    compressed_size = huffman_compress(bytesString, codes_list)
    print("Original --> %d Kb \nCompressed --> %d Kb" %(orig_size, compressed_size))
elif mode == "d" or mode == "D":
    huffman_decompress()
