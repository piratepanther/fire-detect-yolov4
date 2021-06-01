'''
注释：
    @author is CC
    google图片爬虫，采用selenium模拟鼠标点击形式
    1. 将要搜索的文本表示成list
    2. 打开google图片官网，输入文本，搜索
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
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 键盘类
from crawl import base64_image_download_to_local

def send_param_to_google(name, browser):
    '''
    :param name:    str
    :param browser: webdriver.Chrome 实际应该是全局变量的
    :return:        将要输入的 关键字 输入google图片
    '''
    # 采用id进行xpath选择，id一般唯一
    inputs = browser.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
    inputs.clear()
    inputs.send_keys(name)
    time.sleep(1)
    inputs.send_keys(Keys.ENTER)
    time.sleep(2)
    print(name+' send_param_to_google successful!')

    return

def download_google_images(save_path, img_num, img_num_num, browser):
    ''' 此函数应在
    :param save_path: 下载路径 str
    :param img_num:   下载图片数量 int
    :param browser:   webdriver.Chrome
    :return:
    '''
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    img_link = browser.find_elements_by_xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')

    img_link[0].click()

    while True:
        try:
            browser.execute_script("location.reload()")
            time.sleep(1)
            print('download_google_images刷新成功！')
            break
        except Exception as e:
            print(str(e))
            print('download_google_images刷新失败，继续尝试！')
            continue
    # browser.execute_script("location.reload()")
    # time.sleep(1)
    # print(browser.execute_script("location.reload()"))
    # print(type(browser.execute_script("location.reload()")))

    see_more_page_download(browser, img_num_num, save_path)

    for i in range(img_num-1):

        next_link_ = browser.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/a[2]/div')
        next_link_.click()
        time.sleep(1)
        print(str(i+1)+'th google see_more_link')
        see_more_page_download(browser, img_num_num, save_path)

    # img_link2 = browser.find_elements_by_xpath('//*[@id="headerButtons"]/div[2]')
    # //*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/a[2]/div
    # img_link2[0].click()

    return


def see_more_page_download(browser, img_num_num, save_path):
    see_more = browser.find_element_by_xpath(
        '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[3]/div[4]/c-wiz/div/div/div[1]/div[2]/a')
    see_more_link = see_more.get_attribute("href")
    print('------------')
    print(see_more_link)
    # executor.executeScript("window.open('" + href + "')")
    browser.execute_script("window.open('" + see_more_link + "')")
    # see_more.click()
    # 切换窗口
    time.sleep(1)
    windows = browser.window_handles
    browser.switch_to.window(windows[1])  # 切换到图像界面
    time.sleep(random.random())
    # browser.refresh()
    # browser.execute_script("location.reload()")
    img_link_ = browser.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
    img_link_.click()

    while True:
        try:
            browser.execute_script("location.reload()")
            time.sleep(1)
            print('see_more_page_download刷新成功！')
            break
        except Exception as e:
            print(str(e))
            print('see_more_page_download刷新失败，继续尝试！')
            continue


    # 切换窗口
    # windows = browser.window_handles
    # browser.switch_to.window(windows[0])  # 切换到图像界面
    time.sleep(random.random())
    # 设置默认timeout时间，防止卡死
    socket.setdefaulttimeout(5)
    for i in range(img_num_num):
        print(i)
        # 模拟浏览器headers，防止403forbidden
        # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
        opener = ur.build_opener()
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
        ur.install_opener(opener)


        img_link_final = browser.find_element_by_xpath(
            '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img')
        # print(img_link_)

        # //div[@class="imgContainer"]/img[1]
        # // *[ @ id = "currentImg"]
        # //*[@id="mainImageWindow"]/div[1]/div/div/div/img
        # //*[@id="mainImageWindow"]/div[1]/div/div/div/img
        # //*[@id="mainImageWindow"]/div[2]/div[1]/div/div/img
        # /html/body/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div/img
        # /html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/div/div/div/div/img
        # //*[@id="mainImageWindow"]/div[1]/div/div/div/img
        # //*[@id="mainImageWindow"]/div[1]/div/div/div/img
        # / html / body / div[1] / div[2] / div / div[1] / div / img
        # // *[ @ id = "mainImageWindow"] / div[1] / div / div / div / img
        src_link = img_link_final.get_attribute('src')
        print(src_link)
        # 保存图片，使用urlib
        img_name = uuid.uuid4()

        # data:image/jpeg;base64,/9j/4AAQSkZJRgABA

        str_base64 = 'base64'
        src_link_split = src_link.split(",")

        try:
            # req = ur.Request(src_link, headers=headers)
            # data = ur.urlopen(req).read()
            # path=os.path.join(save_path, str(img_name) + '.jpg'
            # with open(path, 'wb') as f:
            #     f.write(data)
            #     f.close()

            if str_base64 in src_link_split[0]:
                src_link = src_link_split[-1]
                base64_image_download_to_local.base64_image_download_to_local(src_link,save_path,img_name)
                time.sleep(random.random())
            else:
                ur.urlretrieve(src_link, os.path.join(save_path, str(img_name) + '.jpg'))
                time.sleep(random.random())

        except Exception as e:
            print(str(e))
        # "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
        # browser.refresh()

        # 点击下一张图片
        browser.find_element_by_xpath(
            '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/a[2]/div').click()
        time.sleep(random.random())
    # 关闭当前窗口，并选择之前的窗口
    browser.close()
    browser.switch_to.window(windows[0])


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
    browser.get(r'https://www.google.com.hk/imghp?hl=en&ogbl')
    time.sleep(1)

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
        send_param_to_google(name, browser)

        download_google_images(save_path=save_path, img_num=img_num[i][0], img_num_num=img_num[i][1],browser=browser)

        browser.get(r'https://www.google.com.hk/imghp?hl=en&ogbl')
        time.sleep(1)
    # 全部关闭
    browser.quit()
    return



if __name__=="__main__":

    # main(names=['施工人员穿反光衣', '反光衣',],\
    #      save_root=r'F:\Reflective_vests',\
    #      img_num=500)

    main(names=['森林火灾','山火'],\
         save_root=r'E:\navida\firedata\positive\google',\
         img_num=[[100,50], [100,50]],\
         continue_num=0,\
         is_open_chrome=False)
    # img_num[i][0]为第一次搜索到的图片，img_num[i][1]为Google联想seemore图片张数
    # kw：山火监测