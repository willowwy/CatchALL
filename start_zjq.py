# -*- coding: utf-8 -*-
# author:yejunyao
# datetime:2022/4/28 16:10

"""
description:开始文件
"""
import os
from test_transform.py import while_for,switch_if,change_memcpy,change_define

from transform_tool.srcml_tool import *

# author program to be transformed
program_path = './program_file/pre_data'
# save path after transformation
transform_file = './program_file/xml_data'
# path of srcML.exe
srcml_path = './srcML/srcml.exe'

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
    
    dirs=os.listdir(program_path)
    for file in dirs:
        
        file_xml=file.replace(".c",".xml")
        file2=file.replace(".c","2.c")
        file2_xml=file.replace(".c","2.xml")
        
        # 1.将.c 使用 scrML变化为.xml
        pre_path = os.path.join(program_path, file)
        xml_path = os.path.join(transform_file, file_xml)
        # 1.将 switch.c 使用 scrML变化为switch.xml
        srcml_program_xml(pre_path, xml_path)

        # input_path = os.path.join(transform_file, file_xml)
        # output_path = os.path.join(transform_file, file2_xml)

        # #  2.将.xml通过规则变换，变化为.xml
        # change_define.program_transform(input_path, output_path)
        # change_memcpy.program_transform(input_path, output_path)
        
        # #   3. 将.xml通过scrML还原为if.c
        # to_xml_path = os.path.join(transform_file, file2_xml)
        # to_pre_path = os.path.join(program_path, file2)
        # srcml_xml_program(to_xml_path, to_pre_path)
