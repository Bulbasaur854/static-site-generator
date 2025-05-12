import os, shutil
from markdown_blocks import *
from markdown_blocks import *

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
dir_path_template = "./template.html"

def main():
    # make sure `public` folder is empty and exists
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)

    # copy files from `static` folder to `public`
    copy_files_recursive(dir_path_static, dir_path_public)

    # generate html pages to `public` for every markdown file in `content`
    generate_pages_recursive(dir_path_content, dir_path_template, dir_path_public)

# Helper functions
# ----------------

def copy_files_recursive(src_path, dst_path):
    if os.path.isfile(src_path):
        shutil.copy(src_path, dst_path) 
        print(f"Copied: {src_path} --> {dst_path}")
    else:
        # if source is a directory, make sure it exists in destination
        if not os.path.exists(dst_path):
            os.mkdir(dst_path) 

        # recursively process all items in the directory
        for item in os.listdir(src_path):
            source_item = os.path.join(src_path, item)
            dest_item = os.path.join(dst_path, item)
            copy_files_recursive(source_item, dest_item)

def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)

    for block in markdown_blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if block[:2] == "# ":
                return block[2:].strip()
            
    raise Exception("invalid markdown input file: no `h1` block was found, could not generate title!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()

    new_content = markdown_to_html_node(markdown_content).to_html()
    new_title = extract_title(markdown_content)

    template_content = template_content.replace("{{ Title }}", new_title)
    template_content = template_content.replace("{{ Content }}", new_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):    
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path.replace(".md", ".html"))
    else:
        if not os.path.exists(dest_dir_path):
            os.makedirs(dest_dir_path, exist_ok=True)

        for item in os.listdir(dir_path_content):
            new_source = os.path.join(dir_path_content, item)
            new_dest = os.path.join(dest_dir_path, item)
            generate_pages_recursive(new_source, template_path, new_dest)

if __name__=="__main__":
    main()