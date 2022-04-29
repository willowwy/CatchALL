# -*- coding: utf-8 -*-
# author:yejunyao
# datetime:2022/2/25 14:15

"""
description：
"""
import os.path
import subprocess
from io import BytesIO

from sys import stdout, stdin
from xml.etree import ElementTree
from xml.etree.ElementTree import SubElement
from collections import Counter

from typing import Text
from lxml import etree


def with_xpath(xml_data: Text, xpath_expr: str, namespaces: dict = None) -> list:
    """通过xpath提起XML格式的数据"""
    if isinstance(xml_data, str):  # 将字符串转成字节码
        xml_data = xml_data.encode("utf-8")
    try:
        xml = etree.XML(xml_data)
        if namespaces and isinstance(namespaces, dict):
            list_result = xml.xpath(xpath_expr, namespaces=namespaces)
        else:
            list_result = xml.xpath(xpath_expr)
        return list_result
    except Exception as e:
        raise Exception(f"XML-通过xpath获取指定节点信息错误，错误原因：{e}")


if __name__ == "__main__":
    # 1.将for.c 变为 for.xml

    # 2.将for.xml 变为 while.xml

    # 3.将while.xml 变为 for.c

    xml_path = '/program_file/xml_data'
    xml_name = 'for_text.xml'
    tree = etree.parse(os.path.join(xml_path, xml_name))
    rootT = tree.getroot()
    nsp = {'x': 'http://www.srcML.org/srcML/src'}

    for func in rootT.xpath('//x:function', namespaces=nsp):
        for block_content_xml in func.xpath('//x:block/x:block_content', namespaces=nsp):
            for for_xml in block_content_xml.xpath('//x:for', namespaces=nsp):
                for control_xml in for_xml.xpath('//x:control', namespaces=nsp):
                    for init_xml in control_xml.xpath('//x:init', namespaces=nsp):
                        for decl_xml in init_xml.xpath('//x:decl', namespaces=nsp):
                            block_content_tree = etree.SubElement(block_content_xml, 'decl_stmt')
                            etree.dump(decl_xml)
                            block_content_tree.append(decl_xml)
                    # 创建while标签
                    for condition_xml in control_xml.xpath('//x:condition', namespaces=nsp):
                        while_tree = etree.SubElement(block_content_xml, 'while')
                        while_tree.append(condition_xml)
                        while_tree.text = 'while'
                        condition_xml.text = '('
                        # expr后加';'
                        for expr1 in condition_xml.xpath('./x:expr', namespaces=nsp):
                            expr1.tail = ')'

                    # 3.将for内block取出放入while
                    block_xml = for_xml.xpath('./x:block', namespaces=nsp)[0]

                    while_tree.append(block_xml)
                    # 4.将 for- <incr>-<expr>放入block_content中
                    for expr_xml in control_xml.xpath('//x:incr/x:expr', namespaces=nsp):
                        block_content_xml_sub = \
                            block_xml.xpath('./x:block_content', namespaces=nsp)[0]
                        etree.dump(block_content_xml_sub)

                        etree.SubElement(block_content_xml_sub, 'expr_stmt').append(expr_xml)
                        expr_xml.tail = ';'
            # 5.删除for标签
            for for_xml in block_content_xml.xpath('//x:for', namespaces=nsp):
                block_content_xml.remove(for_xml)
    # 写入文件
    tree.write('output.xml')
