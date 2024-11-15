import unittest
from htmlnode import LeafNode, ParentNode
from textnode import BlockType, TextNode, TextType
from markdown_processing import (
    block_to_block_type,
    extract_markdown_links,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestMarkdownProcessing(unittest.TestCase):
    def test_split_nodes(self):
        node = TextNode(
            "This is **text** with a `code block` word, with `code` at the *italic* end too",
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
                TextNode(" at the *italic* end too", TextType.TEXT),
            ],
        )
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word, with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" at the *italic* end too", TextType.TEXT),
            ],
        )

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )
        node = TextNode("This is text with a", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])
        node = TextNode(
            "This is text with a ![image](https://i.imgur.com/asdf.gif) and a [link](/page)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/asdf.gif"),
                TextNode(" and a [link](/page)", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_markdown_to_blocks(self):
        text = """
        This is the first section. It has multiple lines.

        This is the second section. It also has multiple lines.

        Another section is here. It is also separated by blank lines.

        """
        blocks = markdown_to_blocks(text)
        self.assertEqual(
            blocks,
            [
                "This is the first section. It has multiple lines.",
                "This is the second section. It also has multiple lines.",
                "Another section is here. It is also separated by blank lines.",
            ],
        )

    def test_block_to_block_type(self):
        heading = "###### I am Heading"
        para = "I am paragraph"
        unordered_list = """* Item 1
* Item 2"""
        code_block = """```Item
        ```"""
        block_quote = """> Start
> end quote"""
        self.assertEqual(block_to_block_type(heading), BlockType.HEADING)
        self.assertEqual(block_to_block_type(para), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(unordered_list), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        self.assertEqual(block_to_block_type(block_quote), BlockType.QUOTE)

    def test_markdown_to_html_node(self):
        markdown = (
            """some text and a **bold** statement ![alt txt](https://imgur.com/asdf)"""
        )
        nodes = markdown_to_html_node(markdown)
        want = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("", "some text and a "),
                        LeafNode("b", "bold"),
                        LeafNode("", " statement "),
                        LeafNode(
                            "img",
                            None,
                            {"src": "https://imgur.com/asdf", "alt": "alt txt"},
                        ),
                    ],
                )
            ],
        )

        self.assertEqual(nodes, want)

        md = "## Heading2 Element"
        want = ParentNode("div", [ParentNode("h2", "Heading2 Element")])
        self.assertEqual(markdown_to_html_node(md), want)

        md2 = """```
this is code
```"""
        want = ParentNode(
            "div", [ParentNode("pre", [LeafNode("code", "this is code")])]
        )
        self.assertEqual(markdown_to_html_node(md2), want)

        md3 = """> Life is like a box of chocolates
> You never know what yer gonna git."""
        want = ParentNode(
            "div",
            [
                ParentNode(
                    "blockquote",
                    [
                        LeafNode("", "Life is like a box of chocolates"),
                        LeafNode("", "You never know what yer gonna git."),
                    ],
                )
            ],
        )
        self.assertEqual(markdown_to_html_node(md3), want)
        md4 = """* item 1
* item 2 *with a vengeance*
        """
        want = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode(
                            "li",
                            [
                                LeafNode("", "item 1"),
                            ],
                        ),
                        ParentNode(
                            "li",
                            [
                                LeafNode("", "item 2 "),
                                LeafNode("b", "with a vengeance"),
                            ],
                        ),
                    ],
                )
            ],
        )
        self.assertEqual(markdown_to_html_node(md4), want)

    def test_extract_title(self):
        md = """# this title"""
        self.assertEqual(extract_title(md), "this title")
