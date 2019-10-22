from baseLib.commonAPI import commonUtils,OracleQuery
import datetime

__all__ = [
    'merchant_transfer_fee_default',
    'singleTransfer_toTransfer_default',
    'singleTransfer_singleTransferQuery_default',
    'BatchTransfer_notifyCheck_default',
    'BatchTransfer_notifyTransfer_default',
    'BatchTransfer_queryBatchTransferState_default',
    'batchfile_to_suma_template',
    'batchfile_to_bank_template',
]

merchant_transfer_fee_default = {
    'step' : '1',
    'oldMethod' : '1',
    'merchantId' : '104',
    'type' : '5',
    'chargeType' : '1',
    'meth' : '1',
    'feeRate' : '100',
    'minFee' : '0.01',
    'maxFee' : '1',
    'fixFee1' : '',
    'limit1' : '',
    'fixFee2' : '',
    'limit2' : '',
    'fixFee3' : '',
    'limit3' : '',
    'fixFee4' : '',
    'limit4' : '',
    'fixFee5' : '',
    'limit5' : '',
    'limitFund' : '300',
    'fld12' : '0',
    'isNeedChildReview' : '0',
    'merSingleDayLimit' : '',
    'merSingleDayCountLimit' : '',
    'merSingleMonthLimit' : '',
    'merSingleYearLimit' : ''
}

