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
service_args = ['--load-images=no', '--disk-cache=yes', '--ignore-ssl-errors=true']
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(executable_path=r'./library/chromedriver.exe', desired_capabilities=DesiredCapabilities.CHROME, service_args=service_args)
driver.set_window_position(-10000, 0)
url = ("http://space.bilibili.com/", "/#!/index")
step = 5000
start = int(pydb.get_next_id())
delay_seconds = 0.7
j = 0
for i in range(start, start + step):
    j += 1
    target = "{0}{1}{2}".format(url[0], str(i), url[1])
    print("try to search %s :" % target)
    driver.get(target)
    time.sleep(0.5)
    if if_404(driver):
        print("NO.%d 404 !" % i)
    else:
        data = {}
        extend_data = {}
        time.sleep(delay_seconds)
        if if_404(driver):  # 防止网络延迟
            print("NO.%d 404 !" % i)
            continue
        tree = etree.HTML(driver.page_source)
        for key in user_config.keys():
            try:
                data[key] = tree.xpath(user_config[key]).pop()
            except IndexError as e:
                data[key] = ''
        data = deal_user_info(data)
        data['id'] = i

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
            data['name'] += '*'

            user_id = pydb.insert_user(data)
            pydb.insert_extend_user(user_id, extend_data)
            print("NO.%d Successfully !" % j)

end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Spider start at %s , All finished successfully at %s !" % (start_time, end_time))
driver.quit()
