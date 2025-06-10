from textnode import TextNode
from fixed_variables import TextType, source, dest, markdown_path
import os
import shutil
import re
from codesplit import markdown_to_html_node


def copy_dir(src, dest):           #"manual" recursive copying for practice

    local_contents = os.listdir(src)

    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    for file in local_contents:
        path = src + f"/{file}"
        if os.path.isfile(path):
            shutil.copy(path,dest)
        if os.path.isdir(path):
            new_dest = dest + f"/{file}"
            os.mkdir(new_dest)
            copy_dir(path, new_dest)
    return

def extract_title():
    file = open(markdown_path + "/index.md")
    markdown = file.read()
    title = re.search(r"(^|\n)# .*", markdown).group().strip("# ")
    return title

class Default(dict):

    def __missing__(self, key):
        return key

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path + "/index.md")
    text = file.read()
    file.close()
    template = open(template_path + "/template.html").read()

    Title = extract_title()
    html_string = markdown_to_html_node(text).to_html()

    output = template.format(Title, html_string)
    
    return output


def main():
    
    copy_dir(source, dest)
    page = generate_page(markdown_path, markdown_path, dest)
    dest_file = open(dest + "/index.html",'w')
    dest_file.write(page)


main()