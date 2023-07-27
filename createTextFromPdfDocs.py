import os
from extractDocumentText import extractDocumentText
import logging

logger = logging.getLogger(__name__)

def createTextFromPdfDocs(folder_path, dest_path):
    text_docs = [] #[date, title, file_path][]
    items = os.listdir(folder_path)
    for item in items:
        item_path = os.path.join(folder_path, item)
        extracted_text = extractDocumentText(item_path)
        if len(extracted_text) == 0:
            logger.warning("Cannot extract text for %s.", item_path)
            continue
        file_name = item.replace('.pdf', '')
        file_name_list = file_name.split('_')
        title = " ".join(file_name_list[1:-1])
        date = file_name_list[-1]
        dest_file_path = os.path.join(dest_path, f"{item.replace('.pdf', '')}.txt")
        
        with open(dest_file_path, "w", newline="") as text_file:
            text_file.write(extracted_text)
        
        text_docs.append([date, title, dest_file_path])
        logger.info("Created %s", dest_file_path)
    return text_docs
