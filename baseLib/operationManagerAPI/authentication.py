import requests
from baseLib.baseUtils import invokeJar
import re
from configuration import const
from baseLib.baseUtils.recorder import runningRecorder

#运营管理登录
@runningRecorder(desc='运营管理登录')
def login(usrDictionary):
    strUserName = usrDictionary.get('userName')
    strPassword = usrDictionary.get('password')
    loginActionList = ['/Admin/queryUserNameAction_srandNum',
                       '/Admin/j_spring_security_check',
                       '/Admin/terminalUserManage/terminalUserAction_toUserManage']
    getSrandNumResponse = requests.get(const._global_configuration().OptionManagerHttpUrl + loginActionList[0])
    responseCookies = getSrandNumResponse.cookies
    strSandNum = re.findall(r"%7B%27mcryptKey%27%3A%27(.+?)%27%7D",getSrandNumResponse.text)
    strEncodePassword = invokeJar.getEncodePassword(strSandNum[0], strPassword)

    securityCheckFormPara = {'phone':'',
                             'randomValidateId':'',
                             'sendFlag':'',
                             'userNameOld': strUserName,
                             'password': strEncodePassword,
                             'passwordtype': '1',
                             'j_username': strUserName,
                             'validate':'e',
                             'message':''}
    responseCookies.set('tvpay_login_name', strUserName)
    responseByPostForm = requests.post(const._global_configuration().OptionManagerHttpUrl + loginActionList[1],
                                       cookies = responseCookies,
                                       data = securityCheckFormPara,
                                       allow_redirects = False
                                       )
    # print(responseByPostForm.cookies)
    responseCookies.update(responseByPostForm.cookies)
    responseAfterLogin = requests.get(const._global_configuration().OptionManagerHttpUrl + loginActionList[2],
                                      cookies = responseCookies
                                      )
    if '终端用户列表' in responseAfterLogin.text :
        print(strUserName + '登录成功')
        return (True, responseCookies)
    else:
        print(strUserName + '登录失败')
        return (False, responseAfterLogin.text)
