#coding=utf-8


import os
import zipfile
import sys
import shutil
from pathlib import Path
import json
import struct  
from enum import Enum
from parserFunction import checkEffectZip


'''
class
'''
class EffectZip:
    def __init__(self):
        self.version = '0,0,0'
        self.features = [] #config.json 所有的features
        self.luas = {} #所有lua文件
        self.dirs = [] #所有目录
        self.files = [] #资源包所有文件绝对路径
        self.relfiles = [] #资源包所有文件相对路径
        self.requirements = [] #config.json 里面的算法
        self.config_path = [] #config.json 层面所有的路径
        self.zip_name = '' #资源包的名字
        self.zip_path = '' #资源包的路径

    def setVersion(self,version):
        self.version = version
    def clear(self):
        self.__init__()

class Code(Enum):
    SUCCESS = 0
    ERROR = 1
    WARNING = 2

class ErrorType(Enum):
    NOT_ZIP = 'NOT_ZIP' #不是资源包
    NO_VERSIOIN = 'NO_VERSION' #config.json 里面没有version 字段
    HAS_CHINESE = 'HAS_CHINESE' #资源包里有中文
    VERSION_ERROR = 'VERISON_ERRRO' #资源包版本号错误
    VSCODE = 'VSCODE' #资源包含有vscode 目录


class EffectZipLog:
    Error = 0
    Warn = 0
    def __init__(self):
        self.errorString = ''            #错误提示
        self.errorEnglishString = ''     #错误提示英文
        self.IEthing =''                 #IE提示
        self.jsonErrorData = []          #后台提示
        self.code = 0                    #后台提示code 0 ok 1error 2warning 4chinese

    def addErrorThing(self,thing):
        self.errorString += thing
    
    def addEnglishErrorThing(self,thing):
        self.errorEnglishString += thing
    def setCode(self,code):
        if(code > self.code):
            self.code = code
    def clear(self):
        self.__init__()
    '''
    jsonData 说明
    code: 错误级别 参考Code枚举类
    type: 错误类型 参考type枚举类
    fileName: 错误文件名
    line: 发生错误的行号
    msg: 相关信息提示
    '''
    def addJsonData(self,code,typeName,fileName,line,msg,enmsg):
        tempData = {}
        tempData['code'] = code
        tempData['type'] = typeName
        tempData['file'] = fileName
        tempData['line'] = line
        tempData['msg'] = msg
        tempData['enmsg'] = enmsg
        self.jsonErrorData.append(tempData)
    
    def printEnglishErrorThing(self):
        print(self.errorEnglishString)
    
    def printJsonData(self):
        info = {}
        if(self.code == 0 and len(self.jsonErrorData) > 0):
            self.code = 1
        info['status_code'] = self.code
        info['data'] = self.jsonErrorData
        if(len(json.dumps(info,ensure_ascii = False)) < 1000):
            print(json.dumps(info,ensure_ascii = False))
        else:
            res_json_sub = {}
            res_json_sub['status_code'] = info['status_code']
            res_json_sub['data'] = []
            for js in self.jsonErrorData:
                if(len(json.dumps(res_json_sub,ensure_ascii = False))+len(js) < 1000):
                    res_json_sub['data'].append(js)
                else:
                    break
            print(json.dumps(res_json_sub,ensure_ascii = False))
   


'''
#instantiate class is global object
'''
effectZipLog = EffectZipLog()
effectzip = EffectZip()


