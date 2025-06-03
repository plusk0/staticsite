
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        string = ""
        for prop in self.props:
            string += f' {prop}="{self.props[prop]}"'
        return string #string of props as html
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children, self.props})"

class LeafNode(HTMLNode):
    
    def __init__(self, value, tag):
        super().__init__(value, tag)

    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return str(self.value)
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>' 