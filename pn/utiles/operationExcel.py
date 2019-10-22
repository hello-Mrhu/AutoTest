#encoding:utf - 8

import xlrd
from xlutils.copy import copy
import public
from excel_data import *

class operationExcel:
    def getExcel(self):
        db = xlrd.open_workbook(public.data_dir('data','data.xls'))
        sheet = db.sheets()[0]
        return sheet
    # def get_rows(self):
    #     '''获取行数'''
    #     return self.getExcel().nrows
    def get_row_cell(self,row,col):
        return self.getExcel().cell_value(row,col)

    def get_caseid(self,row):
        '''获取caseID'''
        return self.get_row_cell(row,getcaseid())

    def get_url(self,row):
        '''获取请求地址地址'''
        return self.get_row_cell(row,geturl())

    def get_request_data(self,row):
        '''获取请求数据'''
        return self.get_row_cell(row,getequest_data())

    def get_expect(self,row):
        '''获取请求期望结果'''
        return self.get_row_cell(row,getexpect())
    def get_result(self,row):
        '''获取请求实际结果'''
        return self.get_row_cell(row,getresult())


opera = operationExcel()
print(opera.get_caseid(1))