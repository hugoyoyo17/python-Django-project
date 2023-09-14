import re
import time

from django.utils import timezone
from lxml import etree
import requests

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import pymysql
from datetime import datetime



class LangLangSpider:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.url = 'https://www.ntpsa.org.tw/adoption?t=0'
        self.db = pymysql.connect(host='localhost',user='root',password='a123456',database='miumiushop',charset='utf8')
        self.cursor = self.db.cursor()
        self.insert = 'insert into langlang_info(name,gender,age,ligation,be_helped,created_time,updated_time,image) values(%s,%s,%s,%s,%s,%s,%s,%s)'


    def parse_html(self):
        elements = self.browser.find_elements(By.XPATH,'//*[@id="BOX1"]/div/div/a/div')
        result = []
        # 寵物名稱：小米
        # 寵物性別：女生
        # 寵物年齡：
        # 結紮與否：是
        # 助養人數：46人
        # n=1
        for ele in elements:
            style_img = ele.get_attribute('style')
            # print(style_img,type(style_img))
            r = r'background-image: url\("(.*?)"\)'
            img_url = re.findall(r,style_img)[0]
            # print(img_url)

            ActionChains(self.browser).move_to_element(ele).perform()
            info = ele.find_element(By.XPATH,'./div')
            # print(info.text)
            data = info.text.split('\n')
            name = data[0].split('：')[1].strip()
            gender = data[1].split('：')[1].strip()
            age = data[2].split('：')[1].strip()
            ligation = True if data[3].split('：')[1] == '是' else False
            be_helped = data[4].split('：')[1].strip()

            item = [name,gender,age,ligation,be_helped,datetime.now(),datetime.now(),img_url]
            # print(item)
            time.sleep(2)
            result.append(item)
            # n+=1
        return result
        # time.sleep(2)
        # self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        # ele = self.browser.find_element(By.XPATH,'//*[@id="BOX1"]/div[35]/div/a/div')
        # ActionChains(self.browser).move_to_element(ele).perform()
        # time.sleep(300)
        # print(len(elements))
        # for element in elements:
        #     print('elements:',element.text)

    def save_data(self,r_list):
        for r in r_list:
            # ['淡水鐵弟', '男生', '5歲以上', True, '34人']
            # print(r)
            try:
                self.cursor.execute(self.insert,r)
                self.db.commit()
            except Exception as e:
                print(e)
                self.db.rollback()
        print('爬取完畢')


    def run(self):
        self.browser.get(self.url)
        time.sleep(10)
        r_list = self.parse_html()
        self.save_data(r_list)


class LangSpiderHref:
    """
    獲取各個浪浪的個別網址
    :return 返回浪浪個別資訊所對應的網址
    """
    def __init__(self):
        self.url = 'https://www.ntpsa.org.tw/adoption?t=0'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=self.options)
    def get_element_html(self):
        r_list = self.browser.find_elements(By.XPATH,'//*[@id="BOX1"]/div/div/a')
        result = []
        for r in r_list:
            href = r.get_attribute('href')
            print(href)
            result.append(href)
        return result


    def run(self):
        self.browser.get(self.url)
        time.sleep(5)
        result = self.get_element_html()
        self.browser.quit()
        return result

class LangInfoSpider:
    """
    獲取每個浪浪的所有資料 並存入mysql中
    """
    def __init__(self,r_list):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=self.options)
        self.r_list = r_list
        self.db = pymysql.connect(host='localhost', user='root', password='a123456', database='miumiushop',
                                  charset='utf8')
        self.cursor = self.db.cursor()
        self.insert = 'insert into langlang_info(src,name,gender,age,ligation,vaccination,deworming,personality,be_helped,introduction,image,created_time,updated_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    def get_html(self):
        info_list = []
        for url in self.r_list:
            self.browser.get(str(url))
            time.sleep(5)
            try:
                ele = self.browser.find_element(By.XPATH,'/html/body/app-root/app-tw/app-adoption-d/div[3]/div/div[4]/div[1]/img')
            except Exception:
                print('有空數據')
                continue
            # print(ele)
            img_url = ele.get_attribute('src')
            info = self.browser.find_element(By.XPATH,'/html/body/app-root/app-tw/app-adoption-d/div[3]/div/div[4]/div[2]')
            # 寵物名稱：媽祖婆
            # 寵物性別：女生
            # 寵物年齡：至少7 - 8
            # 歲
            # 結紮與否：是
            # 預防針：已施打完畢
            # 體內外寄生蟲：已驅蟲完畢
            # 個性簡介：
            # 助養人數：87人
            src = str(url)
            data = info.text.split('\n')
            name = data[0].split('：')[1].strip()
            gender = data[1].split('：')[1].strip()
            age = data[2].split('：')[1].strip()
            ligation = True if data[3].split('：')[1] == '是' else False
            vaccination = data[4].split('：')[1].strip()
            deworming = data[5].split('：')[1].strip()
            personality = data[6].split('：')[1].strip()
            be_helped = data[7].split('：')[1].strip()
            introduction = self.browser.find_element(By.XPATH,'/html/body/app-root/app-tw/app-adoption-d/div[3]/div/div[4]/div[3]').text
            # timezone.now()帶時區的時間 使用這個就可以把setting中的USE_TZ = False 改為True
            total_info = [src,name,gender,age,ligation,vaccination,deworming,personality,be_helped,introduction,img_url,datetime.now(),datetime.now()]
            print(total_info)
            info_list.append(total_info)
            time.sleep(2)
        return info_list

    def save_data(self,info_list):
        for info in info_list:
            try:
                self.cursor.execute(self.insert,info)
                self.db.commit()
            except Exception as e:
                print(e)
                self.db.rollback()
        print('爬取完畢')
        self.browser.quit()

    def run(self):
        info_list = self.get_html()
        self.save_data(info_list)
        self.cursor.close()
        self.db.close()



if __name__ == '__main__':

    # lan = LangLangSpider()
    # lan.run()

    l = LangSpiderHref()
    result = l.run()
    info = LangInfoSpider(result)
    info.run()