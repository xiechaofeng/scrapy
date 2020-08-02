import base64
import hmac
import json
import re
from hashlib import sha1

import requests
import time
from PIL import Image
from bs4 import BeautifulSoup

#import Properties 


def get_identifying_code(headers):
    '''
      判断页面是否需要填写验证码
      如果需要填写则弹出验证码，进行手动填写
      请求验证码的url 后的参数lang=en，意思是取得英文验证码
    '''
    response = session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers)
    # {"show_captcha":false} 表示不用验证码
    r = re.findall('"show_captcha":(\w+)', response.text)
    if r[0] == 'false':
        return ''
    else:
        response = session.put('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers)
        show_captcha = json.loads(response.text)['img_base64']
        with open('captcha.jpg', 'wb') as f:
            f.write(base64.b64decode(show_captcha))
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
        captcha = input('输入验证码:')
        session.post('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers,
                     data={"input_text": captcha})
        return captcha


def get_signature(grantType, clientId, source, timestamp):
    ''' 处理签名 '''

    hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', None, sha1)
    hm.update(str.encode(grantType))
    hm.update(str.encode(clientId))
    hm.update(str.encode(source))
    hm.update(str.encode(timestamp))

    return str(hm.hexdigest())


def login(username, password, session, headers):
    ''' 处理登录 ,先用浏览器F12查看他要什么参数'''

    # https://www.zhihu.com 尝试出来的，只有去请求这个才能得到_xsrf d_c0 具体什么原因，我也不清楚。。。
    resp1 = session.get('https://www.zhihu.com', headers=headers)  # 拿cookie:_xsrf
    # print(resp1.cookies['_xsrf'])
    _xsrf = resp1.cookies['_xsrf']
    d_c0 = resp1.cookies['d_c0']
    x_udid = d_c0.split("|")[0].lstrip("\"")  # 获取 x_udid
    print(x_udid)
    headers.update({  # 更新请求头，知乎防反爬真的很厉害。
        "X-Xsrftoken": _xsrf,
        "X-UDID": x_udid,
        "X-ZSE-83": '3_1.1',
        "x-requested-with": "fetch"
    })

    grantType = '171200xcf'
    clientId = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    t = time.time() * 1000
    print(t)
    timestamp = str(t).split('.')[0]  # 签名只按这个时间戳变化

    # captcha_content = session.get('https://www.zhihu.com/captcha.gif?r=%d&type=login' % t,
    #                               headers=headers).content  # 验证码
    captcha = get_identifying_code(headers)
    data = {
        "client_id": clientId,
        "grant_type": grantType,
        "timestamp": timestamp,
        "source": source,
        "signature": get_signature(grantType, clientId, source, timestamp),  # 获取签名
        "username": username,
        "password": password,
        #"lang": "en",
        "captcha": captcha  # oncaptcha(captcha_content, need_cap)  # 获取图片验证码
        # "ref_source": "other_",
        # "utm_source": ""
    }

    print("**2**: " + str(data))
    print("-" * 50)
    # session.post('https://www.zhihu.com/api/v3/oauth/sign_in', data, headers=headers).content
    resp = session.post('https://www.zhihu.com/api/v3/oauth/sign_in', data, headers=headers).content
    print(BeautifulSoup(resp, 'html.parser'))

    print("-" * 50)
    # return resp


if __name__ == "__main__":
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        # 'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        # "Referer": "https://www.zhihu.com/",
        # "Host": "www.zhihu.com"
    }
    # print(session.headers)   #'User-Agent': 'python-requests/2.20.0'
    # prp = Properties.parse("D:\project\spider_demo\my_spider\AccAndPwd")  创建读取Properties文件的实例
    # account = prp.get('account')
    # password = prp.get('password')
    login('2657459083@qq.com','171200xcf', session, headers)  # 用户名密码换自己的就好了，我这里引用的是一个自己写的加载properties类，用来提取账号密码

    resp = session.get('https://www.zhihu.com/people/edit', headers=headers)  # 登录进去了，可以看个人信息页面了
    print(BeautifulSoup(resp.content, 'html.parser'))