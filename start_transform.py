# -*- coding: utf-8 -*-

"""
description:开始文件
"""
import os
from test_transform.py import change_memcpy,change_if

from transform_tool.srcml_tool import *

# author program to be transformed
program_path = './program_file/pre_data/'
# author transformed program
o_program_path = './program_file/output_data/'
# save path after transformation
transform_file_bef = './program_file/pre_xml/'
# xml file path after transformation
transform_file_aft = './program_file/aft_xml'
# path of srcML.exe
srcml_path = './srcML/srcml.exe'

def findfile(pathName):
    if os.path.exists(pathName):
        fileList = os.listdir(pathName) #当前目录列表
        for f in fileList:
            if f == "$RECYCLE.BIN" or f == "System Volume Information":
                continue
            fpath = os.path.join(pathName, f)
            if os.path.isdir(fpath):
                fpath=fpath+"/"
                findfile(fpath)
            else:
                changefile(f,fpath)

                
def changefile(file,pre_path):
    print(file)
    if file.endswith('.c'):
        file_xml=file.replace(".c",".xml")
        file2=file.replace(".c","2.c")
        file2_xml=file.replace(".c","2.xml")

        # 1.将.c 使用 scrML变化为.xml
        xml_path = os.path.join(transform_file_bef, file_xml)
        # 1.将 switch.c 使用 scrML变化为switch.xml
        srcml_program_xml(pre_path, xml_path)

        input_path = os.path.join(transform_file_bef, file_xml)
        print(input_path)
        output_path = os.path.join(transform_file_aft, file2_xml)
        print(output_path)

        #  2.将.xml通过规则变换，变化为.xml
        cflag=0
        #cflag=change_define.program_transform(input_path, output_path)
        change_memcpy.program_transform(input_path, output_path)
        cflag=change_if.program_transform(input_path, output_path)
        #cflag=change_inline.program_transform(input_path, output_path)
        
        #   3. 将.xml通过scrML还原为if.c
        to_xml_path = os.path.join(transform_file_aft, file2_xml)
        to_pre_path = os.path.join(o_program_path, file2)
        print(to_pre_path)
        srcml_xml_program(to_xml_path, to_pre_path)

        if cflag==1:
            pre_path = os.path.join(o_program_path, file2)
            xml_path = os.path.join(transform_file_aft, file2_xml)
            srcml_program_xml(pre_path, xml_path)

            output_path = os.path.join(transform_file_aft, file2_xml)

            #cflag=change_define.program_transform(output_path, output_path)
            change_memcpy.program_transform(output_path, output_path)
            cflag=change_if.program_transform(output_path, output_path)
            #cflag=change_inline.program_transform(output_path, output_path)
            
            to_xml_path = os.path.join(transform_file_aft, file2_xml)
            print(to_xml_path)
            to_pre_path = os.path.join(o_program_path, file2)
            print(to_pre_path)
            srcml_xml_program(to_xml_path, to_pre_path)
            
    print("Success!!\n\n")
if __name__ == '__main__':
    
    dirs=os.listdir(program_path)
    for file in dirs:
        findfile(program_path)