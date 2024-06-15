import os
import platform
import subprocess
import requests
from zipfile import ZipFile


# 检测Chrome浏览器版本（这里只是一个示例，具体实现方式可能不同）
def get_chrome_version():
    # 使用platform和subprocess等模块获取Chrome版本
    # ...  
    return chrome_version


# 下载并解压chromedriver
def download_chromedriver(chrome_version):
    # 根据chrome_version构造chromedriver的下载链接
    # ...
    download_url = "https://chromedriver.storage.googleapis.com/..."

    # 下载chromedriver压缩包
    response = requests.get(download_url)
    with open("chromedriver.zip", "wb") as f:
        f.write(response.content)

        # 解压chromedriver到指定目录
    with ZipFile("chromedriver.zip", 'r') as zip_ref:
        zip_ref.extractall("./drivers")

    # 主逻辑


chrome_version = get_chrome_version()
download_chromedriver(chrome_version)

# 配置selenium使用chromedriver
# ...