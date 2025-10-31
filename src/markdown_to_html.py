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
        # if block_to_block_type(block) == BlockType.ULIST:
        #     parent_nodes.append(ParentNode("ul", list_block(block.replace('\n', ' '), r'- ')))
        # elif block_to_block_type(block) == BlockType.OLIST:
        #     parent_nodes.append(ParentNode("ol", list_block(block.replace('\n', ' '), r'\d.')))
        # else:
        #     parent_nodes.append(create_children(block))
        parent_nodes.append(create_children(block))

    return ParentNode("div", parent_nodes).to_html()


def block_tag_and_strip(block):
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return "p", block.replace('\n', ' ')
        case BlockType.HEADING:
            return "h", block.strip('#').replace('\n', ' ')
        case BlockType.CODE:
            return "code", block.strip('`').replace('\n', ' ')
        case BlockType.QUOTE:
            return "blockquote", block.strip('"').replace('\n', ' ')
        case BlockType.ULIST:
            return "ul", block.replace('\n', ' ')
        case BlockType.OLIST:
            return "ol", block.replace('\n', ' ')


def list_block(block, prefix):
    text = block.replace('\n', ' ')
    list = re.split(prefix, text)
    new_list = []
    for item in list:
        new_list.append(ParentNode("li", create_children(item)))
    return new_list


def create_children(block):
    tag, text = block_tag_and_strip(block)
    text_nodes = text_to_textnodes(text)
    ln = []
    for node in text_nodes:
        ln.append(text_node_to_html_node(node))
    return ParentNode(tag, ln)