# -*- coding:utf-8 -*-
#autor :huchengjiang

def transfer_requestSql(request_id):
    transfer_requestSql = 'select status,request_type from merchant_transfer_request where request_id = \'%s\' order by id desc' %request_id
    return transfer_requestSql
def account_bal_frz_recordSql():
    account_bal_frz_recordSql = 'select status,sum from account_bal_frz_record where account_id=\'220000000000000893\' order by row_create_time desc'
    return account_bal_frz_recordSql

def account_balance_change_historySql():
    account_balance_change_historySql = 'select op_type,fund from ACCOUNT_BALANCE_CHANGE_HISTORY where account_id=\'220000000000000893\' order by id desc'
    return account_balance_change_historySql

def trade_recordSql(request_id):
    trade_recordSql = 'select status,id from trade_record where order_id = \'%s\' order by id desc' %request_id
    return trade_recordSql

def actual_separate_account_recordSql(trade_id):
    actual_separate_account_recordSql = 'select trade_id from actual_separate_account_record where trade_id = \'%s\' order by id desc' %trade_id
    return actual_separate_account_recordSql
def fee_AuditSql(merchantFeeRequestId):
    fee_AuditSql='select status from MERCHANT_FEE_REQUEST where id = %s order by id desc' % merchantFeeRequestId

'''
新增查询语句，用于修改费率前查询原费率
'''
def merchant_feeSql(merchant_code,type):
    merchant_feeSql = 'select charge_type,limit_fund from merchant_fee where merchant_code = \'%s\' and type = \'%s\' order by id desc' %(merchant_code,type)
    return merchant_feeSql

'''
冻结解冻表查询预付手续费账户
'''
def account_bal_frz_recordSqlyf():
    account_bal_frz_recordSql = 'select status,sum from account_bal_frz_record where account_id=\'270000000000023398\' order by row_create_time desc'
    return account_bal_frz_recordSql

'''
历史余额变动表查询预付手续费账户
'''
def account_balance_change_historySqlyf():
    account_balance_change_historySql = 'select op_type,fund from ACCOUNT_BALANCE_CHANGE_HISTORY where account_id=\'270000000000023398\' order by id desc'
    return account_balance_change_historySql

'''
可用账户余额查询，不同的环境要更改账户ID
'''
def withdrawable_balance_account():
    withdrawable_balance_accountsql = 'select withdrawable_balance from account where id=\'220000000000000893\''
    return withdrawable_balance_accountsql

'''
商户付款请求表流水号
'''
def merchant_transferrequest():
    merchant_transferrequestsql = 'select request_id from merchant_transfer_request where merchant_id=\'104\' and status=\'2\' order by id desc'
    return merchant_transferrequestsql