from textnode import *
from htmlnode import *
from os_operations import copy_static,generate_page,generate_pages_recursive

source = "./static"
dest = "./public"

def main():
    copy_static(source,dest)
    #generate_page("./content/index.md","template.html",f"{dest}/index.html")  
    generate_pages_recursive("./content","template.html",dest)
    



main()