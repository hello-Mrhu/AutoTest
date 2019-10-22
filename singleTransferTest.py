# -*- coding:utf-8 -*-
#autor :huchengjiang
import requests
from baseLib.commonAPI import commonUtils, OracleQuery
from baseLib.baseUtils.recorder import logging
from baseLib.operationManagerAPI.authentication import login
from baseLib.operationManagerAPI.DisburseManager import transferRiskAudit
from baseLib.operationManagerAPI.DisburseManager import transferConfirm
import unittest
from configuration import const

class transfer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.globalRequestId = None

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
            'accountName': '武孟梦',
            'bankCode': 'icbc',
            'bankAccount': '6212260200036759963',
            'reason': '1555',
            'noticeUrl': 'http://172.16.3.1/testpayMobile/p2pNoticeGBK',
            'refundNoticeUrl': 'http://172.16.3.1/testpayMobile/p2pNoticeGBK',
            'transferPayType': '1',     #选输0：手工审核 1：自动实时
            'signature': ''
        }
        self.key = 'CSSH_KEY'
        self.outputParameter = {}
        self.IOParameter = {'请求参数':self.inputParameter, '响应参数': self.outputParameter}

    @logging(level='INFO', desc='单笔付款')
    def test001(self):
        """
        手工审核付款成功-正例-冒烟
        """
        #发送请求
        self.inputParameter['requestId'] = commonUtils.requestId()
        self.inputParameter['transferPayType'] = '0'
        self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key, self.requestSignatrueRule)
        s = requests.post(url = self.actionUrl, data = commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
        self.outputParameter.update(s.json())
        respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)
        #响应签名断言
        self.assertEqual(respsonseSignatrue, self.outputParameter['signature'], msg = '响应签名验签失败')
        #同步响应断言
        self.assertEqual('00000', self.outputParameter['result'], msg = self.IOParameter)
        #数据库断言
        sqlStatus = 'select status from merchant_transfer_request where request_id = \'%s\' order by id desc' %self.inputParameter.get('requestId').decode()
        requestStatus = str(OracleQuery.sqlAll(sqlStatus)[0][0])
        self.assertEqual('0', requestStatus)
        self.ass

        returnTuple = login(const._global_configuration().optionManagerOperator)
        commonUtils.waiting(15)
        #风控通过
        transferRiskAudit(self.inputParameter.get('requestId'), returnTuple[1])
        requestStatus = str(OracleQuery.sqlAll(sqlStatus)[0][0])
        self.assertEqual('6', requestStatus)

        #财务通过
        transferConfirm(self.inputParameter.get('requestId'), returnTuple[1])
        requestStatus = str(OracleQuery.sqlAll(sqlStatus)[0][0])
        self.assertEqual('9', requestStatus)

    # @logging(level='INFO', desc='单笔实时付款请求')
    # def test002(self):
    #     """
    #     实时付款请求-正例-冒烟
    #     """
    #     #发送请求
    #     self.globalRequestId = commonUtils.requestId()
    #     self.inputParameter['requestId'] = self.globalRequestId
    #     self.inputParameter['transferPayType'] = '0'
    #     self.inputParameter['signature'] = commonUtils.md5Signature(self.inputParameter, self.key, self.requestSignatrueRule)
    #     s = requests.post(url = self.actionUrl, data = commonUtils.encodeDictionaryToGBK(self.inputParameter), verify=False)
    #     self.outputParameter.update(s.json())
    #     respsonseSignatrue = commonUtils.md5Signature(self.outputParameter, self.key, self.syncSignatrueRule)
    #     #响应签名断言
    #     self.assertEqual(respsonseSignatrue, self.outputParameter['signature'], msg = '响应签名验签失败')
    #     #同步响应断言
    #     self.assertEqual('00000', self.outputParameter['result'], msg = self.IOParameter)
    #     #数据库断言
    #     sqlStatus = 'select status from merchant_transfer_request where request_id = \'%s\' order by id desc' %self.inputParameter.get('requestId').decode()
    #     requestStatus = str(OracleQuery.sqlAll(sqlStatus)[0][0])
    #     self.assertEqual('0', requestStatus)
    #
    # @logging(level='INFO', desc='风控通过')
    # def test003(self):
    #     """
    #     风控通过
    #     """
    #     self.subTest(self.test002())
    #     sqlStatus = 'select status from merchant_transfer_request where request_id = \'%s\' order by id desc' % self.globalRequestId
    #     cookies = login('xjd1', 'xjd12345')
    #     commonUtils.waiting(15)
    #     #风控通过
    #     transferRiskAudit(self.globalRequestId, cookies)
    #     requestStatus = str(OracleQuery.sqlAll(sqlStatus)[0][0])
    #     self.assertEqual('6', requestStatus)
    #
    # @logging(level='INFO', desc='财务通过')
    # def test004(self):
    #     """
    #     财务通过
    #     """
    #     self.subTest(self.test002())
    #     self.subTest(self.test003())
    #     sqlStatus = 'select status from merchant_transfer_request where request_id = \'%s\' order by id desc' % self.globalRequestId
    #     cookies = login('xjd1', 'xjd12345')
    #     transferConfirm(self.globalRequestId, cookies)
    #     requestStatus = str(OracleQuery.sqlAll(sqlStatus)[0][0])
    #     self.assertEqual('9', requestStatus)
if __name__=='__main__':
    unittest.main()









