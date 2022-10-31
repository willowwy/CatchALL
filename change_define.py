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
    for defi in rootT.xpath('//cpp:define', namespaces=ns):
        if defi[0].text == "define":  # text属性，里面的内容
            ex = defi[1][0].text
            nx = defi[2].text
            index = defi[1].find('./x:parameter_list', namespaces=ns)
            if (index):  # define含变量替换
                # if(defi[1][1].tag=='{http://www.srcML.org/srcML/src}parameter_list'):
                i = 1
                for para in defi[1][1].xpath('./x:parameter', namespaces=ns):
                    if para[0][0].tag == '{http://www.srcML.org/srcML/src}name':
                        locals()['para'+str(i)] = para[0][0].text
                    i = i+1

        for namex in rootT.xpath('//x:name', namespaces=ns):
            pn = namex.getparent()
            ppn = pn.getparent()
            if ppn.tag != '{http://www.srcML.org/srcML/cpp}define':
                if namex.text == ex:
                    namex.text = nx                     # 直接替换value值      x→xxx
                    cflag = 1
                    index = pn.find('./x:argument_list', namespaces=ns)
                    if (index):  # 替换变量名
                        # if pn[1].tag=='{http://www.srcML.org/srcML/src}parameter_list':
                        i = 1
                        for argu in pn[1].xpath('./x:argument', namespaces=ns):
                            if argu and argu[0][0].tag == '{http://www.srcML.org/srcML/src}name':
                                res = argu[0][0].xpath('string(.)')
                                locals()['argu'+str(i)
                                         ] = argu[0][0].xpath('string(.)')
                                i = i+1
                        pn.remove(pn[1])
                        for op in range(1, i):
                            if 'para'+str(op)  in locals() and 'argu'+str(op) in locals():
                                a = locals()['para'+str(op)]
                                b = locals()['argu'+str(op)]
                                c = namex.text
                                c = c.replace(a, b or "")
                                namex.text = c

    # 写入文件
    tree.write(output_path)
    return cflag