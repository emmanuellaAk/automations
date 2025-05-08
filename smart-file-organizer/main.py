import argparse
from pathlib import Path
from datetime import datetime
import logging

log_path = Path("file_move_log.txt")
logging.basicConfig(filename=log_path, level=logging.INFO, format="%(message)s")

def organize_files(folder: Path, dry_run: bool = False):
    if not folder.exists():
        print("❌ Folder does not exist.")
        return

    for item in folder.iterdir():
        if item.is_file():
            file_ext = item.suffix.lower().lstrip('.')
            target_folder = folder / (file_ext.upper() if file_ext else "no_extension")
            destination = target_folder / item.name

            if dry_run:
                print(f"[DRY RUN] Would move {item.name} → {target_folder.name}/")
                logging.info(f"{datetime.now()} | DRY RUN | Would move: {item.name} | From: {item.parent} | To: {target_folder}")
            else:
                target_folder.mkdir(exist_ok=True)
                item.rename(destination)
                logging.info(f"{datetime.now()} | Moved: {item.name} | From: {item.parent} | To: {target_folder}")
                print(f"✅ Moved {item.name} → {target_folder.name}/")

def undo_last_move():
    with log_path.open("r") as log_file:
        lines = log_file.readlines()

    for i in range(len(lines) - 1, -1, -1):
        if "Moved:" in lines[i]:
            last_move = lines[i]
            break
    else:
        print("⚠️ No real moves found to undo.")
        return

    try:
        _, moved_part, from_part, to_part = last_move.strip().split(" | ")
        file_name = moved_part.replace("Moved:", "").strip()
        source_folder = from_part.replace("From:", "").strip()
        dest_folder = to_part.replace("To:", "").strip()

        source_path = Path(source_folder) / file_name
        dest_path = Path(dest_folder) / file_name

        if dest_path.exists():
            dest_path.rename(source_path)
            print(f"🔄 Undo complete: {file_name} moved back to {source_folder}")
            del lines[i]
            with log_path.open("w") as log_file:
                log_file.writelines(lines)
            # Remove empty dest folder
            if not any(Path(dest_folder).iterdir()):
                Path(dest_folder).rmdir()
        else:
            print("⚠️ File not found in destination. Cannot undo.")
    except Exception as e:
        print("❌ Error during undo:", e)

def undo_all():
    while True:
        with log_path.open("r") as log_file:
            lines = log_file.readlines()
        if not any("Moved:" in line for line in lines):
            break
        undo_last_move()

def main():
    parser = argparse.ArgumentParser(description="Smart File Organizer CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # organize command
    organize_parser = subparsers.add_parser("organize", help="Organize files in a folder")
    organize_parser.add_argument("--folder", type=str, required=True, help="Folder to organize")
    organize_parser.add_argument("--dry-run", action="store_true", help="Simulate the organizing process")

    # undo command
    subparsers.add_parser("undo", help="Undo the last move")

    # undo-all command
    subparsers.add_parser("undo-all", help="Undo all moves")

    args = parser.parse_args()

    if args.command == "organize":
        organize_files(Path(args.folder), dry_run=args.dry_run)
    elif args.command == "undo":
        undo_last_move()
    elif args.command == "undo-all":
        undo_all()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


