from fastapi import FastAPI, Query
from pathlib import Path
from datetime import datetime
import logging
from typing import Optional
import shutil

app = FastAPI()

log_path = Path("file_move_log.txt")
redo_log_path = Path("file_redo_log.txt")
logging.basicConfig(filename=log_path, level=logging.INFO, format="%(message)s")


def organize_files(folder: Path, dry_run: bool = False):
    if not folder.exists():
        return {"status": "error", "message": "Folder does not exist."}

    organized = []
    for item in folder.iterdir():
        if item.is_file():
            file_ext = item.suffix.lower().lstrip('.')
            target_folder = folder / (file_ext.upper() if file_ext else "no_extension")
            destination = target_folder / item.name

            if dry_run:
                organized.append(f"[DRY RUN] Would move {item.name} → {target_folder.name}/")
                logging.info(f"{datetime.now()} | DRY RUN | Would move: {item.name} | From: {item.parent} | To: {target_folder}")
            else:
                target_folder.mkdir(exist_ok=True)
                item.rename(destination)
                log_msg = f"{datetime.now()} | Moved: {item.name} | From: {item.parent} | To: {target_folder}"
                logging.info(log_msg)
                organized.append(f"✅ Moved {item.name} → {target_folder.name}/")
    return {"status": "success", "details": organized}

def undo_last_move():
    try:
        with log_path.open("r") as log_file:
            lines = log_file.readlines()

        for i in range(len(lines) - 1, -1, -1):
            if "Moved:" in lines[i]:
                last_move = lines[i]
                break
        else:
            return {"status": "warning", "message": "No real moves to undo."}

        _, moved_part, from_part, to_part = last_move.strip().split(" | ")
        file_name = moved_part.replace("Moved:", "").strip()
        source_folder = Path(from_part.replace("From:", "").strip())
        dest_folder = Path(to_part.replace("To:", "").strip())
        source_path = source_folder / file_name
        dest_path = dest_folder / file_name

        if dest_path.exists():
            dest_path.rename(source_path)
            with redo_log_path.open("a") as redo_log:
                redo_log.write(last_move)

            del lines[i]
            with log_path.open("w") as log_file:
                log_file.writelines(lines)

            if not any(dest_folder.iterdir()):
                dest_folder.rmdir()

            return {"status": "success", "message": f"Undo complete: {file_name} moved back to {source_folder}"}
        else:
            return {"status": "error", "message": "File not found in destination. Cannot undo."}
    except Exception as e:
        return {"status": "error", "message": f"Error during undo: {str(e)}"}

def undo_all():
    results = []
    while True:
        with log_path.open("r") as log_file:
            lines = log_file.readlines()
        if not any("Moved:" in line for line in lines):
            break
        result = undo_last_move()
        if result["status"] != "success":
            break
        results.append(result["message"])
    return {"status": "done", "details": results}


def redo_last_move():
    if not redo_log_path.exists():
        return {"status": "error", "message": "No redo log found."}

    lines = redo_log_path.read_text().splitlines()
    for i in range(len(lines) - 1, -1, -1):
        if "Moved:" in lines[i]:
            last_redo = lines[i]
            break
    else:
        return {"status": "warning", "message": "No moves to redo."}

    try:
        _, moved_part, from_part, to_part = last_redo.strip().split(" | ")
        file_name = moved_part.replace("Moved:", "").strip()
        source_folder = Path(from_part.replace("From:", "").strip())
        dest_folder = Path(to_part.replace("To:", "").strip())
        source_path = source_folder / file_name
        dest_path = dest_folder / file_name

        if source_path.exists():
            dest_folder.mkdir(exist_ok=True)
            source_path.rename(dest_path)
            with log_path.open("a") as log_file:
                log_file.write(last_redo + "\n")
            updated_redo_log = lines[:i] + lines[i+1:]
            redo_log_path.write_text("\n".join(updated_redo_log) + "\n")
            return {"status": "success", "message": f"Redo complete: {file_name} moved to {dest_folder}"}
        else:
            return {"status": "error", "message": "File not found in source to redo."}
    except Exception as e:
        return {"status": "error", "message": f"Error during redo: {str(e)}"}

def redo_all():
    results = []
    while True:
        result = redo_last_move()
        if result["status"] != "success":
            break
        results.append(result["message"])
    return {"status": "done", "details": results}


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
