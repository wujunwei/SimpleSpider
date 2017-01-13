
from bili_spider.db import pydb
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
from bili_spider.user_info import *

start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
driver = webdriver.PhantomJS(desired_capabilities=DesiredCapabilities.PHANTOMJS)
url = ("http://space.bilibili.com/", "/#!/index")
step = 5937
start = int(pydb.get_next_id())
j = 0
delay_seconds = 1.4
for i in range(start, start + step):
    j += 1
    data = {}
    extend_data = {}
    target = "{0}{1}{2}".format(url[0], str(i), url[1])
    print("try to search %s :" % target)
    driver.get(target)
    time.sleep(delay_seconds)
    tree = etree.HTML(driver.page_source)
    for key in user_config.keys():
        try:
            data[key] = tree.xpath(user_config[key]).pop()
        except IndexError as e:
            data[key] = ''
    data = deal_user_info(data)

    for key in extend_config.keys():
        try:
            extend_data[key] = tree.xpath(extend_config[key]).pop()
        except IndexError as e:
            extend_data[key] = ''
    extend_data = deal_user_info(extend_data)
    try:
        user_id = pydb.insert_user(data)
        pydb.insert_extend_user(user_id, extend_data)
        print("NO.%d Successfully !" % j)
    except Exception as e:
        print(e)
        exit()
    if j % 500 == 0:
        time.sleep(10)
end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Spider start at %s , All finished successfully at %s !" % (start_time, end_time))
driver.quit()

