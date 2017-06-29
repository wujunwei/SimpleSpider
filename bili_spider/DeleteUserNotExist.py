import os

import time

from bili_spider.db import pydb

path = r'./tmp/'
file_name = 'lock.lock'
if not os.path.exists(path):
    os.makedirs(path)
    print('operator locked  \r\nplease run FixFailedDownloader.py first')
    exit()
if os.path.exists(path + file_name):
    print('operator locked  \r\nplease run FixFailedDownloader.py first')
    exit()
limit = pydb.get_fail_user()
if len(limit) > 50:
    print("please check the num of 404 people")
    exit()
num = pydb.delete_fail_user()
print('delete %d rows' % num)

with open(path + file_name, 'a+') as file:
    file.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' delete %d rows' % num)
