from fastapi import FastAPI, HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import Dict, List
import os

app = FastAPI(title="📁 Smart File Organizer")

app.add_middleware(
CORSMiddleware,
allow_origins=[""],
allow_credentials=True,
allow_methods=[""],
allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Smart File Organizer backend is running."}

@app.get("/scan", response_model=Dict[str, List[str]])
def scan_folder(path: str = Query(..., description="Absolute path to folder")):
    folder = Path(path)

    if not folder.exists() or not folder.is_dir():
        raise HTTPException(status_code=400, detail="Folder does not exist or is not a directory.")

    file_map: Dict[str, List[str]] = {}

    for item in folder.rglob("*"):
        if item.is_file():
            ext = item.suffix.lower().lstrip(".") or "no_extension"
            file_map.setdefault(ext, []).append(item.name)

    return file_map