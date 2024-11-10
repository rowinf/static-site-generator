import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes(self):
        node = TextNode(
            "This is **text** with a `code block` word, with `code` at the end too",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is **text** with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word, with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" at the end too", TextType.TEXT),
            ],
        )
