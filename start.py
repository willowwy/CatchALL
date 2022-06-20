# -*- coding: utf-8 -*-
# author:yejunyao
# datetime:2022/4/28 16:10

"""
description：开始文件
"""
import os
from test_transform.py import for_while

from transform_tool.srcml_tool import *


def while2for():
    pass


if __name__ == '__main__':
    # author program to be transformed
    program_path = './program_file/code_data'
    # save path after transformation
    transform_file = './program_file/xml_data'
    srcml_path = 'D:\software\srcML\srcml.exe' 
    # 1.将 for.c 使用 scrML变化为for.xml
    pre_path = os.path.join(program_path, 'test.c')
    xml_path = os.path.join(transform_file, 'test.xml')
    # 1.将 for.c 使用 scrML变化为for.xml
    srcml_program_xml(pre_path, xml_path)

    # input_path = os.path.join(transform_file, 'for.xml')
    # output_path = os.path.join(transform_file, 'while.xml')

    # #  2.将for.xml通过规则变换，变化为while.xml
    # for_while.program_transform(input_path, output_path)
    # #   3. 将while.xml通过scrML还原为while.c
    # to_xml_path = os.path.join(transform_file, 'while.xml')
    # to_pre_path = os.path.join(program_path, 'while_trans.c')
    # srcml_xml_program(to_xml_path, to_pre_path)
