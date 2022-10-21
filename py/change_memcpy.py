import os.path
from typing import Text
from lxml import etree


def program_transform(input_path, output_path):

    xml_path = 'xml'
    xml_name = 'test.xml'
    tree = etree.parse(input_path)
    rootT = tree.getroot()
    nsp = {'x': 'http://www.srcML.org/srcML/src'}

    for func in rootT.xpath('//x:function', namespaces=nsp):
        for block_content_xml in func.xpath('//x:block/x:block_content', namespaces=nsp):
            for expr_stmt_xml in block_content_xml.xpath('//x:expr_stmt', namespaces=nsp):
                for expr_xml in expr_stmt_xml.xpath('x:expr', namespaces=nsp):
                    for call_xml in expr_xml.xpath('x:call', namespaces=nsp):
                        if call_xml[0].text=='memcpy':
                            for argument_list_xml in call_xml.xpath('x:argument_list', namespaces=nsp):
                              #for argument_xml in argument_list_xml('//x:argument', namespaces=nsp):
                                v1=argument_list_xml[0][0][0]
                                vname=v1.xpath('string(.)')     #变量a
                                q = argument_list_xml[2][0][0]
                                if q.text=='sizeof': #第三参数为sizeof
                                    m=q[0]
                                    v3=m[0][0][0]   #sizeof中的变量
                                    if vname!=None and v3.xpath('string(.)') ==vname: #a,sizeof(a)
                                        if m.tag=='{http://www.srcML.org/srcML/src}argument_list':
                                            m.tail='/1'
                                    elif v3.xpath('string(.)') !=vname:#在前面查找参数c的定义    a,sizeof(c)
                                        v1_type= ''
                                        v3_type= ''
                                        for decl_stmt_xml in block_content_xml.xpath('//x:decl_stmt', namespaces=nsp): #在当前函数中查找变量
                                            xname= decl_stmt_xml[0][1].xpath('string(.)') 
                                            if xname==vname:
                                                v1_type=decl_stmt_xml[0][0][0].xpath('string(.)') 
                                            elif xname==v3.xpath('string(.)') :
                                                v3_type=decl_stmt_xml[0][0][0].xpath('string(.)') 
                                        if(v1_type== '' or v3_type== ''):
                                            for decl_stmt_xml in rootT.xpath('//x:decl_stmt', namespaces=nsp):#查找全局变量
                                                xname = decl_stmt_xml[0][1].xpath('string(.)') 
                                                if xname == vname:
                                                    v1_type = decl_stmt_xml[0][0][0].xpath('string(.)') 
                                                elif xname == v3.xpath('string(.)') :
                                                    v3_type = decl_stmt_xml[0][0][0].xpath('string(.)') 
                                        if v1_type==v3_type:#a,sizeof(c)
                                            if m.tag == '{http://www.srcML.org/srcML/src}argument_list':
                                                m.tail = '/1'
                                elif q.tag=='{http://www.srcML.org/srcML/src}call': #第三参数为strlen？  q='call'
                                    m = q[1]
                                    v3 = m[0][0][0]  # strlen中的变量name标签
                                    if vname != None and v3.xpath('string(.)')  == vname:  # a,strlen(a)
                                        if m.tag == '{http://www.srcML.org/srcML/src}argument_list':
                                            m.tail = '/1'
                                elif q.tag=='{http://www.srcML.org/srcML/src}literal':#第三参数为数字
                                    continue
                                else:
                                    qstr=q.xpath('string(.)')
                                    #if q.tag== '{http://www.srcML.org/srcML/src}name':
                                    if qstr!=vname:
                                        v3=q
                                        v1_type = ''
                                        v3_type = ''
                                        for decl_stmt_xml in block_content_xml.xpath('//x:decl_stmt',namespaces=nsp):  # 在当前函数中查找变量
                                            xname = decl_stmt_xml[0][1].xpath('string(.)') 
                                            if xname==None and decl_stmt_xml[0][1][0].tag=='{http://www.srcML.org/srcML/src}name':
                                                xname=decl_stmt_xml[0][1][0].xpath('string(.)') 
                                            if xname == vname:#找到a的类型定义
                                                v1_type = decl_stmt_xml[0][0][0].xpath('string(.)') 
                                            elif xname == v3.xpath('string(.)') : #找到c的类型定义
                                                init_xml=decl_stmt_xml[0][1]
                                                if init_xml.text=='=':      #int a=x
                                                    if init_xml[0][0].text=='sizeof':
                                                        if init_xml[0][0][0][0][0][0].tag=='{http://www.srcML.org/srcML/src}name':
                                                            v3_type=init_xml[0][0][0][0][0][0].xpath('string(.)') 
                                                    elif init_xml[0][0].tag=='{http://www.srcML.org/srcML/src}call':
                                                        if init_xml[0][0][0].text=='strlen':
                                                            if init_xml[0][0][1][0][0][0].tag == '{http://www.srcML.org/srcML/src}name':
                                                                v3_type = init_xml[0][0][1][0][0][0].xpath('string(.)') 
                                                                if v3_type==vname:
                                                                    v3_type=v1_type
                                                                    
                                        for expr_stmt_xml in block_content_xml.xpath('//x:expr_stmt',namespaces=nsp):  # 在当前函数中查找变量
                                            xname = expr_stmt_xml[0][0].xpath('string(.)') 
                                            # if xname==None and decl_stmt_xml[0][1][0].tag=='{http://www.srcML.org/srcML/src}name':
                                            #     xname=decl_stmt_xml[0][1][0].xpath('string(.)') 
                                            # if xname == vname:#找到a的类型定义
                                            #     v1_type = decl_stmt_xml[0][0][0].xpath('string(.)') 
                                            # if xname == v3.xpath('string(.)') : #找到c的类型定义
                                            #     init_xml=expr_stmt_xml[0][1]
                                            #     if init_xml.text=='=':      #int a=x
                                            #         if init_xml[0][0].text=='sizeof':
                                            #             if init_xml[0][0][0][0][0][0].tag=='{http://www.srcML.org/srcML/src}name':
                                            #                 v3_type=init_xml[0][0][0][0][0][0].xpath('string(.)') 
                                            #         elif init_xml[0][0].tag=='{http://www.srcML.org/srcML/src}call':
                                            #             if init_xml[0][0][0].text=='strlen':
                                            #                 if init_xml[0][0][1][0][0][0].tag == '{http://www.srcML.org/srcML/src}name':
                                            #                     v3_type = init_xml[0][0][1][0][0][0].xpath('string(.)') 
                                            #                     if v3_type==vname:
                                            #                         v3_type=v1_type  
                                        
                                        if (v1_type == '' or v3_type == ''):
                                            for decl_stmt_xml in rootT.xpath('//x:decl_stmt', namespaces=nsp):  # 查找全局变量
                                                xname = decl_stmt_xml[0][1].xpath('string(.)') 
                                                if xname == vname:
                                                    v1_type = decl_stmt_xml[0][0][0].xpath('string(.)') 
                                                elif xname == v3.xpath('string(.)') :
                                                    init_xml = decl_stmt_xml[0][1]
                                                    if init_xml.text == '=':
                                                        if init_xml[0][0].text == 'sizeof':
                                                            if init_xml[0][0][0][0][0][0].tag == '{http://www.srcML.org/srcML/src}name':
                                                                v3_type = init_xml[0][0][0][0][0][0].xpath('string(.)') 
                                                        elif init_xml[0][0].text == 'strlen':
                                                            if init_xml[0][0][0][0][0][0].tag == '{http://www.srcML.org/srcML/src}name':
                                                                v3_type = init_xml[0][0][0][0][0][0].xpath('string(.)') 
                                                                if v3_type==vname:
                                                                    v3_type=v1_type
                                        if v1_type == v3_type :  # 替换
                                            if q.tag == '{http://www.srcML.org/srcML/src}argument':
                                                q[0].tail = '/1'
    # 写入文件
    tree.write(output_path)


