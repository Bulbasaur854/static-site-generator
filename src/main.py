import os
from htmlnode import *
from textnode import *
from inline_markdown import *

def main():
    copy_static_to_public()

def copy_static_to_public(path):
    # print(os.listdir("static"))
    if os.path.isfile(path):
        

if __name__=="__main__":
    main()