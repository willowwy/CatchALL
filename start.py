# -*- coding: utf-8 -*-
# author:zjq
# datetime:2022/4/28 16:10

"""
description:开始文件
"""
import os
from test_transform.py import while_for,switch_if,change_memcpy,change_define,change_if,if_spilt,if_combine

from transform_tool.srcml_tool import *

# author program to be transformed
program_path = './program_file/pre_data'
# author transformed program
o_program_path = './program_file/output_data'
# save path after transformation
transform_file = './program_file/xml_data'
# path of srcML.exe
srcml_path = './srcML/srcml.exe'

if __name__ == '__main__':

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

        input_path = os.path.join(transform_file, file_xml)
        output_path = os.path.join(transform_file, file2_xml)

        #  2.将.xml通过规则变换，变化为.xml
        cflag=0
        #cflag=change_define.program_transform(input_path, output_path)
        #change_memcpy.program_transform(input_path, output_path)
        cflag=change_if.program_transform(input_path, output_path)
        
        #   3. 将.xml通过scrML还原为if.c
        to_xml_path = os.path.join(transform_file, file2_xml)
        to_pre_path = os.path.join(o_program_path, file2)
        srcml_xml_program(to_xml_path, to_pre_path)

        while(cflag):
            pre_path = os.path.join(o_program_path, file2)
            xml_path = os.path.join(transform_file, file2_xml)
            srcml_program_xml(pre_path, xml_path)

            output_path = os.path.join(transform_file, file2_xml)

            #cflag=change_define.program_transform(output_path, output_path)
            #change_memcpy.program_transform(output_path, output_path)
            cflag=change_if.program_transform(output_path, output_path)
            
            to_xml_path = os.path.join(transform_file, file2_xml)
            to_pre_path = os.path.join(o_program_path, file2)
            srcml_xml_program(to_xml_path, to_pre_path)