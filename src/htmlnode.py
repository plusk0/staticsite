from fixed_variables import TextType


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
        if self.tag == "code":
            pass
        for prop in self.props:
            string += f' {prop}="{self.props[prop]}"'

        return string 
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children, self.props})"

class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value)
        self.props = props

    def __repr__(self):
        return f"LeafNode({self.tag},{self.value},{self.props})"
    
    def to_html(self):

        if self.value == None:
            raise ValueError
        match self.tag:
            case None:
                return str(self.value)
            case _:
                if self.props != None:
                    return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>' 
                else:
                    return f'<{self.tag}>{self.value}</{self.tag}>' 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, props)
        self.children = children

    def to_html(self):
        output = ""

        if self.tag == None:
            raise ValueError
        if self.children == None:
            if self.tag == "pre":
                print("error:", self.children)
            raise ValueError("Missing children for ParentNode object")
        for child in self.children:
            output += child.to_html()
        if self.props != None:
            return f'<{self.tag}{self.props_to_html()}>{output}</{self.tag}>'
        else:
            return f'<{self.tag}>{output}</{self.tag}>'