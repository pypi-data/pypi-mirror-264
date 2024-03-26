import os
from typing import List


def find_delete_files(folder_path: str, target_extensions: List[str], target_suffix: str):
    counter = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            for target_extension in target_extensions:
                if file.lower().endswith(target_extension.lower()):
                    if target_suffix.lower() in file.lower():
                        counter += 1
                        file_path = os.path.join(root, file)
                        print("Deleting:", file_path)
                        # os.remove(file_path)
    print(f'Deleted {counter} files.')
    return counter