import json
from pathlib import Path

def detect_extensions(folder_path: Path, output_file: Path = Path("detected_extensions.json")):
    extensions = set()

    for item in folder_path.iterdir():
        if item.is_file():
            ext = item.suffix.lower().lstrip('.')
            if ext:
                extensions.add(ext)

    config = {"UNASSIGNED": sorted(extensions)}
    output_file.write_text(json.dumps(config, indent=4))
    print(f"✅ Detected {len(extensions)} extensions.")
    print(f"🔍 Saved to {output_file}")

if __name__ == "__main__":
    folder = Path(r"C:\Users\DELL LATITTUDE 7280\Desktop\logic")  # Change as needed
    detect_extensions(folder)
