'''
注释：
    @author is leilei
    百度图片爬虫，采用selenium模拟鼠标点击形式
    1. 将要搜索的文本表示成list
    2. 打开百度图片官网，输入文本，搜索
    3. 逐条下载对应的图片
注：
    本代码支持断点续爬！
'''

import os
import uuid
import time
import random
import urllib
import urllib.request as ur
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 键盘类

def send_param_to_baidu(name, browser):
    '''
    :param name:    str
    :param browser: webdriver.Chrome 实际应该是全局变量的
    :return:        将要输入的 关键字 输入百度图片
    '''
    # 采用id进行xpath选择，id一般唯一
    inputs = browser.find_element_by_xpath('//input[@id="kw"]')
    inputs.clear()
    inputs.send_keys(name)
    time.sleep(1)
    inputs.send_keys(Keys.ENTER)
    time.sleep(1)

    return

def download_baidu_images(save_path, img_num, browser):
    ''' 此函数应在
    :param save_path: 下载路径 str
    :param img_num:   下载图片数量 int
    :param browser:   webdriver.Chrome
    :return:
    '''
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    img_link = browser.find_elements_by_xpath('//li/div[@class="imgbox"]/a/img[@class="main_img img-hover"]')
    # img_link = browser.find_elements_by_xpath('//li/div[@class="imgbox"]/a/img[@class="main_img img-hover"]')
    img_link[2].click()
    # 切换窗口
    windows = browser.window_handles
    browser.switch_to.window(windows[-1])  # 切换到图像界面
    time.sleep(random.random())

    for i in range(img_num):
        img_link_ = browser.find_element_by_xpath('//div/img[@class="currentImg"]')
        # print(img_link_)
        # img_link_ = browser.find_element_by_xpath('//*[@id="currentImg"]')
        # //*[@id="currentImg"]
        src_link = img_link_.get_attribute('src')
        print(src_link)
        # 保存图片，使用urlib
        img_name = uuid.uuid4()
        ur.urlretrieve(src_link, os.path.join(save_path, str(img_name) + '.jpg'))
        # 关闭图像界面，并切换到外观界面
        time.sleep(random.random())

        # 点击下一张图片
        browser.find_element_by_xpath('//span[@class="img-next"]').click()
        time.sleep(random.random())

    # 关闭当前窗口，并选择之前的窗口
    browser.close()
    browser.switch_to.window(windows[0])

    return

def main(names, save_root, img_num=[1000,], continue_num=0, is_open_chrome=False):
    '''
    :param names: list str
    :param save_root: str
    :param img_num: int list or int
    :param continue_num: int 断点续爬开始索引
    :param is_open_chrome: 爬虫是否打开浏览器爬取图像 bool default=False
    :return:
    '''
    options = webdriver.ChromeOptions()
    # 设置是否打开浏览器
    if not is_open_chrome:
        options.add_argument('--headless')  # 不打开浏览器
    else:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

    chrome_driver = r'F:\chrome\chromedriver_win32\chromedriver.exe'  #chromedriver的文件位置
    # chrome_driver = webdriver.Chrome(r'J:\nvida\firedata\chromedriver.exe')

    browser = webdriver.Chrome(chrome_options=options,executable_path = chrome_driver)
    browser.maximize_window()
    browser.get(r'https://image.baidu.com/')
    time.sleep(random.random())

    assert type(names) == list, "names参数必须是字符串列表"
    assert continue_num <= len(names), "中断续爬点需要小于爬虫任务数量"

    if type(img_num) == int:
        img_num = [img_num] * len(names)
        print(img_num)
    elif type(img_num) == list:
        print(img_num)
    else:
        print("None, img_num 必须是int list or int")
        return

    for i in range(continue_num, len(names)):
        name = names[i]
        save_path = os.path.join(save_root, str(names[i]))  # 以索引作为文件夹名称
        send_param_to_baidu(name, browser)
        download_baidu_images(save_path=save_path, img_num=img_num[i], browser=browser)
    # 全部关闭
    browser.quit()
    return



if __name__=="__main__":

    # main(names=['施工人员穿反光衣', '反光衣',],\
    #      save_root=r'F:\Reflective_vests',\
    #      img_num=500)

    # names = ['丛林大火', '森林火灾', '森林烟雾', '山火', '林火'],
    main(names=['丛林大火', '山火','森林烟雾', '山火', '林火'],\
         save_root=r'E:\navida\firedata\positive\baidu',\
         img_num=[100, 100,100,100,100],\
         continue_num=0, \
         is_open_chrome=False)
         # is_open_chrome=False)
    # bing国际版
    # 西班牙语：Incendios forestales 俄语： Лесные пожары 
    # 阿拉伯语： حرائق الغابات 波兰语：pożar lasu
    # 保加利亚语：горски пожар 波斯语：آتش جنگل
    # 德语：Waldbrand 法语：Feux de forêt
    # 韩语：삼림 화재 荷兰语：bosbrand
    # 马来语：api hutan 挪威语：Skogbrann
    # 葡萄牙语：Incêndio Florestal 日语：森林火災
    # 瑞典语：Brand i skogen 英语：forest fire
    # 泰语：ไฟป่า 意大利语：Incendio della foresta
    # 印度语：जंगल की आग

    # google：点击图片查看相似，选择see more