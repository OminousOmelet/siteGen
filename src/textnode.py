from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return self.text == node.text and self.text_type == node.text_type and self.url == node.url
    
    def __repr__(self):
        url = ""
        if self.url:
            url = f', "{self.url}"'
        return f'TextNode("{self.text}", {self.text_type}{url})'
    
