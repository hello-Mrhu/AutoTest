import requests
from lxml import etree
from configuration import const
from baseLib.commonAPI.OracleQuery import select_table
from baseLib.commonAPI import commonUtils

def merchant_info_mgmodify(inputFormParam, cookie, merchant_code):
    merchant_info_list = select_table(
        'merchant',
        list_view = [
            'ID',
            'MERCHANT_NAME',
            'MERCHANT_CODE',
            'LEGAL_PERSON',
            'CONTACT_PERSON',
            'CONTACT_TELEPHONE',
            'ZIP_CODE',
            'BUSINESS_LICENSE',
            'SIGN_TYPE',
            'SIGN_KEY',
            'FLD7',
            'FLD8',
            'FLD9',
            'FLD10',
            'FLD13',
            'FLD16'
        ],
        where_condition = "merchant_code = '%s'" %merchant_code
    )
    merchant_info_default = {
        'id': str(merchant_info_list[0][0]),
        'oldfld9': '0',
        'oldisd': '',
        'selectBizs': '',
        'flag': '1',
        'name': str(merchant_info_list[0][1]),
        'code': str(merchant_info_list[0][2]),
        'address': '',
        'owner': commonUtils.decryptDes(str(merchant_info_list[0][3])),
        'manager': commonUtils.decryptDes(str(merchant_info_list[0][4])),
        'telphone': commonUtils.decryptDes(str(merchant_info_list[0][5])),
        'addressCode': str(merchant_info_list[0][6]),
        'permitId': str(merchant_info_list[0][7]),
        'signType': str(merchant_info_list[0][8]),
        'merKey': str(merchant_info_list[0][9]),
        'fld7': str(merchant_info_list[0][10]),
        'fld8': str(merchant_info_list[0][11]),
        'serviceTelphone': '',
        'fld9': str(merchant_info_list[0][12]),
        'isSameCard': '0',
        'fld10': str(merchant_info_list[0][13]),
        'fld13': str(merchant_info_list[0][14]),
        'fld16': str(merchant_info_list[0][15])  # 0手工审核 1实时自动
    }
    merchant_info_default.update(inputFormParam)
    mgmodifyActionList = ['/Admin/merchantManage/merchantManageAction_mgtoUpdate',
                          '/Admin/merchantManage/merchantManageAction_mgmodify']
    getTokenParam = '?id=' + merchant_info_default.get('id')
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
    allFormParam.update(merchant_info_default)
    responseByPostForm = requests.post(const._global_configuration().OptionManagerHttpUrl + mgmodifyActionList[1],
                                       cookies=cookie,
                                       data = allFormParam)
    return responseByPostForm.text

def merchant_realtime_transfer_info_mgmodify(inputFormParam, cookie, merchant_code):
    merchant_info_list = select_table(
        'merchant',
        list_view = ['ID', 'MERCHANT_NAME', 'MERCHANT_CODE'],
        where_condition = "merchant_code = '%s'" %merchant_code
    )
    merchant_realtime_transfer_config_list = select_table(
        'MER_REALTIME_TRANSFER_CONFIG',
        list_view = ['ID', 'MER_SINGLE_LIMIT', 'MER_SINGLE_DAY_LIMIT', 'REQUEST_START_TIME', 'REQUEST_END_TIME'],
        where_condition = "merchant_code = '%s'" %merchant_code
    )
    mer_realtime_transfer_config_default = {
            'merchantId' : str(merchant_info_list[0][0]),
            'id': str(merchant_realtime_transfer_config_list[0][0]),
            'name': str(merchant_info_list[0][1]),
            'code': str(merchant_info_list[0][2]),
            'merSingleLimit': str(merchant_realtime_transfer_config_list[0][1]),
            'merSingleDayLimit': str(merchant_realtime_transfer_config_list[0][2]),
            'requestStartTime': str(merchant_realtime_transfer_config_list[0][3]),
            'requestEndTime': str(merchant_realtime_transfer_config_list[0][4])
        }
    mer_realtime_transfer_config_default.update(inputFormParam)
    mgmodifyActionList = ['/Admin/merchantManage/merchantManageAction_mgtoModifyMerchantRealtime',
                          '/Admin/merchantManage/merchantManageAction_mgmodifyMerchantRealtime']
    # getTokenParam = '?merchantId=' + mer_realtime_transfer_config_default.get('merchantId')
    getTokenParam = '?merchantId=%s&merName=%s'%(
        mer_realtime_transfer_config_default.get('merchantId'),
        mer_realtime_transfer_config_default.get('name')
    )
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
    allFormParam.update(mer_realtime_transfer_config_default)
    responseByPostForm = requests.post(const._global_configuration().OptionManagerHttpUrl + mgmodifyActionList[1],
                                       cookies=cookie,
                                       data = allFormParam)
    return responseByPostForm.text