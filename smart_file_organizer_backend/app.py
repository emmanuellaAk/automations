from fastapi import FastAPI, Query
from pathlib import Path
from typing import Optional
from file_ops import (
    organize_files, undo_last_move, undo_all,
    redo_last_move, redo_all
)

app = FastAPI(title="Smart File Organizer API")

@app.post("/organize")
def api_organize(folder: str = Query(...), dry_run: Optional[bool] = False):
    return organize_files(Path(folder), dry_run)

@app.post("/undo")
def api_undo():
    return undo_last_move()

@app.post("/undo-all")
def api_undo_all():
    return undo_all()

@app.post("/redo")
def api_redo():
    return redo_last_move()

@app.post("/redo-all")
def api_redo_all():
    return redo_all()