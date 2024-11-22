from fastapi import APIRouter, Depends
from fastapi import FastAPI, HTTPException, File, UploadFile, Query
from fastapi.responses import JSONResponse
from services.functions import extract_text_from_pdf, filter_medical_terms, get_definition_from_excel
from schema.auth_model import TermResponse
import logging
import nltk
import base64

logging.basicConfig(level=logging.INFO)

nltk.download('stopwords', quiet=True)

router = APIRouter()

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")
    
    pdf_text = extract_text_from_pdf(file)
    technique_index = pdf_text.find("TECHNIQUE:")
    if technique_index != -1:
        technique_content = pdf_text[technique_index:]
    else:
        technique_content = pdf_text
    
    medical_words = filter_medical_terms(technique_content)
    unique_medical_words = list(set(medical_words))
    response_data = []

    for word in unique_medical_words:
        definition, image = get_definition_from_excel(word, language='en')[1:]  # Only get definition and image
        response_data.append({
            "term": word,
            "has_image": bool(image)
        })
    
    return JSONResponse(content={
        "pdf_text": pdf_text,
        "highlighted_words": response_data
    })

@router.get("/get_definition/{word}", response_model=TermResponse)
async def get_definition(word: str, language: str = Query(..., regex="^(en|ta)$")):
    term, definition, image = get_definition_from_excel(word, language)
    response = {"term": term, "definition": definition}
    if image:
        response["image"] = image
    return JSONResponse(content=response)