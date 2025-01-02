import tkinter as tk
from tkinter import messagebox
from huffman import makeFrequencyLibrary, makeHeap, makeHuffmanTreeFromHeap, generateHuffmanCodes, encodeText, decodeText
import ast  # For safely parsing dictionary input

# Function to encode the input text
def encode_message():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showerror("Err   or", "Please enter text to encode.")
        return

    frequency = makeFrequencyLibrary(text)
    heap = makeHeap(frequency)
    huffman_tree = makeHuffmanTreeFromHeap(heap)
    huffman_codes = generateHuffmanCodes(huffman_tree)
    encoded_message = encodeText(text, huffman_codes)

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Input Text:\n{text}\n\nHuffman Codes:\n{huffman_codes}\n\nEncoded Message:\n{encoded_message}")
    output_text.config(state=tk.DISABLED)

# Function to decode the input text
def decode_message():
    encoded_text = input_text.get("1.0", tk.END).strip()
    codes_input = huffman_codes_entry.get().strip()



    if not encoded_text or not codes_input:
        messagebox.showerror("Error", "Please enter both encoded text and Huffman codes.")
        return

    try:
        # Parse the dictionary input
        huffman_codes = ast.literal_eval(codes_input)

        if not isinstance(huffman_codes, dict):
            raise ValueError("Input must be a valid dictionary.")

        decoded_message = decodeText(encoded_text, huffman_codes)

        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Decoded Message:\n{decoded_message}")
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Create the main window
root = tk.Tk()
root.title("Huffman Encoding and Decoding")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Style Configuration
title_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")

# Title Label
title_label = tk.Label(root, text="Huffman Encoding and Decoding", font=title_font, bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

# Input Frame
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10, padx=10, fill="x")

tk.Label(input_frame, text="Input Text:", font=label_font, bg="#f0f0f0").grid(row=0, column=0, sticky="w")
input_text = tk.Text(input_frame, height=4, width=50, wrap="word", relief="solid", borderwidth=1)
input_text.grid(row=1, column=0, columnspan=2, pady=5)

tk.Label(input_frame, text="Huffman Codes (for decoding - dictionary format):", font=label_font, bg="#f0f0f0").grid(row=2, column=0, sticky="w")
huffman_codes_entry = tk.Entry(input_frame, font=label_font, relief="solid", borderwidth=1, width=50)
huffman_codes_entry.grid(row=3, column=0, columnspan=2, pady=5)

# Button Frame
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

encode_button = tk.Button(button_frame, text="Encode", font=button_font, bg="#4CAF50", fg="white", command=encode_message)
encode_button.grid(row=0, column=0, padx=10)

decode_button = tk.Button(button_frame, text="Decode", font=button_font, bg="#2196F3", fg="white", command=decode_message)
decode_button.grid(row=0, column=1, padx=10)

# Output Frame
output_frame = tk.Frame(root, bg="#f0f0f0")
output_frame.pack(pady=10, padx=10, fill="both", expand=True)

tk.Label(output_frame, text="Output:", font=label_font, bg="#f0f0f0").pack(anchor="w")
output_text = tk.Text(output_frame, height=10, wrap="word", relief="solid", borderwidth=1, state=tk.DISABLED, bg="#f9f9f9")
output_text.pack(fill="both", expand=True, pady=5)

# Run the application
root.mainloop()
