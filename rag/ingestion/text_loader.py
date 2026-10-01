from pathlib import Path 
from typing import Any
from langchain_core.documents import Document

def text_loader(file_path:str|Path, encoding: str = "utf-8")->list[dict[str,Any]]:

    file_path=Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"file not found :{file_path}")
    
    if file_path.suffix.lower() != ".txt":
        raise ValueError(f"Expected text file got :{file_path}")

    
    text=file_path.read_text(encoding=encoding).strip()
    if not text:
        return[]


    return [Document(
    page_content=text,
    metadata={"file_name": file_path.name, "file_type": "txt"},
    )]

