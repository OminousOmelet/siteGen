class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        text = ""
        for key, value in self.props.items():
            text += f'{key}="{value}" '
        return text[:-1]
    
    def __repr__(self):
        props = self.props_to_html()
        if props != "":
            props = " " + props
        if self.tag == "img":
            props += " /"
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        # An image passes an empty string as value, must explicitly test 'None' value
        if self.value is None:
            raise ValueError
        if not self.tag:
            return self.value
        return self.__repr__()
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("No children provided")
        full_text = ""
        for child in self.children:
            full_text += child.to_html()
        props = super().props_to_html()
        if props != "":
            props = " " + props
        return f'<{self.tag}{props}>{full_text}</{self.tag}>'