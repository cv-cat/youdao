import json
import math
import re
import requests
import execjs
from time import time


js = execjs.compile(open('youdao.js', 'r', encoding='utf-8').read())
headers = {
    "Referer": "https://fanyi.youdao.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
}
session = requests.session()
index_url = 'https://fanyi.youdao.com/index.html'
js_url = 'https://fanyi.youdao.com/js/'
cookies_url = 'https://dict.youdao.com/login/acc/query/accountinfo'
sign_key_url = 'https://dict.youdao.com/webtranslate/key?keyid=webfanyi-key-getter&client=fanyideskweb&product=webfanyi&appVersion=1.0.0&vendor=web&pointParam=client,mysticTime,product&keyfrom=fanyi.web'
url = "https://dict.youdao.com/webtranslate"
data = {
    "i": "buses",
    "from": "auto",
    "to": "",
    "domain": "0",
    "dictResult": "true",
    "keyid": "webfanyi",
    "sign": "",
    "client": "fanyideskweb",
    "product": "webfanyi",
    "appVersion": "1.0.0",
    "vendor": "web",
    "pointParam": "client,mysticTime,product",
    "mysticTime": '',
    "keyfrom": "fanyi.web"
}
params = {
    "keyid": "webfanyi-key-getter",
    "sign": "",
    "client": "fanyideskweb",
    "product": "webfanyi",
    "appVersion": "1.0.0",
    "vendor": "web",
    "pointParam": "client,mysticTime,product",
    "mysticTime": "",
    "keyfrom": "fanyi.web"
}
# 获取js文件名
response = requests.get(index_url, headers=headers)
js_name = 'app.' + re.findall(r'<script src="js/app.(.*?).js">', response.text)[0] + '.js'
response = requests.get(js_url + js_name, headers=headers)
decodeKey = re.findall(r'dictResult:\{},decodeKey:"(.*?)",decodeIv:', response.text)[0]
decodeIv = re.findall(r'dictResult:\{},decodeKey:".*?",decodeIv:"(.*?)"', response.text)[0]
first_sign = re.findall(r'const o="webfanyi-key-getter",a="(.*?)"', response.text)[0]
# 获取 OUTFOX_SEARCH_USER_ID
response = requests.get(cookies_url, headers=headers)
OUTFOX_SEARCH_USER_ID = '='.join(response.cookies.items()[0])
# 获取 OUTFOX_SEARCH_USER_ID_NCOO
cookies = js.call('get_cookies') + ';' + OUTFOX_SEARCH_USER_ID
cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies.split(';') if i.split('=')[0].find('USER_ID') != -1}
session.cookies.update(cookies)
# 获取sign_key
mysticTime = str(math.floor(time() * 1000))
sign = js.call('get_sign', mysticTime, first_sign)
params['sign'] = sign
params['mysticTime'] = mysticTime
response = session.get(sign_key_url, headers=headers, params=params)
key_sign = response.json()['data']['secretKey']

def translate(word):
    mysticTime = str(math.floor(time() * 1000))
    data['i'] = word
    data['mysticTime'] = mysticTime
    sign = js.call('get_sign', mysticTime, key_sign)
    data['sign'] = sign
    response = session.post(url, headers=headers, data=data)
    result = js.call('decode_code', decodeKey, decodeIv, response.text)
    return json.loads(result)

while True:
    word = input('请输入要翻译的单词：q退出\n')
    if word == 'q':
        break
    result = translate(word)
    print(result['translateResult'][0][0]['tgt'])