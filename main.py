import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to the database
conn = sqlite3.connect('HebrowContractSentences.db')
cursor = conn.cursor()

def fetch_sentences():
    cursor.execute("SELECT id, sentence FROM sentences WHERE ambiguous IS NULL")
    return cursor.fetchall()

class SentenceLabelerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sentence Labeling Tool")

        self.sentences = fetch_sentences()
        self.index = 0

        if not self.sentences:
            messagebox.showinfo("Info", "No sentences to label.")
            self.master.destroy()
            return

        self.current_sentence_id = None
        self.current_sentence = None

        self.create_widgets()
        self.display_sentence()

    def create_widgets(self):
        # Sentence display
        self.sentence_label = tk.Label(self.master, text="", wraplength=500, font=("Arial", 16), justify="right")
        self.sentence_label.pack(pady=20)

        # Button frame
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)

        # Ambiguous button
        self.ambiguous_button = tk.Button(
            self.button_frame,
            text="Ambiguous",
            command=lambda: self.save_label(True),
            width=15
        )
        self.ambiguous_button.grid(row=0, column=0, padx=5)

        # Not Ambiguous button
        self.not_ambiguous_button = tk.Button(
            self.button_frame,
            text="Not Ambiguous",
            command=lambda: self.save_label(False),
            width=15
        )
        self.not_ambiguous_button.grid(row=0, column=1, padx=5)

        # Delete button
        self.delete_button = tk.Button(
            self.button_frame,
            text="Delete",
            command=self.delete_sentence,
            width=15,
            fg="red"
        )
        self.delete_button.grid(row=0, column=2, padx=5)

        # Progress label
        self.progress_label = tk.Label(self.master, text="")
        self.progress_label.pack(pady=5)

    def display_sentence(self):
        if self.index < len(self.sentences):
            self.current_sentence_id, self.current_sentence = self.sentences[self.index]
            self.sentence_label.config(text=self.current_sentence)
            self.update_progress()
        else:
            messagebox.showinfo("Info", "All sentences have been labeled.")
            self.master.destroy()

    def update_progress(self):
        total = len(self.sentences)
        current = self.index + 1
        self.progress_label.config(text=f"Sentence {current} of {total}")

    def save_label(self, is_ambiguous):
        # Update the database with the ambiguous value
        cursor.execute("UPDATE sentences SET ambiguous = ? WHERE id = ?", (is_ambiguous, self.current_sentence_id))
        conn.commit()

        # Move to the next sentence
        self.index += 1
        self.display_sentence()

    def delete_sentence(self):
        # Confirm deletion
        confirm = messagebox.askyesno("Delete Sentence", "Are you sure you want to delete this sentence?")
        if confirm:
            # Delete the sentence from the database
            cursor.execute("DELETE FROM sentences WHERE id = ?", (self.current_sentence_id,))
            conn.commit()

            # Remove the sentence from the local list
            del self.sentences[self.index]

            # Adjust the index since we've removed the current sentence
            if self.index >= len(self.sentences):
                self.index = len(self.sentences) - 1

            # Display the next sentence
            self.display_sentence()

if __name__ == "__main__":
    root = tk.Tk()
    app = SentenceLabelerApp(root)
    root.mainloop()
    conn.close()
