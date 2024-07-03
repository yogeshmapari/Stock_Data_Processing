import time
import sys
import os
import subprocess
import glob
import random
# Hardcoded configuration parameters
CHECK_INTERVAL = 5  # Check for new files every 5 seconds

def process_files(folder_path):
    files = glob.glob(os.path.join(folder_path, '*.txt'))  # Adjust the pattern as needed
    random.shuffle(files)
    for file_path in files:
        print(f"Processing file: {file_path}")
        subprocess.run(['python', 'raw_load.py', file_path])

if __name__ == "__main__":


    folder_path = "landing_area"

    

    print(f"Monitoring folder: {folder_path}")

    while True:
        process_files(folder_path)
        time.sleep(CHECK_INTERVAL)
