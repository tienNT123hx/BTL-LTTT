def lempel_ziv_encoding(data):
    dictionary = {}
    current = ""
    encoded = []
    dict_size = 1

    for char in data:
        temp = current + char
        if temp in dictionary:
            current = temp
        else:
            if current:
                encoded.append((dictionary[current], char))
            else:
                encoded.append((0, char))
            dictionary[temp] = dict_size
            dict_size += 1
            current = ""

    if current:
        encoded.append((dictionary[current], ""))

    return encoded, len(dictionary)

# Hàm tính toán các chỉ số Lempel-Ziv
def lempel_ziv_metrics(data, encoded, dict_size):
    original_size = len(data) * 8  # Mỗi ký tự gốc là 8 bit
    compressed_size = sum(len(bin(index)[2:]) + 8 for index, _ in encoded)  # Chỉ số từ điển + ký tự mới

    # Hệ số nén
    compression_ratio = original_size / compressed_size

    # Độ dài trung bình (mỗi đoạn mã tính là trung bình bit)
    avg_code_length = compressed_size / len(data)

    # Không tính entropy vì Lempel-Ziv không dựa trên xác suất từng ký tự

    return avg_code_length, compression_ratio

# Ví dụ Lempel-Ziv
data = "lempel lempel lempel-ziv encoding example"
encoded_data, dict_size = lempel_ziv_encoding(data)
avg_code_length, compression_ratio = lempel_ziv_metrics(data, encoded_data, dict_size)

print("Lempel-Ziv Encoded:", encoded_data)
print(f"Average Code Length: {avg_code_length:.4f}")
print(f"Compression Ratio: {compression_ratio:.4f}")
