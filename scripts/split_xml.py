import os
import xml.etree.ElementTree as ET


def split_xml(file, elements_per_file, output_dir):
    context = iter(ET.iterparse(file, events=('start', 'end')))
    _, root = next(context)  # get root element
    items = []

    for event, elem in context:
        if event == 'end' and elem.tag == 'metabolite':  # substitute 'metabolite'
            items.append(elem)
            if len(items) == elements_per_file:
                write_file(items, output_dir)
                items = []
            root.clear()  # free memory

    if items:  # handle leftovers
        write_file(items, output_dir)


def write_file(items, output_dir):
    root = ET.Element('hmdb')  # or ET.Element('hmdb') if you want to keep the root tag
    root.extend(items)
    tree = ET.ElementTree(root)
    filename = os.path.join(output_dir, "part_{}.xml".format(write_file.counter))
    tree.write(filename)
    print(f"Written {filename}")
    write_file.counter += 1


write_file.counter = 1
output_dir = "/splitted_xml"
os.makedirs(output_dir, exist_ok=True)  # create directory if not exists
split_xml('../notebooks/hmdb_metabolites.xml', 1000, output_dir)  # split every 1000 elements
