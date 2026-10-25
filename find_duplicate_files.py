import os
import random
import numpy as np

def create_sample_files():
    #Create sample files with different variants of overlap
    os.makedirs("sample_files", exist_ok=True)

    text_1 = "Insanity is doing the same thing, over and over again, but expecting different results."
    text_2 = "In three words I can sum up everything I've learned about life: it goes on."

    docs = {
        "original.txt": text_1,
        "similar.txt": text_1 + " additional words and notes.",
        "unrelated.txt": text_2
    }

    for filename, text in docs.items():
        path = os.path.join("sample_files", filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    return list(docs.keys())


def calculate_similarity_jaccard(set1, set2):
    #Calculate similarity using Jaccard Similarity: J(A,B) = |A intersect B| / |A union B|
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0
    return intersection / union

def get_set_shingles(text):
    #Convert a string into a set of word shingles
    words = text.lower().split(" ")
    shingles = set()
    for word in words:
        shingles.add(word)
    return shingles


def generate_minhash_sign(shingles, num_hashes=20):

    # Compute a MinHash signature vector for a set of shingles
    prime = 9420858323   #random large prime number
    signature = []

    #standardize hashing to 32-bits positive number
    shingle_hashes = [hash(s) & 0xffffffff for s in shingles]
    if not shingle_hashes:
        return [0] * num_hashes

    for i in range(num_hashes):
        a = random.randint(1, 1000)
        b = random.randint(0, 1000)

        # using infiinty as a starting point for hash
        min_val = float('inf')
        for sh in shingle_hashes:
            h_val = (a * sh + b) % prime
            if h_val < min_val:
                min_val = h_val
        signature.append(min_val)

    return signature


if __name__ == "__main__":
    sample_files = create_sample_files()

    doc_shingles = {}
    for filename in sample_files:
        path = os.path.join("sample_files", filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        doc_shingles[filename] = get_set_shingles(content)
    print(doc_shingles)

    doc_names = list(doc_shingles.keys())
    matrix_data = []
    for d1 in doc_names:
        row = []
        for d2 in doc_names:
            sim = calculate_similarity_jaccard(doc_shingles[d1], doc_shingles[d2])
            row.append(round(sim, 3))
        matrix_data.append(row)

    print(matrix_data)

    signatures = []
    for name in doc_names:
        sig = generate_minhash_sign(doc_shingles[name], num_hashes=20)
        signatures.append(sig)

    print(signatures)

