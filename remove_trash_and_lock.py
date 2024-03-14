# This script parses a folder structure and removes old `.trash` folders and lock files
# Was created to cleanup years worth of junk trash files on a file server

import os
import datetime
import argparse
import shutil

def is_old_file(file_path):
    modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    time_difference = (datetime.datetime.now() - modified_time).days
    return time_difference > 365

def delete_file_or_folder(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)  # Recursively remove directories
        return "Deleted"
    except Exception as e:
        return f"Error: {str(e)}"

def search_and_delete(directory):
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.startswith(".~lock.") and is_old_file(file_path):
                result = (file_path, os.path.getmtime(file_path), delete_file_or_folder(file_path))
                results.append(result)
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if folder.startswith(".Trash") and is_old_file(folder_path):
                result = (folder_path, os.path.getmtime(folder_path), delete_file_or_folder(folder_path))
                results.append(result)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for and delete old .~lock. files and .Trash folders.")
    parser.add_argument("directory", help="Directory to search for files and folders.")
    args = parser.parse_args()

    directory_to_search = args.directory

    results = search_and_delete(directory_to_search)

    for result in results:
        file_or_folder = result[0]
        modified_time = datetime.datetime.fromtimestamp(result[1])
        deleted_status = result[2]
        print(f"{file_or_folder},{modified_time},{deleted_status}")

