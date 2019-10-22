#coding:utf-8


import os
import xlrd

'''查找文件的路径'''

def data_dir(data = None,filename = None):
    return os.path.join(os.path.dirname(os.path.dirname((__file__))),data,filename)



