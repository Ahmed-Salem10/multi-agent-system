from pathlib import Path
from typing import Any 
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document

def docx_loader(file_path:str|Path)->list[dict[str,Any]]:
    file_path=Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"docx file not found :{file_path}")

    if file_path.suffix.lower() !=".docx":
        raise ValueError(f"Expected a docx file got :{file_path}")

    documents=[]
    pages=Docx2txtLoader(str(file_path)).load

    for page in pages:
        text=page.page_content.strip()
        if text:
            documents.append(Document(

            page_content=text,
            metadata={
                "file_name":file_path.name,
                "file_type":"docx",
               
            }
        ))
