# 根据MD5，下载effect.zip，再对effect.zip进行解压，解压后文件信息保存到类EffectZip中
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import queue
import requests
import io
import zipfile
import json
import csv
import logging
import os


# 定义logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义全局变量,读取config.json文件
with open('config.json', 'r') as f:
    config_info = json.load(f)
# 下载effect.zip，并把信息传递给EffectZip类

class EffectZip:
    def __init__(self, md5):
        self.md5 = md5
        self.file_info = None
        self.file_list = []
        self.config_info = {}
        self.algorithmn_info = {}
        self.pic_info = {}
        self.__download_unzip()
        self.__process_file_info()
        self.temp_file = "effect.zip"
        self.__read_config()
        self.__read_algorithmn()
        self.__read_pic()

    def __del__(self):
        # 删除临时文件
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def __download_unzip(self, max_retries=3, retry_delay=2):
        retries = 0
        while retries < max_retries:
            try:
                pkgUrl = (
                    "https://lf3-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/" + md5
                )
                matResponse = requests.get(pkgUrl, stream=True, timeout=20)
                matResponse.raise_for_status()
                self.temp_file = io.BytesIO(matResponse.content)
                # 将zip_file传递给EffectZip类进行解压
                self.__unzip(self.temp_file)
                break
            except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:

                logging.error(f"Request for {pkgUrl} failed: {e}, retrying...")
                retries += 1
                if retries < max_retries:
                    time.sleep(retry_delay)  # 等待一段时间后重试

            if retries == max_retries:
                logging.error(f"Max retries reached for {pkgUrl}")

    def __unzip(self, zip_file):

        # 解压zip_file并获取文件信息
        with zipfile.ZipFile(zip_file) as zf:
            self.file_info = zf.infolist()

    # 处理文件信息，list_file保存文件名称、大小(kb)、路径
    def __process_file_info(self):
        # 遍历文件信息列表，处理文件名和文件大小
        if self.file_info:
            base_path = os.path.abspath(__file__)
            for info in self.file_info:
                if '/' in info.filename:
                    file_name = info.filename.split('/')[-1]
                    file_size = info.file_size / 1024
                    self.file_list.append((file_name, file_size, os.path.join(base_path, file_name)))
                else:
                    file_name = info.filename
                    file_size = info.file_size / 1024
                    self.file_list.append((file_name, file_size, os.path.join(base_path, file_name)))
        else:
            logging.error("No file information found.")

    # 根据文件名获取指定文件名的文件路径，返回文件路径，如果没有找到返回None，如果有多个文件返回路径最短的文件
    def get_file_path(self, file_name):
        file_path = None
        for file in self.file_list:
            if file_name == file[0]:
                if not file_path:
                    file_path = file[2]
                else:
                    if len(file[2]) < len(file_path):
                        file_path = file[2]
        return file_path

    # 读取config.json文件
    def __read_config(self):
        file_path = self.get_file_path("config.json")
        if file_path:
            with open(file_path, 'r') as f:
                self.config_info = json.load(f)
        else:
            logging.error("No config.json file found.")
    # 读取algorithmn.json文件
    def __read_algorithmn(self):
        file_path = self.get_file_path("algorithmn.json")
        if file_path:
            with open(file_path, 'r') as f:
                self.algorithmn_info = json.load(f)
        else:
            logging.error("No algorithmn.json file found.")

    # 读取不同格式的图片文件，存储到pic_info字典中，key为文件格式，value为文件路径（list）
    def __read_pic(self):
        pic_format = config_info.get("pic_format")
        for v in pic_format:
            self.pic_info[v] = []
        for file in self.file_list:
            file_name = file[0]
            if file_name.split('.')[-1] in pic_format:
                if file_name.split('.')[-1] in self.pic_info:
                    self.pic_info[file_name.split('.')[-1]].append(file[2])
                else:
                    self.pic_info[file_name.split('.')[-1]] = [file[2]]




if __name__ == '__main__':
    md5 = "28ccd9558430679f89a1c65310ed3803"
    effect_zip = EffectZip(md5)
    for file_name in effect_zip.file_list:
        print(file_name)
