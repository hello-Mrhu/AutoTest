#coding:utf-8

class Excelvariable:
    caseid = 0
    url = 2
    request_data = 3
    expect = 4
    result = 5

def getcaseid():
    return Excelvariable.caseid

def geturl():
    return Excelvariable.url

def getequest_data():
    return Excelvariable.request_data

def getexpect():
    return Excelvariable.expect

def getresult():
    return Excelvariable.result