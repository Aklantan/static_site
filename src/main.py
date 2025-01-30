from textnode import *
from htmlnode import *
from os_operations import copy_static

source = "./static"
dest = "./public"

def main():
    copy_static(source,dest)



main()