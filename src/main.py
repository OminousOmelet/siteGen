from copy_content import *
from generate_page import *

def main():
    copy_content("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")
   
    return

main()