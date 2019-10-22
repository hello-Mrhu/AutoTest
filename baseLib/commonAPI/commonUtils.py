# -*- coding:utf-8 -*-
#autor :huchengjiang
import hmac
import hashlib
import random
import time
import base64
from baseLib.baseUtils.recorder import runningRecorder
from pyDes import *
from binascii import b2a_hex, a2b_hex
####################设置Key值##############
def md5Signature(param,ekey, rule):
    to_enc = ''
    for i in rule:
        # to_enc = to_enc + param[i]
        # print(param.get(i))
        if param.get(i):
            to_enc += str(param[i])
        elif param.get(i) == '':
            pass
        else:
            raise RuntimeError('获取不到%s关键字'%i)
    enc_res = hmac.new(ekey.encode(), to_enc.encode(), hashlib.md5).hexdigest()
    return enc_res

def encodeDictionaryToGBK(dictionary):
    for key in dictionary:
        dictionary[key] = dictionary[key].encode('GBK')
    return dictionary

# def requestId():
#     randomNum = ''.join(str(i) for i in random.sample(range(0, 9), 6))
#     CurrentTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
#     return 'auto' + CurrentTime + randomNum

def requestId(num = 24):
    randomNum = ''.join(str(i) for i in random.sample(range(0, 9), num - 18))
    CurrentTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    return 'auto' + CurrentTime + randomNum

@runningRecorder(desc='执行挂起')
def waiting(sec):
    i = 0
    while  i < sec:
        print('waiting for %s sec' % (sec - i))
        time.sleep(1)
        i += 1

def encryptDes(str):
    Des_Key = b"fL2*0a_-"
    print(Des_Key)
    Des_IV = b"\x22\x33\x35\x81\xBC\x38\x5A\xE7"  # 自定IV向量（不知道什么用，官网例子就是这么写的）
    k = des(Des_Key, ECB, Des_IV, pad=None, padmode=PAD_PKCS5)
    encrystr = k.encrypt(str.encode())
    return base64.b64encode(encrystr).decode()
def decryptDes(encrystr):
    Des_Key = b"fL2*0a_-"
    Des_IV = b"\x22\x33\x35\x81\xBC\x38\x5A\xE7"  # 自定IV向量（不知道什么用，官网例子就是这么写的）
    k = des(Des_Key, ECB, Des_IV, pad=None, padmode=PAD_PKCS5)
    str = k.decrypt(base64.b64decode(encrystr))
    return str.decode()
# print('===========>', encryptDes('王娜'))
# print('===========>', decryptDes('IWnIh3As5mg='))

def encryptDesFromStrTofile(key, str, filename):
    m = hashlib.md5()
    m.update(key.encode('GBK'))
    bm = m.digest()
    Des_Key = bm[0:8]
    # print(Des_Key)
    # print(len(Des_Key))
    Des_IV = b"\x22\x33\x35\x81\xBC\x38\x5A\xE7"  # 自定IV向量（不知道什么用，官网例子就是这么写的）
    k = des(Des_Key, ECB, Des_IV, pad=None, padmode=PAD_PKCS5)
    encrystr = k.encrypt(str.encode('GBK'))
    # print(encrystr)
    # filename = 'programming.txt'
    with open(filename, 'wb') as file_object:
        file_object.write(encrystr)
        file_object.closed
    return encrystr

# batchFileContext = '''日期,,批次号,%s,明细数目,2,总金额(元),0.03,,
# ,,,,,,,,,
# 商户流水号,商户号,商户名称,金额(元),用途,,,
# 1,CSSH,测试商户,0.02,付款至丰付,,,
# 2,CSSH,测试商户,0.01,付款至丰付,,,
# '''

# batchFileContext = '日期,,批次号,%s,明细数目,2,总金额(元),0.03,,\n' \
#                    ',,,,,,,,,\n' \
#                    '商户流水号,商户号,商户名称,金额(元),用途,,,\n' \
#                    '1,CSSH,测试商户,0.02,付款至丰付,,,\n' \
#                    '2,CSSH,测试商户,0.01,付款至丰付,,,'
# print(batchFileContext)
# print(encryptDesFromStrTofile('CSSH123456',batchFileContext, 'programming.txt'))
