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
from parserFunction import checkLokiEffectZip


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
        self.model_names = []  #config.json 层面所有的model_names
        self.zip_name = '' #资源包的名字
        self.zip_path = '' #资源包的路径
        self.png = []    #所有png文件绝对路径
        self.zorder = [] #config.json所有的zorder
        self.fsh = []    #老引擎，所有fsh后缀文件绝对路径 
        self.vsh = []    #老引擎，所有vsh后缀文件的绝对路径  
        self.vert = []   #新引擎，所有vert后缀文件绝对路径  
        self.frag = []   #新引擎，所有frag后缀文件绝对路径   
        self.jpg = []   #所有jpg后缀文件绝对路径
        self.gif = []   #所有gif后缀文件绝对路径
        self.glb =[]    #所有glb后缀文件绝对路径
        self.webp = []  #所有webp后缀文件绝对路径
        self.content_requirements = [] #content.json文件中requirement为true
        self.algorithmConfig = []   #algorithmConfig.json中type字段,代表接入bach算法能力
        self.systemList = [] # sticker.config中"systemList"

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
    
    def printJsonData(self, isReturn = False):
        info = {}
        if(self.code == 0 and len(self.jsonErrorData) > 0):
            self.code = 1
        info['status_code'] = self.code
        info['data'] = self.jsonErrorData
        if(len(json.dumps(info,ensure_ascii = False)) < 4000):
            if isReturn:
                return info
            else:
                print(json.dumps(info,ensure_ascii = False))
        else:
            res_json_sub = {}
            res_json_sub['status_code'] = info['status_code']
            res_json_sub['data'] = []
            for js in self.jsonErrorData:
                if(len(json.dumps(res_json_sub,ensure_ascii = False))+len(js) < 4000):
                    res_json_sub['data'].append(js)
                else:
                    break
            if isReturn:
                return res_json_sub
            else:
                print(json.dumps(res_json_sub,ensure_ascii = False))
   


'''
#instantiate class is global object
'''
effectZipLog = EffectZipLog()
effectzip = EffectZip()


