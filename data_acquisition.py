import os
import shutil
import time

SOURCE_DIR = 'source_data'
LANDING_DIR = 'landing_area'
FILE_TO_REMOVE = 'dummy.txt'
def move_files():
    for filename in os.listdir(SOURCE_DIR):
        source_file = os.path.join(SOURCE_DIR, filename)
        destination_file = os.path.join(LANDING_DIR, filename)
        if os.path.isfile(source_file):
            shutil.move(source_file, destination_file)
            print(f"Moved: {source_file} -> {destination_file}")

def remove_dummy_file():
    file_path = os.path.join(LANDING_DIR, FILE_TO_REMOVE)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed: {file_path}")

if __name__ == "__main__":
    while True:
        move_files()
        remove_dummy_file()


