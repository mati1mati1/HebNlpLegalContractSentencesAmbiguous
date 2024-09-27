import os
import sqlite3
from pdfminer.high_level import extract_text
from hebrew_tokenizer import tokenize
import stanza

# Download the Hebrew model if you haven't already
stanza.download('he')

# Load the Hebrew pipeline
nlp = stanza.Pipeline('he')

def stanza_tokenize_sentences(text):
    doc = nlp(text)
    return [sentence.text for sentence in doc.sentences]
def reverse_hebrew_text(text):
    return text[::-1]

def tokenize_hebrew_sentences(text):
    tokens = tokenize(text)
    sentences = []
    current_sentence = ''
    for token_type, token_text, line_number, (start_index, end_index) in tokens:
        print(token_text)
        if token_type == 'PUNCTUATION':
            current_sentence += token_text  # No space before punctuation
        else:
            current_sentence += ' ' + token_text
        if token_text == '.':
            sentences.append(current_sentence.strip() + " ")
            current_sentence = ''
    if current_sentence.strip():
        if len(current_sentence.split(" ")) >=3 :
            sentences.append(current_sentence.strip())
    return sentences

conn = sqlite3.connect('HebrewContractSentences.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sentences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sentence TEXT NOT NULL,
        ambiguous BOOLEAN NULL,
        source_file TEXT NOT NULL
    )
''')
conn.commit()

def process_pdfs(directory_path):
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            print(f"Processing {file_path}...")
            try:
                # Extract text from the PDF
                text = extract_text(file_path)
                if text:
                    # Reverse the text for correct Hebrew order
                    text = reverse_hebrew_text(text)
                    # Split text into sentences
                    sentences = stanza_tokenize_sentences(text)
                    # Save sentences to the database
                    save_sentences_to_db(sentences, filename)
                else:
                    print(f"No text found in {file_path}.")
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

def save_sentences_to_db(sentences, source_file):
    for sentence in sentences:
        # Clean up the sentence
        sentence = sentence.strip()
        # Split the sentence into words
        words = sentence.split()
        # Check if the sentence has at least 3 words
        if len(words) > 3:
            cursor.execute('INSERT INTO sentences (sentence, source_file) VALUES (?, ?)', (sentence, source_file))
    conn.commit()


if __name__ == '__main__':
    directory_path = './contracts'  # Replace with your actual folder path
    process_pdfs(directory_path)
    conn.close()
    print("Processing complete.")
