import os
import fitz
from fastapi import UploadFile
import pandas as pd
import re

# Load medical terms from a file
def load_medical_terms(file_path: str) -> set:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as file:
        return set(line.strip().lower() for line in file if line.strip())

# Load common words from a file
def load_common_words(file_path: str) -> set:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as file:
        return set(line.strip().lower() for line in file)

MEDICAL_TERMS = load_medical_terms('wordlist-mvp.txt')
COMMON_WORDS = load_common_words('common.txt')

# Load definitions from an Excel file
def load_definitions_from_excel(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_excel(file_path)

DEFINITIONS_DF = load_definitions_from_excel('medical_dataset.xlsx')

# Extract text from a PDF file
def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    text = ""
    pdf_document = fitz.open(stream=pdf_file.file.read(), filetype="pdf")
    for page in pdf_document:
        text += page.get_text()
    pdf_document.close()
    return text

# Get the definition of a word from the Excel file
def get_definition_from_excel(word: str, language: str = 'en'):
    word_column = 'WORD_EN'
    definition_column = 'DEFINITION_EN' if language == 'en' else 'DEFINITION_TA'
    image_column = 'IMAGE_EN' if language == 'en' else 'IMAGE_TA'
    
    if word_column not in DEFINITIONS_DF.columns:
        return word, "Definition not found.", None

    result = DEFINITIONS_DF[DEFINITIONS_DF[word_column].str.lower() == word.lower()]
    if not result.empty:
        term = result['WORD_TA'].values[0] if language == 'ta' else word
        definition = result[definition_column].values[0]
        image = result[image_column].values[0] if image_column in DEFINITIONS_DF.columns and not pd.isna(result[image_column].values[0]) else None
        return term, definition, image
    return word, "Definition not found.", None

# Filter medical terms from the text
def filter_medical_terms(text: str) -> list:
    highlighted_terms = []
    
    # Iterate over each medical term/phrase in the wordlist
    for term in MEDICAL_TERMS:
        # Create a regex pattern to match the term as a whole word/phrase
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        
        # Search for the term in the original text
        matches = pattern.findall(text)
        
        # If matches are found, extend the highlighted terms with the matches in their original case
        if matches:
            highlighted_terms.extend(matches)
    
    return highlighted_terms
