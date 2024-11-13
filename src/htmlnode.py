from textnode import TextType
import textnode


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self):
        if self.props is None:
            return " "
        items = list(map(lambda x: f' {x[0]}="{x[1]}"', self.props.items()))
        return "".join(items)

    def to_html(self):
        raise NotImplementedError()

    def __eq__(self, other):
        no_children = self.children is None and other.children is None
        has_children = self.children is not None and other.children is not None
        equal_children = has_children and len(self.children) == len(other.children)
        return (
            self.tag == other.tag
            and self.value == other.value
            and ((has_children and equal_children) or no_children)
            and self.props == other.props
        )

    def __repr__(self):
        child = []
        if self.children is not None:
            child = [c for c in self.children]
        return (
            f"HTMLNode({self.tag}, {self.value}, Children[{len(child)}], {self.props})"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag:
            return (
                f"<{self.tag}{self.props_to_html().rstrip()}>{self.value}</{self.tag}>"
            )
        return self.value


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        childs = map(lambda x: x.to_html(), self.children)
        child_html = "".join(childs)
        return f"<{self.tag}{self.props_to_html().rstrip()}>\n  {child_html}\n</{self.tag}>"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode("", text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception()
