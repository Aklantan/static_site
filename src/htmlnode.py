class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
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