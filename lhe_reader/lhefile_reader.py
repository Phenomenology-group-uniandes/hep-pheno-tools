import gzip
import xml.etree.ElementTree as ET


def readLHEF(path_to_file):
    with gzip.open(path_to_file, 'rb') as lhe_file:
        tree = ET.parse(lhe_file)
        root = tree.getroot()
        childs = [child for child in root if child.tag == 'event']
    return childs
