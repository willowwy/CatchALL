from argparse import Namespace
from typing import Text
from lxml import etree

ns = {'x': 'http://www.srcML.org/srcML/src',
	'cpp': 'http://www.srcML.org/srcML/cpp',
	'pos': 'http://www.srcML.org/srcML/position'}

def program_transform(input_path, output_path):

    tree = etree.parse(input_path)
    rootT = tree.getroot()
    
    for defi in rootT.xpath('//cpp:define', namespaces=ns):
        if defi[0].text=="define":
            ex=defi[1][0].text
            nx=defi[2].text
        for namex in rootT.xpath('//x:name', namespaces=ns):
            pn=namex.getparent()
            ppn=pn.getparent()
            if ppn.tag!='{http://www.srcML.org/srcML/cpp}define':
                if namex.text==ex:
                    namex.text=nx
    # 写入文件
    tree.write(output_path)


