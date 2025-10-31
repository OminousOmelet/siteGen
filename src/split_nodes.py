import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for i in range(0, len(old_nodes)):
        if old_nodes[i].text == "":
            continue
        if delimiter not in old_nodes[i].text:
            new_nodes.append(old_nodes[i])
            continue
        str_list = old_nodes[i].text.split(delimiter)
        if len(str_list) % 2 == 0:
            raise ValueError("Invalid markdoown, formatted section not closed")
        for j in range(0, len(str_list)):
            if str_list[j] == "":
                continue
            if j % 2 == 0:
                new_nodes.append(TextNode(str_list[j], TextType.TEXT))
            else:
                new_nodes.append(TextNode(str_list[j], text_type))
    return new_nodes

def split_nodes(old_nodes, regex, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        match text_type:
            case TextType.IMAGE:
                matches = extract_markdown_images(node.text)
            case TextType.LINK:
                matches = extract_markdown_links(node.text)     
                
        if not matches:
            new_nodes.append(node)
            continue
        sections = re.split(regex, node.text)
        step = 0
        index = 0
        while index < len(sections):
            if sections[index] == "":
                index += 1
                continue
            if step < len(matches) and sections[index] == matches[step][0]:
                new_nodes.append(TextNode(sections[index], text_type, matches[step][1]))
                step += 1
                index += 2
            else:
                new_nodes.append(TextNode(sections[index], TextType.TEXT))
                index += 1
    return new_nodes

# I know
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
# This
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
# is
def split_nodes_image(old_nodes):
        return split_nodes(old_nodes, r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", TextType.IMAGE)
# gross
def split_nodes_link(old_nodes):
        return split_nodes(old_nodes, r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", TextType.LINK)
