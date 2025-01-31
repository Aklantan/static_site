import os
import shutil
from markdown_totextnodes import *
from htmlnode import *
from textnode import *
from pathlib import Path





def copy_static(src,dest):
   if not os.path.exists(src):
      raise Exception ("Source folder not found")
   if os.path.exists(dest):
    shutil.rmtree(dest)
   os.makedirs(dest)
   with os.scandir(src) as entries:
      for entry in entries:
        src_path = os.path.join(src,entry.name)
        dest_path = os.path.join(dest,entry.name)
        if entry.is_file():
           print(entry.path)
           shutil.copy2(src_path,dest_path)
        elif entry.is_dir():
           print(entry.path)
           copy_static(src_path,dest_path)
          
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as markdown:
        md_content = markdown.read()
    with open(template_path,"r") as template:
        template_content = template.read()
    html_string = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)

    new_html_content = template_content.replace("{{ Title }}",title).replace("{{ Content }}",html_string)

    dest_dir = os.path.dirname(dest_path)

    if not os.path.exists(dest_dir):
       os.makedirs(dest_dir)

    with open(dest_path,"w") as page:
       page.write(new_html_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
   files = os.listdir(dir_path_content)
   for file in files:
      full_path = os.path.join(dir_path_content, file)
      dest_file = file.replace("md","html")
      dest_path = os.path.join(dest_dir_path,dest_file)
      
      if os.path.isdir(full_path):
         Path(dest_path).mkdir(parents=True,exist_ok=True)
         generate_pages_recursive(full_path,template_path, dest_path)
      elif os.path.isfile(full_path) and file.endswith(".md"):
         generate_page(full_path,template_path,dest_path)