def parseZipFile(zipPath, ctxEffectZip = effectzip, ctxEffectZipLog = effectZipLog):
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
        ctxEffectZip.zip_path = file_dir
        for root,dirs,files in os.walk(file_dir):
            for fi in files:
                ctxEffectZip.relfiles.append(fi)
                ctxEffectZip.files.append(os.path.join(root,fi))
                if(fi[-4:] == '.lua'):
                    ctxEffectZip.luas[fi] = []
                    ctxEffectZip.luas[fi].append(os.path.join(root,fi))
            for di in dirs:
                ctxEffectZip.dirs.append(os.path.join(root,di))
        file_list =  os.listdir(file_dir)
        
        #提取zip包中所有的png文件夹路径
        ctxEffectZip.png = []
        for fi in ctxEffectZip.files:
            if(fi[-4:] == '.png'):
                ctxEffectZip.png.append(fi)
            elif(fi[-4:] == '.jpg'):
                ctxEffectZip.jpg.append(fi)
            elif(fi[-4:]=='.gif'):
                ctxEffectZip.gif.append(fi)
            elif(fi[-4:]=='.vsh'):
                ctxEffectZip.vsh.append(fi)
            elif(fi[-5:] == '.vert'):
                ctxEffectZip.vert.append(fi)
            elif(fi[-5:] == '.frag'):
                ctxEffectZip.frag.append(fi)
            elif(fi[-4:] == '.fsh'):
                ctxEffectZip.fsh.append(fi)
            elif(fi[-4:] == '.glb'):
                ctxEffectZip.glb.append(fi)
            elif(fi[-5:] == '.webp'):
                ctxEffectZip.webp.append(fi)
        #return

        if('config.json' in file_list):
            config_path = file_dir + "/config.json"
            with open(config_path,'r') as f:
                json_string = json.loads(f.read())
                if('version' in json_string):
                    ctxEffectZip.setVersion(json_string['version'])
                else:
                    ctxEffectZipLog.addJsonData(Code.ERROR,ErrorType.NO_VERSIOIN,'config.json','-1','config.json is no version','config.json is no version')
                if('effect' in json_string):
                    effects = json_string['effect']
                try:
                    if('requirement' in effects and effects['requirement'] != None):
                        req = effects['requirement']
                        for key in req:
                            if(req[key] == True):
                                ctxEffectZip.requirements.append(key)
                    config_path = []
                    if('Link' in effects):
                        link = effects['Link']
                        for eff in link:
                            if('type' in eff):
                                ctxEffectZip.features.append(eff['type'])
                            if('path' in eff):
                                config_path.append(eff['path'])
                            if('zorder' in eff):
                                ctxEffectZip.zorder.append(eff['zorder'])

                    if('bgms' in effects):
                        bgms = effects['bgms']
                        for bgm in bgms:
                            if(isinstance(bgm,dict)):
                                if('music_path' in bgm):
                                    config_path.append(bgm['music_path'])
                    if('model_names' in effects):
                        for i in effects['model_names']:
                            for j in effects['model_names'][i]:
                                ctxEffectZip.model_names.append(j)
                except:
                    pass
                for path in config_path:
                    tempPath = path.split('/',1)
                    tempPath = tempPath[0].split('\\',1)
                    if(tempPath not in ctxEffectZip.config_path):
                        ctxEffectZip.config_path.append(tempPath[0])

        # content.json文件提取requirement中打开为true的算法列表，提取到self.content_requirements = []
        list_dir = os.listdir(ctxEffectZip.zip_path)
        fi = get_Filepath(ctxEffectZip,'content.json')
        if fi != None:
            with open(fi) as f:
                content_string = json.loads(f.read())
                try:
                    if('requirement' in content_string and content_string['requirement'] != None):
                        req = content_string['requirement']
                        for key in req:
                            if(req[key] == True):
                                ctxEffectZip.content_requirements.append(key)
                except:
                    pass
        
        # 提取algorithmConfig.json的"nodes"中的"type"字段，代表接入bach算法
        fi = get_Filepath(ctxEffectZip,'algorithmConfig.json')
        if fi != None:
            with open(fi) as f:
                algorithmConfig_string = json.loads(f.read())
                if('nodes' in algorithmConfig_string):
                    string_nodes = algorithmConfig_string['nodes']
                    try:
                        for item in string_nodes:
                            ctxEffectZip.algorithmConfig.append(item['type'])
                    except:
                        pass
                elif(algorithmConfig_string.get('model_names')):
                    try:
                        for key in algorithmConfig_string.get('model_names'):
                            ctxEffectZip.model_names.extend(algorithmConfig_string.get('model_names')[key])
                    except:
                        pass

        # 提取sticker.config文件中systemList列表
        fi = get_Filepath(ctxEffectZip,'sticker.config')
        if fi != None:
            with open(fi) as f:
                stickerconfig_string = json.loads(f.read())
                if('systemList' in stickerconfig_string):
                    try:
                        ctxEffectZip.systemList = stickerconfig_string['systemList']
                    except:
                        pass
    else:
        ctxEffectZipLog.Error = 1
        ctxEffectZipLog.addJsonData(Code.ERROR,ErrorType.NOT_ZIP,'error',0,'is not zip package','is not zip package')

# 13 通用方法获取指定文件路径
def get_Filepath(effectzip,filename):
    for fi in effectzip.files:
        fis = fi.split('/')
        if(fis[-1]== filename):
            #print(fi)
            return fi

def getBusinessParam(path):
    
    print("lsh ",path)
    with open(path,'r') as f:
        json_string = json.loads(f.read())
        print('json: ',json_string)
        return json_string

    
    return

