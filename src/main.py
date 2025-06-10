from textnode import TextNode
from fixed_variables import TextType, source, dest, markdown_path, basepath
import os
import shutil
import re
from codesplit import markdown_to_html_node
import sys


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

def extract_title(from_path):
    file = open(from_path)
    markdown = file.read()
    title = re.search(r"(^|\n)# .*", markdown).group().strip("# ")
    return title

def generate_page(from_path, template_path, dest_path, filename = "index"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path)
    text = file.read()
    file.close()
    template = open(template_path).read()

    Title = extract_title(from_path)
    html_string = markdown_to_html_node(text).to_html()

    output = template.format(Title, html_string)
    output.replace('href="/', 'href="{basepath}')
    output.replace('src="/', 'src="{basepath}')

    new_file = open(dest_path+"/"+filename+".html", "w")
    new_file.write(output)

    return 

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    local_contents = os.listdir(dir_path_content)

    for file in local_contents:
        file_path = dir_path_content + f"/{file}"
        
        if os.path.isfile(file_path):
            name, file_type = file.split(".")
            if file_type == "md":
                generate_page(file_path,template_path, dest_dir_path, name)
        if os.path.isdir(file_path):
            new_dest = dest_dir_path + f"/{file}"
            os.mkdir(new_dest)
            generate_pages_recursive(file_path, template_path ,new_dest)

    return

def main():
    

    copy_dir(source, dest)
    generate_pages_recursive(markdown_path, markdown_path+"/template.html", dest)

    


main()