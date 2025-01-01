from collections import Counter
from math import log2

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

def calculate_metrics(data, code_map):
    # Tính xác suất của từng ký tự
    freq_map = Counter(data)
    total_chars = len(data)
    probabilities = {char: freq / total_chars for char, freq in freq_map.items()}

    # Độ dài trung bình của mã
    avg_code_length = sum(probabilities[char] * len(code_map[char]) for char in probabilities)

    # Entropy
    entropy = -sum(probabilities[char] * log2(probabilities[char]) for char in probabilities)

    # Hệ số nén
    initial_bits_per_char = log2(len(probabilities))  # Số bit cố định để mã hóa mỗi ký tự
    compression_ratio = initial_bits_per_char / avg_code_length

    # Hệ số tối ưu tương đối
    optimality_ratio = entropy / avg_code_length

    return avg_code_length, entropy, compression_ratio, optimality_ratio

# Ví dụ
data = "hoang tien"
freq = Counter(data).most_common()
code_map = shannon_fano(freq)

# Mã hóa dữ liệu
encoded_data = "".join(code_map[char] for char in data)

# Tính các chỉ số
avg_code_length, entropy, compression_ratio, optimality_ratio = calculate_metrics(data, code_map)

# Kết quả
print("Shannon-Fano Encoded:", encoded_data)
print("Shannon-Fano Code Map:", code_map)
print(f"Average Code Length: {avg_code_length:.4f}")
print(f"Entropy: {entropy:.4f}")
print(f"Compression Ratio: {compression_ratio:.4f}")
print(f"Optimality Ratio: {optimality_ratio:.4f}")