def parseZipFile(zipPath):
    bool_zip = zipfile.is_zipfile(zipPath)
    index = zipPath.rfind('/')
    file_last_dir = zipPath[0:index]
    zip_name = zipPath[index+1:]
    file_name = zip_name[0:len(zip_name)-4]
    os.chdir(file_last_dir)
    file_dir = file_last_dir +'/'+ file_name
    if(os.path.exists(file_dir)):
        shutil.rmtree(file_dir)
    os.mkdir(file_dir)

    if bool_zip:
        fz = zipfile.ZipFile(zipPath,'r')
        #避免zip包含中文导致解压乱码 参考https://blog.csdn.net/u010099080/article/details/79829247
        #https://www.cnblogs.com/alex3714/articles/7550940.html
        for fi in fz.namelist():
            if fi.find('__MACOSX') >= 0: continue
            fz.extract(fi,file_dir)
        #todo 中文乱码问题
        # for fi in fz.namelist():
        #     correct_fi = ''
        #     try:
        #         correct_fi = fi.encode('cp437').decode('gbk')
        #     except:
        #         correct_fi = fi.encode('utf-8').decode('utf-8')
        #     if correct_fi.find('__MACOSX') >= 0: continue
        effectzip.zip_path = file_dir
        for root,dirs,files in os.walk(file_dir):
            for fi in files:
                effectzip.relfiles.append(fi)
                effectzip.files.append(os.path.join(root,fi))
                if(fi[-4:] == '.lua'):
                    effectzip.luas[fi] = []
                    effectzip.luas[fi].append(os.path.join(root,fi))
            for di in dirs:
                effectzip.dirs.append(os.path.join(root,di))
        file_list =  os.listdir(file_dir)
        if('config.json' in file_list):
            config_path = file_dir + "/config.json"
            with open(config_path,'r') as f:
                json_string = json.loads(f.read())
                if('version' in json_string):
                    effectzip.setVersion(json_string['version'])
                else:
                    effectZipLog.addJsonData(Code.ERROR,ErrorType.NO_VERSIOIN,'config.json','-1','config.json is no version')
                if('effect' in json_string):
                    effects = json_string['effect']
                if('requirement' in effects and effects['requirement'] != None):
                    req = effects['requirement']
                    for key in req:
                        if(req[key] == True):
                            effectzip.requirements.append(key)
                
                config_path = []
                if('Link' in effects):
                    link = effects['Link']
                    for eff in link:
                        if('type' in eff):
                            effectzip.features.append(eff['type'])
                        if('path' in eff):
                            config_path.append(eff['path'])
                if('bgms' in effects):
                    bgms = effects['bgms']
                    for bgm in bgms:
                        if(isinstance(bgm,dict)):
                            if('music_path' in bgm):
                                config_path.append(bgm['music_path'])
                
                for path in config_path:
                    tempPath = path.split('/',1)
                    tempPath = tempPath[0].split('\\',1)
                    if(tempPath not in effectzip.config_path):
                        effectzip.config_path.append(tempPath[0])


    else:
        effectZipLog.Error = 1
        effectZipLog.addJsonData(Code.ERROR,ErrorType.NOT_ZIP,'error',0,'is not zip package')

def getBusinessParam(path):
    
    print("lsh ",path)
    with open(path,'r') as f:
        json_string = json.loads(f.read())
        print('json: ',json_string)
        return json_string

    
    return

def testData(path):
    effectzip.clear()
    effectZipLog.clear()
    if(path[-4:] == '.zip'):
        parseZipFile(path)  
        checkEffectZip(effectzip,effectZipLog,'DEFAULT')
        info = {}
        if(effectZipLog.code == 0 and len(effectZipLog.jsonErrorData) > 0):
            effectZipLog.code = 1
        info['status_code'] = effectZipLog.code
        info['data'] = effectZipLog.jsonErrorData
        if(len(json.dumps(info,ensure_ascii = False)) < 1000):
            return info
        else:
            res_json_sub = {}
            res_json_sub['status_code'] = info['status_code']
            res_json_sub['data'] = []
            for js in effectZipLog.jsonErrorData:
                if(len(json.dumps(res_json_sub,ensure_ascii = False))+len(js) < 1000):
                    res_json_sub['data'].append(js)
                else:
                    break
            return res_json_sub

if __name__ == '__main__':
    if(len(sys.argv) == 2):
        path = sys.argv[1]
        if(path[-4:] == '.zip'):
            parseZipFile(path)  
            checkEffectZip(effectzip,effectZipLog,'DEFAULT')          
            effectZipLog.printJsonData()
            effectZipLog.printEnglishErrorThing()
    elif(len(sys.argv) == 3):
        path = sys.argv[1]
        param = sys.argv[2]
        #print(path)
        #print(param)
        # params = getBusinessParam('/Users/lvshaohui1234/Desktop/backGround/effect_file_utils/luaAuto/newLuaAuto/business.json')
        paramList = { "DOUYIN","TIKTOK","DEFAULT","QINGYAN","XIGUA"}
        parseZipFile(path)  
        if(param in paramList):
            checkEffectZip(effectzip,effectZipLog,param)  
            effectZipLog.printJsonData()
             # effectZipLog.printEnglishErrorThing()
        elif(param == 'QA'):
            checkEffectZip(effectzip,effectZipLog,'DEFAULT')
            effectZipLog.printEnglishErrorThing()
        else:
            checkEffectZip(effectzip,effectZipLog,'DEFAULT')
            effectZipLog.printJsonData()
            # effectZipLog.printEnglishErrorThing()
