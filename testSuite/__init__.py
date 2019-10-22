from ftplib import FTP
from baseLib.commonAPI import OracleQuery

__all__ = [
    'merchant_info_default',
    'ftp_connect'
]

merchant_info_default = {
    'id': '104',
    'oldfld9': '0',
    'oldisd': '',
    'selectBizs': '',
    'flag': '1',
    'name': '测试商户',
    'code': 'CSSH',
    'address': '',
    'owner': '张三',
    'manager': '张三',
    'telphone': '13013579246',
    'addressCode': '100085',
    'permitId': '123456',
    'signType': '0',
    'merKey': 'CSSH_KEY',
    'fld7': '0',
    'fld8': '数码视讯',
    'serviceTelphone': '',
    'fld9': '0',
    'isSameCard': '0',
    'fld10': '1',
    'fld13': '0',
    'fld16': '0'#0手工审核 1实时自动
}

def ftp_connect(remote_ip, remote_path, username, password):
    ftp = FTP()
    ftp.connect(remote_ip)
    ftp.login(username, password)
    ftp.cwd(remote_path)
    return ftp

