from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
from datetime import datetime
import logging
import shutil
import os

app = FastAPI(title="Smart File Organizer API")

log_path = Path("file_move_log.txt")
logging.basicConfig(filename=log_path, level=logging.INFO, format="%(message)s")

class OrganizeRequest(BaseModel):
    folder: str
    dry_run: Optional[bool] = False

@app.post("/organize")
def organize_files(request: OrganizeRequest):
    folder = Path(request.folder)
    dry_run = request.dry_run

    if not folder.exists():
        return {"status": "error", "message": "Folder does not exist."}

    result = []
    for item in folder.iterdir():
        if item.is_file():
            file_ext = item.suffix.lower().lstrip('.')
            target_folder = folder / (file_ext.upper() if file_ext else "no_extension")
            destination = target_folder / item.name

            if dry_run:
                msg = f"[DRY RUN] Would move {item.name} → {target_folder.name}/"
                logging.info(f"{datetime.now()} | DRY RUN | Would move: {item.name} | From: {item.parent} | To: {target_folder}")
            else:
                target_folder.mkdir(exist_ok=True)
                item.rename(destination)
                msg = f"✅ Moved {item.name} → {target_folder.name}/"
                logging.info(f"{datetime.now()} | Moved: {item.name} | From: {item.parent} | To: {target_folder}")
            result.append(msg)

    return {"status": "success", "log": result}

@app.post("/undo")
def undo_last_move():
    if not log_path.exists():
        return {"status": "error", "message": "No log file found."}

    with log_path.open("r") as log_file:
        lines = log_file.readlines()

    for i in range(len(lines) - 1, -1, -1):
        if "Moved:" in lines[i]:
            last_move = lines[i]
            break
    else:
        return {"status": "info", "message": "No real moves found to undo."}

    try:
        _, moved_part, from_part, to_part = last_move.strip().split(" | ")
        file_name = moved_part.replace("Moved:", "").strip()
        source_folder = from_part.replace("From:", "").strip()
        dest_folder = to_part.replace("To:", "").strip()

        source_path = Path(source_folder) / file_name
        dest_path = Path(dest_folder) / file_name

        if dest_path.exists():
            dest_path.rename(source_path)
            del lines[i]
            with log_path.open("w") as log_file:
                log_file.writelines(lines)
            if not any(Path(dest_folder).iterdir()):
                Path(dest_folder).rmdir()
            return {"status": "success", "message": f"Undo complete: {file_name} moved back to {source_folder}"}
        else:
            return {"status": "error", "message": "File not found in destination. Cannot undo."}
    except Exception as e:
        return {"status": "error", "message": f"Exception occurred: {str(e)}"}

@app.post("/undo-all")
def undo_all():
    if not log_path.exists():
        return {"status": "error", "message": "No log file found."}

    undone = []
    while True:
        with log_path.open("r") as log_file:
            lines = log_file.readlines()
        if not any("Moved:" in line for line in lines):
            break
        result = undo_last_move()
        if result.get("status") == "success":
            undone.append(result.get("message"))
        else:
            break

    return {"status": "success", "messages": undone}
