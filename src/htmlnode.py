

class HTMLNode():
    def __init__(self,tag=None,children=None,props=None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_list = []
        if self.props == None:
            return ""
        for key in self.props:
            html_list.append(" " + key + "=\""+ self.props[key] + "\"")
        return "".join(html_list)


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,None,props)
        self.value = value


    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError ("No tag provided")
        if self.children == None:
            raise ValueError ("No children provided")
        html_content = ""
        for child in self.children:
            html_content += child.to_html()
        return f"<{self.tag}>{html_content}</{self.tag}>"
        





