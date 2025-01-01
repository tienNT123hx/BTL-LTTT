import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
from math import log2

# Hàm mã hóa Huffman
def huffman_encode(freq):
    from heapq import heappush, heappop, heapify

    heap = [[weight, [symbol, ""]] for symbol, weight in freq]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = "0" + pair[1]
        for pair in hi[1:]:
            pair[1] = "1" + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return dict(sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p)))

# Hàm mã hóa Shannon-Fano
def shannon_fano(symbols, prefix=""):
    if len(symbols) == 1:
        return {symbols[0][0]: prefix}

    total = sum(freq for _, freq in symbols)
    acc = 0
    split = 0

    for i, (_, freq) in enumerate(symbols):
        acc += freq
        if acc >= total / 2:
            split = i + 1
            break

    left = symbols[:split]
    right = symbols[split:]
    code_map = {}
    code_map.update(shannon_fano(left, prefix + "0"))
    code_map.update(shannon_fano(right, prefix + "1"))
    return code_map

# Hàm mã hóa Lempel-Ziv
def lz_encode(data):
    dictionary = {}
    current_string = ""
    encoded_data = []
    dict_size = 1

    for char in data:
        current_string += char
        if current_string not in dictionary:
            dictionary[current_string] = dict_size
            dict_size += 1
            if len(current_string) == 1:
                encoded_data.append((0, 0, char))
            else:
                encoded_data.append((dictionary[current_string[:-1]], len(current_string) - 1, char))
            current_string = ""
    return encoded_data

# Tính toán các chỉ số
def calculate_metrics(freq_map, code_map, encoded_data, input_length):
    probabilities = {char: freq / input_length for char, freq in freq_map.items()}
    
    # Độ dài mã trung bình
    avg_code_length = sum(probabilities[char] * len(code_map[char]) for char in code_map)

    # Entropy
    entropy = -sum(p * log2(p) for p in probabilities.values())

    # Hệ số nén
    # original_size = input_length * 8  # Giả sử mỗi ký tự chiếm 8 bit
    # compressed_size = len(encoded_data)
    # compression_ratio = compressed_size / original_size
    initial_bits_per_char = log2(len(probabilities))  # Fixed bits per character
    compression_ratio = initial_bits_per_char / avg_code_length
    
    # Hệ số tối ưu tương đối
    optimality_ratio = entropy / avg_code_length if avg_code_length > 0 else 0

    return avg_code_length, entropy, compression_ratio, optimality_ratio

# Hàm thực hiện mã hóa
def perform_encoding():
    input_data = input_text.get("1.0", tk.END).strip()
    if not input_data:
        messagebox.showerror("Lỗi", "Vui lòng nhập dữ liệu!")
        return

    selected_method = encoding_method.get()
    if selected_method == "Huffman":
        freq_map = Counter(input_data)
        code_map = huffman_encode(freq_map.items())
        encoded_data = "".join(code_map[char] for char in input_data)
        avg_code_length, entropy, compression_ratio, optimality_ratio = calculate_metrics(freq_map, code_map, encoded_data, len(input_data))
    elif selected_method == "Shannon-Fano":
        freq_map = Counter(input_data)
        sorted_freq = sorted(freq_map.items(), key=lambda x: -x[1])
        code_map = shannon_fano(sorted_freq)
        encoded_data = "".join(code_map[char] for char in input_data)
        avg_code_length, entropy, compression_ratio, optimality_ratio = calculate_metrics(freq_map, code_map, encoded_data, len(input_data))
    elif selected_method == "Lempel-Ziv":
        encoded_data = lz_encode(input_data)
        avg_code_length, entropy, compression_ratio, optimality_ratio = 0, 0, 0, 0  # Lempel-Ziv không áp dụng các chỉ số này
    else:
        messagebox.showerror("Lỗi", "Vui lòng chọn phương pháp mã hóa!")
        return

    # Hiển thị kết quả
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Encoded: {encoded_data}\n")
    if selected_method != "Lempel-Ziv":
        output_text.insert(tk.END, f"Chiều dài trung bình của từ mã: {avg_code_length:.4f}\n")
        output_text.insert(tk.END, f"Entropy: {entropy:.4f}\n")
        output_text.insert(tk.END, f"Hệ số nén: {compression_ratio:.4f}\n")
        output_text.insert(tk.END, f"Hệ số tối ưu: {optimality_ratio:.4f}\n")

# Giao diện Tkinter
root = tk.Tk()
root.title("Mã hóa dữ liệu")

# Label nhập dữ liệu
tk.Label(root, text="Nhập dữ liệu:").pack(anchor="w", padx=10, pady=5)
input_text = tk.Text(root, height=5, width=50)
input_text.pack(padx=10, pady=5)

# Lựa chọn phương pháp mã hóa
tk.Label(root, text="Chọn phương pháp mã hóa:").pack(anchor="w", padx=10, pady=5)
encoding_method = ttk.Combobox(root, values=["Huffman", "Shannon-Fano", "Lempel-Ziv"])
encoding_method.pack(padx=10, pady=5)
encoding_method.set("Huffman")

# Nút mã hóa
encode_button = tk.Button(root, text="Mã hóa", command=perform_encoding)
encode_button.pack(pady=10)

# Kết quả mã hóa
tk.Label(root, text="Kết quả mã hóa:").pack(anchor="w", padx=10, pady=5)
output_text = tk.Text(root, height=10, width=50, state="normal")
output_text.pack(padx=10, pady=5)

# Chạy giao diện
root.mainloop()
