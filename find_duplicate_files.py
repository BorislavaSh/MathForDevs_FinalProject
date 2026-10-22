import os

def create_sample_files():
    # create sample files with different variants of overlap
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

create_sample_files()


