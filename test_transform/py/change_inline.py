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
program_path = './program_file/pre_data/'
# author transformed program
o_program_path = './program_file/output_data/'
# save path after transformation
transform_file = './program_file/xml_data/'
# path of srcML.exe
srcml_path = './srcML/srcml.exe'

globalflag=0
def findfile(fname,flag,expr_xml,pathName):
    findflag=0
    #print(fname," ",pathName)
    if os.path.exists(pathName):
        fileList = os.listdir(pathName) #当前目录列表
        for f in fileList:
            if f == "$RECYCLE.BIN" or f == "System Volume Information":
                continue
            fpath = os.path.join(pathName, f)
            if os.path.isdir(fpath):
                fpath=fpath+'/'
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
                #print("finline:",finline)
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
    global globalflag
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
                            name = expr_xml.xpath('x:name', namespaces=ns)
                            if len(name):
                                #print(name)
                                tmp_final = name[0].xpath('string(.)') + "="
                            else:
                                tmp_final=''
                            fname=call_xml[0].xpath('string(.)')
                            #print(fname)
                            #记录所调用的函数为下一步转化做准备
                            i=1
                            for argu in call_xml[1].xpath('./x:argument',namespaces=ns):
                                if argu[0][0].tag=='{http://www.srcML.org/srcML/src}name' or argu[0][0].tag=='{http://www.srcML.org/srcML/src}literal' \
                                        or argu[0][0].tag=='{http://www.srcML.org/srcML/src}call':
                                    #函数实参
                                    globals()['argu'+str(i)]=argu[0][0].text

                                i=i+1
                            findflag=0
                            for fuc in rootT.xpath('//x:function', namespaces=ns):
                                xname=fuc[1].xpath('string(.)')

                                if fname==xname:
                                    findflag=1
                                    lines=[]
                                    varname=[]
                                    if len(fuc.xpath('./x:block',namespaces=ns)):
                                        blockc=fuc.xpath('./x:block',namespaces=ns)[0]
                                        tmp = blockc.xpath('string(.)')
                                    else:
                                        continue
                                    tmp=blockc.xpath('string(.)')
                                    #print("tmp: ",tmp)
                                    for block in fuc.xpath('./x:block/x:block_content', namespaces=ns):
                                        #print("block",block.xpath('string(.)'))
                                        for defineline in block.xpath('./x:decl_stmt', namespaces=ns):
                                            lines.append(defineline.xpath('string(.)'))
                                            for vname in defineline.xpath('./x:decl/x:name', namespaces=ns):
                                                varname.append(vname.xpath('string(.)'))
                                            # block.remove(defineline)
                                    finline = fuc[3].xpath('string(.)')

                                    fuc.remove(blockc)
                                    newnode = etree.SubElement(fuc, 'newnode')
                                    newnode.text = tmp
                                    #print(newnode.text)

                                    #print(lines)
                                    #print(varname)

                                    #print(fuc[3].text)
                                    #print(finline)

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
                                        c=c.replace(a,b or "")
                                        finline = c
                                    #局部变量替换
                                    #print(varname)

                                    if len(varname)>0:
                                        globalflag=globalflag+1
                                        for var in varname:
                                            var1=xname+"_"+str(globalflag)+"_"+var
                                            c=finline
                                            c=c.replace(var,var1)
                                            finline=c

                                    # c = c.replace("{", "(")
                                    # c = c.replace("}", ")")
                                    # c = c.replace(";", ",")
                                    c = c.replace("return", tmp_final)
                                    # tmp=c.rindex(",")
                                    # c=c[:tmp]+c[tmp+1:]
                                    finline=c
                                   # print(expr_xml.xpath('string(.)'))
                                    expr_stmt_xml.remove(expr_xml)
                                    #替换
                                    newnode=etree.SubElement(expr_stmt_xml,'newnode')
                                    newnode.text=finline
                                    globals()['cflag']=1


                                    tmp2=''
                                    for i in lines:
                                        tmp2=tmp2+i+'\n'
                                    #print(tmp1)
                                    #print(str(expr_xml.text))
                                    expr_xml.text=tmp2
                                    if len(varname)>0:
                                        for var in varname:
                                            var1=xname+"_"+str(globalflag)+"_"+var
                                            c=expr_xml.text.replace(var,var1)
                                            expr_xml.text=c

                                    break
                            #暂时只在本地找
                            if findflag==0:
                                continue
                                    #findfile(fname,1,expr_xml,program_path)
                        else:#不存在参数调用
                            continue
                            # fname=call_xml[0].xpath('string(.)')
                            # findflag=0
                            # for fuc in rootT.xpath('//x:function', namespaces=ns):
                            #     xname=fuc[1].xpath('string(.)')
                            #     if fname==xname:
                            #         findflag=1
                            #         finline=fuc[3].xpath('string(.)')
                            #         expr_xml.remove(expr_xml[0])
                            #         newnode=etree.SubElement(expr_xml,'newnode')
                            #         newnode.text=finline
                            #         globals()['cflag']=1
                            #         break
                            #
                            # if findflag==0:
                            #         findfile(fname,0,expr_xml,program_path)

    # 写入文件
    tree.write(output_path)
    return globals()['cflag']