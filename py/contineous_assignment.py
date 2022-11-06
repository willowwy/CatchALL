"""

    A=B=C; -> B=C,A=B;


"""



import copy
import os
from lxml import etree
from lxml.etree import Element
flag = True
doc = None
ns = {'src':'http://www.srcML.org/srcML/src'}
e = None



def init_parse(file):
    global doc
    doc = etree.parse(file)
    global e
    e = etree.XPathEvaluator(doc, namespaces={'src': 'http://www.srcML.org/srcML/src'})
    return e


def get_expr(e):
    #获得所有的表达式
    return e('//src:expr')

def trans_tree(e, ignore_list=[], instances=None):
    global flag
    flag = False
    expr_elems = [get_expr(e) if instances is None else (instance[0] for instance in instances)]
    tree_root = e('/*')[0].getroottree()
    new_ignore_list = []
    for item in expr_elems:
        for expr_elem in item:
            expr_elem_prev = expr_elem.getprevious()
            expr_elem_prev = expr_elem_prev if expr_elem_prev is not None else expr_elem
            expr_elem_prev_path = tree_root.getpath(expr_elem_prev)
            if expr_elem_prev_path in ignore_list:
                continue

            if(len(expr_elem)) == 5:
                tag = etree.QName(expr_elem.getparent())
                if tag.localname == 'condition':
                    continue
                var = []
                if expr_elem[1].text == '=' and expr_elem[3].text == '=':
                    flag = True
                    var.append(expr_elem[0])
                    var.append(expr_elem[2])
                    var.append(expr_elem[4])
                    #进行替换
                    parent = expr_elem.getparent()
                    parent.remove(expr_elem)
                    node = Element('expr')
                    node.append(Element('name'))
                    node.append(Element('operator'))
                    node.append(Element('name'))
                    node.append(Element('name'))
                    node.append(Element('operator'))
                    node.append(Element('name'))
                    node[0].text = var[1].text
                    node[2].text = var[2].text
                    node[3].text = var[0].text
                    node[5].text = var[1].text
                    node[1].text = '='
                    node[4].text = '='
                    node[2].tail = ','
                    node[5].tail = ';'
                    parent.append(node)
    return flag



                

def save_tree_to_file(tree, path):
    with open(path, 'w') as f:
        f.write(etree.tostring(tree).decode('utf8'))

def program_transform(input_path, output_path):
    e = init_parse(input_path)
    trans_tree(e)
    cflag = save_tree_to_file(doc,output_path)
    return cflag


