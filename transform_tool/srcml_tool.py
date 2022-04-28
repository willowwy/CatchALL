# -*- coding: utf-8 -*-
# author:yejunyao
# datetime:2022/4/28 16:31


"""
description：格式更改工具
1.将代码文件格式转为xml文件格式
2.将xml转为代码
"""

import os
import subprocess
import re
import sys

cur_path = os.path.abspath('.')
up_path = os.path.dirname(cur_path)
sys.path.append(up_path)
sys.path.append(cur_path)


flag = True  # indicates whether the shell command runs successfully
program_style_flag = 'c'  # program's style c++/java/c


# express shell command
def cmd(command):
    """"""
    global flag
    flag = True
    subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    subp.wait(10)
    if subp.poll() == 0:
        flag = True
    else:
        print("False!")
        flag = False


# convert program to xml
def srcml_program_xml(pre_path, xml_path):
    # srcml rotate.c -o rotate.xml
    commend_str = 'srcml \"' + pre_path + '\" -o \"' + xml_path + '.xml\" --position --src-encoding UTF-8'
    cmd(commend_str)


# convert xml to program
def srcml_xml_program(pre_path, xml_path):
    commend_str = "srcml \"" + pre_path + '\" -o \"' + xml_path + "\" --src-encoding UTF-8"
    cmd(commend_str)
