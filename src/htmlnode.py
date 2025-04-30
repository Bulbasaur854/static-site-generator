class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError # child classes will override this
    
    def props_to_html(self):
        result = ""        

        if self.props:
            for atr in self.props:
                result += f" {atr}=\"{self.props[atr]}\""
        
        return result
    
    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"