class singleTransfer_toTransfer_default(object):
    def __init__(self, http_ip = '172.16.3.9:8080', merchant_code = 'CSSH', merchant_key = 'CSSH_KEY'):
        self.action_url = 'http://%s/main/singleTransfer_toTransfer' % http_ip
        self.input_parameter = {
            'requestId': commonUtils.requestId(num = 20),
            'merchantCode': merchant_code,
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
        self.request_signatrue_rule = [
            'requestId',
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
            'transferPayType'
        ]
        self.sync_signatrue_rule = [
            'requestId',
            'result',
            'sum'
        ]
        self.asyn_signatruerule = []
        self.key = merchant_key
        self.output_parameter = {}
        self.io_parameter = {'请求参数': self.input_parameter, '响应参数': self.output_parameter}

class singleTransfer_singleTransferQuery_default(object):
    def __init__(self, http_ip = '172.16.3.9:8080', merchant_code = 'CSSH', merchant_key = 'CSSH_KEY'):
        self.action_url = 'http://%s/main/singleTransfer_singleTransferQuery' % http_ip
        self.input_parameter = {
            'requestId': commonUtils.requestId(num = 20),
            'merchantCode': merchant_code,
            'originalRequestId': '',
            'signature': ''
        }
        self.request_signatrue_rule = [
            'requestId',
            'merchantCode',
            'originalRequestId'
        ]
        self.sync_signatrue_rule = [
            'requestId',
            'result',
            'status',
            'dealRemark'
        ]
        self.asyn_signatruerule = []
        self.key = merchant_key
        self.output_parameter = {}
        self.io_parameter = {'请求参数': self.input_parameter, '响应参数': self.output_parameter}

class BatchTransfer_notifyCheck_default(object):
    def __init__(self, http_ip = '172.16.3.9:8080', merchant_code = 'CSSH', merchant_key = 'CSSH_KEY'):
        self.action_url = 'http://%s/main/BatchTransfer_notifyCheck'%http_ip
        self.input_parameter = {
            'requestId' : commonUtils.requestId(num = 20),
            'merchantCode' : merchant_code,
            'batchTransferNo' : datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%M%S'),
            'payType' : '1',#1：付款至丰付账户；2：付款至银行账户
            'inAccountType' : '0',#选输（付款方式为付款至银行账户时必输）0：普通；1：快速
            'transferPayType' : '0',#选输0 ：手工审核 1：自动实时 默认为0
            'signature': ''
        }
        self.request_signatrue_rule = [
            'merchantCode',
            'requestId',
            'batchTransferNo',
            'payType',
            'inAccountType',
            'transferPayType']
        self.sync_signatrue_rule = [
            'merchantCode',
            'requestId',
            'batchTransferNo',
            'result']
        self.asyn_signatrue_rule = []
        self.key = merchant_key
        self.output_parameter = {}
        self.io_parameter = {'请求参数': self.input_parameter, '响应参数': self.output_parameter}
        self.batchfile_name = '%s.csv'%self.input_parameter['batchTransferNo']
        # self.ftp = self.ftp_connect()
        self.ftp_remote_path = 'provider/%s/batchTransfer/' % merchant_code
        self.batchpay_details_to_suma = [
            ['1','CSSH','测试商户','0.02','付款至丰付'],
            ['2','CSSH','测试商户','0.01','付款至丰付']
        ]
        self.batchpay_details_to_bank = [
            ['1','个人银行账户','tester01','0.04','6217000010031195525','ccb','北京市','北京市','中国建设银行北京上地支行','建行个人'],
            ['2','个人银行账户','tester01','0.05','6217000010031195525','ccb','北京市','北京市','中国建设银行北京上地支行','建行个人']
        ]
        self.batchfile_tuple = \
            batchfile_to_suma_template(
                datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'),
                self.input_parameter['batchTransferNo'],
                self.batchpay_details_to_suma
            ) if self.input_parameter['payType'] == 1 else \
                batchfile_to_bank_template(
                datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'),
                self.input_parameter['batchTransferNo'],
                self.batchpay_details_to_bank
                )
        self.batchfile_context = self.batchfile_tuple[2]
        # self.batchfile_context = \
        #     '日期,%s,批次号,%s,明细数目,2,总金额(元),0.03\r\n' \
        #     ',,,,,,\r\n' \
        #     '商户流水号,商户号,商户名称,金额(元),用途\r\n' \
        #     '1,%s,测试商户,0.02,付款至丰付\r\n' \
        #     '2,%s,测试商户,0.01,付款至丰付'\
        #     %(datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d'),
        #       self.input_parameter['batchTransferNo'],
        #       merchant_code,
        #       merchant_code) if self.input_parameter['payType'] == 1 else \
        #     '日期,%s,批次号,%s,明细数目,2,总金额(元),0.09,,\r\n'\
        #     ',,,,,,,,,\r\n'\
        #     '商户流水号,账户类型,收款方户名,金额(元),银行账号,开户银行,开户省份,开户城市,支行名称,银行用途\r\n'\
        #     '1,个人银行账户,tester01,0.04,6217000010031195525,ccb,北京市,北京市,中国建设银行北京上地支行,建行个人\r\n'\
        #     '2,个人银行账户,tester02,0.05,6217000010031195525,ccb,北京市,北京市,中国建设银行北京上地支行,建行个人'\
        #     %(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'), self.input_parameter['batchTransferNo'])

        self.batchfile_des_key = 'CSSH123456'

class BatchTransfer_notifyTransfer_default(object):
    def __init__(self, http_ip = '172.16.3.9:8080', merchant_code = 'CSSH', merchant_key = 'CSSH_KEY'):
        self.action_url = 'http://%s/main/BatchTransfer_notifyTransfer' % http_ip
        self.input_parameter = {
            'requestId': commonUtils.requestId(num = 20),
            'merchantCode': merchant_code,
            'batchTransferNo': '',
            'method': '0',
            'noticeUrl': 'http://172.16.3.1',
            'refundNoticeUrl': 'http://172.16.3.1',
            'signature': ''
        }
        self.request_signatrue_rule = [
            'merchantCode',
            'requestId',
            'batchTransferNo',
            'method',
            'noticeUrl',
            'refundNoticeUrl'
        ] if self.input_parameter['method'] == '1' else [
            'merchantCode',
            'requestId',
            'batchTransferNo',
            'method'
        ]
        self.sync_signatrue_rule = [
            'merchantCode',
            'requestId',
            'batchTransferNo',
            'result'
        ]
        self.asyn_signatruerule = []
        self.key = merchant_key
        self.output_parameter = {}
        self.io_parameter = {'请求参数': self.input_parameter, '响应参数': self.output_parameter}

class BatchTransfer_queryBatchTransferState_default(object):
    def __init__(self, http_ip='172.16.3.9:8080', merchant_code='CSSH', merchant_key='CSSH_KEY'):
        self.action_url = 'http://%s/main/BatchTransfer_queryBatchTransferState' % http_ip
        self.input_parameter = {
            'requestId': commonUtils.requestId(num = 20),
            'merchantCode': merchant_code,
            'batchTransferNo': '',
            'signature': ''
        }
        self.request_signatrue_rule = [
            'merchantCode',
            'requestId',
            'batchTransferNo'
        ]
        self.sync_signatrue_rule = [
            'merchantCode',
            'requestId',
            'batchTransferNo',
            'result',
            'status'
        ]
        self.asyn_signatruerule = []
        self.key = merchant_key
        self.output_parameter = {}
        self.io_parameter = {'请求参数': self.input_parameter, '响应参数': self.output_parameter}

def batchfile_to_suma_template(date, batchTransferNo, list_data):
    batchpay_detail_list = []
    for sub_list in list_data:
        batchpay_detail_list.append(sub_list[0] + ''.join(',' + sub_list[i] for i in range(1, len(sub_list))) + '\r\n')
    batchpay_detail_records = ''.join(batchpay_detail_list)
    # print(batchpay_detail_records)
    batchpay_detail_count = str(len(list_data))
    batchpay_sum = 0
    for sub_list in list_data:
        batchpay_sum += float(sub_list[3])
    context  = ''\
    '日期,%s,批次号,%s,明细数目,%s,总金额(元),%s\r\n' \
    ',,,,,,\r\n' \
    '商户流水号,商户号,商户名称,金额(元),用途\r\n' \
    '%s'% (date, batchTransferNo, batchpay_detail_count, str(batchpay_sum), batchpay_detail_records)
    return (batchpay_detail_count, batchpay_sum, context)

def batchfile_to_bank_template(date, batchTransferNo, list_data):
    batchpay_detail_list = []
    for sub_list in list_data:
        batchpay_detail_list.append(sub_list[0] + ''.join(',' + sub_list[i] for i in range(1, len(sub_list))) + '\r\n')
    batchpay_detail_records = ''.join(batchpay_detail_list)
    # print(batchpay_detail_records)
    batchpay_detail_count = str(len(list_data))
    batchpay_sum = 0
    for sub_list in list_data:
        batchpay_sum += float(sub_list[3])
    context  = ''\
    '日期,%s,批次号,%s,明细数目,%s,总金额(元),%s,,\r\n' \
    ',,,,,,,,,\r\n' \
    '商户流水号,账户类型,收款方户名,金额(元),银行账号,开户银行,开户省份,开户城市,支行名称,银行用途\r\n' \
    '%s'% (date, batchTransferNo, batchpay_detail_count, str(batchpay_sum), batchpay_detail_records)
    return (batchpay_detail_count, batchpay_sum, context)

# bank_list = [
#     ['1','个人银行账户','tester01','0.04','6217000010031195525','ccb','北京市','北京市','中国建设银行北京上地支行','建行个人'],
#     ['2','个人银行账户','tester01','0.05','6217000010031195525','ccb','北京市','北京市','中国建设银行北京上地支行','建行个人'],
#     ['3','个人银行账户','tester01','0.06','6217000010031195525','ccb','北京市','北京市','中国建设银行北京上地支行','建行个人']
# ]
# suma_list = [
#     ['1', 'CSSH', '测试商户', '0.02', '付款至丰付'],
#     ['2', 'CSSH', '测试商户', '0.2', '付款至丰付'],
#     ['3', 'CSSH', '测试商户', '0.01', '付款至丰付']
# ]
# print(batchfile_to_bank_template('20190524', '201905240001', bank_list))
# print(batchfile_to_suma_template('20190524', '201905240001', suma_list))

