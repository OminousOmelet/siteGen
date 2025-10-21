from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    text = text_node.text
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text)
        case TextType.BOLD:
            return LeafNode("b", text)
        case TextType.ITALIC:
            return LeafNode("i", text)
        case TextType.CODE:
            return LeafNode("code", text)
        case TextType.LINK:
            return LeafNode("a", text)
        case TextType.IMAGE:
            return LeafNode("img", "", None, {"src": text_node.url, "alt": text_node.text})