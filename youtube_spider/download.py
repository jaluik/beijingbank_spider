import os
import sys
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class YoutubeSpider():
    num = 1
    driver = None
    fd = None
    youtube_down_list = []

    def main(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        self.driver = webdriver.Chrome(sys.path[0] + "/chromedriver")
        try:
            self.get_youtube_url()
            self.get_download_url()
            print(self.youtube_down_list)
        finally:
            self.driver.close()

    def get_youtube_url(self):
        save_name = sys.path[0] + "/youtube.npy"
        if os.path.exists(save_name):
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
        file_name = sys.path[0] + "/href.txt"
        file_err_name = sys.path[0] + "/href.txt"
        fd = open(file_name, "w")
        fe = open(file_err_name, "w")
        num = 1
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
            try:
                elem = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.def-btn-box > a")))
                print(elem)
                name = elem.get_attribute("download")
                href = elem.get_attribute("href")
                text = f"{href}\r\n"
                print(f"正在写入{num}个文件： {name}")
                fd.write(text)
                num += 1
            except:
                print("某个文件出问题啦")
                print("未能下载的url:", youtube_url)
                fe.write(youtube_url)
                continue

        print(f"{num - 1}个文件地址写入成功！")
        fd.close()
        fe.close()


if __name__ == "__main__":
    spider = YoutubeSpider()
    spider.main()
