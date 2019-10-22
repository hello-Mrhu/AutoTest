import requests
from configuration import const
from baseLib.baseUtils.recorder import runningRecorder
import json
from baseLib.commonAPI import OracleQuery
from baseLib.commonAPI import commonUtils

@runningRecorder(desc='获取商户自助登录短信验证码')
def sendMerchantSMS(usrDictionary):
    sendMerchantSMSParam = {'operatorName': usrDictionary.get('userName'),
                        'merchantNo': usrDictionary.get('merchantCode'),
                        'mobilePhoneFlag': '1'}
    responseByPostForm = requests.post(const._global_configuration().merchantHttpUrl + 'Login_sendPhoneMessage',
                                       data = sendMerchantSMSParam,
                                       verify = False)
    dict = json.loads(responseByPostForm.text)
    if dict.get('dataMap').get('result') == 0:
        randomValidateId = dict.get('dataMap').get('randomValidateId')
        sql = "select t.random_code from sms_request t where t.random_id = '%s'"%randomValidateId
        randomCode = OracleQuery.sqlOne(sql)
        return (True, randomValidateId, commonUtils.decryptDes(randomCode[0]))
    else:
        return (False, responseByPostForm.text)

@runningRecorder(desc='商户自助登录')
def login(usrDictionary, smsTuple):
    loginParam = {'randomValidateId': smsTuple[1],
                  'sendFlag': '1',
                  'mobilePhoneFlag': '1',
                  'supportedPwdCtrl': '0',
                  'operatorName': usrDictionary.get('userName'),
                  'merchantNo': usrDictionary.get('merchantCode'),
                  'password': usrDictionary.get('password'),
                  'phoneRandomCode': smsTuple[2]}
    responseByPostForm = requests.post(const._global_configuration().merchantHttpUrl + 'Login_init',
                                       data=loginParam, verify=False)
    if responseByPostForm.text.find('商户自助 - -账户信息'):
        print(usrDictionary.get('userName') + '登录成功')
        return (True, responseByPostForm.cookies)
    else:
        print(usrDictionary.get('userName') + '登录失败')
        return (False, responseByPostForm.text)