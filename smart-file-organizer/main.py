import os
import shutil
import logging
from datetime import datetime
from pathlib import Path


logging.basicConfig(filename ="file_move_log.txt", level=logging.INFO, format="%(message)s")
DRY_RUN = False
folder_to_organize = Path(r"C:\Users\DELL LATITTUDE 7280\Desktop\first-aurora-law-firm")

#check if folder exists
# print("Folder exists:", folder_to_organize.exists()) 
# Check if the folder exists
if not folder_to_organize.exists():
    print("Folder does not exist.")
    exit()
#loop through everything in the folder
for item in folder_to_organize.iterdir():
#Checks if it's a file (ignores folders)
  if item.is_file():
      #get the file extention
      #gets the file’s extension 
      #makes it lowercase — so .PDF becomes 
      #remove the dot 
      file_ext = item.suffix.lower().lstrip('.')    
      #print file name and its extensions
      # print(f"{item.name} → {file_ext}")

      if file_ext == '':
         target_folder = folder_to_organize/"no_extension"
      else:
         target_folder = folder_to_organize/file_ext.upper()
      destination = target_folder/item.name
      if not DRY_RUN:
            target_folder.mkdir(exist_ok = True)
            item.rename(destination)
             # Log the action
            log_message = f"{datetime.now()} | Moved: {item.name} | From: {item.parent} | To: {target_folder}"
            logging.info(log_message)
            print(f"Moved {item.name} → {target_folder.name}/")
      else: 
             log_message = f"{datetime.now()} | DRY RUN | Would move: {item.name} | From: {item.parent} | To: {target_folder}"
             # Log the dry run action
             logging.info(log_message)  
             print(f"[DRY RUN] Would move {item.name} -> {target_folder.name}/")


