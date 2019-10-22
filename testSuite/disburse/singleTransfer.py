#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/9 0009 下午 2:19
# @Author  : Administrator
# @Site    : 
# @File    : singleTransfer.py
# @Software: PyCharm
import requests
from baseLib.commonAPI import commonUtils, OracleQuery, SqlStatement
from baseLib.baseUtils.recorder import runningRecorder
from baseLib.operationManagerAPI.authentication import login
from baseLib.operationManagerAPI.DisburseManager import mgmodifyDisburseFee, transferRiskAudit
from baseLib.operationManagerAPI.feeAudit import merchantFeeAuditAction_auditConfirm
import unittest
from configuration import const
from baseLib.operationManagerAPI import merchantManage
from decimal import Decimal
import random


class singleTransfer(unittest.TestCase):
    """
    测试功能描述：
    	... ...
    """

    # 类运行时只调用一次，方法内参数可作为class内的全局变量使用
    @classmethod
    def setUpClass(self):
        self.globalRequestId = None
        # self.cookies = None

    # 每个testcase运行前执行，可作为测试用例初始化数据使用
    def setUp(self):
        self.actionUrl = 'http://172.16.3.9:8080/main/singleTransfer_toTransfer'
        # self.actionUrl = 'https://172.16.3.1/main/singleTransfer_toTransfer'
        self.requestSignatrueRule = ['requestId',
                                     'merchantCode',
                                     'transferType',
                                     'transToMerCode',
                                     'transToMerName',
                                     'sum',
                                     'accountType',
                                     'unionBankNum',
                                     'openBankName',
                                     'openBankProvince',
                                     'openBankCity',
                                     'accountName',
                                     'bankCode',
                                     'bankAccount',
                                     'reason',
                                     'noticeUrl',
                                     'refundNoticeUrl',
                                     'transferPayType']
        self.syncSignatrueRule = ['requestId',
                                  'result',
                                  'sum']
        self.asynSignatrueRule = []
        self.inputParameter = {
            'requestId': '',
            'merchantCode': 'CSSH',
            'transferType': '1',
            'transToMerCode': '',
            'transToMerName': '',
            'unionBankNum': '',
            'openBankName': '',
            'openBankProvince': '',
            'openBankCity': '',
            'sum': '0.03',
            'accountType': '1',
            'accountName': 'tester',
            'bankCode': 'ccb',
            'bankAccount': '6217000010031195525',
            'reason': '1555',
            'noticeUrl': 'http://172.16.3.1/testpayMobile/p2pNoticeGBK',
            'refundNoticeUrl': 'http://172.16.3.1/testpayMobile/p2pNoticeGBK',
            'transferPayType': '1',     #选输0：手工审核 1：自动实时
            'signature': ''
        }
        self.key = 'CSSH_KEY'
        self.outputParameter = {}
        self.IOParameter = {'请求参数':self.inputParameter, '响应参数': self.outputParameter}
        self.login_operator_returnTuple = login(const._global_configuration().optionManagerOperator)
        self.login_operator_status = self.login_operator_returnTuple[0]
        self.login_operator_cookies = self.login_operator_returnTuple[1]
        self.login_auditor_returnTuple = login(const._global_configuration().optionManagerAuditor)
        self.login_auditor_status = self.login_auditor_returnTuple[0]
        self.login_auditor_cookies = self.login_auditor_returnTuple[1]
        merLimit = {
                'type' : '5',
                'merSingleDayLimit': '',
                'merSingleDayCountLimit' : ''
        }
        mgmodifyDisburseFee(merLimit, self.login_operator_cookies, self.inputParameter['merchantCode'])
        smerchant_realtime_config_modify = {
            'merSingleLimit': '',
            'merSingleDayLimit': '',
        }
        merchantManage.merchant_realtime_transfer_info_mgmodify(smerchant_realtime_config_modify, self.login_operator_cookies,
                                                                self.inputParameter['merchantCode'])

    @runningRecorder(desc='')
    def test_singleTransfer_107040101003(self):
        """
            作者：刘佳琪
            需求版本号：SP_S_20170002（历史版本号:）
            用例编号：
                107040101003
            用例名称：
             付款至个人银行账户-跨行-普通商户付款配置：1自动实时
             签名规则：MD5
            用例描述：
                1、商户配置普通付款至个人银行账户手续费，手续费收取方式为预付
                2、商户配置代发-对私银行渠道
                3、商户付款配置：1自动实时
        """
        self.globalRequestId = commonUtils.requestId(num = 24)
        self.inputParameter['requestId'] = self.globalRequestId
        '''根据用例前置条件初始化输入参数'''
        updateinputParameter = {'transferType': '1', 'accountType': '0', 'unionBankNum': '105100005078',
                                'openBankName': '中国建设银行北京上地支行', 'openBankProvince': '北京市',
                                'openBankCity': '北京市', 'accountName': 'tester', 'bankCode': 'ccb',
                                'bankAccount': '6217000010031195525'
                                }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数
        self.inputParameter['signature'] = commonUtils.md5Signature(
            self.inputParameter,
            self.key,
            self.requestSignatrueRule)

        """修改商户为实时付款商户"""
        merchantManage.merchant_info_mgmodify({'fld16': '1'}, self.login_operator_cookies, self.inputParameter['merchantCode'])
        # 修改手续费收取方式为预付
        merchant_fee_type5 = OracleQuery.select_table(
            'merchant_fee',
            list_view = [
                'CHARGE_TYPE',
                'METHOD',
                'FIX_FEE',
                'FEE_RATE',
                'LIMIT_FIX_RATE_FUND'
            ],
            where_condition = "merchant_code = '%s' and type = '5' order by limit_layer" % self.inputParameter['merchantCode'])

        if str(merchant_fee_type5[0][0]) != '1' \
                or str(merchant_fee_type5[0][1]) != '2' \
                or merchant_fee_type5[0][2] != 0.02 \
                or merchant_fee_type5[1][3] != 1 \
                or merchant_fee_type5[0][4] != 300:
            inputFormParam = {
                'type': '5',
                'chargeType': '1',
                'meth' : '2',
                'fixFee': '0.02',
                'feeRate': '1',
                'limitFixRateFund': '300',
            }
            mgmodifyDisburseFee(inputFormParam, self.login_operator_cookies, self.inputParameter['merchantCode'])
            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view = ['ID'],
                where_condition = "merchant_code = '%s' and type = '5' and status = '0' and charge_type = '1'" % self.inputParameter['merchantCode'])[0][0]
            auditstatus = merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.login_auditor_cookies)
            self.assertEqual(auditstatus[0][0], 1, msg='费率修改失败')

        '''发起单笔付款请求'''
        respondse = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter),
                                  verify=False)
        self.outputParameter.update(respondse.json())
        syncSignature = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)

        '''同步返回参数校验'''
        # 请求流水
        self.assertEqual(self.outputParameter['requestId'], self.inputParameter['requestId'].decode(), msg='请求流水不一致')
        # 判断请求结果
        self.assertEqual(self.outputParameter['result'], '00000', msg='请求不成功')
        # 判断同步响应签名
        self.assertEqual(syncSignature, self.outputParameter['signature'], msg='同步签名验证不通过')
        # 判断请求金额
        self.assertEqual(self.outputParameter['sum'], self.inputParameter['sum'].decode(), msg='请求金额不正确')

        '''等待调度复核'''
        commonUtils.waiting(20)
        # 判断数据库状态
        merchant_transfer_request = OracleQuery.select_table(
            'merchant_transfer_request',
            list_view = [
                'status',
                'request_type',
                'id'
            ],
            where_condition = "request_id = '%s'" % self.inputParameter['requestId'].decode()
        )
        self.assertEqual(str(merchant_transfer_request[0][0]), '9', msg='请求状态正确')
        self.assertEqual(str(merchant_transfer_request[0][1]), '1', msg='请求类型正确')

        # account_bal_frz_record
        '''交易金额冻结'''
        MERCHANT = OracleQuery.select_table(
            'MERCHANT',
            list_view = [
                'ID'
            ],
            where_condition = "merchant_code = '%s'" % self.inputParameter['merchantCode'].decode()
        )
        MERCHANT_PREPAYMENT_ACCOUNT = OracleQuery.select_table(
            'MERCHANT_PREPAYMENT_ACCOUNT',
            list_view = [
                'ACCOUNT_ID'
            ],
            where_condition = "merchant_id = '%s'" % str(MERCHANT[0][0])
        )
        merchant_account_association = OracleQuery.select_table(
            'merchant_account_association',
            list_view = [
                'ACCOUNT_ID'
            ],
            where_condition = "merchant_id = '%s'" % str(MERCHANT[0][0])
        )

        account_bal_frz_record = OracleQuery.select_table(
            'account_bal_frz_record',
            list_view=[
                'SUM'
            ],
            where_condition="account_id = '%s' and status = '0' and table_name = 'MERCHANT_TRANSFER_REQUEST' and table_key = '%s'"
                            % (str(merchant_account_association[0][0]), str(merchant_transfer_request[0][2]))
        )
        self.assertEqual('0.03', str(account_bal_frz_record[0][0]))

        '''手续费冻结'''
        perpayment_account_bal_frz_record = OracleQuery.select_table(
            'account_bal_frz_record',
            list_view = [
                'SUM'
            ],
            where_condition = "account_id = '%s' and status = '0' and table_name = 'MERCHANT_TRANSFER_REQUEST' and table_key = '%s'"
                            % (str(MERCHANT_PREPAYMENT_ACCOUNT[0][0]), str(merchant_transfer_request[0][2]))
        )
        self.assertEqual('0.02', str(perpayment_account_bal_frz_record[0][0]))

        # ACCOUNT_BALANCE_CHANGE_HISTORY
        # account_balance_changehistory_OP_TYPE = str(
        #     OracleQuery.sqlAll(SqlStatement.account_balance_change_historySql())[0][0])
        # account_balance_changehistory_Fund = str(
        #     OracleQuery.sqlAll(SqlStatement.account_balance_change_historySql())[0][1])
        # self.assertEqual('0', account_balance_changehistory_OP_TYPE)
        # self.assertEqual(self.outputParameter['sum'], account_balance_changehistory_Fund)

    @runningRecorder(desc='')
    def test_singleTransfer_107040101004(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101004
        用例名称：
            付款至个人银行账户-快速-自动实时
        用例描述：
            1、商户配置快速付款至个人银行账户手续费，手续费收取方式为预付
            2、商户配置代发-对私银行渠道
            3、商户付款配置：1自动实时

        """
        self.globalRequestId = commonUtils.requestId(num=24)
        self.inputParameter['requestId'] = self.globalRequestId
        '''根据用例前置条件初始化输入参数'''
        updateinputParameter = {'transferType': '1', 'accountType': '0', 'unionBankNum': '105100005078',
                                'openBankName': '中国建设银行北京上地支行', 'openBankProvince': '北京市',
                                'openBankCity': '北京市', 'accountName': 'tester', 'bankCode': 'ccb',
                                'bankAccount': '6217000010031195525'
                                }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数
        self.inputParameter['signature'] = commonUtils.md5Signature(
            self.inputParameter,
            self.key,
            self.requestSignatrueRule)

        """修改商户为实时付款商户"""
        merchantManage.merchant_info_mgmodify({'fld16': '1'}, self.login_operator_cookies, self.inputParameter['merchantCode'])
        # 修改手续费收取方式为预付
        merchant_fee_type5 = OracleQuery.select_table(
            'merchant_fee',
            list_view=[
                'CHARGE_TYPE',
                'METHOD',
                'FIX_FEE',
                'FEE_RATE',
                'LIMIT_FIX_RATE_FUND'
            ],
            where_condition="merchant_code = '%s' and type = '12'" % self.inputParameter['merchantCode'])

        if str(merchant_fee_type5[0][0]) != '1' \
                or str(merchant_fee_type5[0][1]) != '2' \
                or str(merchant_fee_type5[0][2]) != '0.02' \
                or str(merchant_fee_type5[0][3]) != '1' \
                or str(merchant_fee_type5[0][4]) != '300':
            inputFormParam = {
                'type': '12',
                'chargeType': '1',
                'meth': '2',
                'fixFee': '0.02',
                'feeRate': '1',
                'limitFixRateFund': '300',
            }
            mgmodifyDisburseFee(inputFormParam, self.login_operator_cookies, self.inputParameter['merchantCode'])
            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['ID'],
                where_condition="merchant_code = '%s' and type = '12' and status = '0' and charge_type = '1'" %
                                self.inputParameter['merchantCode'])[0][0]
            auditstatus = merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.login_auditor_cookies)
            self.assertEqual(auditstatus[0][0], 1, msg='费率修改失败')

        '''发起单笔付款请求'''
        respondse = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter),
                                  verify=False)
        self.outputParameter.update(respondse.json())
        syncSignature = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)

        '''同步返回参数校验'''
        # 请求流水
        self.assertEqual(self.outputParameter['requestId'], self.inputParameter['requestId'].decode(), msg='请求流水不一致')
        # 判断请求结果
        self.assertEqual(self.outputParameter['result'], '00000', msg='请求不成功')
        # 判断同步响应签名
        self.assertEqual(syncSignature, self.outputParameter['signature'], msg='同步签名验证不通过')
        # 判断请求金额
        self.assertEqual(self.outputParameter['sum'], self.inputParameter['sum'].decode(), msg='请求金额不正确')

        '''等待调度复核'''
        commonUtils.waiting(20)
        # 判断数据库状态
        merchant_transfer_request = OracleQuery.select_table(
            'merchant_transfer_request',
            list_view=[
                'status',
                'request_type',
                'id'
            ],
            where_condition="request_id = '%s'" % self.inputParameter['requestId'].decode()
        )
        # requestStatus = str(
        #     OracleQuery.sqlAll(SqlStatement.transfer_requestSql(self.outputParameter['requestId']))[0][0])
        # request_type = str(
        #     OracleQuery.sqlAll(SqlStatement.transfer_requestSql(self.outputParameter['requestId']))[0][1])
        self.assertEqual(str(merchant_transfer_request[0][0]), '9', msg='请求状态正确')
        self.assertEqual(str(merchant_transfer_request[0][1]), '1', msg='请求类型正确')

        # account_bal_frz_record
        '''交易金额冻结'''
        MERCHANT = OracleQuery.select_table(
            'MERCHANT',
            list_view=[
                'ID'
            ],
            where_condition="merchant_code = '%s'" % self.inputParameter['merchantCode'].decode()
        )
        MERCHANT_PREPAYMENT_ACCOUNT = OracleQuery.select_table(
            'MERCHANT_PREPAYMENT_ACCOUNT',
            list_view=[
                'ACCOUNT_ID'
            ],
            where_condition="merchant_id = '%s'" % str(MERCHANT[0][0])
        )
        merchant_account_association = OracleQuery.select_table(
            'merchant_account_association',
            list_view=[
                'ACCOUNT_ID'
            ],
            where_condition="merchant_id = '%s'" % str(MERCHANT[0][0])
        )

        account_bal_frz_record = OracleQuery.select_table(
            'account_bal_frz_record',
            list_view=[
                'SUM'
            ],
            where_condition="account_id = '%s' and status = '0' and table_name = 'MERCHANT_TRANSFER_REQUEST' and table_key = '%s'"
                            % (str(merchant_account_association[0][0]), str(merchant_transfer_request[0][2]))
        )
        self.assertEqual('0.03', str(account_bal_frz_record[0][0]))

        '''手续费冻结'''
        perpayment_account_bal_frz_record = OracleQuery.select_table(
            'account_bal_frz_record',
            list_view=[
                'SUM'
            ],
            where_condition="account_id = '%s' and status = '0' and table_name = 'MERCHANT_TRANSFER_REQUEST' and table_key = '%s'"
                            % (str(MERCHANT_PREPAYMENT_ACCOUNT[0][0]), str(merchant_transfer_request[0][2]))
        )
        self.assertEqual('0.02', str(perpayment_account_bal_frz_record[0][0]))

        # ACCOUNT_BALANCE_CHANGE_HISTORY
        # account_balance_changehistory_OP_TYPE = str(
        #     OracleQuery.sqlAll(SqlStatement.account_balance_change_historySql())[0][0])
        # account_balance_changehistory_Fund = str(
        #     OracleQuery.sqlAll(SqlStatement.account_balance_change_historySql())[0][1])
        # self.assertEqual('0', account_balance_changehistory_OP_TYPE)
        # self.assertEqual(self.outputParameter['sum'], account_balance_changehistory_Fund)

    @unittest.skip('未执行')
    @runningRecorder(desc='')
    def test_singleTransfer_107040101005(self):
        """
          作者：刘佳琪
          需求版本号：SP_S_20170008（历史版本号）
          用例编号：
              107040101005
          用例名称：
          	付款至企业银行账户-普通-实时-固定/阶梯值
            商户付款配置：0手工审核
        """
        pass

    @unittest.skip('手工复合还未实现自动化')
    @runningRecorder(desc='')
    def test_singleTransfer_107040101006(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101006
        用例名称：
            付款至企业银行账户-快速-预付-固定值+费率
        用例描述：
            1、商户配置快速付款至企业银行账户手续费，手续费收取方式为预付-固定值+费率
            2、商户配置代发-对公银行渠道
            3、商户付款配置：0手工审核

        """
        self.globalRequestId = commonUtils.requestId(num=24)
        self.inputParameter['requestId'] = self.globalRequestId
        '''根据用例前置条件初始化输入参数'''
        updateinputParameter = {
            'transferType': '2',
            'accountType': '1',
            'unionBankNum': '105100005078',
            'openBankName': '中国建设银行北京上地支行',
            'openBankProvince': '北京市',
            'openBankCity': '北京市',
            'accountName': 'tester',
            'bankCode': 'ccb',
            'bankAccount': '6217000010031195525',
            'transferPayType' : '0'
        }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数
        self.inputParameter['signature'] = commonUtils.md5Signature(
            self.inputParameter,
            self.key,
            self.requestSignatrueRule)
        respondsecookies = login(const._global_configuration().optionManagerOperator)
        """修改商户为实时付款商户"""
        merchantManage.merchant_info_mgmodify({'fld16': '1'}, respondsecookies[1], self.inputParameter['merchantCode'])
        # 修改手续费收取方式为预付
        merchant_fee_type5 = OracleQuery.select_table(
            'merchant_fee',
            list_view=[
                'CHARGE_TYPE',
                'METHOD',
                'FIX_FEE',
                'FEE_RATE',
                'LIMIT_FIX_RATE_FUND'
            ],
            where_condition="merchant_code = '%s' and type = '13'" % self.inputParameter['merchantCode']
        )

        if str(merchant_fee_type5[0][0]) != '1' \
                or str(merchant_fee_type5[0][1]) != '2' \
                or str(merchant_fee_type5[0][2]) != '0.02' \
                or str(merchant_fee_type5[0][3]) != '1' \
                or str(merchant_fee_type5[0][4]) != '300':
            inputFormParam = {
                'type': '13',
                'chargeType': '1',
                'meth': '2',
                'fixFee': '0.02',
                'feeRate': '1',
                'limitFixRateFund': '300',
            }
            mgmodifyDisburseFee(inputFormParam, respondsecookies[1], self.inputParameter['merchantCode'])
            self.cookies = login(const._global_configuration().optionManagerAuditor)
            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['ID'],
                where_condition="merchant_code = '%s' and type = '13' and status = '0' and charge_type = '1'" %
                                self.inputParameter['merchantCode'])[0][0]
            auditstatus = merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.cookies[1])
            self.assertEqual(auditstatus[0][0], 1, msg='费率修改失败')

        '''发起单笔付款请求'''
        respondse = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter),
                                  verify=False)
        self.outputParameter.update(respondse.json())
        syncSignature = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)

        '''同步返回参数校验'''
        # 请求流水
        self.assertEqual(self.outputParameter['requestId'], self.inputParameter['requestId'].decode(), msg='请求流水不一致')
        # 判断请求结果
        self.assertEqual(self.outputParameter['result'], '00000', msg='请求不成功')
        # 判断同步响应签名
        self.assertEqual(syncSignature, self.outputParameter['signature'], msg='同步签名验证不通过')
        # 判断请求金额
        self.assertEqual(self.outputParameter['sum'], self.inputParameter['sum'].decode(), msg='请求金额不正确')

        '''等待调度复核'''
        commonUtils.waiting(20)
        # 判断数据库状态
        merchant_transfer_request = OracleQuery.select_table(
            'merchant_transfer_request',
            list_view=[
                'status',
                'request_type',
                'id'
            ],
            where_condition="request_id = '%s'" % self.inputParameter['requestId'].decode()
        )
        # requestStatus = str(
        #     OracleQuery.sqlAll(SqlStatement.transfer_requestSql(self.outputParameter['requestId']))[0][0])
        # request_type = str(
        #     OracleQuery.sqlAll(SqlStatement.transfer_requestSql(self.outputParameter['requestId']))[0][1])
        self.assertEqual(str(merchant_transfer_request[0][0]), '9', msg='请求状态正确')
        self.assertEqual(str(merchant_transfer_request[0][1]), '1', msg='请求类型正确')

        # account_bal_frz_record
        '''交易金额冻结'''
        MERCHANT = OracleQuery.select_table(
            'MERCHANT',
            list_view=[
                'ID'
            ],
            where_condition="merchant_code = '%s'" % self.inputParameter['merchantCode'].decode()
        )
        MERCHANT_PREPAYMENT_ACCOUNT = OracleQuery.select_table(
            'MERCHANT_PREPAYMENT_ACCOUNT',
            list_view=[
                'ACCOUNT_ID'
            ],
            where_condition="merchant_id = '%s'" % str(MERCHANT[0][0])
        )
        merchant_account_association = OracleQuery.select_table(
            'merchant_account_association',
            list_view=[
                'ACCOUNT_ID'
            ],
            where_condition="merchant_id = '%s'" % str(MERCHANT[0][0])
        )

        account_bal_frz_record = OracleQuery.select_table(
            'account_bal_frz_record',
            list_view=[
                'SUM'
            ],
            where_condition="account_id = '%s' and status = '0' and table_name = 'MERCHANT_TRANSFER_REQUEST' and table_key = '%s'"
                            % (str(merchant_account_association[0][0]), str(merchant_transfer_request[0][2]))
        )
        self.assertEqual('0.03', str(account_bal_frz_record[0][0]))

        '''手续费冻结'''
        perpayment_account_bal_frz_record = OracleQuery.select_table(
            'account_bal_frz_record',
            list_view=[
                'SUM'
            ],
            where_condition="account_id = '%s' and status = '0' and table_name = 'MERCHANT_TRANSFER_REQUEST' and table_key = '%s'"
                            % (str(MERCHANT_PREPAYMENT_ACCOUNT[0][0]), str(merchant_transfer_request[0][2]))
        )
        self.assertEqual('0.02', str(perpayment_account_bal_frz_record[0][0]))

        # ACCOUNT_BALANCE_CHANGE_HISTORY
        # account_balance_changehistory_OP_TYPE = str(
        #     OracleQuery.sqlAll(SqlStatement.account_balance_change_historySql())[0][0])
        # account_balance_changehistory_Fund = str(
        #     OracleQuery.sqlAll(SqlStatement.account_balance_change_historySql())[0][1])
        # self.assertEqual('0', account_balance_changehistory_OP_TYPE)
        # self.assertEqual(self.outputParameter['sum'], account_balance_changehistory_Fund)


    @unittest.skip('未执行')
    @runningRecorder(desc='')
    def test_singleTransfer_107040101008(self):
        """
          作者：刘佳琪
          需求版本号：SP_S_20170008（历史版本号）
          用例编号：
              107040101008
          用例名称：
          	商户未进行付款配置
        """
        pass

    @runningRecorder(desc='')
    def test_singleTransfer_107040101009(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101009
        用例名称：
            付款请求金额大于商户可用金额-手续费实时收取
        用例描述：
            手续费实时收取

        """

        MERCHANT = OracleQuery.select_table(
            'MERCHANT',
            list_view = [
                'ID'
            ],
            where_condition = "merchant_code = '%s'" % self.inputParameter['merchantCode']
        )
        merchant_account_association = OracleQuery.select_table(
            'merchant_account_association',
            list_view = [
                'ACCOUNT_ID'
            ],
            where_condition = "merchant_id = '%s'" % str(MERCHANT[0][0])
        )
        account = OracleQuery.select_table(
            'account',
            list_view = [
                'withdrawable_balance'
            ],
            where_condition = "id = '%s'" % str(merchant_account_association[0][0])
        )
        voucher = OracleQuery.select_table(
            'voucher',
            list_view = [
                'sum(credited)-sum(debited)'
            ],
            where_condition = "account_id = '%s' and UPDATE_BALANCE_STATUS = '0'" % str(merchant_account_association[0][0])
        )
        sum = Decimal(str(voucher[0][0])) + Decimal(str(account[0][0]))
        pay_fund = sum + Decimal('0.02')

        merchant_fee_type12 = OracleQuery.select_table(
            'merchant_fee',
            list_view=[
                'CHARGE_TYPE',
                'LIMIT_FUND'
            ],
            where_condition="merchant_code = '%s' and type = '12'" % self.inputParameter['merchantCode']
        )
        # 修改手续费收取方式为实时(快速个人)
        if str(merchant_fee_type12[0][0]) != '0' or Decimal(str(merchant_fee_type12[0][1])) < pay_fund:
            inputFormParam = {
                'type': '12',
                'chargeType': '0',
                'minFee' : '0.01',
                'maxFee' : '4',
                'limitFund' : str(pay_fund)
            }
            mgmodifyDisburseFee(inputFormParam, self.login_operator_cookies, self.inputParameter['merchantCode'])

            '''审核费率'''
            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['ID'],
                where_condition="merchant_code = '%s' and type = '12' and status = '0' and charge_type = '0'" %
                                self.inputParameter['merchantCode'])[0][0]
            merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.login_auditor_cookies)
        # 发送请求
        self.globalRequestId = commonUtils.requestId()
        self.inputParameter['requestId'] = self.globalRequestId
        self.inputParameter['sum'] = str(pay_fund)
        self.inputParameter['transferType'] = '1'
        self.inputParameter['accountType'] = '1'
        self.inputParameter['transferPayType'] = '0'
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        s = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
        self.outputParameter.update(s.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)
        '''代发请求'''

        # 响应错误码断言
        self.assertEqual('200300162', self.outputParameter['result'], msg=self.IOParameter)

    @runningRecorder(desc='')
    def test_singleTransfer_107040101010(self):
        """
            作者：刘佳琪
            需求版本号：SP_S_20170002（历史版本号:sp_20150011）
            用例编号：
                107040101010
            用例名称：
             付款请求金额大于商户可用金额-手续费预付
             签名规则：MD5
            用例描述：
                1、手续费收取方式为预付
        """
        merchant_fee_type5 = OracleQuery.select_table(
            'merchant_fee',
            list_view=[
                'CHARGE_TYPE'
            ],
            where_condition="merchant_code = '%s' and type = '5'" % self.inputParameter['merchantCode']
        )

        if str(merchant_fee_type5[0][0]) != '1':
            respondsecookies = login(const._global_configuration().optionManagerOperator)
            inputFormParam = {
                'type': '5',
                'chargeType': '1'
            }
            # Method = str( OracleQuery.sqlAll('select METHOD from merchant_fee where merchant_id=\'104\' and type =\'12\'')[0][0])
            # inputFormParam['oldMethod'] = Method
            mgmodifyDisburseFee(inputFormParam, respondsecookies[1], self.inputParameter['merchantCode'])

            '''审核费率'''
            self.cookies = login(const._global_configuration().optionManagerAuditor)
            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['ID'],
                where_condition="merchant_code = '%s' and type = '5' and status = '0' and charge_type = '1'" %
                                self.inputParameter['merchantCode'])[0][0]
            merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.cookies[1])
        # 发送请求
        self.globalRequestId = commonUtils.requestId()
        self.inputParameter['requestId'] = self.globalRequestId
        # withdrawablebalance = float(OracleQuery.sqlAll(SqlStatement.withdrawable_balance_account())[0][0])
        MERCHANT = OracleQuery.select_table(
            'MERCHANT',
            list_view=[
                'ID'
            ],
            where_condition="merchant_code = '%s'" % self.inputParameter['merchantCode']
        )
        merchant_account_association = OracleQuery.select_table(
            'merchant_account_association',
            list_view=[
                'ACCOUNT_ID'
            ],
            where_condition="merchant_id = '%s'" % str(MERCHANT[0][0])
        )
        account = OracleQuery.select_table(
            'account',
            list_view=[
                'withdrawable_balance'
            ],
            where_condition="id = '%s'" % str(merchant_account_association[0][0])
        )
        voucher = OracleQuery.select_table(
            'voucher',
            list_view=[
                'sum(credited)-sum(debited)'
            ],
            where_condition="account_id = '%s' and UPDATE_BALANCE_STATUS = '0'" % str(
                merchant_account_association[0][0])
        )
        sum = Decimal(str(voucher[0][0])) + Decimal(str(account[0][0]))
        self.inputParameter['sum'] = str(sum + Decimal('0.02'))
        self.inputParameter['transferType'] = '1'
        self.inputParameter['accountType'] = '1'
        self.inputParameter['transferPayType'] = '0'
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        s = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
        self.outputParameter.update(s.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)
        '''代发请求'''

        # 响应错误码断言
        self.assertEqual('200300162', self.outputParameter['result'], msg=self.IOParameter)

    @runningRecorder(desc='')
    def test_singleTransfer_107040101015(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101015
        用例名称：
            普通付款至个人银行账户-金额大于单笔限额
        用例描述：
            付款方式选择付款至个人银行账户，
            到账类型选择普通
            输入付款金额>商户配置的普通付款至个人银行账户单笔限额

        """
        # '''查询普通付款至银行账户单笔限额'''
        # limit_FundSql='select LIMIT_FUND from merchant_fee where merchant_code=\'CSSH\' and type=\'5\' order by id desc'
        # limit_Fund=OracleQuery.sqlAll(limit_FundSql)[0][0]

        merchant_fee_type5 = OracleQuery.select_table(
            'merchant_fee',
            list_view = [
                'LIMIT_FUND'
            ],
            where_condition = "merchant_code = '%s' and type = '5'" % self.inputParameter['merchantCode'])
        if str('{:g}'.format(merchant_fee_type5[0][0])) != '301':
            '''初始化商户配置'''
            self.cookies = login(const._global_configuration().optionManagerOperator)
            commonUtils.waiting(1)
            '''修改单笔限额'''
            inputFormParam = {
                'type': '5',
                'limitFund': '301'
            }
            mgmodifyDisburseFee(inputFormParam, self.cookies[1], self.inputParameter['merchantCode'])
            '''审核费率'''
            self.cookies = login(const._global_configuration().optionManagerAuditor)
            # commonUtils.waiting(1)
            # fee_AuditSql = 'select id from MERCHANT_FEE_REQUEST order by id desc'
            # merchantFeeRequestId = str(OracleQuery.sqlAll(fee_AuditSql)[0][0])
            # merchantFeeAuditAction_auditConfirm(merchantFeeRequestId, self.cookies[1])

            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['ID'],
                where_condition="merchant_code = '%s' and type = '5' and status = '0' and limit_Fund = '301'" %
                                self.inputParameter['merchantCode'])[0][0]
            auditstatus = merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.cookies[1])
            self.assertEqual(auditstatus[0][0], 1, msg='费率修改失败')

        updateinputParameter = {'transferType': '1', 'accountType': '0', 'unionBankNum': '105100005078',
                                'openBankName': '中国建设银行北京上地支行', 'openBankProvince': '北京市',
                                'openBankCity': '北京市', 'accountName': 'tester', 'bankCode': 'ccb',
                                'bankAccount': '6217000010031195525'
                                }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数
        # 发送请求
        self.globalRequestId = commonUtils.requestId()
        self.inputParameter['requestId'] = self.globalRequestId
        self.inputParameter['sum'] = '301.02'
        self.inputParameter['transferPayType'] = '0'
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        s = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
        self.outputParameter.update(s.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)
        '''代发请求'''

        # 响应签名断言
        self.assertEqual('200300277', self.outputParameter['result'], msg=self.IOParameter)

    @runningRecorder(desc='')
    def test_singleTransfer_107040101016(self):
        """
            作者：刘佳琪
            需求版本号：SP_S_20170002（历史版本号:sp_20150011）
            用例编号：
                107040101016
            用例名称：
             快速付款至个人银行账户-金额大于单笔限额
             签名规则：MD5
            用例描述：
            1、商户配置快速付款至个人银行账户手续费收取方式、单笔限额（运营管理-商户付款管理中）
            select * from merchant_fee where merchant_code='商户编码' and type='12' order by id desc;
        """
        merchant_fee_type12 = OracleQuery.select_table(
            'merchant_fee',
            list_view=[
                'LIMIT_FUND'
            ],
            where_condition="merchant_code = '%s' and type = '12'" % self.inputParameter['merchantCode'])

        if str('{:g}'.format(merchant_fee_type12[0][0])) != '301':
            '''初始化商户配置'''
            self.cookies = login(const._global_configuration().optionManagerOperator)
            commonUtils.waiting(1)
            '''修改单笔限额'''
            inputFormParam = {
                'type': '12',
                'limitFund': '301'
            }
            mgmodifyDisburseFee(inputFormParam, self.cookies[1], self.inputParameter['merchantCode'])
            '''审核费率'''
            self.cookies = login(const._global_configuration().optionManagerAuditor)
            # commonUtils.waiting(1)
            # fee_AuditSql = 'select id from MERCHANT_FEE_REQUEST order by id desc'
            # merchantFeeRequestId = str(OracleQuery.sqlAll(fee_AuditSql)[0][0])
            # merchantFeeAuditAction_auditConfirm(merchantFeeRequestId, self.cookies[1])

            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['ID'],
                where_condition="merchant_code = '%s' and type = '12' and status = '0' and limit_Fund = '301'" %
                                self.inputParameter['merchantCode'])[0][0]
            auditstatus = merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.cookies[1])
            self.assertEqual(auditstatus[0][0], 1, msg='费率修改失败')

        updateinputParameter = {'transferType': '1', 'accountType': '1', 'unionBankNum': '105100005078',
                                'openBankName': '中国建设银行北京上地支行', 'openBankProvince': '北京市',
                                'openBankCity': '北京市', 'accountName': 'tester', 'bankCode': 'ccb',
                                'bankAccount': '6217000010031195525'
                                }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数
        # 发送请求
        self.globalRequestId = commonUtils.requestId()
        self.inputParameter['requestId'] = self.globalRequestId
        self.inputParameter['sum'] = '301.02'
        self.inputParameter['transferPayType'] = '0'
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        s = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
        self.outputParameter.update(s.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)
        '''代发请求'''

        # 响应签名断言
        self.assertEqual('200300277', self.outputParameter['result'], msg=self.IOParameter)

    @runningRecorder(desc='')
    def test_singleTransfer_107040101017(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101017
        用例名称：
        	普通付款至企业银行账户-金额大于单笔限额
        """
        merchant_fee_type6 = OracleQuery.select_table(
            'merchant_fee',
            list_view = [
                'LIMIT_FUND'
            ],
            where_condition = "merchant_code = '%s' and type = '6'" % self.inputParameter['merchantCode'])

        if str('{:g}'.format(merchant_fee_type6[0][0])) != '301':
            '''初始化商户配置'''
            self.cookies = login(const._global_configuration().optionManagerOperator)
            commonUtils.waiting(1)
            '''修改单笔限额'''
            inputFormParam = {
                'type': '6',
                'limitFund': '301'
            }
            mgmodifyDisburseFee(inputFormParam, self.cookies[1], self.inputParameter['merchantCode'])
            '''审核费率'''
            self.cookies = login(const._global_configuration().optionManagerAuditor)

            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['ID'],
                where_condition="merchant_code = '%s' and type = '6' and status = '0' and limit_Fund = '301'" %
                                self.inputParameter['merchantCode'])[0][0]
            auditstatus = merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.cookies[1])
            self.assertEqual(auditstatus[0][0], 1, msg='费率修改失败')

        updateinputParameter = {'transferType': '1', 'accountType': '0', 'unionBankNum': '105100005078',
                                'openBankName': '中国建设银行北京上地支行', 'openBankProvince': '北京市',
                                'openBankCity': '北京市', 'accountName': 'tester', 'bankCode': 'ccb',
                                'bankAccount': '6217000010031195525'
                                }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数
        # 发送请求
        self.globalRequestId = commonUtils.requestId()
        self.inputParameter['requestId'] = self.globalRequestId
        self.inputParameter['sum'] = '301.02'
        self.inputParameter['transferPayType'] = '0'
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        s = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
        self.outputParameter.update(s.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)
        '''代发请求'''

        # 响应签名断言
        self.assertEqual('200300277', self.outputParameter['result'], msg=self.IOParameter)

    @runningRecorder(desc='')
    def test_singleTransfer_107040101018(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101018
        用例名称：
        	快速付款至企业银行账户-金额大于单笔限额
        """
        merchant_fee_type13 = OracleQuery.select_table(
            'merchant_fee',
            list_view = [
                'LIMIT_FUND'
            ],
            where_condition = "merchant_code = '%s' and type = '13'" % self.inputParameter['merchantCode'])

        if str('{:g}'.format(merchant_fee_type13[0][0])) != '301':
            '''初始化商户配置'''
            self.cookies = login(const._global_configuration().optionManagerOperator)
            commonUtils.waiting(1)
            '''修改单笔限额'''
            inputFormParam = {
                'type': '13',
                'limitFund': '301'
            }
            mgmodifyDisburseFee(inputFormParam, self.cookies[1], self.inputParameter['merchantCode'])
            '''审核费率'''
            self.cookies = login(const._global_configuration().optionManagerAuditor)

            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['ID'],
                where_condition="merchant_code = '%s' and type = '13' and status = '0' and limit_Fund = '301'" %
                                self.inputParameter['merchantCode'])[0][0]
            auditstatus = merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.cookies[1])
            self.assertEqual(auditstatus[0][0], 1, msg='费率修改失败')

        updateinputParameter = {'transferType': '2', 'accountType': '1', 'unionBankNum': '105100005078',
                                'openBankName': '中国建设银行北京上地支行', 'openBankProvince': '北京市',
                                'openBankCity': '北京市', 'accountName': 'tester', 'bankCode': 'ccb',
                                'bankAccount': '6217000010031195525'
                                }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数
        # 发送请求
        self.globalRequestId = commonUtils.requestId()
        self.inputParameter['requestId'] = self.globalRequestId
        self.inputParameter['sum'] = '301.02'
        self.inputParameter['transferPayType'] = '0'
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        s = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
        self.outputParameter.update(s.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)
        '''代发请求'''

        # 响应签名断言
        self.assertEqual('200300277', self.outputParameter['result'], msg=self.IOParameter)

    @runningRecorder(desc='')
    def test_singleTransfer_107040101024(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101024
        用例名称：
            请求流水号重复
        用例描述：
            请求流水号重复

        """
        merchant = OracleQuery.select_table(
            'merchant',
            list_view = [
                'ID'
            ],
            where_condition = "merchant_code = '%s'" % self.inputParameter['merchantCode']
        )
        merchant_transfer_request = OracleQuery.select_table(
            'merchant_transfer_request',
            list_view = [
                'request_id'
            ],
            where_condition = "merchant_id='%s' and status='2' order by id desc"%str(merchant[0][0])
        )
        self.inputParameter['requestId'] = str(merchant_transfer_request[0][0])
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        s1 = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter),
                           verify=False)
        self.outputParameter.update(s1.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)
        '''代发请求'''

        # 响应签名断言
        self.assertEqual(respsonseSignatrue, self.outputParameter['signature'], msg='响应签名验签失败')
        self.assertEqual('200300301', self.outputParameter['result'], msg=self.IOParameter)

    @runningRecorder(desc='')
    def test_singleTransfer_107040101031(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101031
        用例名称：
        	付款至个人银行账户-普通-手续费收取方式为后付
        """
        self.globalRequestId = commonUtils.requestId(num = 24)
        self.inputParameter['requestId'] = self.globalRequestId
        '''根据用例前置条件初始化输入参数'''
        updateinputParameter = {'transferType': '1', 'accountType': '0', 'unionBankNum': '105100005078',
                                'openBankName': '中国建设银行北京上地支行', 'openBankProvince': '北京市',
                                'openBankCity': '北京市', 'accountName': 'tester', 'bankCode': 'ccb',
                                'bankAccount': '6217000010031195525'
                                }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数
        self.inputParameter['signature'] = commonUtils.md5Signature(
            self.inputParameter,
            self.key,
            self.requestSignatrueRule)
        respondsecookies = login(const._global_configuration().optionManagerOperator)
        """修改商户为实时付款商户"""
        merchantManage.merchant_info_mgmodify({'fld16': '1'}, respondsecookies[1], self.inputParameter['merchantCode'])
        # 修改手续费收取方式为预付
        merchant_fee_type5 = OracleQuery.select_table(
            'merchant_fee',
            list_view = [
                'CHARGE_TYPE',
                'METHOD',
                'FIX_FEE',
                'FEE_RATE',
                'LIMIT_FIX_RATE_FUND'
            ],
            where_condition = "merchant_code = '%s' and type = '5' order by limit_layer" % self.inputParameter['merchantCode'])

        if str(merchant_fee_type5[0][0]) != '3' \
                or str(merchant_fee_type5[0][1]) != '2' \
                or merchant_fee_type5[0][2] != 0.02 \
                or merchant_fee_type5[1][3] != 1 \
                or merchant_fee_type5[0][4] != 300:
            inputFormParam = {
                'type': '5',
                'chargeType': '3',
                'meth' : '2',
                'fixFee': '0.02',
                'feeRate': '1',
                'limitFixRateFund': '300',
            }
            mgmodifyDisburseFee(inputFormParam, respondsecookies[1], self.inputParameter['merchantCode'])
            self.cookies = login(const._global_configuration().optionManagerAuditor)
            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view = ['ID'],
                where_condition = "merchant_code = '%s' and type = '5' and status = '0' and charge_type = '3'" % self.inputParameter['merchantCode'])[0][0]
            auditstatus = merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.cookies[1])
            self.assertEqual(auditstatus[0][0], 1, msg='费率修改失败')

        '''发起单笔付款请求'''
        respondse = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter),
                                  verify=False)
        self.outputParameter.update(respondse.json())
        syncSignature = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)

        '''同步返回参数校验'''
        # 请求流水
        self.assertEqual(self.outputParameter['requestId'], self.inputParameter['requestId'].decode(), msg='请求流水不一致')
        # 判断请求结果
        self.assertEqual(self.outputParameter['result'], '00000', msg='请求不成功')
        # 判断同步响应签名
        self.assertEqual(syncSignature, self.outputParameter['signature'], msg='同步签名验证不通过')
        # 判断请求金额
        self.assertEqual(self.outputParameter['sum'], self.inputParameter['sum'].decode(), msg='请求金额不正确')

        '''等待调度复核'''
        commonUtils.waiting(20)
        # 判断数据库状态
        merchant_transfer_request = OracleQuery.select_table(
            'merchant_transfer_request',
            list_view=[
                'status',
                'request_type',
                'id'
            ],
            where_condition="request_id = '%s'" % self.inputParameter['requestId'].decode()
        )
        self.assertEqual(str(merchant_transfer_request[0][0]), '9', msg='请求状态正确')
        self.assertEqual(str(merchant_transfer_request[0][1]), '1', msg='请求类型正确')

        # account_bal_frz_record
        '''交易金额冻结'''
        MERCHANT = OracleQuery.select_table(
            'MERCHANT',
            list_view=[
                'ID'
            ],
            where_condition="merchant_code = '%s'" % self.inputParameter['merchantCode'].decode()
        )
        merchant_account_association = OracleQuery.select_table(
            'merchant_account_association',
            list_view=[
                'ACCOUNT_ID'
            ],
            where_condition="merchant_id = '%s'" % str(MERCHANT[0][0])
        )

        account_bal_frz_record = OracleQuery.select_table(
            'account_bal_frz_record',
            list_view=[
                'SUM'
            ],
            where_condition="account_id = '%s' and status = '0' and table_name = 'MERCHANT_TRANSFER_REQUEST' and table_key = '%s'"
                            % (str(merchant_account_association[0][0]), str(merchant_transfer_request[0][2]))
        )
        self.assertEqual('0.03', str(account_bal_frz_record[0][0]))
        frz_record_count = OracleQuery.select_table(
            'account_bal_frz_record',
            list_view=[
                'count(*)'
            ],
            where_condition="account_id = '%s' and status = '0' and table_key = '%s'"
                            % (str(merchant_account_association[0][0]), str(merchant_transfer_request[0][2]))
        )
        self.assertEqual('1', str(frz_record_count[0][0]))

    @runningRecorder(desc='')
    def test_singleTransfer_107040101032(self):
        """
            作者：刘佳琪
            需求版本号：SP_S_20170002（历史版本号:sp_20150011）
            用例编号：
                107040101032
            用例名称：
             付款至企业银行账户-普通-后付-固定值+费率
             签名规则：MD5
            用例描述：
            1、商户配置普通付款至企业银行账户手续费，手续费收取方式为后付-固定值+费率
            2、商户配置代发-对公银行渠道
        """

        self.globalRequestId = commonUtils.requestId(num=24)
        self.inputParameter['requestId'] = self.globalRequestId
        '''根据用例前置条件初始化输入参数'''
        updateinputParameter = {'transferType': '2', 'accountType': '0', 'unionBankNum': '105100005078',
                                'openBankName': '中国建设银行北京上地支行', 'openBankProvince': '北京市',
                                'openBankCity': '北京市', 'accountName': 'tester', 'bankCode': 'ccb',
                                'bankAccount': '6217000010031195525'
                                }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数
        self.inputParameter['signature'] = commonUtils.md5Signature(
            self.inputParameter,
            self.key,
            self.requestSignatrueRule)
        respondsecookies = login(const._global_configuration().optionManagerOperator)
        """修改商户为实时付款商户"""
        merchantManage.merchant_info_mgmodify({'fld16': '1'}, respondsecookies[1], self.inputParameter['merchantCode'])
        # 修改手续费收取方式为预付
        merchant_fee_type6 = OracleQuery.select_table(
            'merchant_fee',
            list_view=[
                'CHARGE_TYPE',
                'METHOD',
                'FIX_FEE',
                'FEE_RATE',
                'LIMIT_FIX_RATE_FUND'
            ],
            where_condition="merchant_code = '%s' and type = '6' order by limit_layer" % self.inputParameter['merchantCode'])

        if str(merchant_fee_type6[0][0]) != '3' \
                or str(merchant_fee_type6[0][1]) != '2' \
                or merchant_fee_type6[0][2] != 0.02 \
                or merchant_fee_type6[1][3] != 1 \
                or merchant_fee_type6[0][4] != 300:
            inputFormParam = {
                'type': '6',
                'chargeType': '3',
                'meth': '2',
                'fixFee': '0.02',
                'feeRate': '1',
                'limitFixRateFund': '300',
            }
            mgmodifyDisburseFee(inputFormParam, respondsecookies[1], self.inputParameter['merchantCode'])
            self.cookies = login(const._global_configuration().optionManagerAuditor)
            modify_disburse_fee_id = OracleQuery.select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['ID'],
                where_condition="merchant_code = '%s' and type = '6' and status = '0' and charge_type = '3'" %
                                self.inputParameter['merchantCode'])[0][0]
            auditstatus = merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.cookies[1])
            self.assertEqual(auditstatus[0][0], 1, msg='费率修改失败')

        '''发起单笔付款请求'''
        respondse = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter),
                                  verify=False)
        self.outputParameter.update(respondse.json())
        syncSignature = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)

        '''同步返回参数校验'''
        # 请求流水
        self.assertEqual(self.outputParameter['requestId'], self.inputParameter['requestId'].decode(), msg='请求流水不一致')
        # 判断请求结果
        self.assertEqual(self.outputParameter['result'], '00000', msg='请求不成功')
        # 判断同步响应签名
        self.assertEqual(syncSignature, self.outputParameter['signature'], msg='同步签名验证不通过')
        # 判断请求金额
        self.assertEqual(self.outputParameter['sum'], self.inputParameter['sum'].decode(), msg='请求金额不正确')

        '''等待调度复核'''
        commonUtils.waiting(20)
        # 判断数据库状态
        merchant_transfer_request = OracleQuery.select_table(
            'merchant_transfer_request',
            list_view=[
                'status',
                'request_type',
                'id'
            ],
            where_condition="request_id = '%s'" % self.inputParameter['requestId'].decode()
        )
        self.assertEqual(str(merchant_transfer_request[0][0]), '9', msg='请求状态正确')
        self.assertEqual(str(merchant_transfer_request[0][1]), '2', msg='请求类型正确')

        # account_bal_frz_record
        '''交易金额冻结'''
        MERCHANT = OracleQuery.select_table(
            'MERCHANT',
            list_view=[
                'ID'
            ],
            where_condition="merchant_code = '%s'" % self.inputParameter['merchantCode'].decode()
        )
        merchant_account_association = OracleQuery.select_table(
            'merchant_account_association',
            list_view=[
                'ACCOUNT_ID'
            ],
            where_condition="merchant_id = '%s'" % str(MERCHANT[0][0])
        )

        account_bal_frz_record = OracleQuery.select_table(
            'account_bal_frz_record',
            list_view=[
                'SUM'
            ],
            where_condition="account_id = '%s' and status = '0' and table_name = 'MERCHANT_TRANSFER_REQUEST' and table_key = '%s'"
                            % (str(merchant_account_association[0][0]), str(merchant_transfer_request[0][2]))
        )
        self.assertEqual('0.03', str(account_bal_frz_record[0][0]))
        frz_record_count = OracleQuery.select_table(
            'account_bal_frz_record',
            list_view=[
                'count(*)'
            ],
            where_condition="account_id = '%s' and status = '0' and table_key = '%s'"
                            % (str(merchant_account_association[0][0]), str(merchant_transfer_request[0][2]))
        )
        self.assertEqual('1', str(frz_record_count[0][0]))

    @unittest.skip('暂未开发此接口，用例遗留')
    def test_singleTransfer_107040101038(self):
        """
            作者：刘佳琪
            需求版本号：SP_S_20170002（历史版本号:SP_S_20160021）
            用例编号：
                107040101038
            用例名称：
             商户冻结-商户单笔付款请求
             签名规则：MD5
            用例描述：

        """

    @runningRecorder(desc='')
    def test_singleTransfer_107040101039(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101039
        用例名称：
            单笔付款至银行账户超过日累计笔数8笔
        用例描述：
     1、配置的商户配置中已添加单日累计必输和单日累计金额
     2、merchant_transfer_request表中存在存在0待复核、1已接收、6待确认、8处理中、9已请求、11待父商户复核 成功和退票 交易 共8笔数据
    数据要求普通付款至企业银行 同行
    快速付款至企业银行 跨行
    普通付款至个人银行 同行
    快速付款至个人银行 跨行
    包括线上和线下渠道
        """
        self.cookies = login(const._global_configuration().optionManagerOperator)
        commonUtils.waiting(1)
        merchant = OracleQuery.select_table(
            'merchant',
            list_view = [
                'id'
            ],
            where_condition = "merchant_code = '%s'" % self.inputParameter['merchantCode']
        )
        # 查询merchant_transfer_request表中存在交易的笔数
        merchant_transfer_request_count = OracleQuery.select_table(
            'merchant_transfer_request',
            list_view = [
                'count(*)'
            ],
            where_condition = "merchant_id = '%s' and to_char(row_create_time, 'yyyymmdd') =(select  TO_CHAR(SYSDATE, 'yyyymmdd') FROM DUAL) and status in (0,1,6,8,9,11,2,10)"
                              % str(merchant[0][0])
        )
        # countsql = (
        #     "select count (*) from merchant_transfer_request where merchant_id=104 and to_char(row_create_time, 'yyyymmdd') =(select  TO_CHAR(SYSDATE, 'yyyymmdd') FROM DUAL) and status in (0,1,6,8,9,11,2,10)")
        # a = str(OracleQuery.sqlAll(countsql)[0][0])
        # 修改手续费商品单日累计笔数
        respondsecookies = login(const._global_configuration().optionManagerOperator)
        moddata = {
                'type' : '5',
                'merSingleDayCountLimit': merchant_transfer_request_count[0][0]
        }
        mgmodifyDisburseFee(moddata, respondsecookies[1], self.inputParameter['merchantCode'])

        '''审核费率'''
        self.cookies = login(const._global_configuration().optionManagerAuditor)
        commonUtils.waiting(1)
        fee_AuditSql = 'select id from MERCHANT_FEE_REQUEST order by id desc'
        merchantFeeRequestId = str(OracleQuery.sqlAll(fee_AuditSql)[0][0])
        merchantFeeAuditAction_auditConfirm(merchantFeeRequestId, self.cookies[1])
        commonUtils.waiting(1)
        # 发送请求
        self.globalRequestId = commonUtils.requestId(num=24)
        self.inputParameter['requestId'] = self.globalRequestId
        self.inputParameter['transferType'] = '1'  # 付款至个人银行
        self.inputParameter['accountType'] = '1'  # 到账模式为快速
        self.inputParameter['transferPayType'] = '0'  # 审核方式为手工审核
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        s = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
        self.outputParameter.update(s.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)

        # 响应签名断言
        self.assertEqual('200300358', self.outputParameter['result'], msg=self.IOParameter)

    @unittest.skip('批量用例实现后再实现本用例')
    @runningRecorder(desc='')
    def test_singleTransfer001_107040101040(self):
        """
            作者：刘佳琪
            需求版本号：SP_S_20170002（历史版本号:SP_S_20160021）
            用例编号：
                107040101040
            用例名称：
             单笔和批量明细付款至银行账户超过日累计笔数13笔
             签名规则：MD5
            用例描述：
            1、配置的商户配置中已添加单日累计必输和单日累计金额
            2、merchant_transfer_request表中存在存在0待复核、1已接收、6待确认、8处理中、9已请求、
            11待父商户复核 成功和退票 交易 共8笔数据
            batchpay_detail表中存在3初始、6已请求、中间状态7 成功和退票 5种状态
            数据要求普通付款至企业银行 同行
            快速付款至企业银行 跨行
            普通付款至个人银行 同行
            快速付款至个人银行 跨行
            包括线上渠道和线下渠道
        """
        singledaycount = "select  count(*) from merchant_transfer_request where merchant_id = 104 and to_char(row_create_time, 'yyyymmdd') =  (select  TO_CHAR(SYSDATE, 'yyyymmdd') from DUAL) and status in (0, 1, 6, 8, 9, 11, 2, 10)"
        batchdaycount = "select count(*) from batchpay_detail where (batchpay_no in (select batchpay_no from batchpay_record t where merchant_id='104')) and status in (3, 6, 7, 2, 0) and to_char(row_create_time, 'yyyymmdd') = (select  TO_CHAR(SYSDATE, 'yyyymmdd') FROM DUAL)"
        singledaycount = OracleQuery.sqlAll(singledaycount)[0][0]
        batchdaycount = OracleQuery.sqlAll(batchdaycount)[0][0]
        totaltransferamount = str(singledaycount + batchdaycount)

        '''修改单日付款次数'''
        respondsecookies = login(const._global_configuration().optionManagerOperator)
        moddata = {'step': '1', 'oldMethod': '1', 'merchantId': '104', 'type': '12', 'chargeType': '0', 'meth': '1',
                   'feeRate': '100', 'minFee': '0.01', 'maxFee': '0.1',
                   'fixFee1': '', 'limit1': '', 'fixFee2': '', 'limit2': '', 'fixFee3': '', 'limit3': '', 'fixFee4': '',
                   'limit4': '', 'fixFee5': '', 'limit5': '',
                   'limitFund': '100100', 'fld12': '0', 'isNeedChildReview': '0', 'merSingleDayLimit': '',
                   'merSingleDayCountLimit': totaltransferamount,
                   'merSingleMonthLimit': '', 'merSingleYearLimit': ''}
        mgmodifyDisburseFee(moddata, respondsecookies[1])

        '''审核费率'''
        self.cookies = login(const._global_configuration().optionManagerAuditor)
        fee_AuditSql = 'select id from MERCHANT_FEE_REQUEST order by id desc'
        merchantFeeRequestId = str(OracleQuery.sqlAll(fee_AuditSql)[0][0])
        auditstatus = merchantFeeAuditAction_auditConfirm(merchantFeeRequestId, self.cookies[1])
        self.assertEqual(auditstatus[0][0], 1, msg='费率修改成功')

        '''
                根据用例前置条件初始化输入参数
                '''
        updateinputParameter = {'transferType': '1', 'accountType': '1', 'unionBankNum': '105100005078',
                                'openBankName': '中国建设银行北京上地支行', 'openBankProvince': '北京市',
                                'openBankCity': '北京市', 'accountName': 'tester', 'bankCode': 'ccb',
                                'bankAccount': '6217000010031195525', 'transferPayType': '0'
                                }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数

        '''发起付款请求'''
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        respondse = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter),
                                  verify=False)
        self.outputParameter.update(respondse.json())
        syncSignature = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)

        '''同步返回参数校验'''
        # 请求流水
        self.assertEqual(self.outputParameter['requestId'], self.inputParameter['requestId'].decode(), msg='请求流水一致')
        # 判断请求结果
        self.assertEqual(self.outputParameter['result'], '200300358', msg='付款笔数超过限制笔数')
        # 判断同步响应签名
        self.assertEqual(syncSignature, self.outputParameter['signature'], msg='同步签名验证通过')
        # 判断请求金额
        self.assertEqual(self.outputParameter['sum'], self.inputParameter['sum'].decode(), msg='请求金额正确')

    @runningRecorder(desc='')
    def test_singleTransfer_107040101041(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101041
        用例名称：
        	单笔付款至银行账户超过日累计金额
        """
        self.cookies = login(const._global_configuration().optionManagerOperator)
        commonUtils.waiting(1)
        merchant = OracleQuery.select_table(
            'merchant',
            list_view = [
                'id'
            ],
            where_condition = "merchant_code = '%s'" % self.inputParameter['merchantCode']
        )
        # 查询merchant_transfer_request表中存在交易的笔数
        merchant_transfer_request_sum = OracleQuery.select_table(
            'merchant_transfer_request',
            list_view = [
                'sum(FUND)'
            ],
            where_condition = "merchant_id = '%s' and to_char(row_create_time, 'yyyymmdd') =(select  TO_CHAR(SYSDATE, 'yyyymmdd') FROM DUAL) and status in (0,1,6,8,9,11,2,10)"
                              % str(merchant[0][0])
        )
        # 修改手续费商品单日累计金额
        respondsecookies = login(const._global_configuration().optionManagerOperator)
        moddata = {
                'type' : '5',
                'merSingleDayLimit': merchant_transfer_request_sum[0][0],
                'merSingleDayCountLimit' : ''
        }
        mgmodifyDisburseFee(moddata, respondsecookies[1], self.inputParameter['merchantCode'])

        '''审核费率'''
        self.cookies = login(const._global_configuration().optionManagerAuditor)
        commonUtils.waiting(1)
        fee_AuditSql = 'select id from MERCHANT_FEE_REQUEST order by id desc'
        merchantFeeRequestId = str(OracleQuery.sqlAll(fee_AuditSql)[0][0])
        merchantFeeAuditAction_auditConfirm(merchantFeeRequestId, self.cookies[1])
        commonUtils.waiting(1)
        # 发送请求
        self.globalRequestId = commonUtils.requestId(num=24)
        self.inputParameter['requestId'] = self.globalRequestId
        self.inputParameter['transferType'] = '1'  # 付款至个人银行
        self.inputParameter['accountType'] = '1'  # 到账模式为快速
        self.inputParameter['transferPayType'] = '0'  # 审核方式为手工审核
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        s = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
        self.outputParameter.update(s.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)

        # 响应签名断言
        self.assertEqual('200300357', self.outputParameter['result'], msg=self.IOParameter)

    @unittest.skip('未执行')
    @runningRecorder(desc='')
    def test_singleTransfer_107040101042(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101042
        用例名称：
        	单笔和批量明细付款至银行账户超过日累计金额
        """
        pass

    @runningRecorder(desc='')
    def test_singleTransfer_107040101045(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            107040101045
        用例名称：
            商户配置实时付款单笔限额，发起自动实时付款至个人银行账户，付款金额大于单笔限额
        用例描述：
            商户配置实时付款单笔限额

        """
        # 修改实时付款单笔限额
        self.login_cookies = login(const._global_configuration().optionManagerOperator)[1]
        commonUtils.waiting(1)
        merchant_info_modify = {'fld16': '1'}
        smerchant_realtime_config_modify = {
            'merSingleLimit': '10',
            'merSingleDayLimit': '5000',
        }
        merchantManage.merchant_info_mgmodify(merchant_info_modify, self.login_cookies, "CSSH")
        merchantManage.merchant_realtime_transfer_info_mgmodify(smerchant_realtime_config_modify, self.login_cookies,
                                                                "CSSH")

        commonUtils.waiting(1)
        # 发送请求
        self.globalRequestId = commonUtils.requestId(num = 24)
        self.inputParameter['requestId'] = self.globalRequestId
        self.inputParameter['sum'] = '11'
        self.inputParameter['transferType'] = '1'
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        s = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
        self.outputParameter.update(s.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)
        '''代发请求'''

        # 响应签名断言
        self.assertEqual(respsonseSignatrue, self.outputParameter['signature'], msg='响应签名验签失败')
        self.assertEqual('200300277', self.outputParameter['result'], msg=self.IOParameter)

    @runningRecorder(desc='')
    def test_singleTransfer001_107040101046(self):
        """
            作者：刘佳琪
            需求版本号：SP_S_20170002（历史版本号:SP_S_20160021）
            用例编号：
                107040101046
            用例名称：
             商户配置实时付款单笔限额，发起自动实时付款至企业银行账户，付款金额大于单笔限额
             签名规则：MD5
            用例描述：
            商户配置实时付款单笔限额
        """
        '''self.globalRequestId = self.inputParameter['requestId']
        self.inputParameter['requestId'] = self.globalRequestId'''
        '''
        根据用例前置条件初始化输入参数
        '''
        updateinputParameter = {'transferType': '2', 'accountType': '1', 'sum': '11', 'accountName': 'tester',
                                'bankCode': 'ccb',
                                'bankAccount': '6217000010031195525', 'transferPayType': '1'
                                }
        self.inputParameter.update(updateinputParameter)  # 更新请求参数

        self.login_cookies = login(const._global_configuration().optionManagerOperator)[1]
        # 设置实时付款单笔限额
        merchant_info_modify = {'fld16': '1'}
        smerchant_realtime_config_modify = {
            'merSingleLimit': '10',
            'merSingleDayLimit': '258',
        }
        merchantManage.merchant_info_mgmodify(merchant_info_modify, self.login_cookies, "CSSH")
        merchantManage.merchant_realtime_transfer_info_mgmodify(smerchant_realtime_config_modify, self.login_cookies,
                                                                "CSSH")

        '''发起单笔付款请求'''
        self.inputParameter['requestId'] = commonUtils.requestId(num = 24)
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key,
                                                                    self.requestSignatrueRule)
        respondse = requests.post(url=self.actionUrl, data=commonUtils.encodeDictionaryToGBK(self.inputParameter),
                                  verify=False)
        self.outputParameter.update(respondse.json())
        syncSignature = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)

        '''同步返回参数校验'''
        # 请求流水
        self.assertEqual(self.outputParameter['requestId'], self.inputParameter['requestId'].decode(), msg='请求流水一致')
        # 判断请求结果
        self.assertEqual(self.outputParameter['result'], '200300277', msg='请求金额大于单笔限额')
        # 判断同步响应签名
        self.assertEqual(syncSignature, self.outputParameter['signature'], msg='同步签名验证通过')
        # 判断请求金额
        self.assertEqual(self.outputParameter['sum'], self.inputParameter['sum'].decode(), msg='请求金额正确')

    @unittest.skip('未执行')
    @runningRecorder(desc='')
    def test_singleTransfer_406010101004(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号）
        用例编号：
            406010101004
        用例名称：
        	普通付款至个人银行账户-风控审核通过（实时）
        """
        '''发起付款请求'''
        self.subTest(self.test_singleTransfer_107040101031())

        '''风控通过'''
        transferRiskAudit(self.globalRequestId,self.cookies[1])
        # 请求表merchant_transfer_request
        requestStatus = str(OracleQuery.sqlAll(SqlStatement.transfer_requestSql(self.globalRequestId))[0][0])
        self.assertEqual('6', requestStatus)




# if __name__ == '__main__':
#     unittest.main()
