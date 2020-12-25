import requests
import time
import os
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



class YoutubeSpider():
    num = 1
    file_name = "./href.txt"
    driver = None
    fd=None
    youtube_down_list = []

    def main(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        self.driver = webdriver.Chrome("./chromedriver")
        try:
            self.get_youtube_url()
            # self.get_download_url()
            print(self.youtube_down_list)
        finally:
            self.driver.close()


    def get_youtube_url(self): 
        save_name = "youtube.npy"
        if(os.path.exists(save_name)):
            youtube = np.load(save_name)
            self.youtube_down_list = youtube.tolist()
            return
        youtube_base = "https://www.youtube.com"
        youtube_url = f"{youtube_base}/watch?v=ozmr55-fihs&list=PL5YAbMpT3Nh32QekRRMnZmSj41T7Sg2rL&index=1"
        self.driver.get(youtube_url)
        elems = self.driver.find_elements_by_css_selector('a#wc-endpoint')
        for elem in elems:
            youtube_down = elem.get_attribute("href")
            print("下载地址: " + youtube_down)
            self.youtube_down_list.append(str(youtube_down))
        youtube = np.array(self.youtube_down_list)
        np.save(save_name, youtube)
        

    def get_download_url(self):
        fd = open(self.file_name, "w")
        num= 1
        base_url = "https://zh.savefrom.net/7/"
        self.driver.get(base_url)
        for youtube_url in self.youtube_down_list: 
            inputs = self.driver.find_elements_by_css_selector('.tarea-wrap > input')
            for input in inputs:
                input.send_keys(youtube_url)
            btns = self.driver.find_elements_by_css_selector('.r-box')
            for btn in btns:
                btn.click()
                input.clear()
            # 等到元素出现后再显示
            elem = WebDriverWait(self.driver, ).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.def-btn-box > a")))
            print(elem)
            name = elem.get_attribute("download")
            href = elem.get_attribute("href")
            text = f"{href}\r\n"
            print(f"正在写入{num}个文件： {name}")
            fd.write(text)
            num += 1
        print(f"{num - 1}个文件地址写入成功！")
        fd.close()

if __name__ == "__main__":
    spider = YoutubeSpider()
    spider.main()
