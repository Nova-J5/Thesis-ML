import xml.etree.ElementTree as ET

def extract_header_keys(xml_filepath):
    tree = ET.parse(xml_filepath)
    root = tree.getroot()

    def recurse(node, path):
        # Append current node tag to path
        current_path = path + [node.tag]

        # If node has no children, yield the path
        if len(node) == 0:
            path_string = "/".join(current_path)
            if path_string.startswith('metabolite/'):
                path_string = path_string[len('metabolite/'):]
            yield path_string
        else:
            # If node has children, recurse
            for child in node:
                yield from recurse(child, current_path)

    return list(recurse(root, []))

# %%
