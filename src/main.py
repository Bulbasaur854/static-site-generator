import os, shutil
from copy_static import *

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    # delete contents of `public` folder if it exists
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)

    copy_files(dir_path_static, dir_path_public)

if __name__=="__main__":
    main()