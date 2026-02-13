from copy_content import *
from generate_page import *
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    copy_content("static", "docs")
    generate_pages_recursive(basepath, "content", "template.html", "docs")
   
    return

main()