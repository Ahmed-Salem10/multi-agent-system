from pathlib import Path 
from typing import Any 
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def pdf_loader(file_path:str|Path)->list[dict[str,Any]]:
    file_path=Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found :{file_path}")
    if file_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDf file got :{file_path}")
    documents=[]

    loader = PyPDFLoader(str(file_path))
    file_pages = loader.load()

    for page in file_pages: 
        text=page.page_content.strip()
        if text:
            documents.append(Document(
                page_content=text,
                metadata={
                    "file_name":file_path.name,
                    "file_type":"pdf",
                    "page":page.metadata.get("page",0)+1
                },
            )
            )

    return documents