import os
import shutil

def copy_files(src_path, dst_path):
    if (os.path.isfile(src_path)):
        shutil.copy(src_path, dst_path) 
        print(f"copied: {src_path} --> {dst_path}")
    else:
        # if source is a directory, make sure it exists in destination
        if not os.path.exists(dst_path):
            os.mkdir(dst_path) 

        # process all items in the directory
        for item in os.listdir(src_path):
            source_item = os.path.join(src_path, item)
            dest_item = os.path.join(dst_path, item)
            copy_files(source_item, dest_item)