from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import fitz  # PyMuPDF for PDF text extraction
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import pandas as pd  # For handling Excel files
import nltk
from nltk.corpus import stopwords
import logging

# Set up logging to monitor API responses
logging.basicConfig(level=logging.INFO)

# Download stopwords (only if not previously downloaded)
nltk.download('stopwords', quiet=True)

# Initialize FastAPI application
app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define response model for terms
class TermResponse(BaseModel):
    term: str
    definition: str

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

# Adjust paths as necessary
MEDICAL_TERMS = load_medical_terms('medical_terms.txt')
COMMON_WORDS = load_common_words('common.txt')
STOPWORDS = set(stopwords.words('english'))

# Load definitions from Excel file
def load_definitions_from_excel(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_excel(file_path)

# Initialize definitions DataFrame
DEFINITIONS_DF = load_definitions_from_excel('Book.xlsx')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    text = ""
    pdf_document = fitz.open(stream=pdf_file.file.read(), filetype="pdf")
    for page in pdf_document:
        text += page.get_text()
    pdf_document.close()
    return text

# Function to get definition from Excel
def get_definition_from_excel(word: str) -> str:
    result = DEFINITIONS_DF[DEFINITIONS_DF['WORD'].str.lower() == word.lower()]
    if not result.empty:
        return result['DEFINITION'].values[0]
    return "Definition not found."

# Function to filter and find medical terms in extracted text
def filter_medical_terms(text: str) -> list:
    words = text.split()
    return [
        word for word in words
        if word.lower() in MEDICAL_TERMS and
           word.isalpha() and
           word.lower() not in STOPWORDS and
           word.lower() not in COMMON_WORDS
    ]

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")
    
    # Extract text from the PDF file
    pdf_text = extract_text_from_pdf(file)

    # Find the text following the "TECHNIQUE" section
    technique_index = pdf_text.find("TECHNIQUE:")
    if technique_index != -1:
        technique_text = pdf_text[technique_index:]
        technique_content = ' '.join(technique_text.splitlines()[1:])
    else:
        technique_content = pdf_text
    
    # Filter words that match medical terms and are not stopwords or common words
    medical_words = filter_medical_terms(technique_content)
    
    # Retrieve unique medical terms for frontend highlighting
    unique_medical_words = list(set(medical_words))

    # Return extracted text and highlighted medical terms
    return JSONResponse(content={
        "pdf_text": pdf_text,
        "highlighted_words": unique_medical_words
    })

@app.get("/get_definition/{word}", response_model=TermResponse)
async def get_definition(word: str):
    definition = get_definition_from_excel(word)
    return {"term": word, "definition": definition}
