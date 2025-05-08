from pathlib import Path
import logging

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
                else:
                    print(f"⚠️ {file_name} not found in destination. Cannot undo this move.")
            except Exception as e:
                print("Error while undoing:", e)

    # Write the updated log back
    with log_path.open("w") as log_file:
        log_file.writelines(lines)

# Run undo for a single move
# undo_last_move()

# Or run undo for all moves
undo_all_moves()
