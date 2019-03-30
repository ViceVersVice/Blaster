import os
import shutil

def remove_cache():
    allowed_extensions = [".py", ".pyc"]
    allowed_directories = ["__pycache__"]
    
    for root, dirs, files in os.walk("."):
        print(root)
        for name in files:
            
            file_extension = os.path.splitext(name)[1]
            if file_extension not in allowed_extensions:
                pathname = os.path.join(root, name)
                print(pathname)
                os.remove(pathname)      
        for directory in dirs:
            if directory not in allowed_directories:
                #shutil.rmtree(directory)
                pass





