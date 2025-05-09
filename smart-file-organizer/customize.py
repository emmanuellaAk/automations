# import json
# import logging
# from pathlib import Path
# from datetime import datetime

# logging.basicConfig(filename="file_move_log.txt", level=logging.INFO, format="%(message)s")

# DRY_RUN = True
# folder_to_organize = Path(r"C:\Users\DELL LATITTUDE 7280\Desktop\logic")
# config_path = Path("organize_config.json")
# # Load custom extension config
# with config_path.open("r") as f:
#     config = json.load(f)
# # Reverse map: extension -> folder name
# extension_to_folder = {}
# for folder, extensions in config.items():
#     for ext in extensions:
#         extension_to_folder[ext] = folder

# for item in folder_to_organize.iterdir():
#     if item.is_file():
#         ext = item.suffix.lower().lstrip('.')
#         folder_name = extension_to_folder.get(ext, "Others")
#         target_folder = folder_to_organize / folder_name
#         destination = target_folder / item.name

#         if not DRY_RUN:
#             target_folder.mkdir(exist_ok=True)
#             item.rename(destination)
#             log_message = f"{datetime.now()} | Moved: {item.name} | From: {item.parent} | To: {target_folder}"
#             logging.info(log_message)
#             print(f"✅ Moved {item.name} → {folder_name}/")
#         else:
#             print(f"[DRY RUN] Would move {item.name} → {folder_name}/")


# import json
# import logging
# import argparse
# from pathlib import Path
# from datetime import datetime

# logging.basicConfig(filename="file_move_log.txt", level=logging.INFO, format="%(message)s")

# def load_config(config_path: Path):
#     with config_path.open("r") as f:
#         config = json.load(f)
#     extension_to_folder = {}
#     for folder, extensions in config.items():
#         for ext in extensions:
#             extension_to_folder[ext.lower()] = folder
#     return extension_to_folder

# def organize_files(folder: Path, config: dict, dry_run: bool = True):
#     for item in folder.iterdir():
#         if item.is_file():
#             ext = item.suffix.lower().lstrip('.')
#             folder_name = config.get(ext, "Others")
#             target_folder = folder / folder_name
#             destination = target_folder / item.name

#             if not dry_run:
#                 target_folder.mkdir(exist_ok=True)
#                 item.rename(destination)
#                 log_message = f"{datetime.now()} | Moved: {item.name} | From: {item.parent} | To: {target_folder}"
#                 logging.info(log_message)
#                 print(f"✅ Moved {item.name} → {folder_name}/")
#             else:
#                 print(f"[DRY RUN] Would move {item.name} → {folder_name}/")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="📁 Smart File Organizer")
#     parser.add_argument("--folder", type=str, required=True, help="Path to the folder to organize")
#     parser.add_argument("--config", type=str, default="organize_config.json", help="Path to config JSON")
#     parser.add_argument("--dry-run", action="store_true", help="Simulate the organization without moving files")

#     args = parser.parse_args()

#     folder_path = Path(args.folder)
#     config_path = Path(args.config)

#     if not folder_path.exists():
#         print("❌ Error: Folder does not exist.")
#     elif not config_path.exists():
#         print("❌ Error: Config file does not exist.")
#     else:
#         extension_map = load_config(config_path)
#         organize_files(folder_path, extension_map, dry_run=args.dry_run)

import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(filename="file_move_log.txt", level=logging.INFO, format="%(message)s")

def load_config(config_path: Path):
    with config_path.open("r") as f:
        config = json.load(f)
    extension_to_folder = {}
    for folder, extensions in config.items():
        for ext in extensions:
            extension_to_folder[ext.lower()] = folder
    return extension_to_folder

def organize_files(folder: Path, config: dict, dry_run: bool = True):
    for item in folder.iterdir():
        if item.is_file():
            ext = item.suffix.lower().lstrip('.')
            folder_name = config.get(ext, "Others")
            target_folder = folder / folder_name
            destination = target_folder / item.name

            if not dry_run:
                target_folder.mkdir(exist_ok=True)
                item.rename(destination)
                log_message = f"{datetime.now()} | Moved: {item.name} | From: {item.parent} | To: {target_folder}"
                logging.info(log_message)
                print(f"✅ Moved {item.name} → {folder_name}/")
            else:
                print(f"[DRY RUN] Would move {item.name} → {folder_name}/")

