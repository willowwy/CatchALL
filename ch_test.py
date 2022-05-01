# -*- coding: utf-8 -*-
# author:chenghao
# datetime:2022/4/28 16:10

"""
description：开始文件
"""
import imp
import os
from test_transform.py import for_while
from test_transform.py import while_for
from test_transform.py import switch_if
from transform_tool.srcml_tool import *

 # author program to be transformed
program_path = 'C:\\Users\\28673\\Desktop\\gittest\\program_file\\code_data'
# save path after transformation
transform_file = 'C:\\Users\\28673\\Desktop\\gittest\\program_file\\xml_data'
# the path of your local srcml.exe
srcml_path = 'E:\srcML\srcml.exe' 

def input_c2xml(input_c, input_xml):
    # 1.将 input.c 使用 scrML变化为input.xml
    pre_path = os.path.join(program_path, input_c)
    xml_path = os.path.join(transform_file, input_xml)
    srcml_program_xml(pre_path, xml_path)

def output_xml2c(output_xml, output_c):
    # 3. 将output.xml通过scrML还原为output.c
    to_xml_path = os.path.join(transform_file, output_xml)
    to_pre_path = os.path.join(program_path, output_c)
    srcml_xml_program(to_xml_path, to_pre_path)

def for2while(input_xml, output_xml):
    # 2.将for.xml通过规则变换，变化为while.xml
    input_path = os.path.join(transform_file, input_xml)
    output_path = os.path.join(transform_file, output_xml)
    for_while.program_transform(input_path, output_path)
    
def while2for(input_xml, output_xml):
    # 2.将while.xml通过规则变换，变化为for.xml
    input_path = os.path.join(transform_file, input_xml)
    output_path = os.path.join(transform_file, output_xml)
    while_for.program_transform(input_path, output_path)

def switch2if(input_xml, output_xml):
    # 2.将while.xml通过规则变换，变化为for.xml
    input_path = os.path.join(transform_file, input_xml)
    output_path = os.path.join(transform_file, output_xml)
    switch_if.program_transform(input_path, output_path)

menuTup = ("1.for2while", "2.while2for", "3.switch2if", "0.退出")
if __name__ == '__main__':
    for item in menuTup:
       print(item)
    print('input choice:')
    num = int(input())
    while(num):
        if num == 1:
            input_c2xml('for_text.c', 'for.xml')
            for2while('for.xml', 'while.xml')
            output_xml2c('while.xml', 'while_trans.c')
        elif num == 2:
            input_c2xml('while_text.c', 'while.xml')
            while2for('while.xml', 'for.xml')
            output_xml2c('for.xml', 'for_trans.c')
        elif num == 3:
            input_c2xml('switch_text.c', 'switch.xml')
            switch2if('switch.xml', 'if.xml')
            output_xml2c('if.xml', 'if_trans.c')
        print('input choice:')
        num = int(input())


