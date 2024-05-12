# -*- coding: utf-8 -*-
#风神 --> 对应数据库
#hive --> 对应数据库字段解释
#风神 https://data.bytedance.net/aeolus/#/queryEditor/query/5abb3e2967670521?appId=555126&blockId=2861639&group=default&taskId=20519490
#hive https://data.bytedance.net/coral/datamap/detail/table_info/hive/dm_effect/effects_daily/schema#group=default
#数据结构{'android_max_frame': 9999, 'android_min_frame': 0, 'android_model': '', 'android_type': 0, 'app_id': '184', 'channel': '0', 'created_at': '1545792282', 'created_time': 1545792282, 'effect_description': 'Smile to light up the sky', 'effect_id': '22510', 'en_name': '', 'extra': '', 'features': '2DStickerV3', 'file_uri': '45b13d89cad408ee2931387f90192fd1', 'first_publish_time': 0, 'icon_uri': '2c33d06e3aa49776f31175da98b5ab89', 'id': '100111', 'ios_max_frame': 9999, 'ios_min_frame': 0, 'ios_model': '', 'ios_type': 0, 'is_business': 0, 'is_poi': 0, 'name': '2019 Fireworks', 'original_name': '微笑点亮2019', 'original_region': '', 'p_date': '2019-11-16', 'panel': 'default', 'parent_id': 0, 'platform': 'all', 'publish_status': 0, 'publish_time': 1545792282, 'region': 'gb', 'region_name': 'UK+', 'related_words': '', 'requirements': 'faceDetect,expressionDetect', 'sdk_extra': '', 'source': 0, 'sync_id': 97916, 'tags': '', 'type': 0, 'updated_at': '1566719746', 'updated_time': 1566719746}
# from Users.lvshaohui1234.lvByteDance.python.python_down_load2.clip_house_api import luaAuto
import os
from six.moves.urllib.parse import urlparse, parse_qsl, urlencode
import sys
print(os.getcwd())
sys.path.append(os.getcwd()+'/luaAuto')

import luaAuto.luaAuto
import luaAuto.parserFunction
import luaAuto.data

import requests
import json
import pandas as pd
import time 
# import multiprocessing
import shutil
import zipfile
import hashlib
import csv




#中文对应部分，方便观看。 具体查看hive表
app_id_dict= {'184':'抖音','167':'火山','128':'modeo'}

#download
def download_zip(tar_name, url):
    # os.system("curl -o {0} -ss http://sf1-hscdn-tos.pstatp.com/obj/ies.fe.effect/{1}".format(tar_name, file_uri))
    preUrl = "https://sf1-hscdn-tos.pstatp.com/obj/ies.fe.effect/"
    icon_url = preUrl + url
    wirteFile = url + '.zip'
    # #写入下载文件
    req = 0
    try:
        req = requests.get(icon_url, timeout=15)
        if req.status_code != 200:
            print(" fail %s %s %s" % (icon_url, req.status_code, req.content[:20]))
            return False
    except:
        return False
        
    with open(wirteFile, "wb+") as f:
        f.write(req.content)
    return True

def filename_should_encrypt(filename):
    patterns = ['.vsh', '.fsh', '.lua', '.vert', '.frag']
    for p in patterns:
        if filename.endswith(p):
            return True
    return False

def encrypt(path_from, path_to):
    cmd = './encrypt -e {} {}'.format(path_from, path_to)
    os.system(cmd)

def encrypt_dir(path_from, path_to):
    # copy
    if os.path.exists(path_to):
        shutil.rmtree(path_to)
    shutil.copytree(path_from, path_to)

    # scan
    paths = []
    for root, dirs, files in os.walk(path_from):
        for f in files:
            p = os.path.join(root, f)
            if filename_should_encrypt(f):
                paths.append(p)

    # process
    for p in paths:
        p_to = p.replace(path_from, path_to, 1)
        encrypt(p, p_to)

## hash tag
count = 0








def get_effect_file_list(path):
    with open(path) as f:
        f_csv = csv.reader(f)
        name_list = next(f_csv)
        print(name_list)
        result_list = []
        for row in f_csv:
            result_list.append(row)
        
    return name_list,result_list


if __name__ == "__main__":
    
    name_list,result_list =  get_effect_file_list('douyin.csv')
    file_uri_num = 0
    for j in range(0,len(name_list)):
        if(str(name_list[j]) == 'file_uri'):
                file_uri_num = j
                break
    
    name_list.append('msg')
    result_right = []
    result_error = []
    result_warning = []
    md5_list = []
    md5_sum = len(result_list)
    print('result_list length is ',md5_sum)
    if(os.path.isdir('douyin_0_1000')):
        shutil.rmtree('douyin_0_1000')
    os.mkdir('douyin_0_1000')
    os.chdir('douyin_0_1000')
    for j in range(0,md5_sum):
        name = result_list[j][file_uri_num]
        print("##process ",j,"####")
        if(name not in  md5_list and download_zip(str(name),str(name))):
            md5_list.append(name)
            zip_name = str(name) + ".zip"
            zip_path = os.getcwd() +"/" +  zip_name
            dst_dir = os.getcwd()  +"/" +  str(name)
            if(os.path.exists(dst_dir)):
                shutil.rmtree(dst_dir)
          

            data = luaAuto.luaAuto.testData(zip_path)
            os.remove(zip_path)
            shutil.rmtree(str(name))
            json_data = data
            temp_data = result_list[j]
            temp_data.append(str(json_data["data"]))

            if(json_data["status_code"] == 1):
                result_error.append(temp_data)
            elif(json_data["status_code"] == 2):
                result_warning.append(temp_data)
            else:
                result_right.append(temp_data)

    csv_list=pd.DataFrame(columns=name_list,data=result_right)
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    effect_name = 'right_'+time_str+'.csv'
    csv_list.to_csv(effect_name,encoding = 'utf-8')

    csv_list=pd.DataFrame(columns=name_list,data=result_error)
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    effect_name = 'error_'+time_str+'.csv'
    csv_list.to_csv(effect_name,encoding = 'utf-8')

    csv_list=pd.DataFrame(columns=name_list,data=result_warning)
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    effect_name = 'warn_'+time_str+'.csv'
    csv_list.to_csv(effect_name,encoding = 'utf-8')
         
