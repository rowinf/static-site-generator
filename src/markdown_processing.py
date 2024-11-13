import re
from htmlnode import LeafNode, ParentNode, text_node_to_html_node
from textnode import BlockType, TextType, TextNode


def _delimiter_segment(text, delimiter, segments, start=0, inside=False):
    index = text.find(delimiter, start)
    if index == -1:
        segments.append((text[start : len(text)], inside))
        return segments
    else:
        next_start = index + len(delimiter)
        segments.append((text[start:index], inside))
        return _delimiter_segment(text, delimiter, segments, next_start, not inside)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            segments = _delimiter_segment(node.text, delimiter, [])
            for segment in segments:
                if segment[1]:
                    nodes.append(TextNode(segment[0], text_type))
                else:
                    nodes.append(TextNode(segment[0], TextType.TEXT))
        else:
            nodes.append(node)
    return nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            last_index = 0
            for match in re.finditer(image_regex, node.text):
                start, end = match.span()
                if last_index < start:
                    nodes.append(TextNode(node.text[last_index:start], TextType.TEXT))
                nodes.append(TextNode(match.group(1), TextType.IMAGE, match.group(2)))
                last_index = end
            if last_index < len(node.text):
                nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
        else:
            nodes.append(node)
    return nodes


def split_nodes_link(old_nodes):
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            last_index = 0
            for match in re.finditer(link_regex, node.text):
                start, end = match.span()
                if last_index < start:
                    nodes.append(TextNode(node.text[last_index:start], TextType.TEXT))
                nodes.append(TextNode(match.group(1), TextType.LINK, match.group(2)))
                last_index = end
            if last_index < len(node.text):
                nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
        else:
            nodes.append(node)
    return nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes


def markdown_to_blocks(markdown):
    blocks = []
    block_pattern = r"((?:[^\n]+\n?)+?)(?:\n{2,}|\Z)"
    for match in re.finditer(block_pattern, markdown):
        content = match.group(1).strip()
        if content:
            blocks.append(content)
    return blocks


def all_lines_start_with_asterisk(section):
    lines = section.splitlines()  # Split section into lines
    return all(re.match(r"^\* ", line) for line in lines)


def all_lines_start_with_number(section):
    lines = section.splitlines()  # Split section into lines
    return all(re.match(r"^\d+\. ", line) for line in lines)


def enclosed_with_code_ticks(section):
    lines = section.splitlines()
    return (
        len(lines) > 1
        and lines[0][0:3] == "```"
        and lines[len(lines) - 1][-3:] == "```"
    )


def all_lines_start_with_caret(section):
    lines = section.splitlines()  # Split section into lines
    return all(re.match(r"^\> ", line) for line in lines)


def block_to_block_type(block):
    if re.match(r"^#{1,6}\s+", block):
        return BlockType.HEADING
    elif all_lines_start_with_asterisk(block):
        return BlockType.UNORDERED_LIST
    elif all_lines_start_with_number(block):
        return BlockType.ORDERED_LIST
    elif enclosed_with_code_ticks(block):
        return BlockType.CODE
    elif all_lines_start_with_caret(block):
        return BlockType.QUOTE
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                text_nodes = text_to_textnodes(block)
                inline_elements = [text_node_to_html_node(tn) for tn in text_nodes]
                block_element = ParentNode("p", inline_elements)
                children.append(block_element)
            case BlockType.HEADING:
                h_tag, text = block.split(maxsplit=1)
                block_element = LeafNode(f"h{len(h_tag)}", text)
                children.append(block_element)
            case BlockType.CODE:
                _, text, _ = block.split(sep="```")
                child_element = LeafNode("code", text)
                block_element = ParentNode("pre", [child_element])
                children.append(block_element)
            case BlockType.UNORDERED_LIST:
                text_nodes = [text_to_textnodes(line) for line in block.splitlines()]
                inline_elements = [text_node_to_html_node(tn) for tn in text_nodes]
                block_element = ParentNode("ul", inline_elements)
                children.append(block_element)
            case BlockType.ORDERED_LIST:
                text_nodes = [text_to_textnodes(line) for line in block.splitlines()]
                inline_elements = [text_node_to_html_node(tn) for tn in text_nodes]
                block_element = ParentNode("ul", inline_elements)
                children.append(block_element)
            case BlockType.QUOTE:
                text_nodes = [text_to_textnodes(line) for line in block.splitlines()]
                inline_elements = [text_node_to_html_node(tn) for tn in text_nodes]
                block_element = ParentNode("blockquote", inline_elements)
                children.append(block_element)
    return ParentNode("div", children)
