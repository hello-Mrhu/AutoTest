
class _global_configuration(object):
    def __init__(self):
        self.__OracleConnectUri = 'tvpay2/tvpay@172.16.219.99/sumapay'
        self.__OptionManagerHttpUrl = 'http://172.16.9.3:9191'
        self.__MerchantHttpUrl = 'https://172.16.3.1/merchant/'
        self.__InvokeJarPath = 'D:/pycharm_workspace/venv/Lib/toolLib.jar'
        self.__InvokeJarDependencyPath =  'D:/pycharm_workspace/venv/Lib/'
        self.__OptionManagerOperator = {'userName': 'xjd', 'password': 'xjd12345'}
        self.__OptionManagerAuditor = {'userName': 'xjd1', 'password': 'xjd12345'}
        self.__MerchantAdmin = {'userName': 'Admin', 'merchantCode': 'CSSH', 'password': 'suma1234'}
        self.__MerchantAuditor = {'userName': 'Auditor', 'merchantCode': 'CSSH', 'password': 'suma1234'}

    @property
    def OracleConnectUri(self):
        return  self.__OracleConnectUri
    @property
    def OptionManagerHttpUrl(self):
        return  self.__OptionManagerHttpUrl
    @property
    def merchantHttpUrl(self):
        return self.__MerchantHttpUrl
    @property
    def invokeJarPath(self):
        return self.__InvokeJarPath
    @property
    def invokeJarDependencyPath(self):
        return self.__InvokeJarDependencyPath
    @property
    def optionManagerOperator(self):
        return self.__OptionManagerOperator
    @property
    def optionManagerAuditor(self):
        return self.__OptionManagerAuditor
    @property
    def merchantAdmin(self):
        return self.__MerchantAdmin
    @property
    def merchantAuditor(self):
        return self.__MerchantAuditor