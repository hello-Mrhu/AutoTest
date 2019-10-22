import requests
from lxml import etree
from baseLib.commonAPI.OracleQuery import select_table,sqlOne,sqlAll
from configuration import const
from baseLib.baseUtils.recorder import runningRecorder


#代发费率修改
@runningRecorder(desc='修改付款费率')
def mgmodifyDisburseFee(inputFormParam, cookie, merchant_code):
    disburse_fee_list = select_table(
        'merchant_fee',
        list_view=[
            'METHOD',
            'MERCHANT_ID',
            'TYPE',
            'FIX_FEE',
            'FEE_RATE',
            'MIN_FEE',
            'MAX_FEE',
            'LIMIT_FIX_RATE_FUND',
            'LOWER_LIMIT',
            'UPPER_LIMIT',
            'LIMIT_LAYER',
            'LIMIT_FUND',
            'CHARGE_TYPE'
        ],
        where_condition="merchant_code = '%s' and type = '%s' order by limit_layer"
                        % (merchant_code, inputFormParam['type'])
    )
    merchant_transfer_config_default = select_table(
        'merchant_transfer_config',
        list_view=[
            'IS_NEED_REVIEW',
            'IS_NEED_SUB_REVIEW',
            'MER_SINGLE_DAY_LIMIT',
            'MER_SINGLE_DAY_COUNT_LIMIT',
            'MER_SINGLE_MONTH_LIMIT',
            'MER_SINGLE_YEAR_LIMIT'
        ],
        where_condition="merchant_code = '%s'" % merchant_code
    )
    merchant_transfer_fee_default = {
        'step': '1',
        'oldMethod': str(disburse_fee_list[0][0]),
        'merchantId': str(disburse_fee_list[0][1]),
        'type': str(disburse_fee_list[0][2]),# 4付款至企业账户、5普通付款至个人银行、6普通付款至企业银行、12快速付款至个人银行、13快速付款至企业银行
        'chargeType': str(disburse_fee_list[0][12]),# 丰付手续费收取类型，0为实时，1为预付，2为垫付，3为后付
        'meth': str(disburse_fee_list[0][0]),
        'fixFee' : '',
        'feeRate': str('{:g}'.format(disburse_fee_list[0][4])) if disburse_fee_list[0][4] != None else '',
        'minFee': str('{:g}'.format(disburse_fee_list[0][5])) if disburse_fee_list[0][5] != None else '',
        'maxFee': str('{:g}'.format(disburse_fee_list[0][6])) if disburse_fee_list[0][6] != None else '',
        'limitFixRateFund': str('{:g}'.format(disburse_fee_list[0][7])) if disburse_fee_list[0][7] != None else '',
        'fixFee1': '',
        'limit1': '',
        'fixFee2': '',
        'limit2': '',
        'fixFee3': '',
        'limit3': '',
        'fixFee4': '',
        'limit4': '',
        'fixFee5': '',
        'limit5': '',
        'limitFund': str('{:g}'.format(disburse_fee_list[0][11])) if disburse_fee_list[0][11] != None else '',
        'fld12': str(merchant_transfer_config_default[0][0]) if merchant_transfer_config_default[0][0] != None else '',
        'isNeedChildReview': str(merchant_transfer_config_default[0][1]) if merchant_transfer_config_default[0][1] != None else '',
        'merSingleDayLimit': str('{:g}'.format(merchant_transfer_config_default[0][2])) if merchant_transfer_config_default[0][2] != None else '',
        'merSingleDayCountLimit': str('{:g}'.format(merchant_transfer_config_default[0][3])) if merchant_transfer_config_default[0][3] != None else '',
        'merSingleMonthLimit': str('{:g}'.format(merchant_transfer_config_default[0][4])) if merchant_transfer_config_default[0][4] != None else '',
        'merSingleYearLimit': str('{:g}'.format(merchant_transfer_config_default[0][5])) if merchant_transfer_config_default[0][5] != None else ''
    }

    if str(disburse_fee_list[0][0]) == '2':
        merchant_fix_rate_fee = {
            'step': '2',
            'fixFee': str('{:g}'.format(disburse_fee_list[0][3])) if disburse_fee_list[0][3] != None else '',
            'feeRate': (str('{:g}'.format(disburse_fee_list[1][4])) if disburse_fee_list[1][4] != None else '') if len(disburse_fee_list) == 2 else '',
        }
        merchant_transfer_fee_default.update(merchant_fix_rate_fee)
    elif str(disburse_fee_list[0][0]) == '3':
        merchant_step_fee = {
            'step': str(len(disburse_fee_list)),
            'fixFee1': str('{:g}'.format(disburse_fee_list[0][3])) if disburse_fee_list[0][3] != None else '',
            'limit1': str('{:g}'.format(disburse_fee_list[0][9])) if disburse_fee_list[0][9] != None else '',
            'fixFee2': (str('{:g}'.format(disburse_fee_list[1][3])) if disburse_fee_list[1][3] != None else '') if len(
                disburse_fee_list) > 1 else '',
            'limit2': (str('{:g}'.format(disburse_fee_list[1][9])) if disburse_fee_list[1][9] != None else '') if len(
                disburse_fee_list) > 1 else '',
            'fixFee3': (str('{:g}'.format(disburse_fee_list[2][3])) if disburse_fee_list[2][3] != None else '') if len(
                disburse_fee_list) > 2 else '',
            'limit3': (str('{:g}'.format(disburse_fee_list[2][9])) if disburse_fee_list[2][9] != None else '') if len(
                disburse_fee_list) > 2 else '',
            'fixFee4': (str('{:g}'.format(disburse_fee_list[3][3])) if disburse_fee_list[3][3] != None else '') if len(
                disburse_fee_list) > 3 else '',
            'limit4': (str('{:g}'.format(disburse_fee_list[3][9])) if disburse_fee_list[3][9] != None else '') if len(
                disburse_fee_list) > 3 else '',
            'fixFee5': (str('{:g}'.format(disburse_fee_list[4][3])) if disburse_fee_list[4][3] != None else '') if len(
                disburse_fee_list) > 4 else '',
            'limit5': ''
        }
        merchant_transfer_fee_default.update(merchant_step_fee)

    merchant_transfer_fee_default.update(inputFormParam)
    # print(merchant_transfer_fee_default)
    mgmodifyActionList = ['/Admin/withdrawManage/merchantTransferConfigManageAction_mgtoUpdateBatchpay',
                          '/Admin/withdrawManage/merchantTransferConfigManageAction_mgmodifyBatchpay']
    getTokenParam = '?merchantId=' + merchant_transfer_fee_default.get('merchantId') + '&type=' + merchant_transfer_fee_default.get('type') + '&meth=' + merchant_transfer_fee_default.get('oldMethod')
    getTokenResponseHtmlStr = requests.get(
        const._global_configuration().OptionManagerHttpUrl + mgmodifyActionList[0] + getTokenParam,
        cookies=cookie)
    selector = etree.HTML(getTokenResponseHtmlStr.text)
    try:
        strToken = (selector.xpath('//input[@name=\"token\"]/@value'))[0].strip()
    except IndexError:
        strToken = 'none'
    hideFormParam = {'struts.token.name': 'token',
                 'token': strToken}
    allFormParam = hideFormParam.copy()
    allFormParam.update(merchant_transfer_fee_default)
    responseByPostForm = requests.post(const._global_configuration().OptionManagerHttpUrl + mgmodifyActionList[1],
                                       cookies=cookie,
                                       data = allFormParam)
    responseHtmlStr = responseByPostForm.text