def undo_last_move():
    log_path = Path("file_move_log.txt")

    with log_path.open("r") as log_file:
        lines = log_file.readlines()

    if not lines:
        print("No moves to undo.")
        return

    for i in range(len(lines) - 1, -1, -1):
        if "Moved:" in lines[i]:
            last_move = lines[i]
            break
    else:
        print("No real moves found in log.")
        return

    try:
        timestamp, moved_part, from_part, to_part = last_move.strip().split(" | ")

        file_name = moved_part.replace("Moved:", "").strip()
        source_folder = from_part.replace("From:", "").strip()
        dest_folder = to_part.replace("To:", "").strip()

        source_path = Path(source_folder) / file_name
        dest_path = Path(dest_folder) / file_name

        # Ask for confirmation before undoing
        confirmation = input(f"Are you sure you want to undo the move of {file_name}? (y/n): ").strip().lower()

        if confirmation == 'y':
            if dest_path.exists():
                dest_path.rename(source_path)
                print(f"✅ Undo complete: {file_name} moved back to {source_folder}")

                # Remove the undone entry from the log
                del lines[i]
                with log_path.open("w") as log_file:
                    log_file.writelines(lines)
            else:
                print("⚠️ File not found in destination. Cannot undo.")
        else:
            print("Undo operation canceled.")
    except Exception as e:
        print("Error while undoing:", e)

def undo_all_moves():
    log_path = Path("file_move_log.txt")

    with log_path.open("r") as log_file:
        lines = log_file.readlines()

    if not lines:
        print("No moves to undo.")
        return

    # Undo each move
    for i in range(len(lines) - 1, -1, -1):
        if "Moved:" in lines[i]:
            last_move = lines[i]
            try:
                timestamp, moved_part, from_part, to_part = last_move.strip().split(" | ")
                file_name = moved_part.replace("Moved:", "").strip()
                source_folder = from_part.replace("From:", "").strip()
                dest_folder = to_part.replace("To:", "").strip()

                source_path = Path(source_folder) / file_name
                dest_path = Path(dest_folder) / file_name

                if dest_path.exists():
                    dest_path.rename(source_path)
                    print(f"✅ Undo complete: {file_name} moved back to {source_folder}")

                    # Remove the undone entry from the log
                    del lines[i]
                    with log_path.open("w") as log_file:
                      log_file.writelines(lines)
                    dest_dir = Path(dest_folder)
                    if dest_dir.exists() and not any(dest_dir.iterdir()):
                        dest_dir.rmdir()
                    print(f"🧹 Removed empty folder: {dest_folder}")
                else:
                    print(f"⚠️ {file_name} not found in destination. Cannot undo this move.")
            except Exception as e:
                print("Error while undoing:", e)

    # Write the updated log back
    with log_path.open("w") as log_file:
        log_file.writelines(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="📁 Smart File Organizer")
    parser.add_argument("--folder", type=str, required=True, help="Path to the folder to organize")
    parser.add_argument("--config", type=str, default="organize_config.json", help="Path to config JSON")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the organization without moving files")
    parser.add_argument("--undo", action="store_true", help="Undo the last move")
    parser.add_argument("--undo-all", action="store_true", help="Undo all moves")

    args = parser.parse_args()

    folder_path = Path(args.folder)
    config_path = Path(args.config)

    if args.undo:
        undo_last_move()
    elif args.undo_all:
        undo_all_moves()
    else:
        if not folder_path.exists():
            print("❌ Error: Folder does not exist.")
        elif not config_path.exists():
            print("❌ Error: Config file does not exist.")
        else:
            extension_map = load_config(config_path)
            organize_files(folder_path, extension_map, dry_run=args.dry_run)

