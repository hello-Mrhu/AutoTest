#encoding:utf-8


import requests
import json


url = 'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=20198311401'

data = {"email":"15010869212",
        "icode":"",
        "origURL":"http://www.renren.com/home",
        "domain":"renren.com",
        "key_id":"1",
        "captcha_type":"web_login",
        "password":"31b3a88b68ee820185785661ede3fe84def0069150536c5a30358444e06f5676",
        "rkey":"91cf3a17836ab652544e044c85f155a9",
        "f":"http%3A%2F%2Fwww.renren.com%2F972329422%2Fnewsfeed%2Fphoto"
        }
headers = {"Content-Type":"application/x-www-form-urlencoded",
           "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
           "Referer":"http://www.renren.com/SysHome.do"
            }

r = requests.post(url,data=data,headers = headers)

print(r.text)

dict = json.loads(r.text)
