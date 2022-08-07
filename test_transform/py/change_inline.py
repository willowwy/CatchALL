from argparse import Namespace
from typing import Text
from lxml import etree
from lxml import html
import os
from transform_tool.srcml_tool import *
ns = {'x': 'http://www.srcML.org/srcML/src',
	'cpp': 'http://www.srcML.org/srcML/cpp',
	'pos': 'http://www.srcML.org/srcML/position'}

# author program to be transformed
program_path = './program_file/pre_data'
# author transformed program
o_program_path = './program_file/output_data'
# save path after transformation
transform_file = './program_file/xml_data'
# path of srcML.exe
srcml_path = './srcML/srcml.exe'


def findfile(fname,flag,expr_xml,pathName):
    findflag=0
    if os.path.exists(pathName):
        fileList = os.listdir(pathName) #当前目录列表
        for f in fileList:
            if f == "$RECYCLE.BIN" or f == "System Volume Information":
                continue
            fpath = os.path.join(pathName, f)
            if os.path.isdir(fpath):
                findflag=findfile(fname,flag,expr_xml,fpath)
                if findflag==1:
                    return
            else:
                if f.endswith('.c') or f.endswith('.h'):
                    xml_path=changefuc(fpath)
                    findflag=findfuc(xml_path,fname,flag,expr_xml)
                    if findflag==1:
                        return 1
                
def findfuc(input_path,fname,flag,expr_xml):
    tree = etree.parse(input_path)
    rootT = tree.getroot()
    findflag=0
    if flag==0:
        for fuc in rootT.xpath('//x:function', namespaces=ns):
            xname=fuc[1].xpath('string(.)')
            if fname==xname:
                findflag=1
                finline=fuc[3].xpath('string(.)')
                expr_xml.remove(expr_xml[0])
                newnode=etree.SubElement(expr_xml,'newnode')
                newnode.text=finline
                globals()['cflag']=1
                break
    elif flag==1:
        for fuc in rootT.xpath('//x:function', namespaces=ns):
            xname=fuc[1].xpath('string(.)')
            if fname==xname:
                findflag=1
                finline=fuc[3].xpath('string(.)')
                i=1
                for para in fuc[2].xpath('./x:parameter',namespaces=ns):
                    index=para[0].find('./x:name',namespaces=ns)
                    if index is not None:#存在参数调用                        
                        if para[0][1].tag=='{http://www.srcML.org/srcML/src}name':
                            globals()['para'+str(i)]=para[0][1].xpath('string(.)')
                            i=i+1

                for op in range(1,i):
                    a=globals()['para'+str(op)]
                    b=globals()['argu'+str(op)]
                    c=finline
                    c=c.replace(a,b)
                    finline=c

                expr_xml.remove(expr_xml[0])
                newnode=etree.SubElement(expr_xml,'newnode')
                newnode.text=finline
                globals()['cflag']=1
                break
    return findflag

def changefuc(file):
    file_xml='xinline.xml'
    xml_path = os.path.join(transform_file, file_xml)

    # 使用 scrML变化为临时xml文件
    srcml_program_xml(file, xml_path)
    tree = etree.parse(xml_path)
    rootT = tree.getroot()
    return xml_path
    
    

def program_transform(input_path, output_path):
    globals()['cflag']=0
    tree = etree.parse(input_path)
    rootT = tree.getroot()

    for func in rootT.xpath('//x:function', namespaces=ns):
        for block_content_xml in func.xpath('//x:block/x:block_content', namespaces=ns):
            for expr_stmt_xml in block_content_xml.xpath('//x:expr_stmt', namespaces=ns):
                for expr_xml in expr_stmt_xml.xpath('x:expr', namespaces=ns):
                    for call_xml in expr_xml.xpath('x:call', namespaces=ns):
                        index=call_xml[1].find('./x:argument',namespaces=ns)
                        if index is not None:#存在参数调用
                            fname=call_xml[0].xpath('string(.)')
                            i=1
                            for argu in call_xml[1].xpath('./x:argument',namespaces=ns):
                                if argu[0][0].tag=='{http://www.srcML.org/srcML/src}name' or argu[0][0].tag=='{http://www.srcML.org/srcML/src}literal':
                                    globals()['argu'+str(i)]=argu[0][0].text
                                i=i+1
                            findflag=0
                            for fuc in rootT.xpath('//x:function', namespaces=ns):
                                xname=fuc[1].xpath('string(.)')
                                if fname==xname:
                                    findflag=1
                                    finline=fuc[3].xpath('string(.)')
                                    i=1
                                    for para in fuc[2].xpath('./x:parameter',namespaces=ns):                                
                                        index=para[0].find('./x:name',namespaces=ns)
                                        if index is not None:#存在参数调用                        
                                            if para[0][1].tag=='{http://www.srcML.org/srcML/src}name':
                                                globals()['para'+str(i)]=para[0][1].xpath('string(.)')
                                                i=i+1

                                    for op in range(1,i):
                                        a=globals()['para'+str(op)]
                                        b=globals()['argu'+str(op)]
                                        c=finline
                                        c=c.replace(a,b)
                                        finline=c

                                    expr_xml.remove(expr_xml[0])
                                    newnode=etree.SubElement(expr_xml,'newnode')
                                    newnode.text=finline
                                    globals()['cflag']=1
                                    break
                            if findflag==0:
                                    findfile(fname,1,expr_xml,program_path)
                        else:#不存在参数调用
                            fname=call_xml[0].xpath('string(.)')
                            findflag=0
                            for fuc in rootT.xpath('//x:function', namespaces=ns):
                                xname=fuc[1].xpath('string(.)')
                                if fname==xname:
                                    findflag=1
                                    finline=fuc[3].xpath('string(.)')
                                    expr_xml.remove(expr_xml[0])
                                    newnode=etree.SubElement(expr_xml,'newnode')
                                    newnode.text=finline
                                    globals()['cflag']=1
                                    break
                            if findflag==0:
                                    findfile(fname,0,expr_xml,program_path)

    # 写入文件
    tree.write(output_path)
    return globals()['cflag']