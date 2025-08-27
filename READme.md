A Python-powered file organization system with undo/redo functionality, logging, and a REST API backend (FastAPI).
It automatically organizes files into folders, keeps track of moves, and allows undo/redo operations — making file management safe and customizable.

Features
	•	Organize files into categorized folders (Documents, Images, Videos, etc.)
	•	Customizable organization rules via organize_config.json
	•	Undo the last move or redo it (safe file handling)
	•	Logs all operations for transparency
	•	REST API built with FastAPI
	•	Lightweight, easy to run locally

Installation & Setup

git clone https://github.com/YOUR-USERNAME/smart_file_organizer_backend.git
cd smart_file_organizer_backend

Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

Install dependencies:
pip install -r requirements.txt

Run the server:
uvicorn app:app --reload

The server will start at: http://127.0.0.1:8000

API Endpoints
	•	POST /organize → Organize files
	•	POST /undo → Undo last move
	•	POST /redo → Redo last undone move
	•	GET /logs → Fetch operation logs


Tech Stack
	•	Python 3.10+
	•	FastAPI (REST API framework)
	•	Uvicorn (ASGI server)
