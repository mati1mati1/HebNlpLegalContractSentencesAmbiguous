Hebrew Contract Ambiguity Detection Project
This repository contains scripts and tools for an NLP project aimed at determining whether sentences in Hebrew contracts are ambiguous or not. The project involves extracting sentences from Hebrew contract PDFs, storing them in a SQLite database, and providing a GUI for manual labeling of sentence ambiguity.

Table of Contents
Overview
Prerequisites
Installation
Directory Structure
Usage
1. Extracting Sentences from PDFs
2. Labeling Sentences Using the GUI
Scripts
PdfSentenceScraping.py
SentenceLabelerUI.py
Database Schema
Notes and Considerations
License
Acknowledgments
Overview
The goal of this project is to create a dataset of sentences extracted from Hebrew contracts, labeled as ambiguous or not, to train an NLP model for ambiguity detection. The project consists of:

Extracting text from PDF contracts.
Tokenizing and splitting the text into sentences.
Storing the sentences in a SQLite database.
Providing a GUI tool for manual labeling of sentences.
Prerequisites
Ensure you have the following installed:

Python 3.6 or higher
pip package manager
Python Libraries:

pdfminer.six for PDF text extraction
hebrew_tokenizer for Hebrew text tokenization
python-bidi for handling bidirectional text (Hebrew)
tkinter for the GUI application (comes with Python)
sqlite3 for database interactions (comes with Python)
