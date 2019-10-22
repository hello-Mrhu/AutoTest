# -*- coding: utf-8 -*-
# description:RSA
import rsa
import base64

# 密文写入文件
def CypherWriter(CypherCodename):
    f = open('Cyphertext.txt', 'w')
    f.write(CypherCodename)
    f.close()

# 初始化
Code = 'Test1'
VerifyCode = 'Test1'

# 生成一对密钥并保存
(pubkey, privkey) = rsa.newkeys(2048)

pub = pubkey.save_pkcs1()
pubfile = open('public.pem', 'w+')
pubfile.write(pub)
pubfile.close()

pri = privkey.save_pkcs1()
prifile = open('private.pem', 'w+')
prifile.write(pri)
prifile.close()

# 载入公钥和密钥
message = Code
with open('public.pem') as publickfile:
    p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)

with open('private.pem') as privatefile:
    p = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)

# 用公钥加密，并用Base64编码后输出
crypto = rsa.encrypt(message, pubkey)
crypto64 = base64.b64encode(crypto)
CypherWriter(crypto64)
print('The cyphertext is :')
print(crypto64)

# 通过Base64解码，用私钥解密
crypto = base64.b64decode(crypto64)
message = rsa.decrypt(crypto, privkey)
print('The code is: ')
print(message)

# 签名 用私钥签名认证、再用公钥验证签名
signature = rsa.sign(message, privkey, 'SHA-1')
rsa.verify(VerifyCode, signature, pubkey)