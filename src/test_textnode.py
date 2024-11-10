import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("This is a text node", TextType.ITALIC, "https://boot.dev")
        node4 = TextNode("This is a text node", TextType.ITALIC, "https://boot.dev")
        self.assertEqual(node3, node4)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        node5 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node4, node5)

if __name__ == "__main__":
    unittest.main()
