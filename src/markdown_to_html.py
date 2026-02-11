import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from split_nodes import split_nodes_image, split_nodes_link, split_nodes_delimiter
from text_to_nodes import text_node_to_html_node, text_to_textnodes
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    parent_nodes = []
    for block in blocks:
        block.strip()
        if block_to_block_type(block) == BlockType.CODE:
            parent_nodes.append(ParentNode("pre", [LeafNode("code", block.strip('`').lstrip('\n'))]))
        else:
            parent_nodes.append(create_children(block))

    return ParentNode("div", parent_nodes)


def block_tag_and_strip(block):
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return "p", block.replace('\n', ' ')
        case BlockType.HEADING:
            nblock = block.lstrip('#')
            hl = len(block) - len(nblock)
            return f"h{hl}", nblock.lstrip().replace('\n', ' ')
        # Need to fix (only the first line is stripped, requires something like 'list' code)
        case BlockType.QUOTE:
            quoteLines = block.split('\n')
            stripped = []
            for line in quoteLines:
                stripped.append(line.lstrip('>').lstrip())
                newBlock = ' '.join(stripped)
            return "blockquote", newBlock
        # Each element will be stripped in list_elements function
        case BlockType.ULIST:
            return "ul", block
        case BlockType.OLIST:
            return "ol", block


def list_elements(text, prefix):
    list = re.split(prefix, text)
    new_list = []
    for item in list:
        # First item in split is always empty, creates error with no children for ParentNode
        if item == "":
            continue
        # Strip text here instead
        new_list.append(ParentNode("li", create_inner_nodes(item.strip('\n').replace('\n', ' '))))
    return new_list


def create_children(block):
    tag, text = block_tag_and_strip(block)
    if tag == "ul":
        return ParentNode(tag, list_elements(text, r'- '))
    if tag == "ol":
        return ParentNode(tag, list_elements(text, r'\d+. '))
    
    inner_nodes = create_inner_nodes(text)
    return ParentNode(tag, inner_nodes)
    
def create_inner_nodes(text):
    inner_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        inner_nodes.append(text_node_to_html_node(node))
    return inner_nodes