# -*- coding: utf-8 -*-
# author:yejunyao
# datetime:2022/4/28 16:10

"""
description：开始文件
"""
import os

from transform_tool.srcml_tool import srcml_program_xml


def while2for():
    pass


if __name__ == '__main__':
    # author program to be transformed
    program_path = './program_file/code_data'
    # save path after transformation
    transform_file = './program_file/xml_data'
    srcml_path = 'D:\software\srcML\srcml.exe'
    #
    pre_path = os.path.join(program_path, 'for_text.c')
    xml_path = os.path.join(transform_file, 'for')
    srcml_program_xml(pre_path, xml_path)
