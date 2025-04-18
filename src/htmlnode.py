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
        attr_strings = []
        for item in self.props.items():
            attr_strings.append(f'{item[0]}="{item[1]}"')
        return " ".join(attr_strings)

    def __repr__(self):
        #print(self.tag)
        #print(self.value)
        #print(self.children)
        #print(self.props)
