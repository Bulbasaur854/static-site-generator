import os, shutil
from markdown_blocks import *

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    # delete contents of `public` folder if it exists
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)

    # copy_files(dir_path_static, dir_path_public)

    title = extract_title("# Hello")
    print(title)

def copy_files(src_path, dst_path):
    if (os.path.isfile(src_path)):
        shutil.copy(src_path, dst_path) 
        print(f"copied: {src_path} --> {dst_path}")
    else:
        # if source is a directory, make sure it exists in destination
        if not os.path.exists(dst_path):
            os.mkdir(dst_path) 

        # recursively process all items in the directory
        for item in os.listdir(src_path):
            source_item = os.path.join(src_path, item)
            dest_item = os.path.join(dst_path, item)
            copy_files(source_item, dest_item)

def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)

    for block in markdown_blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if block[:2] == "# ":
                return block[2:].strip()
            
    raise Exception("invalid markdown input file: no `h1` block was found, could not generate title!")

if __name__=="__main__":
    main()