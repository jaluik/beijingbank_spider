import requests
from bs4 import BeautifulSoup
import os

host = "http://www.bankofbeijing.com.cn"
save_dir = "./pdfs/"
num = 1


# 获取alink的url
def get_a_url(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "lxml")
    a_list = soup.select("ul.f_000_12 > li > a")
    result_list = []
    for dom_a in a_list:
        real_link = host + dom_a["href"]
        result_list.append(real_link)
    return result_list


# 获取pdf的url
def get_pdf_url(url):
    data = requests.get(url)
    data.encoding = "utf-8"
    soup = BeautifulSoup(data.text, "lxml")
    a_list = soup.select("#con > p > a")
    for dom_a in a_list:
        real_link = host + dom_a["href"]
        if dom_a:
            return real_link


def download_pdf(download_url):
    file_name = download_url.split("/")[-1]
    global num
    save_file_name = save_dir + file_name
    req = requests.get(download_url)
    with open(save_file_name, 'wb') as f:
        f.write(req.content)
        print(f"第{str(num)}个文件 -- {file_name} 下载成功")
        num = num + 1


def download_all(page_size=1):
    for i in range(page_size):
        if i == 0:
            base_url = f"{host}/licai/bf-gonggao.shtml"
        else:
            base_url = f"{host}/licai/bf-gonggao_{i}.shtml"
        a_urls = get_a_url(base_url)
        for a_url in a_urls:
            url = get_pdf_url(a_url)
            if url:
                download_pdf(url)


if __name__ == "__main__":
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    count = input("输入你想查询的总页数：")
    download_all(int(count))
    print(f"总共下载{str(num - 1)}个文件！")
