from pathlib import Path
import logging

# Paths for logs
log_path = Path("logs/file_move_log.txt")
redo_log_path = Path("logs/file_redo_log.txt")

# Ensure logs directory exists
log_path.parent.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(message)s"
)