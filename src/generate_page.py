from markdown_to_html import *
import os

def extract_title(markdown):
    md_lines = markdown.splitlines()
    strippedList = []
    for line in md_lines:
        strippedList.append(line.strip())

    for line in strippedList:
        if line.startswith("# "):
            return line[2:]
    
    raise Exception("No title found!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    m = open(from_path, 'r')
    markdown = m.read()
    t = open(template_path, 'r')
    template = t.read()
    m.close()
    t.close()

    title = extract_title(markdown)
    mNode = markdown_to_html_node(markdown)
    html = mNode.to_html()
    temp1 = template.replace("{{ Title }}", title)
    temp2 = temp1.replace("{{ Content }}", html)
    dir = os.path.dirname(dest_path)
    if not os.path.isdir(dir):
        os.makedirs(dir)
    
    if not os.path.exists(dest_path):
        with open(dest_path, 'x'):
            pass
    f = open(dest_path, 'w')    
    f.write(temp2)
    f.close()

    return temp2

# Just recursive version of generate page func
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    entryList = os.listdir(dir_path_content)
    for e in entryList:
        entry = os.path.join(dir_path_content, e)
        print(entry + " | " + e)
        if os.path.isfile(entry):
            entry_dest = os.path.join(dest_dir_path, "index.html")
            generate_page(entry, template_path, entry_dest)
        else:
            branch = os.path.join(dest_dir_path, e)
            generate_pages_recursive(entry, template_path, branch)
    return