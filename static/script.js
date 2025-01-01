document.getElementById("encodeButton").addEventListener("click", () => {
    const inputText = document.getElementById("inputText").value;
    if (!inputText) {
        alert("Please enter some text to encode.");
        return;
    }

    fetch("/encode", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: inputText }),
    })
        .then((response) => response.json())
        .then((data) => {
            document.getElementById("huffmanOutput").innerText = JSON.stringify(data.huffman, null, 2);
            document.getElementById("shannonFanoOutput").innerText = JSON.stringify(data.shannon_fano, null, 2);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});
