# -*- coding: utf-8 -*-
# author:yejunyao
# datetime:2022/4/28 16:10

"""
description:开始文件
"""
import os
from test_transform.py import while_for,switch_if,change_memcpy

from transform_tool.srcml_tool import *

# author program to be transformed
program_path = 'C:\\Users\\79374\\Desktop\\gittest\\program_file\\code_data'
# save path after transformation
transform_file = 'C:\\Users\\79374\\Desktop\\gittest\\program_file\\xml_data'
srcml_path = 'D:\\APPS\\srcML\\srcml.exe'

def while2for():
    # 1.将 while.c 使用 scrML变化为while.xml
    pre_path = os.path.join(program_path, 'while_text.c')
    xml_path = os.path.join(transform_file, 'while.xml')
    # 1.将 while.c 使用 scrML变化为while.xml
    srcml_program_xml(pre_path, xml_path)

    input_path = os.path.join(transform_file, 'while.xml')
    output_path = os.path.join(transform_file, 'for.xml')

    #  2.将while.xml通过规则变换，变化为for.xml
    while_for.program_transform(input_path, output_path)
    #   3. 将for.xml通过scrML还原为for.c
    to_xml_path = os.path.join(transform_file, 'for.xml')
    to_pre_path = os.path.join(program_path, 'for_trans.c')
    srcml_xml_program(to_xml_path, to_pre_path)


def switch2if():
    # 1.将 switch.c 使用 scrML变化为switch.xml
    pre_path = os.path.join(program_path, 'switch_text.c')
    xml_path = os.path.join(transform_file, 'switch.xml')
    # 1.将 switch.c 使用 scrML变化为switch.xml
    srcml_program_xml(pre_path, xml_path)

    input_path = os.path.join(transform_file, 'switch.xml')
    output_path = os.path.join(transform_file, 'if.xml')

    #  2.将switch.xml通过规则变换，变化为if.xml
    switch_if.program_transform(input_path, output_path)
    #   3. 将if.xml通过scrML还原为if.c
    to_xml_path = os.path.join(transform_file, 'if.xml')
    to_pre_path = os.path.join(program_path, 'if_trans.c')
    srcml_xml_program(to_xml_path, to_pre_path)

if __name__ == '__main__':

    #while2for()
    
    #switch2if()

    # 1.将.c 使用 scrML变化为.xml
    pre_path = os.path.join(program_path, 'memcpy_text.c')
    xml_path = os.path.join(transform_file, 'memcpy_text.xml')
    # 1.将 switch.c 使用 scrML变化为switch.xml
    srcml_program_xml(pre_path, xml_path)

    input_path = os.path.join(transform_file, 'memcpy_text.xml')
    output_path = os.path.join(transform_file, 'memcpy2_text.xml')

    #  2.将switch.xml通过规则变换，变化为if.xml
    change_memcpy.program_transform(input_path, output_path)
    #   3. 将if.xml通过scrML还原为if.c
    to_xml_path = os.path.join(transform_file, 'memcpy2_text.xml')
    to_pre_path = os.path.join(program_path, 'memcpy2_text.c')
    srcml_xml_program(to_xml_path, to_pre_path)