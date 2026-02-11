from copy_content import *
from generate_page import generate_page

def main():
    copy_content("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    return

main()