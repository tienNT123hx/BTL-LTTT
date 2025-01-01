from flask import Flask, request, jsonify
from collections import Counter

app = Flask(__name__)

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

# API để xử lý mã hóa
@app.route('/encode', methods=['POST'])
def encode():
    data = request.json
    text = data.get("text")
    method = data.get("method")
    
    if not text or not method:
        return jsonify({"error": "Missing text or method"}), 400

    freq = Counter(text).items()
    if method == "Huffman":
        code_map = huffman_encode(freq)
        encoded_data = "".join(code_map[char] for char in text)
    elif method == "Shannon-Fano":
        freq = sorted(freq, key=lambda x: -x[1])
        code_map = shannon_fano(freq)
        encoded_data = "".join(code_map[char] for char in text)
    else:
        return jsonify({"error": "Unsupported method"}), 400

    return jsonify({
        "encoded": encoded_data,
        "code_map": code_map
    })

if __name__ == '__main__':
    app.run(debug=True)
