from textnode import TextType, TextNode


def _dive(text, delimiter, segments, start=0, inside=False):
    index = text.find(delimiter, start)
    if index == -1:
        segments.append((text[start : len(text)], inside))
        return segments
    else:
        segments.append((text[start:index], inside))
        return _dive(text, delimiter, segments, index + 1, not inside)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            segments = _dive(node.text, delimiter, [])
            for segment in segments:
                if segment[1]:
                    nodes.append(TextNode(segment[0], text_type))
                else:
                    nodes.append(TextNode(segment[0], TextType.TEXT))
        else:
            nodes.append(node)
    return nodes
