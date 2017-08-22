import os

from selenium.common.exceptions import NoAlertPresentException
from bili_spider.db import pydb
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
from bili_spider.user_info import *


def if_404(browser):
    try:
        browser.switch_to.alert.accept()
        return True
    except NoAlertPresentException:
        return False


start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
driver = webdriver.Chrome(executable_path=r'./library/chromedriver.exe', desired_capabilities=DesiredCapabilities.CHROME, chrome_options=options)
driver.set_window_position(-10000, 0)
url = ("http://space.bilibili.com/", "/#!/index")
info_arr = pydb.get_fail_user()
for j in info_arr:
    i = j[0]
    data = {}
    extend_data = {}
    target = "{0}{1}{2}".format(url[0], str(i), url[1])
    print("try to search %s :" % target)
    driver.get(target)
    time.sleep(1.5)
    if if_404(driver):
        print("NO.%d 404 !" % i)
        continue

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
        data['name'] += '*'
        user_id = pydb.insert_user(data)
        pydb.insert_extend_user(user_id, extend_data)
        print("NO.%d Successfully !" % j)

pydb.close()
end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Spider start at %s , %d finished successfully at %s !" % (start_time, len(info_arr), end_time))
driver.quit()

# delete log
if os.path.exists('./tmp/lock.lock'):
    os.remove('./tmp/lock.lock')



