import json
import os
import sqlite3
from win32crypt import CryptUnprotectData
import time
import requests

from bili_spider.db import pydb

from bili_spider.user_info import *


def get_cookie_from_chrome(host='.bilibili.com'):
    cookie_path = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookie_path) as conn:
        cu = conn.cursor()
        cookies = {name: CryptUnprotectData(encrypted_value)[1].decode() for host_key, name, encrypted_value in
                   cu.execute(sql).fetchall()}
        return cookies


# 运行环境windows10 python3.5 x64 chrome 50

def get_info(id):
    url = 'http://space.bilibili.com/ajax/member/GetInfo'
    httphead = {'Referer': 'http://space.bilibili.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/50.0.2661.102 Safari/537.36 '
                }
    data = {'mid': id, '_': int(time.time() * 1000)}
    try:
        r = requests.post(url, data=data, headers=httphead, cookies=get_cookie_from_chrome('.bilibili.com'),
                          allow_redirects=1)
        decode_json = json.loads(r.text)
        return decode_json['data']
    except Exception as err:
        print(err)
        return None


start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
step = 1000
start = int(pydb.get_next_id())
j = 0

for i in range(start, start + step):
    j += 1
    res = get_info(i)
    data, extend_data = deal_api_data(res)

    if extend_data == {} or data == {}:
        print("NO.%d 404 !" % i)
        continue
    data['id'] = i
    extend_data['user_id'] = i
    print(data, extend_data)
    try:
        user_id = pydb.insert_user(data)
        pydb.insert_extend_user(user_id, extend_data)
        print("NO.%d Successfully !" % i)
    except Exception as e:
        print(e)
        data['name'] += '*'
        user_id = pydb.insert_user(data)
        pydb.insert_extend_user(user_id, extend_data)
        print("NO.%d Successfully !" % j)

    if j > 50 and i < start + step:
        j = 0
        time.sleep(10)
    else:
        time.sleep(0.2)
end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Spider start at %s , All finished successfully at %s !" % (start_time, end_time))
pydb.close()
