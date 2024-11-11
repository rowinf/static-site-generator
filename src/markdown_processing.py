import re
from htmlnode import LeafNode
from textnode import TextType, TextNode


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
