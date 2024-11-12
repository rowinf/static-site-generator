from textnode import TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self):
        if self.props == None:
            return " "
        items = list(map(lambda x: f' {x[0]}="{x[1]}"', self.props.items()))
        return "".join(items)

    def to_html(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, Chilren, Props)"


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