#风控通过
@runningRecorder(desc='风控通过')
def transferRiskAudit(merchantTransferRequestId, cookie):
    sqlId = 'select id from merchant_transfer_request where request_id = \'%s\'' %merchantTransferRequestId#.decode()
    indexId = sqlOne(sqlId)[0]
    transferRiskAuditActionList = ['/Admin/withdrawManage/merchantWithdrawManageAction_query',
                          '/Admin/withdrawManage/merchantWithdrawManageAction_mgconfirm?requestId=%s&fld1=0'%(indexId)]
    getTokenParam = {'requestDateStart': '2999/03/12'}
    getTokenResponseHtmlStr = requests.post(
        const._global_configuration().OptionManagerHttpUrl + transferRiskAuditActionList[0],
        cookies=cookie, data = getTokenParam)
    selector = etree.HTML(getTokenResponseHtmlStr.text)
    try:
        strToken = (selector.xpath('//input[@name=\"token\"]/@value'))[0].strip()
    except IndexError:
        strToken = 'none'
    hideFormParam = {'struts.token.name': 'token',
                 'token': strToken}
    allFormParam = hideFormParam.copy()
    responseByPostForm = requests.post(const._global_configuration().OptionManagerHttpUrl + transferRiskAuditActionList[1],
                                       cookies=cookie,
                                       data = allFormParam)
    responseHtmlStr = responseByPostForm.text

#财务通过
@runningRecorder(desc = '财务通过')
def transferConfirm(merchantTransferRequestId, cookie):
    sqlId = 'select id from merchant_transfer_request where request_id = \'%s\'' % merchantTransferRequestId#.decode()
    indexId = sqlOne(sqlId)[0]
    transferRiskAuditActionList = ['/Admin/withdrawManage/merchantWithdrawManageAction_query',
                                   '/Admin/withdrawManage/merchantWithdrawManageAction_mgfinanceConfirm?requestIds=%s|0' % (
                                       indexId)]
    getTokenParam = {'requestDateStart': '2999/03/12'}
    getTokenResponseHtmlStr = requests.post(
        const._global_configuration().OptionManagerHttpUrl + transferRiskAuditActionList[0],
        cookies=cookie, data=getTokenParam)
    selector = etree.HTML(getTokenResponseHtmlStr.text)
    try:
        strToken = (selector.xpath('//input[@name=\"token\"]/@value'))[0].strip()
    except IndexError:
        strToken = 'none'
    hideFormParam = {'struts.token.name': 'token',
                     'token': strToken}
    allFormParam = hideFormParam.copy()
    # allFormParam.update(inputFormParam)
    responseByPostForm = requests.post(
        const._global_configuration().OptionManagerHttpUrl + transferRiskAuditActionList[1],
        cookies=cookie,
        data=allFormParam)
    responseHtmlStr = responseByPostForm.text
