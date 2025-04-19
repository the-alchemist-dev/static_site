#!/usr/bin/python3

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Implementation in subclass")

    def props_to_html(self):
        if self.props != None:
            attr_strings = []
            for item in self.props.items():
                attr_strings.append(f' {item[0]}="{item[1]}"')
            return "".join(attr_strings)
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise valueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        properties = self.props_to_html()
        return f"<{self.tag}{properties}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"
