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

def get_set_shingles(text, keywords = 2):
    #Convert a string into a set of word shingles
    words = text.lower().split(" ")
    shingles = set()
    for i in range(len(words) - keywords + 1):
        word = " ".join(words[i:i + keywords])
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

        # using infiinty as a starting point for hash comparison
        min_val = float('inf')
        for sh in shingle_hashes:
            h_val = (a * sh + b) % prime
            if h_val < min_val:
                min_val = h_val
        signature.append(min_val)

    return signature


def lsh_band(sig_matrix, file_names, num_bands=5):
    # add LSH branding for scalability optimization
    num_hashes, num_files = sig_matrix.shape
    rows_per_band = num_hashes // num_bands

    bucket = {}
    possible_pairs = set()

    for band_index in range(num_bands):
        start_row = band_index * rows_per_band
        end_row = start_row + rows_per_band

        band_slice = sig_matrix[start_row:end_row, :]

        for file_index in range(num_files):
            bucket_key = (band_index, tuple(band_slice[:, file_index]))

            if bucket_key not in bucket:
                bucket[bucket_key] = []
            bucket[bucket_key].append(file_names[file_index])

    for bucket_key, members in bucket.items():
        if len(members) > 1:
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    possible_pairs.add(tuple(sorted((members[i], members[j]))))

    return list(possible_pairs)

if __name__ == "__main__":
    sample_files = create_sample_files()

    doc_shingles = {}
    for filename in sample_files:
        path = os.path.join("sample_files", filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        doc_shingles[filename] = get_set_shingles(content)
    print(doc_shingles)

    file_names = list(doc_shingles.keys())
    matrix_data = []
    for d1 in file_names:
        row = []
        for d2 in file_names:
            sim = calculate_similarity_jaccard(doc_shingles[d1], doc_shingles[d2])
            row.append(round(sim, 3))
        matrix_data.append(row)

    print(matrix_data)

    signatures = []
    for name in file_names:
        sig = generate_minhash_sign(doc_shingles[name], num_hashes=100)
        signatures.append(sig)

    sig_matrix = np.array(signatures).T
    candidates = lsh_band(sig_matrix, file_names, num_bands=20)

    if candidates:
        for pair in candidates:
            print(f"Match found: {pair[0]} & {pair[1]}")
    else:
        print("No matching candidate pairs found.")