# def testData(path):
#     effectzip.clear()
#     effectZipLog.clear()
#     if(path[-4:] == '.zip'):
#         print(path)
#         parseZipFile(path)
#         checkEffectZip(effectzip,effectZipLog,'DEFAULT')
#         info = {}
#         if(effectZipLog.code == 0 and len(effectZipLog.jsonErrorData) > 0):
#             effectZipLog.code = 1
#         info['status_code'] = effectZipLog.code
#         info['data'] = effectZipLog.jsonErrorData
#         if(len(json.dumps(info,ensure_ascii = False)) < 1000):
#             return info
#         else:
#             res_json_sub = {}
#             res_json_sub['status_code'] = info['status_code']
#             res_json_sub['data'] = []
#             for js in effectZipLog.jsonErrorData:
#                 if(len(json.dumps(res_json_sub,ensure_ascii = False))+len(js) < 1000):
#                     res_json_sub['data'].append(js)
#                 else:
#                     break
#             return res_json_sub

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
        paramList = { "DOUYIN","TIKTOK","DEFAULT","QINGYAN","XIGUA","FACEU","CAPCUT","DEFAULT_I18N","TTAME_2D","DYAME_2D","TTAME_prefab","DYAME_prefab"}
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
    elif(len(sys.argv) == 4):
        path = sys.argv[1]
        param = sys.argv[2]
        lokiInformation = sys.argv[3]
        # print(path)
        # print(param)
        # print(lokiInformation)
        paramList = { "DOUYIN","TIKTOK","DEFAULT","QINGYAN","XIGUA","FACEU","CAPCUT","DEFAULT_I18N","TTAME_2D","DYAME_2D","TTAME_prefab","DYAME_prefab"}
        parseZipFile(path)  
        if(param in paramList):
            checkEffectZip(effectzip,effectZipLog,param)
            checkLokiEffectZip(effectzip,effectZipLog,param,lokiInformation)  
            effectZipLog.printJsonData()
        else:
            checkEffectZip(effectzip,effectZipLog,'DEFAULT')
            checkLokiEffectZip(effectzip,effectZipLog,param,lokiInformation)
            effectZipLog.printJsonData()
            # effectZipLog.printEnglishErrorThing()

def luaCheck(path, param, lokiInformation):
    # 需要重新实例化
    # global effectZipLog, effectzip
    ctxEffectZipLog = EffectZipLog()
    ctxEffectZip = EffectZip()
    paramList = { "DOUYIN","TIKTOK","DEFAULT","QINGYAN","XIGUA","FACEU","CAPCUT","DEFAULT_I18N"}
    parseZipFile(path, ctxEffectZip, ctxEffectZipLog)
    res = None
    if(param in paramList):
        checkEffectZip(ctxEffectZip,ctxEffectZipLog,param,lokiInformation)
        checkLokiEffectZip(ctxEffectZip,ctxEffectZipLog,param,lokiInformation)  
        res = ctxEffectZipLog.printJsonData(isReturn=True)
    else:
        checkEffectZip(ctxEffectZip,ctxEffectZipLog,'DEFAULT',None)
        checkLokiEffectZip(ctxEffectZip,ctxEffectZipLog,param,lokiInformation)
        res = ctxEffectZipLog.printJsonData(isReturn=True)
        # effectZipLog.printEnglishErrorThing()
    return res

r_path = {
"2d":['/Users/bytedance/Downloads/AME-luaauto测试case/复古小动物.zip','/Users/bytedance/Downloads/AME-luaauto测试case/涂鸦相机.zip','/Users/bytedance/Downloads/AME-luaauto测试case/相逢是缘.zip'],
"prefab":['/Users/bytedance/Downloads/AME-luaauto测试case/冷白皮.zip']
}
f_path = {
"2d":['/Users/bytedance/Downloads/AME-luaauto测试case/39_4K.zip','/Users/bytedance/Downloads/AME-luaauto测试case/一天的好心情.zip',r'/Users/bytedance/Downloads/AME-luaauto测试case/gif_test.zip'],
"prefab": [r'/Users/bytedance/Downloads/AME-luaauto测试case/filter_test.zip']
}

lokiInformation = {'appEffectId': 2506926, 'regionKey': 'default', 'panelKey': 'ame_foreground_sticker', 'appVersionIosMin': '99.99.99', 'appVersionIosMax': '99.99.99', 'appVersionAndroidMin': '00.00.00', 'appVersionAndroidMax': '99.99.99', 'effectFileTypes': ['InfoSticker'], 'effectRequirements': [], 'systemList': [], 'platform': 2}
# lokiInformation = {'panelKey':'effecttoolliquify'}

# paths = f_path['prefab']
# for path in paths:
path = r'/Users/bytedance/Downloads/AME-luaauto测试case/一天的好心情.zip'
res = luaCheck(path,'DOUYIN',lokiInformation)
print(res)

