import os

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
    #Calculates similarity using Jaccard Similarity: J(A,B) = |A intersect B| / |A union B|
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0
    return intersection / union

def get_set_words(text):
    #Converts a string into a set of word tokens
    words = text.lower().split(" ")
    set_words = set()
    for word in words:
        set_words.add(word)
    return set_words


if __name__ == "__main__":
    sample_files = create_sample_files()

    doc_words = {}
    for filename in sample_files:
        path = os.path.join("sample_files", filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        doc_words[filename] = get_set_words(content)
    print(doc_words)

    doc_names = list(doc_words.keys())
    matrix_data = []
    for d1 in doc_names:
        row = []
        for d2 in doc_names:
            sim = calculate_similarity_jaccard(doc_words[d1], doc_words[d2])
            row.append(round(sim, 3))
        matrix_data.append(row)

    print(matrix_data)

