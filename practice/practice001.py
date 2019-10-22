import time
import random
import os
from pyDes import *
import base64

#冒泡排序

# list1 = {5,2,78,4,7}
# for i in range(len(list1)):
#     for j in range(0,len(list1) - i -1):
#         if list1[j] > list1[j + 1]:
#             tmp = list1[j]
#             list1[j] = list1[j + 1]
#             list1[j + 1] = tmp
# print(list1)

'''
arr = {5,2,78,4,7}
n = len(arr)
# 遍历所有数组元素
for i in range(n):

    # Last i elements are already in place
    for j in range(0, n - i - 1):

        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
'''
#os使用使用
print(os.getcwd())
path = os.path.dirname(os.path.dirname(__file__))
report_path = os.path.join(path,'report')
print(report_path)
print(dir(str))


#random
print(random.randint(0,100))


#time时间戳
print(time.localtime())
s = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
print(s)


#字符串拼接与分割
str1 = ['1','2','3','4']

str2 = '_ '.join(str1)
print(str2)

str3 = 'a_b_c_d'
str4 = str3.split('_')
print(str4)


#字典
dict1 = {'name':'wangsan','age':'15'}
print(dict1.get('name'))

for key,vlaue in dict1.items():
    print(key , ':' , vlaue)

dict2 = {'sex':'1','name':'wanger'}
dict1.update(dict2)
print(dict1)


#装饰器
def BBB(func):
    def inner():
        print("出版社")
        func()
    return inner
@BBB
def AAA():
    print("hello world")

AAA()

def login(func):
    def inner(token):
        if token == '123456':
            print("恭喜你登陆成功")
            func(token)
        else:
            print("账号密码错误错误")

    return inner

@login
def info(token):
    return "欢迎来到首页"

info('1234567')

#动态参数
# def func(*args,**kwargs)

#map函数
def fn(a):
    return a + 100

list1 = {1, 2, 3, 4}
print(list(map(fn,list1)))


def encryptDes(str):
    Des_Key = b"fL2*0a_-"
    print(Des_Key)
    Des_IV = b"\x22\x33\x35\x81\xBC\x38\x5A\xE7"  # 自定IV向量（不知道什么用，官网例子就是这么写的）
    k = des(Des_Key, ECB, Des_IV, pad=None, padmode=PAD_PKCS5)
    encrystr = k.encrypt(str.encode())
    return base64.b64encode(encrystr).decode()

str1 = "胡承江"
str2 = encryptDes(str1)
print(str2)












