import os
import shutil
import re

def remove_cache(route):
    allowed_extensions = [".py", ".pyc", ".gitignore"]
    allowed_directories = ["__pycache__"]
    #check for safety
    if re.search(r"tool$", route) != None:
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
