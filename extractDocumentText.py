# importing required modules
from pathlib import Path
from PyPDF2 import PdfReader

def extractDocumentText(path: Path):   
    # creating a pdf reader object
    reader = PdfReader(path)
    pdf_content = ""
    for i in list(range(0, len(reader.pages))):
        # getting a specific page from the pdf file
        page = reader.pages[i]
        
        # extracting text from page
        text = page.extract_text()
        pdf_content += text
    return pdf_content