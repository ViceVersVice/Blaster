import os
import shutil
import re

def remove_cache(route):
    """Removes subfolders with user input files

    Args
        route: str
            path for user folder with user input subfolders
    """

    allowed_extensions = [".py", ".pyc", ".gitignore"]
    allowed_directories = ["__pycache__"]
    if re.search(r"tool$", route) != None: #check path for safety
        for root, dirs, files in os.walk(route):
            for directory in dirs:
               if directory not in allowed_directories:
                   dir_path = os.path.join(root, directory)
                   print("REMOVED_DIR:", dir_path)
                   shutil.rmtree(dir_path)
            # for name in files:
            #     file_extension = os.path.splitext(name)[1]
            #     if file_extension not in allowed_extensions and name != ".gitignore":
            #         pathname = os.path.join(root, name)
            #         print("REMOVED_FILE:", pathname)
            #         os.remove(pathname)
