# pylint: disable=import-error
# -*- coding: utf-8 -*-
# author:zjq
# datetime:2022/4/28 16:10

"""
description:开始文件
"""
import os

from test_transform.py import  while_for, change_define

from transform_tool.srcml_tool import srcml_program_xml, srcml_xml_program

# 未转换代码的目录
UNCONVERTED_CODE_DIR = './Unconverted/'
# 转换后代码的目录
CONVERTED_CODE_DIR = './Converted/'
# 临时xml文件的目录
XML_TMP_DIR = './XML_tmp/'
# path of srcML.exe
SRCML_PATH = './srcML/srcml.exe'

def findfile(relative_path):
    """
    递归遍历所有文件和目录,在XML_TMP_DIR与SRCML_PATH中创建对应目录结构
    并调用convert_file函数进行转换
    """
    if os.path.exists(UNCONVERTED_CODE_DIR + relative_path):

        if os.path.isdir(UNCONVERTED_CODE_DIR + relative_path):
            # 在CONVERTED_CODE_DIR中创建相同的目录结构
            if not os.path.exists(CONVERTED_CODE_DIR + relative_path):
                os.makedirs(CONVERTED_CODE_DIR + relative_path)
            # 在XML_TMP_DIR中创建相同的目录结构
            if not os.path.exists(XML_TMP_DIR + relative_path):
                os.makedirs(XML_TMP_DIR + relative_path)

        file_list = os.listdir(UNCONVERTED_CODE_DIR + relative_path)
        for afile in file_list:

            if afile in ("$RECYCLE.BIN" ,"System Volume Information"):
                continue

            fpath = os.path.join(relative_path, afile)
            if os.path.isdir(UNCONVERTED_CODE_DIR + fpath):
                fpath=fpath+"/"
                findfile(fpath)
            else:
                convert_file(afile,fpath)

def convert_file(file_name,relative_path):
    """
    将单个文件进行转换
    """
    if file_name.endswith('.c'):
        file_xml=file_name.replace(".c",".xml")
        file2_xml=file_name.replace(".c","2.xml")

        relative_path=relative_path.replace(file_name,"")
        print(relative_path + file_name)

        # 1.将 switch.c 使用 scrML变化为switch.xml
        input_path = os.path.join(UNCONVERTED_CODE_DIR, relative_path, file_name)
        output_path = os.path.join(XML_TMP_DIR, relative_path, file_xml)
        srcml_program_xml(input_path, output_path)

        
        #  2.将.xml通过规则变换，变化为.xml
        cflag=0
        input_path = os.path.join(XML_TMP_DIR, relative_path, file_xml)
        output_path = os.path.join(XML_TMP_DIR, relative_path, file2_xml)
        # 变换
        cflag = while_for.program_transform(input_path, output_path)

        #   3. 将.xml通过scrML还原为.c
        input_path = os.path.join(XML_TMP_DIR, relative_path, file2_xml)
        output_path = os.path.join(CONVERTED_CODE_DIR, relative_path, file_name)
        srcml_xml_program(input_path, output_path)

        if cflag==1:
            input_path = os.path.join(CONVERTED_CODE_DIR, relative_path, file_name)
            output_path = os.path.join(XML_TMP_DIR, relative_path, file2_xml)
            srcml_program_xml(input_path, output_path)
            # 额外的变换
            cflag=while_for.program_transform(output_path, output_path)
            
            srcml_xml_program(output_path, input_path)


if __name__ == '__main__':
    dirs = os.listdir(UNCONVERTED_CODE_DIR)  # 列出UNCONVERTED_CODE_DIR下的所有文件和目录
    for file in dirs:
        findfile(file) # 调用findfile函数递归遍历所有文件和目录
