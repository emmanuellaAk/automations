import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(filename="file_move_log.txt", level=logging.INFO, format="%(message)s")

DRY_RUN = True
folder_to_organize = Path(r"C:\Users\DELL LATITTUDE 7280\Desktop\logic")
config_path = Path("organize_config.json")
# Load custom extension config
with config_path.open("r") as f:
    config = json.load(f)
# Reverse map: extension -> folder name
extension_to_folder = {}
for folder, extensions in config.items():
    for ext in extensions:
        extension_to_folder[ext] = folder

for item in folder_to_organize.iterdir():
    if item.is_file():
        ext = item.suffix.lower().lstrip('.')
        folder_name = extension_to_folder.get(ext, "Others")
        target_folder = folder_to_organize / folder_name
        destination = target_folder / item.name

        if not DRY_RUN:
            target_folder.mkdir(exist_ok=True)
            item.rename(destination)
            log_message = f"{datetime.now()} | Moved: {item.name} | From: {item.parent} | To: {target_folder}"
            logging.info(log_message)
            print(f"✅ Moved {item.name} → {folder_name}/")
        else:
            print(f"[DRY RUN] Would move {item.name} → {folder_name}/")
