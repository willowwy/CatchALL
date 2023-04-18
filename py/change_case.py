from argparse import Namespace
from typing import Text
from lxml import etree
from lxml import html

ns = {'x': 'http://www.srcML.org/srcML/src',
      'cpp': 'http://www.srcML.org/srcML/cpp',
      'pos': 'http://www.srcML.org/srcML/position'}


def program_transform(input_path, output_path):
    cflag = 0
    tree = etree.parse(input_path)
    rootT = tree.getroot()  # 根节点

    # 该目录下所有//cpp:define的标签，命名空间为ns
    for ty in rootT.xpath('//cpp:type', namespaces=ns):
         