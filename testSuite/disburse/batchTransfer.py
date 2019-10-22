#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/9 0009 下午 3:12
# @Author  : Administrator
# @Site    :
# @File    : batchPay.py
# @Software: PyCharm
import requests
from baseLib.commonAPI import commonUtils
from baseLib.commonAPI.OracleQuery import select_table
from baseLib.baseUtils.recorder import runningRecorder
from baseLib.operationManagerAPI import authentication, merchantManage
from baseLib.operationManagerAPI.DisburseManager import mgmodifyDisburseFee,transferRiskAudit,transferConfirm
from baseLib.operationManagerAPI.feeAudit import merchantFeeAuditAction_auditConfirm
import unittest
from configuration import const
import datetime
from testSuite.disburse import *
from testSuite import *

class BatchTransfer_notifyCheck(unittest.TestCase):
    """
    测试功能描述：
    	... ...
    """

    # 类运行时只调用一次，方法内参数可作为class内的全局变量使用
    @classmethod
    def setUpClass(cls):
        cls.global_requestId = None
        cls.global_batchTransferNo = None
        cls.cookies_operator = None
        cls.cookies_auditor = None

    # 每个testcase运行前执行，可作为测试用例初始化数据使用
    def setUp(self):
        self.BatchTransfer_notifyCheck_sample = BatchTransfer_notifyCheck_default(
            http_ip = '172.16.3.9:8080',
            merchant_code = 'CSSH',
            merchant_key = 'CSSH_KEY'
        )
        self.BatchTransfer_notifyTransfer_sample = BatchTransfer_notifyTransfer_default(
            http_ip='172.16.3.9:8080',
            merchant_code='CSSH',
            merchant_key='CSSH_KEY'
        )
        self.BatchTransfer_queryBatchTransferState_sample = BatchTransfer_queryBatchTransferState_default(
            http_ip='172.16.3.9:8080',
            merchant_code='CSSH',
            merchant_key='CSSH_KEY'
        )
        self.ftp_client = ftp_connect(
            '192.161.14.157',
            self.BatchTransfer_notifyCheck_sample.ftp_remote_path,
            'batchtransfer',
            '58858547',
        )
        self.global_requestId = self.BatchTransfer_notifyCheck_sample.input_parameter['requestId']
        self.global_batchTransferNo = self.BatchTransfer_notifyCheck_sample.input_parameter['batchTransferNo']

    @unittest.skip('未实现自动化')
    @runningRecorder(desc='付款至丰付企业账户（csv）-实时')
    def test_BatchTransfer_notifyCheck_107010101001(self):
        """
        作者：刘佳琪
        需求版本号：不详（历史版本号：无）
        用例编号：
            107010101001
        用例名称：
        	付款至丰付企业账户（csv）-实时
        用例描述：
            无
        """
        commonUtils.encryptDesFromStrTofile(
            self.BatchTransfer_notifyCheck_sample.batchfile_des_key,
            self.BatchTransfer_notifyCheck_sample.batchfile_context,
            self.BatchTransfer_notifyCheck_sample.batchfile_name)
        with open(self.BatchTransfer_notifyCheck_sample.batchfile_name, 'rb') as fp:
            self.ftp_client.storbinary('STOR ' + self.BatchTransfer_notifyCheck_sample.batchfile_name, fp)

        self.BatchTransfer_notifyCheck_sample.input_parameter['signature'] = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.input_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.request_signatrue_rule)
        respsonse_jsonstr = requests.post(
            url = self.BatchTransfer_notifyCheck_sample.action_url,
            data = commonUtils.encodeDictionaryToGBK(self.BatchTransfer_notifyCheck_sample.input_parameter),
            verify = False)
        self.BatchTransfer_notifyCheck_sample.output_parameter.update(respsonse_jsonstr.json())
        respsonseSignatrue = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.output_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.sync_signatrue_rule)

        #响应签名断言
        self.assertEqual(respsonseSignatrue, self.BatchTransfer_notifyCheck_sample.output_parameter['signature'], msg = '响应签名验签失败')
        self.assertEqual('00000', self.BatchTransfer_notifyCheck_sample.output_parameter['result'], msg = self.BatchTransfer_notifyCheck_sample.io_parameter)

    @unittest.skip('未实现自动化')
    @runningRecorder(desc='付款至丰付企业账户（csv）-实时')
    def test_BatchTransfer_notifyCheck_107010101002(self):
        """
        作者：刘佳琪
        需求版本号：SP_S_20170008（历史版本号：无）
        用例编号：
            107010101002
        用例名称：
        	付款至丰付企业账户(csv)-预付
        用例描述：
            无
        """
        pass

    @runningRecorder(desc='付款至银行账户csv（普通）-实时')
    def test_BatchTransfer_notifyCheck_107010101003(self):
        """
        作者：刘佳琪
        需求版本号：不详（历史版本号：无）
        用例编号：
            107010101003
        用例名称：
        	付款至银行账户csv（普通）-实时
        用例描述：
            无
        """
        """前提条件：设置普通付款费率为实时"""
        merchant_id = select_table(
            'merchant',
            list_view = ['ID'],
            where_condition = "merchant_code = '%s'"
                              % self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'])[0][0]
        charge_type = select_table(
            'merchant_fee',
            list_view = ['CHARGE_TYPE'],
            where_condition = "merchant_id = '%s' and type = '5'" % str(merchant_id))[0][0]
        if str(charge_type) != '0':
            """操作员登录"""
            self.cookies_operator = authentication.login(const._global_configuration().optionManagerOperator)[1]
            set_disburse_fee = {
                'step': '1',
                'oldMethod': '3',
                'merchantId': str(merchant_id),
                'type': '5',#4付款至企业账户、5普通付款至个人银行、6普通付款至企业银行、12快速付款至个人银行、13快速付款至企业银行
                'chargeType': '0',#丰付手续费收取类型，0为实时，1为预付，2为垫付，3为后付
                'meth': '3',
                'fixFee': '0',
                'feeRate': '',
                'minFee': '',
                'maxFee': '',
                'limitFixRateFund': '',
                'fixFee1': '0',
                'limit1': '',
                'fixFee2': '',
                'limit2': '',
                'fixFee3': '',
                'limit3': '',
                'fixFee4': '',
                'limit4': '',
                'fixFee5': '',
                'limit5': '',
                'limitFund': '3000000',
                'fld12': '0',
                'isNeedChildReview': '0',
                'merSingleDayLimit': '40',
                'merSingleDayCountLimit': '',
                'merSingleMonthLimit': '',
                'merSingleYearLimit': '',
            }
            """修改费率"""
            mgmodifyDisburseFee(set_disburse_fee, self.cookies_operator)
            modify_disburse_fee_count = select_table(
                'MERCHANT_FEE_REQUEST',
                list_view = ['count(*)'],
                where_condition = "merchant_id = '%s' and type = '5' and status = '0' and charge_type = '0'"%merchant_id
            )[0][0]
            if str(modify_disburse_fee_count) != '1':
                raise RuntimeError('付款待审核记录数不为1')
            self.cookies_auditor = authentication.login(const._global_configuration.optionManagerAuditor)[1]
            modify_disburse_fee_id = select_table(
                'MERCHANT_FEE_REQUEST',
                list_view = ['ID'],
                where_condition = "merchant_id = '%s' and type = '5' and status = '0' and charge_type = '0'"%merchant_id
            )[0][0]
            merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.cookies_auditor)
            charge_type = select_table(
                'merchant_fee',
                list_view=['CHARGE_TYPE'],
                where_condition="merchant_id = '%s' and type = '5'" % str(merchant_id))[0][0]
            if str(charge_type) != '0':
                raise RuntimeError('修改费率为实时类型失败')

        """步骤一：设置入参：普通-实时付款到银行账户"""
        self.BatchTransfer_notifyCheck_sample.input_parameter['payType'] = '2'
        self.BatchTransfer_notifyCheck_sample.input_parameter['inAccountType'] = '0'
        self.BatchTransfer_notifyCheck_sample.input_parameter['transferPayType'] = '1'
        self.BatchTransfer_notifyCheck_sample.input_parameter['signature'] = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.input_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.request_signatrue_rule)
        """步骤二：生成加密批量文件"""
        print(self.BatchTransfer_notifyCheck_sample.batchfile_context)
        commonUtils.encryptDesFromStrTofile(
            self.BatchTransfer_notifyCheck_sample.batchfile_des_key,
            self.BatchTransfer_notifyCheck_sample.batchfile_context,
            self.BatchTransfer_notifyCheck_sample.batchfile_name)
        """步骤三：上传加密批量文件到ftp"""
        with open(self.BatchTransfer_notifyCheck_sample.batchfile_name, 'rb') as fp:
            self.ftp_client.storbinary('STOR ' + self.BatchTransfer_notifyCheck_sample.batchfile_name, fp)
        """步骤四：批量付款请求"""
        respsonse_jsonstr = requests.post(
            url = self.BatchTransfer_notifyCheck_sample.action_url,
            data = commonUtils.encodeDictionaryToGBK(self.BatchTransfer_notifyCheck_sample.input_parameter),
            verify = False
        )
        self.BatchTransfer_notifyCheck_sample.output_parameter.update(respsonse_jsonstr.json())
        """生成响应签名数据"""
        respsonseSignatrue = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.output_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.sync_signatrue_rule)
        """断言1：同步响应断言"""
        self.assertEqual(
            respsonseSignatrue,
            self.BatchTransfer_notifyCheck_sample.output_parameter['signature'],
            msg='响应签名验签失败'
        )
        self.assertEqual(
            '110180000',
            self.BatchTransfer_notifyCheck_sample.output_parameter['result'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'].decode(),
            self.BatchTransfer_notifyCheck_sample.output_parameter['merchantCode'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            self.BatchTransfer_notifyCheck_sample.input_parameter['batchTransferNo'].decode(),
            self.BatchTransfer_notifyCheck_sample.output_parameter['batchTransferNo'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        """断言2：数据库断言"""
        """查询数据库batchpay_record表数据"""
        batchpay_record_list = select_table(
            'batchpay_record',
            list_view = [
                'STATUS',#0初始、1待复核、2待付款、3已接收、4审核拒绝、5付款失败、 6待财务确认、7财务拒绝、8付款处理中、9处理完成、10、11事务分离中间态、12待父商户复核、13父商户复核拒绝
                'TOTAL_COUNT',#付款明细总笔数
                'TOTAL_SUM',#总金额（不含手续费）
                'VALID_COUNT',#有效付款明细笔数
                'VALID_SUM',#有效付款总额（不含手续费）
                'VALID_FEE',#有效手续费
                'SECCEED_COUNT',#付款成功的交易笔数
                'SECCEED_SUM',#付款成功金额（不含手续费）
                'SECCEED_FEE',#付款成功手续费
                'FLD1',#结算周期
                'FLD3',#快捷同卡批次标识，0为非快捷同卡，1为快捷同卡
                'ACCOUNTING_TYPE',#到账类型0普通1快速
                'TRANSFER_TYPE',#付款类型0混合付款，1付款至丰付账户，2付款至银行账户
                'OPERATOR_AUDITING_SIGN',#运营审核标识（0手工审核，1自动实时）
            ],
            where_condition = "batchpay_no = '%s'" % self.BatchTransfer_notifyCheck_sample.input_parameter['batchTransferNo'].decode()
        )
        self.assertEqual(
            '0',
            str(batchpay_record_list[0][0]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '2',
            str(batchpay_record_list[0][1]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '.09',
            str(batchpay_record_list[0][2]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '2',
            str(batchpay_record_list[0][3]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0.09',
            str(batchpay_record_list[0][4]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0',
            str(batchpay_record_list[0][5]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0',
            str(batchpay_record_list[0][6]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0.0',
            str(batchpay_record_list[0][7]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0.0',
            str(batchpay_record_list[0][8]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0.0',
            str(batchpay_record_list[0][8]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0',
            str(batchpay_record_list[0][9]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0',
            str(batchpay_record_list[0][10]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0',
            str(batchpay_record_list[0][11]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '2',
            str(batchpay_record_list[0][12]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '1',
            str(batchpay_record_list[0][13]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        """查询数据库batchpay_record表数据"""
        batchpay_detail_list = select_table(
            'batchpay_detail',
            list_view = [
                'FUND',#金额
                'ACCOUNT_TYPE',#账户类型(2对公银行账户，1对私银行账户，0对公丰付账户)
                'BANK_CODE',#银行代码
                'BANK_NAME',#收款方开户银行
                'BANK_ACCOUNT',  # 银行账号
                'BANK_ACCOUNT_NAME',#开户姓名
                'STATUS',#-1校验失败、0退票、1失败、2成功、3初始、4审核拒绝、5财务拒绝、6已请求、7事务分离中间态
                'ACCOUNTING_TYPE',#到账类型，0为普通，1为快速
                'PAY_FUND',#已付金额，供校验用
            ],
            where_condition = "batchpay_no = '%s' and detail_no = '1'" % self.BatchTransfer_notifyCheck_sample.input_parameter['batchTransferNo'].decode()
        )
        self.assertEqual(
            '0.04',
            str(batchpay_detail_list[0][0]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '1',
            str(batchpay_detail_list[0][1]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            'ccb',
            str(batchpay_detail_list[0][2]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '中国建设银行',
            str(batchpay_detail_list[0][3].strip()),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '6217000010031195525',
            commonUtils.decryptDes(batchpay_detail_list[0][4].strip()),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            'tester01',
            commonUtils.decryptDes(batchpay_detail_list[0][5].strip()),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '3',
            str(batchpay_detail_list[0][6]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0',
            str(batchpay_detail_list[0][7]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0.04',
            str(batchpay_detail_list[0][8]).strip(),
            msg = self.BatchTransfer_notifyCheck_sample.io_parameter
        )

    @runningRecorder(desc='付款至银行账户csv（快速）-预付')
    def test_BatchTransfer_notifyCheck_107010101004(self):
        """
        作者：刘佳琪
        需求版本号：不详（历史版本号：无）
        用例编号：
            107010101003
        用例名称：
        	付款至银行账户csv（快速）-预付
        用例描述：
            无
        """
        """前提条件：设置快速付款费率为预付"""
        merchant_id = select_table(
            'merchant',
            list_view=['ID'],
            where_condition="merchant_code = '%s'"
                            % self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'])[0][0]
        merchant_fee = select_table(
            'merchant_fee',
            list_view=[
                'FEE_RATE',
                'MIN_FEE',
                'CHARGE_TYPE'
            ],
            where_condition="merchant_id = '%s' and type = '12'" % str(merchant_id))
        if str(merchant_fee[0][0]) != '1' or str(merchant_fee[0][1]) != '0.01' or str(merchant_fee[0][2]) != '1':
            """操作员登录"""
            self.cookies_operator = authentication.login(const._global_configuration().optionManagerOperator)[1]
            set_disburse_fee = {
                'type': '12',  # 4付款至企业账户、5普通付款至个人银行、6普通付款至企业银行、12快速付款至个人银行、13快速付款至企业银行
                'chargeType': '1',  # 丰付手续费收取类型，0为实时，1为预付，2为垫付，3为后付
                'feeRate': '1',
                'minFee': '0.01',
            }
            """修改费率"""
            mgmodifyDisburseFee(
                set_disburse_fee,
                self.cookies_operator,
                self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode']
            )
            modify_disburse_fee_count = select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['count(*)'],
                where_condition="merchant_id = '%s' and type = '12' and status = '0' and charge_type = '1'"%str(merchant_id)
            )[0][0]
            if str(modify_disburse_fee_count) != '1':
                raise RuntimeError('付款待审核记录数不为1')
            self.cookies_auditor = authentication.login(const._global_configuration().optionManagerAuditor)[1]
            modify_disburse_fee_id = select_table(
                'MERCHANT_FEE_REQUEST',
                list_view=['ID'],
                where_condition="merchant_id = '%s' and type = '12' and status = '0' and charge_type = '1'"%str(merchant_id)
            )[0][0]
            merchantFeeAuditAction_auditConfirm(str(modify_disburse_fee_id), self.cookies_auditor)
            charge_type = select_table(
                'merchant_fee',
                list_view=['CHARGE_TYPE'],
                where_condition="merchant_id = '%s' and type = '12'" % str(merchant_id))[0][0]
            if str(charge_type) != '1':
                raise RuntimeError('修改费率为实时类型失败')

        """步骤一：设置入参,快速-预付手续费付款到银行账户"""
        self.BatchTransfer_notifyCheck_sample.input_parameter['payType'] = '2'
        self.BatchTransfer_notifyCheck_sample.input_parameter['inAccountType'] = '1'
        self.BatchTransfer_notifyCheck_sample.input_parameter['transferPayType'] = '1'
        self.BatchTransfer_notifyCheck_sample.input_parameter['signature'] = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.input_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.request_signatrue_rule)
        """步骤二：生成加密批量文件"""
        commonUtils.encryptDesFromStrTofile(
            self.BatchTransfer_notifyCheck_sample.batchfile_des_key,
            self.BatchTransfer_notifyCheck_sample.batchfile_context,
            self.BatchTransfer_notifyCheck_sample.batchfile_name)
        """步骤三：上传加密批量文件到ftp"""
        with open(self.BatchTransfer_notifyCheck_sample.batchfile_name, 'rb') as fp:
            self.ftp_client.storbinary('STOR ' + self.BatchTransfer_notifyCheck_sample.batchfile_name, fp)
        """步骤四：批量付款请求"""
        respsonse_jsonstr = requests.post(
            url=self.BatchTransfer_notifyCheck_sample.action_url,
            data=commonUtils.encodeDictionaryToGBK(self.BatchTransfer_notifyCheck_sample.input_parameter),
            verify=False
        )
        self.BatchTransfer_notifyCheck_sample.output_parameter.update(respsonse_jsonstr.json())
        """生成响应签名数据"""
        respsonseSignatrue = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.output_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.sync_signatrue_rule)
        """断言1：同步响应断言"""
        self.assertEqual(
            respsonseSignatrue,
            self.BatchTransfer_notifyCheck_sample.output_parameter['signature'],
            msg='响应签名验签失败'
        )
        self.assertEqual(
            '110180000',
            self.BatchTransfer_notifyCheck_sample.output_parameter['result'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'].decode(),
            self.BatchTransfer_notifyCheck_sample.output_parameter['merchantCode'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            self.BatchTransfer_notifyCheck_sample.input_parameter['batchTransferNo'].decode(),
            self.BatchTransfer_notifyCheck_sample.output_parameter['batchTransferNo'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        """断言2：数据库断言"""
        """查询数据库batchpay_record表数据"""
        batchpay_record_list = select_table(
            'batchpay_record',
            list_view=[
                'STATUS',  # 0初始、1待复核、2待付款、3已接收、4审核拒绝、5付款失败、 6待财务确认、7财务拒绝、8付款处理中、9处理完成、10、11事务分离中间态、12待父商户复核、13父商户复核拒绝
                'TOTAL_COUNT',  # 付款明细总笔数
                'TOTAL_SUM',  # 总金额（不含手续费）
                'VALID_COUNT',  # 有效付款明细笔数
                'VALID_SUM',  # 有效付款总额（不含手续费）
                'VALID_FEE',  # 有效手续费
                'SECCEED_COUNT',  # 付款成功的交易笔数
                'SECCEED_SUM',  # 付款成功金额（不含手续费）
                'SECCEED_FEE',  # 付款成功手续费
                'FLD1',  # 结算周期
                'FLD3',  # 快捷同卡批次标识，0为非快捷同卡，1为快捷同卡
                'ACCOUNTING_TYPE',  # 到账类型0普通1快速
                'TRANSFER_TYPE',  # 付款类型0混合付款，1付款至丰付账户，2付款至银行账户
                'OPERATOR_AUDITING_SIGN',  # 运营审核标识（0手工审核，1自动实时）
            ],
            where_condition="batchpay_no = '%s'" % self.BatchTransfer_notifyCheck_sample.input_parameter[
                'batchTransferNo'].decode()
        )
        self.assertEqual(
            '0',
            str(batchpay_record_list[0][0]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '2',
            str(batchpay_record_list[0][1]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '.09',
            str(batchpay_record_list[0][2]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '2',
            str(batchpay_record_list[0][3]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0.09',
            str(batchpay_record_list[0][4]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '.02',
            str(batchpay_record_list[0][5]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0',
            str(batchpay_record_list[0][6]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0.0',
            str(batchpay_record_list[0][7]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0.0',
            str(batchpay_record_list[0][8]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0.0',
            str(batchpay_record_list[0][8]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0',
            str(batchpay_record_list[0][9]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0',
            str(batchpay_record_list[0][10]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '1',
            str(batchpay_record_list[0][11]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '2',
            str(batchpay_record_list[0][12]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '1',
            str(batchpay_record_list[0][13]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        """查询数据库batchpay_record表数据"""
        batchpay_detail_list = select_table(
            'batchpay_detail',
            list_view=[
                'FUND',  # 金额
                'ACCOUNT_TYPE',  # 账户类型(2对公银行账户，1对私银行账户，0对公丰付账户)
                'BANK_CODE',  # 银行代码
                'BANK_NAME',  # 收款方开户银行
                'BANK_ACCOUNT',  # 银行账号
                'BANK_ACCOUNT_NAME',  # 开户姓名
                'STATUS',  # -1校验失败、0退票、1失败、2成功、3初始、4审核拒绝、5财务拒绝、6已请求、7事务分离中间态
                'ACCOUNTING_TYPE',  # 到账类型，0为普通，1为快速
                'PAY_FUND',  # 已付金额，供校验用
            ],
            where_condition="batchpay_no = '%s' and detail_no = '1'" %
                            self.BatchTransfer_notifyCheck_sample.input_parameter['batchTransferNo'].decode()
        )
        self.assertEqual(
            '0.04',
            str(batchpay_detail_list[0][0]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '1',
            str(batchpay_detail_list[0][1]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            'ccb',
            str(batchpay_detail_list[0][2]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '中国建设银行',
            str(batchpay_detail_list[0][3].strip()),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '6217000010031195525',
            commonUtils.decryptDes(batchpay_detail_list[0][4].strip()),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            'tester01',
            commonUtils.decryptDes(batchpay_detail_list[0][5].strip()),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '3',
            str(batchpay_detail_list[0][6]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '1',
            str(batchpay_detail_list[0][7]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )
        self.assertEqual(
            '0.04',
            str(batchpay_detail_list[0][8]).strip(),
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )

    @unittest.skip('不对省、市、开户行信息进行校验')
    @runningRecorder(desc='申请普通到账模式，不输省、市、开户支行信息')
    def test_BatchTransfer_notifyCheck_107010101011(self):
        """
                作者：刘佳琪
                需求版本号：不详（历史版本号：无）
                用例编号：
                    107010101011
                用例名称：
                	申请普通到账模式，不输省、市、开户支行信息
                用例描述：
                    无
        """
        self.BatchTransfer_notifyCheck_sample.input_parameter['payType'] = '2'
        self.BatchTransfer_notifyCheck_sample.input_parameter['inAccountType'] = '0'
        self.BatchTransfer_notifyCheck_sample.input_parameter['signature'] = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.input_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.request_signatrue_rule)
        """步骤一：生成加密批量文件"""
        self.BatchTransfer_notifyCheck_sample.batchpay_details_to_bank = [
            ['1','个人银行账户','tester01','0.04','6217000010031195525','ccb','','','','建行个人'],
            ['2','个人银行账户','tester01','0.05','6217000010031195525','ccb','','','','建行个人']
        ]
        self.BatchTransfer_notifyCheck_sample.batchfile_context = batchfile_to_bank_template(
                datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'),
                self.BatchTransfer_notifyCheck_sample.input_parameter['batchTransferNo'],
                self.BatchTransfer_notifyCheck_sample.batchpay_details_to_bank
                )[2]
        commonUtils.encryptDesFromStrTofile(
            self.BatchTransfer_notifyCheck_sample.batchfile_des_key,
            self.BatchTransfer_notifyCheck_sample.batchfile_context,
            self.BatchTransfer_notifyCheck_sample.batchfile_name)
        """步骤二：上传加密批量文件到ftp"""
        with open(self.BatchTransfer_notifyCheck_sample.batchfile_name, 'rb') as fp:
            self.ftp_client.storbinary('STOR ' + self.BatchTransfer_notifyCheck_sample.batchfile_name, fp)
        """步骤三：批量付款请求"""
        respsonse_jsonstr = requests.post(
            url=self.BatchTransfer_notifyCheck_sample.action_url,
            data=commonUtils.encodeDictionaryToGBK(self.BatchTransfer_notifyCheck_sample.input_parameter),
            verify=False
        )
        self.BatchTransfer_notifyCheck_sample.output_parameter.update(respsonse_jsonstr.json())
        """断言1：同步响应断言"""
        self.assertEqual(
            '110180001',
            self.BatchTransfer_notifyCheck_sample.output_parameter['result'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )

    @runningRecorder(desc='批量付款至银行账户，付款类型可以选择0或1')
    def test_BatchTransfer_notifyCheck_107010101048_1(self):
        """
                作者：刘佳琪
                需求版本号：不详（历史版本号：无）
                用例编号：
                    107010101048
                用例名称：
                	批量付款至银行账户，付款类型可以选择0或1'
                用例描述：
                    商户为手工审核商户，批量付款至银行账户，付款类型输入0-手工审核
        """
        """修改商户为手工审核商户"""
        merchant_id = select_table(
            'merchant',
            list_view = ['ID'],
            where_condition = "merchant_code = '%s'"
                              % self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'])[0][0]
        """操作员登录"""
        self.cookies_operator = authentication.login(const._global_configuration().optionManagerOperator)[1]
        merchant_info_default['id'] = str(merchant_id)
        merchant_info_default['fld16'] = '0'
        merchantManage.merchant_info_mgmodify(self.input_dic, self.cookies_operator)
        fld16 = select_table(
            'merchant',
            list_view = ['fld16'],
            where_condition = "merchant_code = '%s'"
                              % self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'])[0][0]
        if str(fld16) != '0':
            raise RuntimeError('修改审核类型失败')
        self.BatchTransfer_notifyCheck_sample.input_parameter['payType'] = '2'
        self.BatchTransfer_notifyCheck_sample.input_parameter['transferPayType'] = '0'
        self.BatchTransfer_notifyCheck_sample.input_parameter['signature'] = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.input_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.request_signatrue_rule)
        """步骤一：生成加密批量文件"""
        commonUtils.encryptDesFromStrTofile(
            self.BatchTransfer_notifyCheck_sample.batchfile_des_key,
            self.BatchTransfer_notifyCheck_sample.batchfile_context,
            self.BatchTransfer_notifyCheck_sample.batchfile_name)
        """步骤二：上传加密批量文件到ftp"""
        with open(self.BatchTransfer_notifyCheck_sample.batchfile_name, 'rb') as fp:
            self.ftp_client.storbinary('STOR ' + self.BatchTransfer_notifyCheck_sample.batchfile_name, fp)
        """步骤三：批量付款请求"""
        respsonse_jsonstr = requests.post(
            url = self.BatchTransfer_notifyCheck_sample.action_url,
            data = commonUtils.encodeDictionaryToGBK(self.BatchTransfer_notifyCheck_sample.input_parameter),
            verify = False
        )
        self.BatchTransfer_notifyCheck_sample.output_parameter.update(respsonse_jsonstr.json())
        self.assertEqual(
            '110180000',
            self.BatchTransfer_notifyCheck_sample.output_parameter['result'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )

    @runningRecorder(desc='批量付款至银行账户，付款类型可以选择0或1')
    def test_BatchTransfer_notifyCheck_107010101048_2(self):
        """
                作者：刘佳琪
                需求版本号：不详（历史版本号：无）
                用例编号：
                    107010101048
                用例名称：
                    批量付款至银行账户，付款类型可以选择0或1'
                用例描述：
                    商户为手工审核商户，批量付款至银行账户，付款类型输入1-自动实时
        """
        """修改商户为手工审核商户"""
        merchant_id = select_table(
            'merchant',
            list_view=['ID'],
            where_condition="merchant_code = '%s'"
                            % self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'])[0][0]
        """操作员登录"""
        self.cookies_operator = authentication.login(const._global_configuration().optionManagerOperator)[1]
        merchant_info_default['id'] = str(merchant_id)
        merchant_info_default['fld16'] = '0'
        merchantManage.merchant_info_mgmodify(self.input_dic, self.cookies_operator)
        fld16 = select_table(
            'merchant',
            list_view=['fld16'],
            where_condition="merchant_code = '%s'"
                            % self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'])[0][0]
        if str(fld16) != '0':
            raise RuntimeError('修改审核类型失败')
        self.BatchTransfer_notifyCheck_sample.input_parameter['payType'] = '2'
        self.BatchTransfer_notifyCheck_sample.input_parameter['transferPayType'] = '1'
        self.BatchTransfer_notifyCheck_sample.input_parameter['signature'] = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.input_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.request_signatrue_rule)
        """步骤一：生成加密批量文件"""
        commonUtils.encryptDesFromStrTofile(
            self.BatchTransfer_notifyCheck_sample.batchfile_des_key,
            self.BatchTransfer_notifyCheck_sample.batchfile_context,
            self.BatchTransfer_notifyCheck_sample.batchfile_name)
        """步骤二：上传加密批量文件到ftp"""
        with open(self.BatchTransfer_notifyCheck_sample.batchfile_name, 'rb') as fp:
            self.ftp_client.storbinary('STOR ' + self.BatchTransfer_notifyCheck_sample.batchfile_name, fp)
        """步骤三：批量付款请求"""
        respsonse_jsonstr = requests.post(
            url=self.BatchTransfer_notifyCheck_sample.action_url,
            data=commonUtils.encodeDictionaryToGBK(self.BatchTransfer_notifyCheck_sample.input_parameter),
            verify=False
        )
        self.BatchTransfer_notifyCheck_sample.output_parameter.update(respsonse_jsonstr.json())
        self.assertEqual(
            '200300344',
            self.BatchTransfer_notifyCheck_sample.output_parameter['result'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )

    @runningRecorder(desc='批量付款至银行账户，付款类型可以选择0或1')
    def test_BatchTransfer_notifyCheck_107010101048_3(self):
        """
                作者：刘佳琪
                需求版本号：不详（历史版本号：无）
                用例编号：
                    107010101048
                用例名称：
                	批量付款至银行账户，付款类型可以选择0或1'
                用例描述：
                    商户为实时付款商户，批量付款至银行账户，付款类型输入0-手工审核
        """
        """修改商户为手工审核商户"""
        merchant_id = select_table(
            'merchant',
            list_view = ['ID'],
            where_condition = "merchant_code = '%s'"
                              % self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'])[0][0]
        """操作员登录"""
        self.cookies_operator = authentication.login(const._global_configuration().optionManagerOperator)[1]
        merchant_info_default['id'] = str(merchant_id)
        merchant_info_default['fld16'] = '1'
        merchantManage.merchant_info_mgmodify(self.input_dic, self.cookies_operator)
        fld16 = select_table(
            'merchant',
            list_view = ['fld16'],
            where_condition = "merchant_code = '%s'"
                              % self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'])[0][0]
        if str(fld16) != '1':
            raise RuntimeError('修改审核类型失败')
        self.BatchTransfer_notifyCheck_sample.input_parameter['payType'] = '2'
        self.BatchTransfer_notifyCheck_sample.input_parameter['transferPayType'] = 0
        self.BatchTransfer_notifyCheck_sample.input_parameter['signature'] = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.input_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.request_signatrue_rule)
        """步骤一：生成加密批量文件"""
        commonUtils.encryptDesFromStrTofile(
            self.BatchTransfer_notifyCheck_sample.batchfile_des_key,
            self.BatchTransfer_notifyCheck_sample.batchfile_context,
            self.BatchTransfer_notifyCheck_sample.batchfile_name)
        """步骤二：上传加密批量文件到ftp"""
        with open(self.BatchTransfer_notifyCheck_sample.batchfile_name, 'rb') as fp:
            self.ftp_client.storbinary('STOR ' + self.BatchTransfer_notifyCheck_sample.batchfile_name, fp)
        """步骤三：批量付款请求"""
        respsonse_jsonstr = requests.post(
            url = self.BatchTransfer_notifyCheck_sample.action_url,
            data = commonUtils.encodeDictionaryToGBK(self.BatchTransfer_notifyCheck_sample.input_parameter),
            verify = False
        )
        self.BatchTransfer_notifyCheck_sample.output_parameter.update(respsonse_jsonstr.json())
        self.assertEqual(
            '110180000',
            self.BatchTransfer_notifyCheck_sample.output_parameter['result'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )

    @runningRecorder(desc='批量付款至银行账户，付款类型可以选择0或1')
    def test_BatchTransfer_notifyCheck_107010101048_4(self):
        """
                作者：刘佳琪
                需求版本号：不详（历史版本号：无）
                用例编号：
                    107010101048
                用例名称：
                	批量付款至银行账户，付款类型可以选择0或1'
                用例描述：
                    商户为实时付款商户，批量付款至银行账户，付款类型输入0-手工审核
        """
        """修改商户为手工审核商户"""
        merchant_id = select_table(
            'merchant',
            list_view = ['ID'],
            where_condition = "merchant_code = '%s'"
                              % self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'])[0][0]
        """操作员登录"""
        self.cookies_operator = authentication.login(const._global_configuration().optionManagerOperator)[1]
        merchant_info_default['id'] = str(merchant_id)
        merchant_info_default['fld16'] = '1'
        merchantManage.merchant_info_mgmodify(self.input_dic, self.cookies_operator)
        fld16 = select_table(
            'merchant',
            list_view = ['fld16'],
            where_condition = "merchant_code = '%s'"
                              % self.BatchTransfer_notifyCheck_sample.input_parameter['merchantCode'])[0][0]
        if str(fld16) != '1':
            raise RuntimeError('修改审核类型失败')
        self.BatchTransfer_notifyCheck_sample.input_parameter['payType'] = '2'
        self.BatchTransfer_notifyCheck_sample.input_parameter['transferPayType'] = '1'
        self.BatchTransfer_notifyCheck_sample.input_parameter['signature'] = commonUtils.md5Signature(
            self.BatchTransfer_notifyCheck_sample.input_parameter,
            self.BatchTransfer_notifyCheck_sample.key,
            self.BatchTransfer_notifyCheck_sample.request_signatrue_rule)
        """步骤一：生成加密批量文件"""
        commonUtils.encryptDesFromStrTofile(
            self.BatchTransfer_notifyCheck_sample.batchfile_des_key,
            self.BatchTransfer_notifyCheck_sample.batchfile_context,
            self.BatchTransfer_notifyCheck_sample.batchfile_name)
        """步骤二：上传加密批量文件到ftp"""
        with open(self.BatchTransfer_notifyCheck_sample.batchfile_name, 'rb') as fp:
            self.ftp_client.storbinary('STOR ' + self.BatchTransfer_notifyCheck_sample.batchfile_name, fp)
        """步骤三：批量付款请求"""
        respsonse_jsonstr = requests.post(
            url = self.BatchTransfer_notifyCheck_sample.action_url,
            data = commonUtils.encodeDictionaryToGBK(self.BatchTransfer_notifyCheck_sample.input_parameter),
            verify = False
        )
        self.BatchTransfer_notifyCheck_sample.output_parameter.update(respsonse_jsonstr.json())
        self.assertEqual(
            '110180000',
            self.BatchTransfer_notifyCheck_sample.output_parameter['result'],
            msg=self.BatchTransfer_notifyCheck_sample.io_parameter
        )

    @runningRecorder(desc='单笔限额校验-商户付款类型为实时付款商户')
    def test_BatchTransfer_notifyCheck_107010101050(self):
        """
                作者：刘佳琪
                需求版本号：不详（历史版本号：无）
                用例编号：
                    107010101048
                用例名称：
                	批量付款至银行账户，付款类型可以选择0或1'
                用例描述：
                    无
        """
        pass

    @unittest.skip('未实现自动化')
    @runningRecorder(desc='未设置单笔限额')
    def test_BatchTransfer_notifyCheck_107010101051(self):
        """
                作者：刘佳琪
                需求版本号：不详（历史版本号：无）
                用例编号：
                    107010101048
                用例名称：
                	批量付款至银行账户，付款类型可以选择0或1'
                用例描述：
                    无
        """
        pass

    @runningRecorder(desc='实时付款总量控制，自动付款且付款至银行账户时才控制')
    def test_BatchTransfer_notifyCheck_107010101052(self):
        """
                作者：刘佳琪
                需求版本号：不详（历史版本号：无）
                用例编号：
                    107010101048
                用例名称：
                	批量付款至银行账户，付款类型可以选择0或1'
                用例描述：
                    无
        """
        pass

    @runningRecorder(desc='确认提交批量付款请求-实时')
    def test_BatchTransfer_notifyTransfer_107020101001(self):
        """
            作者：刘佳琪
            需求版本号：无（历史版本号:）
            用例编号：
                107020101001
            用例名称：
                确认提交批量付款请求-实时
            用例描述：
                操作员已上传批量付款请求
                手续费收取方式为实时收取
                商户可用余额充足
        """
        self.subTest(self.test_BatchTransfer_notifyCheck_107010101003())
        self.BatchTransfer_notifyTransfer_sample.input_parameter['batchTransferNo'] = \
            self.global_batchTransferNo
        self.BatchTransfer_notifyTransfer_sample.input_parameter['signature'] = commonUtils.md5Signature(
            self.BatchTransfer_notifyTransfer_sample.input_parameter,
            self.BatchTransfer_notifyTransfer_sample.key,
            self.BatchTransfer_notifyTransfer_sample.request_signatrue_rule)
        respsonse_jsonstr = requests.post(
            url=self.BatchTransfer_notifyTransfer_sample.action_url,
            data=commonUtils.encodeDictionaryToGBK(self.BatchTransfer_notifyTransfer_sample.input_parameter),
            verify=False
        )
        self.BatchTransfer_notifyTransfer_sample.output_parameter.update(respsonse_jsonstr.json())
        respsonseSignatrue = commonUtils.md5Signature(
            self.BatchTransfer_notifyTransfer_sample.output_parameter,
            self.BatchTransfer_notifyTransfer_sample.key,
            self.BatchTransfer_notifyTransfer_sample.sync_signatrue_rule)
        self.assertEqual(
            respsonseSignatrue,
            self.BatchTransfer_notifyTransfer_sample.output_parameter['signature'],
            msg='响应签名验签失败')
        self.assertEqual(
            '00000',
            self.BatchTransfer_notifyTransfer_sample.output_parameter['result'],
            msg=self.BatchTransfer_notifyTransfer_sample.io_parameter)

    @runningRecorder(desc='批次状态查询')
    def test_BatchTransfer_queryBatchTransferState_107030101001(self):
        """
            作者：刘佳琪
            需求版本号：无（历史版本号:）
            用例编号：
                107030101001
            用例名称：
        	    批次状态查询
            用例描述：
                无
        """
        self.subTest(self.test_BatchTransfer_notifyCheck_107010101003())
        self.BatchTransfer_queryBatchTransferState_sample.input_parameter['batchTransferNo'] = \
            self.global_batchTransferNo
        self.BatchTransfer_queryBatchTransferState_sample.input_parameter['signature'] = commonUtils.md5Signature(
            self.BatchTransfer_queryBatchTransferState_sample.input_parameter,
            self.BatchTransfer_queryBatchTransferState_sample.key,
            self.BatchTransfer_queryBatchTransferState_sample.request_signatrue_rule)
        respsonse_jsonstr = requests.post(
            url=self.BatchTransfer_queryBatchTransferState_sample.action_url,
            data=commonUtils.encodeDictionaryToGBK(self.BatchTransfer_queryBatchTransferState_sample.input_parameter),
            verify=False
        )
        self.BatchTransfer_queryBatchTransferState_sample.output_parameter.update(respsonse_jsonstr.json())
        respsonseSignatrue = commonUtils.md5Signature(
            self.BatchTransfer_queryBatchTransferState_sample.output_parameter,
            self.BatchTransfer_queryBatchTransferState_sample.key,
            self.BatchTransfer_queryBatchTransferState_sample.sync_signatrue_rule)
        self.assertEqual(
            respsonseSignatrue,
            self.BatchTransfer_queryBatchTransferState_sample.output_parameter['signature'],
            msg='响应签名验签失败')
        self.assertEqual(
            '00000',
            self.BatchTransfer_queryBatchTransferState_sample.output_parameter['result'],
            msg = self.BatchTransfer_queryBatchTransferState_sample.io_parameter)
        self.assertEqual(
            '0',
            self.BatchTransfer_queryBatchTransferState_sample.output_parameter['status'],
            msg = self.BatchTransfer_queryBatchTransferState_sample.io_parameter)

    def tearDown(self):
        self.ftp_client.quit()

    # def ftp_connect(self):
    #     ftp = FTP()
    #     ftp.connect(self.ftp_param['IP'])
    #     ftp.login(self.ftp_param['username'], self.ftp_param['passowrd'])
    #     ftp.cwd('provider/%s/batchTransfer/'%self.input_parameter['merchantCode'])
    #     # ftp.ftp.set_debuglevel(0)
    #     return ftp

# if __name__ == '__main__':
#     unittest.main()
