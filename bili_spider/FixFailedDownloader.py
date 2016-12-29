
from bili_spider.db import pydb
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
from bili_spider.user_info import *

start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
driver = webdriver.PhantomJS(desired_capabilities=DesiredCapabilities.PHANTOMJS)
url = ("http://space.bilibili.com/", "/#!/index")
last_id = 19268
info_arr = pydb.get_fail_user(last_id)
for j in info_arr:
    i = j[0]
    data = {}
    extend_data = {}
    target = "{0}{1}{2}".format(url[0], str(i), url[1])
    print("try to search %s :" % target)
    driver.get(target)
    time.sleep(1.4)
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
        pydb.update_user(i, data)
        pydb.update_extend_user(i, extend_data)
        print("NO.%d Successfully !" % i)
    except Exception as e:
        print(e)
        exit()
pydb.close()
end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Spider start at %s , All finished successfully at %s !" % (start_time, end_time))
driver.quit()

