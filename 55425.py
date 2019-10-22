# -*- coding:utf-8 -*-
#autor :huchengjiang
from pyDes import *
import base64

def encryptDes(str):
    Des_Key = b"fL2*0a_-"
    print(Des_Key)
    Des_IV = b"\x22\x33\x35\x81\xBC\x38\x5A\xE7"  # 自定IV向量（不知道什么用，官网例子就是这么写的）
    k = des(Des_Key, ECB, Des_IV, pad=None, padmode=PAD_PKCS5)
    encrystr = k.encrypt(str.encode())
    return base64.b64encode(encrystr).decode()

str='胡承江'
a=encryptDes(str)
print(a)



