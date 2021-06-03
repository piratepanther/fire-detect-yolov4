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
            # browser.execute_script("location.reload()")
            browser.refresh()
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

        try:
            browser.find_element_by_xpath(
                '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/a[2]/div')

        except Exception as e:
            print(str(e))
            # browser.close()
            # browser.switch_to.window(windows[0])
            # print('see_more_page_download刷新失败，继续尝试！')
            print('download_google_images next_link_ not exit,继续下一个keyword！')
            return



        next_link_ = browser.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/a[2]/div')
        time.sleep(1)
        next_link_.click()
        time.sleep(2)
        print(str(i+2)+'th google see_more_link')
        see_more_page_download(browser, img_num_num, save_path)

    # img_link2 = browser.find_elements_by_xpath('//*[@id="headerButtons"]/div[2]')
    # //*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/a[2]/div
    # img_link2[0].click()

    return


def see_more_page_download(browser, img_num_num, save_path):
    socket.setdefaulttimeout(10)
    # 模拟浏览器headers，防止403forbidden
    # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
    opener = ur.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
    ur.install_opener(opener)
    try:
        see_more = browser.find_element_by_xpath(
            '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[3]/div[4]/c-wiz/div/div/div[1]/div[2]/a')

    except Exception as e:
        print(str(e))
        # browser.close()
        # browser.switch_to.window(windows[0])
        # print('see_more_page_download刷新失败，继续尝试！')
        print('see_more link not exit,退出继续！')
        return

    see_more_link = see_more.get_attribute("href")
    print('------------')
    print('see_more_link:'+see_more_link)
    # executor.executeScript("window.open('" + href + "')")
    browser.execute_script("window.open('" + see_more_link + "')")
    # see_more.click()
    # 切换窗口
    time.sleep(2)
    windows = browser.window_handles
    browser.switch_to.window(windows[-1])  # 切换到图像界面
    time.sleep(1)
    # browser.refresh()
    # browser.execute_script("location.reload()")


    try:
        img_link_ = browser.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
    except Exception as e:
        print(str(e))
        # browser.close()
        # browser.switch_to.window(windows[0])
        # print('see_more_page_download刷新失败，继续尝试！')
        print('img_link_ timeout,退出继续！')
        return

    img_link_.click()
    time.sleep(2)

    refresh_time=0

    while True:
        try:
            # browser.execute_script("location.reload()")
            browser.refresh()
            time.sleep(2)
            print('see_more_page_download刷新成功！')
            break
        except Exception as e:
            print(str(e))
            # browser.close()
            # browser.switch_to.window(windows[0])
            print('see_more_page_download刷新失败，继续尝试！')
            refresh_time=refresh_time+1
            if refresh_time==3:
                print('see_more_page_download 3 次刷新失败，退出继续！')
                # browser.close()
                # browser.switch_to.window(windows[0])
                return
            # print('see_more_page_download刷新失败，退出继续！')
            # return
            continue


    # 切换窗口
    # windows = browser.window_handles
    # browser.switch_to.window(windows[0])  # 切换到图像界面
    # time.sleep(random.random())
    # 设置默认timeout时间，防止卡死

    for i in range(img_num_num):
        print(i+1)
        # print(img_link_)
        try:
            # 查找图片链接
            img_link_final = browser.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img')
            time.sleep(random.random())

        except Exception as e:
            print(str(e))
            # browser.close()
            # browser.switch_to.window(windows[0])
            # print('see_more_page_download刷新失败，继续尝试！')
            print('see_more_page_download img_link_final not exit,继续该keyword的下一张图片！')
            return
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

        try:
            # 点击下一张图片
            browser.find_element_by_xpath(
                '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/a[2]/div').click()
            time.sleep(random.random())

        except Exception as e:
                    print(str(e))
                    # browser.close()
                    # browser.switch_to.window(windows[0])
                    # print('see_more_page_download刷新失败，继续尝试！')
                    print('see_more_page_download next_link_ not exit,继续该keyword的下一张图片！')
                    return

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
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    else:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

    chrome_driver = r'F:\chrome\chromedriver_win32\chromedriver.exe'  #chromedriver的文件位置
    # chrome_driver = webdriver.Chrome(r'J:\nvida\firedata\chromedriver.exe')



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
        browser = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)
        browser.maximize_window()

        try:
            browser.get(r'https://www.google.com.hk/imghp?hl=en&ogbl')
            time.sleep(1)
        except Exception as e:
            print(str(e))
            print('网络连接断开，请连接google！')
            browser.quit()
            return

        name = names[i]
        save_path = os.path.join(save_root, str(names[i]))  # 以索引作为文件夹名称
        send_param_to_google(name, browser)

        download_google_images(save_path=save_path, img_num=img_num[i][0], img_num_num=img_num[i][1],browser=browser)

        # browser.get(r'https://www.google.com.hk/imghp?hl=en&ogbl')
        time.sleep(1)
        browser.quit()
    # 全部关闭
    # browser.quit()
    return



if __name__=="__main__":

    # main(names=['施工人员穿反光衣', '反光衣',],\
    #      save_root=r'F:\Reflective_vests',\
    #      img_num=500)

    main(names=['森林火灾','山火'],\
         save_root=r'E:\navida\firedata\positive\google',\
         img_num=[[5,1], [5,1]],\
         continue_num=0,\
         is_open_chrome=False)
    # img_num[i][0]为第一次搜索到的图片，img_num[i][1]为Google联想seemore图片张数
    # kw：山火监测