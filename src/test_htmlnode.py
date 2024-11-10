import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a text node")
        node2 = HTMLNode("p", "This is a text node")
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(
            "p", "This is a text node", None, {"id": "node-id", "class": "para"}
        )
        self.assertEqual(node.props_to_html(), ' id="node-id" class="para"')


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a text node")
        self.assertEqual(node.to_html(), "<p>This is a text node</p>")

        node = LeafNode("p", "This is a text node", {"id": "node"})
        self.assertEqual(node.to_html(), '<p id="node">This is a text node</p>')


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "This is a text node"),
            ],
        )
        self.assertEqual(node.to_html(), "<div><p>This is a text node</p></div>")


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_to_html(self):
        text_node = TextNode("text", TextType.BOLD)
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<b>text</b>")

        inode = TextNode("alt text", TextType.IMAGE)
        node = text_node_to_html_node(inode)
        self.assertEqual(
            node.to_html(), f'<img src="{inode.url}" alt="{inode.text}"></img>'
        )


if __name__ == "__main__":
    unittest.main()
