from argparse import Namespace
from typing import Text
from lxml import etree
from lxml import html

ns = {'x': 'http://www.srcML.org/srcML/src',
	'cpp': 'http://www.srcML.org/srcML/cpp',
	'pos': 'http://www.srcML.org/srcML/position'}



def program_transform(input_path, output_path):
    cflag=0
    print(input_path)
    tree = etree.parse(input_path)
    rootT = tree.getroot()
    
    for ifst in rootT.xpath('//x:if_stmt', namespaces=ns):
        for if_xml in ifst.xpath('./x:if', namespaces=ns):
            condition_xml=if_xml.find('./x:condition',namespaces=ns)
            if(len(condition_xml)):
                expr_xml=condition_xml.find('./x:expr',namespaces=ns)
                if(len(expr_xml)):
                    cond_expr=expr_xml.xpath('string(.)')
                    
                    andnum=cond_expr.count('&&')
                    if andnum!=0:
                        op=split(cond_expr,andnum)
                        # index0=0
                        # if0=0
                        # op=1
                        # used=-2
                        # for num in range (1,andnum+1):#now当前查找的& ，front前一个&，used完成存储的&
                        #     if num==1:
                        #         now=cond_expr.find('&&')
                        #         left=cond_expr.count('(',0,now)
                        #         right=cond_expr.count(')',0,now)
                        #         if left==right:
                        #             globals()['if'+str(op)]=cond_expr[:now]
                        #             op=op+1
                        #             used=now               
                        #     else:
                        #         now=cond_expr.find('&&',front+2)
                        #         if used<0:
                        #             left=cond_expr.count('(',0,now)
                        #             right=cond_expr.count(')',0,now)
                        #         else:
                        #             left=cond_expr.count('(',used,now)
                        #             right=cond_expr.count(')',used,now)
                        #         if left==right:
                        #             globals()['if'+str(op)]=cond_expr[used+2:now]
                        #             op=op+1
                        #             used=now
                                    
                        #     if num==andnum:
                        #         globals()['if'+str(op)]=cond_expr[used+2:]
                        #     front=now

                        #替换增加相应的判断
                        andnum=op-1
                        if_xml.tail=andnum*'}'
                        condition_xml.remove(expr_xml)
                        for op in range (1,andnum+2):
                            if op==1:
                                condition_xml.text='('+globals()['if'+str(op)]+')'
                            else:
                                newnode=etree.SubElement(condition_xml,'newnode')
                                newnode.text='{\n'+'if('+globals()['if'+str(op)]+')'
                                # condition_xml.appendchild()
                        cflag=1
    # 写入文件
    tree.write(output_path)
    return cflag
    
def split(cond_expr,andnum):
    index0=0
    if0=0
    op=1
    used=-2
    for num in range (1,andnum+1):#now当前查找的& ，front前一个&，used完成存储的&
        if num==1:
            now=cond_expr.find('&&')
            left=cond_expr.count('(',0,now)
            right=cond_expr.count(')',0,now)
            if left==right:
                globals()['if'+str(op)]=cond_expr[:now]
                op=op+1
                used=now               
        else:
            now=cond_expr.find('&&',front+2)
            if used<0:
                left=cond_expr.count('(',0,now)
                right=cond_expr.count(')',0,now)
            else:
                left=cond_expr.count('(',used,now)
                right=cond_expr.count(')',used,now)
            if left==right:
                globals()['if'+str(op)]=cond_expr[used+2:now]
                op=op+1
                used=now
                
        if num==andnum:
            globals()['if'+str(op)]=cond_expr[used+2:]
        front=now
    
    for num in range(1,op):
        fir=globals()['if'+str(num)][0]
        las=globals()['if'+str(num)][-1]
        if fir=='(' and las==')':
            globals()['if'+str(num)]=globals()['if'+str(num)][1:-1]
    return op