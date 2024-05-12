# 对不同检测规则进行定义，区分级别：Error、Warning、Info、Debug

# coding=utf-8
import data as EffectData
import os
import json
import struct
import sys
import shutil
import zipfile
from distutils.version import LooseVersion
# from PIL import Image
import hashlib
import hmac
import requests
import time
import re


class MyFunc:
    parameter = 0
    version = '0.0.0'
    funcName = ''
    className = ''
    returnName = ''
    i = 0

    def getVersion(self):
        return self.version

    def getFuncName(self):
        return self.funcName

    def getParameter(self):
        return self.parameter

    def getReturnName(self):
        return self.returnName

    def __init__(self, i):
        self.i = i
        self.funcName = ''
        self.parameter = 0
        self.version = '0.0.0'
        self.className = ''
        self.returnName = ''


class MyClass:
    className = ''
    funcDic = {}

    def getFunc(self, name):
        if (name in self.funcDic):
            return self.funcDic[name]
        else:
            return None

    def __init__(self):
        self.funcDic = {}
        self.className = ''


class ClassManager:
    funcToClass = {}
    funcToReturnName = {}
    classDic = {}
    funcToVerion = {}

    def getClass(self, name):
        if (name in self.classDic):
            return self.classDic[name]
        else:
            return None

    def getfuncToReturnName(self, name):
        if (name in self.funcToReturnName):
            return self.funcToReturnName[name]
        else:
            return None

    def getFuncClass(self, name):
        if (name in self.funcToClass):
            return self.funcToClass[name]
        else:
            return None

    def getFuncVersion(self, name):
        if (name in self.funcToVerion):
            return self.funcToVerion[name]
        else:
            return None


def parseFunction():
    i = 0
    if (len(EffectData.classList) != len(EffectData.returnList) or len(EffectData.classList) != len(
        EffectData.funcList) or len(EffectData.classList) != len(
        EffectData.versionList) or len(EffectData.classList) != len(EffectData.parameterList)):
        print("error:   列表个数不相等 ")
        exit(0)
    myClassManager = ClassManager()
    while (i < len(EffectData.classList)):
        myClassManager.funcToClass[EffectData.funcList[i]] = EffectData.classList[i]
        myClassManager.funcToReturnName[EffectData.funcList[i]] = EffectData.returnList[i]
        myClassManager.funcToVerion[EffectData.funcList[i]] = EffectData.versionList[i]
        if (EffectData.classList[i] not in myClassManager.classDic):
            myClassManager.classDic[EffectData.classList[i]] = MyClass()
            myClassManager.classDic[EffectData.classList[i]].className = EffectData.classList[i]

        if (EffectData.funcList[i] not in myClassManager.classDic[EffectData.classList[i]].funcDic):
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]] = MyFunc(i)
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].className = \
            EffectData.classList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].funcName = \
            EffectData.funcList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].version = \
            EffectData.versionList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].parameter = \
            EffectData.parameterList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].returnName = \
            EffectData.returnList[i]
        else:
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].className = \
            EffectData.classList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].funcName = \
            EffectData.funcList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].version = \
            EffectData.versionList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].parameter = \
            EffectData.parameterList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].returnName = \
            EffectData.returnList[i]

        i += 1

    myClassManager.funcToVerion['getRenderProtocol'] = '4.6.0'  # 临时todo

    return myClassManager


def participle(Strings):
    stringList = []
    tempString = ''
    nBuf = 0
    number = 0
    lines = 1
    numList = {}  # 记录单词和对应

    i = 0
    while (i < len(Strings)):
        if (nBuf == 0):
            if (Strings[i] == ' ' or Strings[i] == '\n' or Strings[i] == '\t' or Strings[i] == '\r'):
                if (Strings[i] == '\n'):
                    lines += 1
                i += 1
                continue
            elif (Strings[i] == '(' or Strings[i] == '{' or Strings[i] == '}' or Strings[i] == ')' or
                  Strings[i] == ':' or Strings[i] == '=' or Strings[i] == ','):
                tempString += Strings[i]
                numList[number] = lines
                number += 1
                stringList.append(tempString)
                tempString = ''
                nBuf = 0
            elif (Strings[i] == '-'):  # 对注释的处理
                if (Strings[i + 1] == '-'):
                    i = i + 2
                    while (Strings[i] != '\n'):
                        i = i + 1
                    lines += 1
                    nBuf = 0
                    tempString = ''
                else:
                    tempString += Strings[i]
                    nBuf += 1
            elif (Strings[i] == '"'):
                # tempString += Strings[i]
                i += 1
                while (Strings[i] != '"'):
                    tempString += Strings[i]
                    i += 1
                # tempString += Strings[i]
                nBuf += 1
            elif (Strings[i] >= '0' and Strings[i] <= '9'):
                tempString += Strings[i]
                nBuf += 1
            elif (Strings[i] >= 'a' and Strings[i] <= 'z'):
                tempString += Strings[i]
                nBuf += 1
            elif (Strings[i] == '+' or Strings[i] == '-' or Strings[i] == '*' or Strings[i] == "'"):
                tempString += Strings[i]
                nBuf += 1
            else:
                tempString += Strings[i]
                nBuf += 1
        else:
            if (Strings[i] == ' ' or Strings[i] == '\t' or Strings[i] == '\n' or Strings[i] == '\r'):
                numList[number] = lines
                number += 1
                stringList.append(tempString)
                if (Strings[i] == '\n'):
                    lines += 1
                tempString = ''
                nBuf = 0
            elif (Strings[i] == '(' or Strings[i] == '{' or Strings[i] == ')' or Strings[i] == '}' or
                  Strings[i] == ',' or Strings[i] == ':' or Strings[i] == '='):
                numList[number] = lines
                number += 1
                stringList.append(tempString)
                numList[number] = lines
                number += 1
                stringList.append(Strings[i])
                tempString = ''
                nBuf = 0
            elif (Strings[i] == '-'):  # 对注释的处理
                if (Strings[i + 1] == '-'):
                    i = i + 2
                    while (Strings[i] != '\n'):
                        i = i + 1
                    if (i == len(Strings) - 1):
                        return ('null', [])
                    lines += 1
                    numList[number] = lines
                    number += 1
                    stringList.append(tempString)
                    nBuf = 0
                    tempString = ''
                else:
                    tempString += Strings[i]
                    nBuf += 1
            elif (Strings[i] == '"'):
                # tempString += Strings[i]
                i += 1
                while (Strings[i] != '"'):
                    tempString += Strings[i]
                    if (i == len(Strings) - 1):
                        return ('null', [])
                    i += 1
                # tempString += Strings[i]
                nBuf += 1

            else:
                tempString += Strings[i]
                nBuf += 1
        i += 1
        # print(stringList)
    # k = 0
    # while(k < len(stringList)):
    #     print(stringList[k],numList[k])
    #     k += 1
    return stringList, numList


def check_type_list():
    return {
        "6C6F6361": "lua",
        "7B0A": "json",
        # "7B0A0922":"json"
        "23646566": "shader",
        "0A707265": "vert",
        "70726563": "frag",
        "0A236465": "vert",
        "0A202020": "glsl",
        "3234300A": "text",
        "61747472": "glsl",
        "5B0A2020": "event",
        "A0A6C6F": "lua",
        "6B436C6F": "lua",
        "0A6C6F63": "lua"
    }


def un_check_type_list():
    return {
        "52617221": "EXT_RAR",
        "504B0304": "EXT_ZIP",
        "89504E47": "PNG",
        "47494638": "GIF",
        "49492A00": "TIFF",
        "424D": "Bitmap",
        "7B5C727466": "rtf",
        "3C3F786D6C": "xml",
        "68746D6C3E": "html",
        "2E7261FD": "Audio",
        "25536572": "scene/mesh",
        "00000001": "DS_Store",
        "25536572": "Xshader",
        "49443303": "bgm",
        "FFFBE040": "bgm"
    }


# 字节码转16进制字符串
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]

        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


# 获取文件类型
def filetype(filename):
    global ErrorThing
    global ErrorEnglishThing
    binfile = open(filename, 'rb')  # 必需二制字读取
    file_size = os.path.getsize(filename)
    if (file_size < 20):
        binfile.close()
        return False
    ctl = check_type_list()
    utl = un_check_type_list()
    ftype = 'unknown'
    checkChinese = True
    for hcode in ctl.keys():
        numOfBytes = int(len(hcode) / 2)  # 需要读多少字节
        binfile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取

        hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))  # 一个 "B"表示一个字节
        f_hcode = bytes2hex(hbytes)

        if f_hcode == hcode:
            ftype = ctl[hcode]
            checkChinese = True
            break
    for hcode in utl.keys():
        numOfBytes = int(len(hcode) / 2)  # 需要读多少字节
        binfile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
        hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))  # 一个 "B"表示一个字节
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = utl[hcode]
            checkChinese = False
            break
            # if(ftype == "unknown"):
    #     ErrorThing = ErrorThing +  "file:%s file_type is unknown, filecode=%s\n"%(filename,f_hcode)
    #     ErrorEnglishThing = ErrorThing + "file:%s file_type is unkonw,filecode=%s\n"%(filename,f_hcode)

    binfile.close()
    return checkChinese


def check_contain_chinese(check_str):
    chineseList = []
    if (type(check_str) == bytes):
        return chineseList
    for ch in check_str.encode().decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            chineseList.append(ch)
    return chineseList


# 检测是否有中文
def checkChinese(effectzip, effectLog):
    for di in effectzip.dirs:
        temp_di = di.split('/')
        if ('__MACOSX' not in temp_di and temp_di[-1] != '.DS_Store'):
            dir_path = di[len(effectzip.zip_path) + 1:]
            # print(dir_path)
            checkList = check_contain_chinese(dir_path)
            if (len(checkList) > 0):
                msg = 'error: file:%s含有中文字符:%s\n等等' % (dir_path, checkList[0:50])
                enmsg = 'error: file:%s has chinese text is:%s\n' % (dir_path, checkList[0:50])
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(1, 'HAS_CHINESE', effectzip.zip_name, -1, msg, enmsg)
                effectLog.setCode(4)

    for fi in effectzip.files:
        temp_fi = fi.split('/')
        if ('__MACOSX' not in temp_fi and temp_fi[-1] != '.DS_Store'):
            fi_path = fi[len(effectzip.zip_path) + 1:]
            checkList = check_contain_chinese(fi_path)
            if (len(checkList) > 0):
                msg = 'error: file:%s has chinese text is:%s\n' % (fi_path, checkList[0:50])
                enmsg = 'error: file:%s has chinese text is:%s\n' % (fi_path, checkList[0:50])
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(1, 'HAS_CHINESE', effectzip.zip_name, -1, msg, enmsg)
            if (filetype(fi) == True):
                if (os.path.isfile(fi)):
                    with open(fi, 'rb') as f:
                        try:
                            file_str = f.read().decode('utf-8')
                            checkList = check_contain_chinese(file_str)
                            if (len(checkList) > 0):
                                msg = 'error: file:%s 含有中文字符:%s\n等等' % (fi_path, checkList[0:50])
                                enmsg = 'error: file:%s has chinese text is:%s\n' % (fi_path, checkList[0:50])
                                effectLog.addEnglishErrorThing(msg)
                                effectLog.addJsonData(1, 'HAS_CHINESE', effectzip.zip_name, -1, msg, enmsg)
                                effectLog.setCode(4)

                        except UnicodeDecodeError:
                            pass


# 检测自定义文字是否送审核
def checkTextIsOk(effectzip, effectLog):
    for fi in effectzip.files:
        temp_fi = fi.split('/')
        if ('__MACOSX' not in temp_fi and temp_fi[-1][-4:] == '.lua' and temp_fi[-1][0] != '.'):
            try:
                with open(fi, 'r') as lua_file:
                    lua_string = lua_file.read()
                    if (lua_string.find('handleKeyboardInput') > 0):  # 说明是新引擎文字贴纸
                        if (lua_string.find('getTextContent') > 0 and lua_string.find('Amaz.StringVector') > 0):
                            lua_textset = True  # ok
                        else:
                            msg = 'error: file:%s text2DV2 handleKeyboardInput 送审文字接口需要添加接口getLuaTextContent()请添加 \n' % (
                                fi)
                            enmsg = 'error: file:%s text2DV2 handleKeyboardInput  need getTextContent() and use Amaz.StringVector Conversion String ,please use\n' % (
                                fi)
                            effectLog.addEnglishErrorThing(msg)
                            effectLog.addJsonData(1, 'TEXT_2DV2', effectzip.zip_name, -1, msg, enmsg)
                    elif (lua_string.find('handleInputText') > 0):  # 说明是旧引擎文字贴纸
                        if (lua_string.find('getLuaTextContent') <= 0):
                            msg = 'error: file:%s text2DV2 handleInputText  送审文字接口需要添加接口getLuaTextContent()请添加' % (
                                fi)
                            enmsg = 'error: file:%s text2DV2 handleInputText  need getLuaTextContent(),please use\n' % (
                                fi)
                            effectLog.addEnglishErrorThing(msg)
                            effectLog.addJsonData(1, 'TEXT_2DV2', effectzip.zip_name, -1, msg, enmsg)
            except:
                return


# 检测函数是否是内建函数
# def checkFunctionIsIn(effectzip,effectLog):
#     return

# 检测是否有ARKIt 版本号
def checkARkitVersion(effectzip, effectLog):
    if ('ARKit' in effectzip.features):
        for fi in effectzip.files:
            temp_fis = fi.split('/')
            if ('extra.json' in temp_fis and '__MACOSX' not in temp_fis and temp_fis[-1] != '.DS_Store'):
                with open(fi, 'r') as f:
                    json_string = json.loads(f.read())
                    if ('worldTracking' in json_string and LooseVersion(effectzip.version) < '6.8.0'):
                        msg = "error file:%s 版本号错误. Config.json 版本号是 %s, ARKit+需要提高到 6.8.0." % (
                        effectzip.zip_name, effectzip.version)
                        enmsg = "error file:%s Wrong config version number. Config.json version number is %s, ARKit+worldTracking Please change the version number to 6.8.0." % (
                        effectzip.zip_name, effectzip.version)
                        effectLog.addEnglishErrorThing(msg)
                        effectLog.addJsonData(1, 'VERSION_ERROR', effectzip.zip_name, -1, msg, enmsg)

    return


# 检测AERender版本号
def checkAERenderVersion(effectzip, effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    if ('data.json' in list_dir and 'user_data.json' in list_dir and LooseVersion(effectzip.version) < '6.3.0'):
        msg = "error file:%s版本号错误 %s, AERender能力的版本号高于6.3.0." % (effectzip.zip_name, effectzip.version)
        enmsg = "error file:%s Wrong config version number. Config.json version number is %s, AERender Please change the version number to 6.3.0." % (
        effectzip.zip_name, effectzip.version)
        effectLog.addEnglishErrorThing(msg)
        effectLog.addJsonData(1, 'VERSION_ERROR', effectzip.zip_name, -1, msg, enmsg)


# 检测3dFaceMeshPerspective版本号
def check3dFaceMeshPerspectiveVersion(effectzip, effectLog):
    return


# 检测是否有禁止feature列表
def checkFeatureDisable(effectzip, effectLog, featureList):
    for feature in effectzip.features:
        if (feature in featureList):
            msg = 'error file:%s feature:%s 不能被使用' % (effectzip.zip_name, feature)
            enmsg = 'error file:%s feature:%s not be use' % (effectzip.zip_name, feature)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'DISABLE_FEATURE', effectzip.zip_name, -1, msg, enmsg)

    # features 是否amazingFeature


# 判断lua 版本号是不是正确的
def checkLuaVersion(effectzip, effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    i = -1
    version = '4.0.0'
    function = ''
    line = 0
    # 定义归一化函数初始值
    effect_stringList = []
    effect_numList = []

    if ('event.lua' in list_dir):
        lua_path = effectzip.zip_path + '/event.lua'
        stringList = []
        numList = {}
        with open(lua_path, 'r') as f:
            try:
                file_string = f.read()
                (stringList, numList) = participle(file_string)
            except:
                msg = "file:%s event.lua particple Error" % (effectzip.zip_name)
                effectLog.addEnglishErrorThing(msg)
        if (len(stringList) == 0 and LooseVersion(effectzip.version) < '4.0.0'):
            msg = 'config.json version is %s please change it to 4.0.0' % (effectzip.version)
            return

        myClassManager = parseFunction()
        name2ClassDic = {}
        # 处理eventHandles
        try:
            while (i < len(stringList)):
                # 判断function 是eventHandles function 还是外面的functions
                # print("test",len(stringList),stringList)
                if (stringList[i] == 'MattingEffect'):
                    i += 1
                    if (version < '6.0.0'):
                        version = '6.0.0'
                        continue
                if (stringList[i] == ':' and stringList[i + 2] == '('):
                    if (stringList[i + 1] in EffectData.coordinateList):
                        msg = (
                                'warning: 贴纸是用了坐标的贴纸，确认一下有没有用归一化处理 function = %s, line = %d \n' % (
                            stringList[i + 1], numList[i + 1]))
                        # effectLog.addEnglishErrorThing(msg)
                        effect_stringList.append(stringList[i + 1])
                        effect_numList.append(numList[i + 1])

                    if (stringList[i + 1] in EffectData.featureList):  # effect 调用基础函数
                        j = i - 1
                        while (stringList[j] != '=' and stringList[j] != '(' and stringList[j] != ')' and j > 0):
                            j -= 1
                        if (stringList[j] == '(' or stringList[j] == ')' or j == 0):
                            i += 1
                            continue
                        className = myClassManager.getfuncToReturnName(stringList[i + 1])

                        knum = i + 3
                        while (knum < len(stringList)):
                            while (stringList[knum] != ')'):
                                knum = knum + 1
                            if (stringList[knum + 1] == ':' and stringList[knum + 3] == '('):
                                tempClass = myClassManager.getClass(className)
                                if (tempClass != None):
                                    className = tempClass.getFunc(stringList[knum + 2])
                                    knum = knum + 4
                                else:
                                    break
                            else:
                                break

                        name2ClassDic[stringList[j - 1]] = myClassManager.getClass(className)
                        if (version < EffectData.featureList[stringList[i + 1]]):
                            version = EffectData.featureList[stringList[(i + 1)]]
                            function = stringList[i + 1]
                            line = numList[i + 1]
                    elif (stringList[i - 1] == 'this' or stringList[i - 1] == 'effect'):  # 这里的this指代effect，如果指代其他不支持
                        if (stringList[i - 2] == '='):  # 表明这里this 得到一个返回值
                            className = myClassManager.getfuncToReturnName(stringList[i + 1])
                            knum = i + 3
                            while (True and knum < len(stringList)):
                                while (stringList[knum] != ')'):
                                    knum = knum + 1
                                if (stringList[knum + 1] == ':' and stringList[knum + 3] == '('):
                                    tempClass = myClassManager.getClass(className)
                                    if (tempClass != None):
                                        className = tempClass.getFunc(stringList[knum + 2])
                                        knum = knum + 4

                                    else:
                                        break

                                else:
                                    break
                            if (myClassManager.getClass(className) != None):
                                name2ClassDic[stringList[i - 3]] = myClassManager.getClass(className)

                        tempClass = myClassManager.getClass('BEFEffect')
                        tempFunc = tempClass.getFunc(stringList[i + 1])
                        if (tempFunc != None):
                            if (version < tempFunc.version):
                                version = tempFunc.version
                                function = stringList[i + 1]
                                line = numList[i + 1]
                    else:
                        if (stringList[i - 1] in name2ClassDic):
                            if (name2ClassDic[stringList[i - 1]] != None):
                                tempFunc = name2ClassDic[stringList[i - 1]].getFunc(stringList[i + 1])
                                if (name2ClassDic[stringList[
                                    i - 1]].className == 'EffectManager' and tempFunc == None):  # EffectInterface 转换成 EffectManager 的todo
                                    tempFunc = myClassManager.getClass('EffectInterface').getFunc(stringList[i + 1])
                                if (tempFunc != None):
                                    if (stringList[i - 2] == '='):  # 在name2ClassDic 重新建立二阶查询
                                        if (myClassManager.getClass(tempFunc.returnName) != None):
                                            name2ClassDic[stringList[i - 3]] = myClassManager.getClass(
                                                tempFunc.returnName)

                                    if (version < tempFunc.version):
                                        version = tempFunc.version
                                        function = stringList[i + 1]
                                        line = numList[i + 1]
                        elif (stringList[i - 1] in EffectData.confirmFiled):  # 某些特殊字段还是当作二阶查询处理
                            tempClass = myClassManager.getClass(EffectData.confirmFiled[stringList[i - 1]])
                            tempFunc = tempClass.getFunc(stringList[i + 1])
                            if (tempFunc != None):
                                if (version < tempFunc.version):
                                    version = tempFunc.version
                                    function = stringList[i + 1]
                                    line = numList[i + 1]
                        else:
                            # 当作一阶函数处理
                            tempVersion = myClassManager.getFuncVersion(stringList[i + 1])
                            if (tempVersion != None):
                                if (version < tempVersion):
                                    version = tempVersion
                                    function = stringList[i + 1]
                                    line = numList[i + 1]
                elif (stringList[i] in EffectData.listCast):
                    j = i - 1
                    while (stringList[j] != '='):
                        j -= 1
                    className = myClassManager.getfuncToReturnName(stringList[i])
                    name2ClassDic[stringList[j - 1]] = myClassManager.getClass(className)
                    tempVersion = myClassManager.getFuncVersion(stringList[i])
                    if (tempVersion != None):
                        if (version < tempVersion):
                            version = tempVersion
                            function = stringList[i]
                            line = numList[i]
                elif (stringList[i] in EffectData.handleFuncList):  # 对handleFunction 处理
                    if (stringList[i] == 'handleFaceInfoEvent'):
                        name2ClassDic[stringList[i + 6]] = myClassManager.getClass('LuaFaceInfo')
                    elif (stringList[i] == 'handleGenderEvent'):
                        name2ClassDic[stringList[i + 6]] = myClassManager.getClass('LuaGenderInfo')
                    elif (stringList[i] == 'handleJointInfoEvent'):
                        name2ClassDic[stringList[i + 6]] = myClassManager.getClass('LuaJointInfo')
                    elif (stringList[i] == 'handleObjectEvent'):
                        name2ClassDic[stringList[i + 6]] = myClassManager.getClass('LuaObjectInfo')
                    elif (stringList[i] == 'handleAnimojiInfoEvent'):
                        name2ClassDic[stringList[i + 6]] = myClassManager.getClass('LuaAnimojiInfo')
                    elif (stringList[i] == 'handleHandInfoEvent'):
                        name2ClassDic[stringList[i + 6]] = myClassManager.getClass('LuaHandInfo')
                    elif (stringList[i] == 'handleSceneInfoEvent'):
                        name2ClassDic[stringList[i + 6]] = myClassManager.getClass('LuaSceneInfo')
                    elif (stringList[i] == 'handleSkeletonInfoEvent'):
                        name2ClassDic[stringList[i + 6]] = myClassManager.getClass('LuaSkeletonInfo')

                    if (version < EffectData.handleFuncList[stringList[i]]):
                        version = EffectData.handleFuncList[stringList[i]]
                        function = stringList[i]
                        line = numList[i]
                i += 1
        except:
            return
            # 定义归一化函数打印错误
        # if len(effect_stringList) !=0:
        #     msg = 'WARNING: 道具用了坐标函数，确认一下有没有用归一化处理 function = %s, line = %s \n'%(effect_stringList,effect_numList)
        #     enmsg = 'WARNING: The effect is used props, please confirm if normalization is used function = %s, line = %s\n'%(effect_stringList,effect_numList)
        #     effectLog.addJsonData(2,'WARNING',effectzip.zip_name,line,msg,enmsg)
        # LooseVersion
        # if(effectzip.version < version):
        if (LooseVersion(effectzip.version) < LooseVersion(version)):
            # print("effectzip.version",effectzip.version)
            msg = 'error: config.json版本为 %s, line = %d function = %s 请提高版本到 %s' % (
            effectzip.version, line, function, version)
            enmsg = 'error: config.json version %s, line = %d function = %s please change version to %s' % (
            effectzip.version, line, function, version)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'VERISON_ERROR', effectzip.zip_name, line, msg, enmsg)


# 检查资源包的lua 是不是判空了
def checkLuaIsNotNil(effectzip, effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    try:
        if ('event.lua' in list_dir):
            lua_path = effectzip.zip_path + '/event.lua'
            with open(lua_path, 'r') as f:
                file_string = f.read()
                stringList = []
                numList = {}
                try:
                    (stringList, numList) = participle(file_string)
                except:
                    msg = "file:%s event.lua particple Error" % (effectzip.zip_name)
                    effectLog.addEnglishErrorThing(msg)
                functionList = ['getFeature', 'addFeature', 'getAudioManager', 'getRenderCacheTexture',
                                'renderCacheFaceInfo', 'getPhotoAlgorithmResultByBitIndex', 'getBgInfo', 'maskInfo',
                                'maskdata']
                i = 0
                while (i < len(stringList)):
                    temp_str = stringList[i]
                    if (temp_str in functionList):
                        j = i - 1
                        while (stringList[j] != '='):
                            j -= 1
                        feature = stringList[j - 1]
                        i += 1
                        if (stringList[i + 5] in EffectData.listCast) or (stringList[i + 6] in EffectData.listCast):
                            i += 5
                        while (stringList[i] != feature and stringList[i] != '}' and i < len(stringList) - 1):
                            i += 1
                        if (i >= len(stringList) - 1):
                            continue
                        if (stringList[i + 1] == ':'):
                            msg = "file:%s event.lua function %s 文件没有判空, 函数路径=%d" % (
                            effectzip.zip_name, temp_str, numList[i + 1])
                            enmsg = "file:%s event.lua function %s doesn't check empty variable,please add, function line=%d" % (
                            effectzip.zip_name, temp_str, numList[i + 1])
                            effectLog.addEnglishErrorThing(msg)
                            effectLog.addJsonData(1, 'FEATURE_NOT_JUDGE_NIL', effectzip.zip_name, numList[i + 1], msg,
                                                  enmsg)
                            i += 1
                            continue

                        if (stringList[i - 2] in EffectData.listCast):
                            j = i - 1
                            while (stringList[j] != '='):
                                j -= 1
                            castFeature = stringList[j - 1]
                            while (stringList[i] != feature):
                                i += 1
                            i += 1
                            while (stringList[i] != castFeature and stringList[i] != feature and stringList[i] != '}'):
                                i += 1
                            if (stringList[i] == '}' or i >= len(stringList) - 1):
                                continue
                            if (stringList[i + 1] == ':'):
                                i += 1
                                msg = "file:%s event.lua function %s 文件没有判空, 函数路径为%d" % (
                                effectzip.zip_name, castFeature, numList[i + 1])
                                enmsg = "file:%s event.lua function %s doesn't check empty variable,please add, function line=%d" % (
                                effectzip.zip_name, temp_str, numList[i + 1])
                                effectLog.addEnglishErrorThing(msg)
                                effectLog.addJsonData(1, 'FEATURE_NOT_JUDGE_NIL', effectzip.zip_name, numList[i + 1],
                                                      msg, enmsg)

                    i += 1
        return
    except:
        return


def checkFileDisable(effectzip, effectLog, disableFiles, disableDirs):
    for di in effectzip.dirs:
        temp_di = di.split('/')
        for disDir in disableDirs:
            if (disDir in temp_di):
                # 展示多余文件夹的绝对路径
                disableDirs_path = di.split('/', 4)[4]
                msg = 'error: 含非法文件夹:%s,多余文件夹会占用包体积，若确认该文件无效，请打开vscode进行删除' % (disDir)
                enmsg = 'error: effect has diable dir%s,If confirm file is invalid, please open vscode to delete' % (
                    disDir)
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(1, 'FILE_DISABLE', disableDirs_path, -1, msg, enmsg)
    # 资源包所有文件绝对路径
    for fi in effectzip.files:
        temp_di = fi.split('/')
        for disfi in disableFiles:
            if (disfi in temp_di):
                msg = 'error: file:%s 文件夹含多余文件%s' % (effectzip.zip_name, disfi)
                enmsg = 'error: file:%s has diable dir%s' % (effectzip.zip_name, disDir)
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(1, 'FILE_DISABLE', effectzip.zip_name, -1, msg, enmsg)

    return


# 1 西瓜新渲染连资源包检测
def checkIsAmazingScene(effectzip, effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    if ('config.json' in list_dir):
        config_path = effectzip.zip_path + '/config.json'
        # print('独立config_path',config_path)
        with open(config_path, 'r') as f:
            config_string = json.loads(f.read())
            if ('effect' in config_string):
                effects = config_string['effect']
            if ('AmazingScene' in effects and effects['AmazingScene']['path'] != None):
                msg = 'error:这是新渲染链资源包'
                enmsg = 'this is a sticker package with New RenderChain mode'
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(2, 'Mino', effectzip.zip_name, -1, msg, enmsg)
            else:
                msg = 'error:这不是新渲染链资源包'
                enmsg = 'this is a sticker package with New RenderChain mode'
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(2, 'Mino', effectzip.zip_name, -1, msg, enmsg)


# 2  Tik Tok轻颜妆容搬运sdk版本检测
def checkIsFaceMakeup(effectzip, effectLog):
    # 打印出第一层文件名字
    list_dir = os.listdir(effectzip.zip_path)
    list_dir_lower = []
    for s in list_dir:
        list_dir_lower.append(s.lower())
    if ('facemakeupv2_bytool' in list_dir_lower):
        for fi in effectzip.files:
            fis = fi.split('/')
            if (fis[-1] == 'makeup.json'):
                with open(fi) as f:
                    makeup_string = json.loads(f.read())
                    if ('filters' in makeup_string):
                        filters = makeup_string['filters']
                        try:
                            fragShaderPath_value = filters[0]['fragShaderPath']
                            # print("轻颜妆",effectzip.version)
                            keyWord = "b'%Shader%@"
                            if ('Shader' in fragShaderPath_value and LooseVersion(effectzip.version) < '8.7.0'):
                                msg = "error file:%s ,资源包版本号为%s, 轻颜妆版本号需要≥8.7.0." % (
                                fis[-1], effectzip.version)
                                enmsg = "error file:%s ,Config.json version number is %s, fragShaderPath Please change the version number ≥ 8.7.0." % (
                                fis[-1], effectzip.version)
                                effectLog.addEnglishErrorThing(msg)
                                effectLog.addJsonData(1, 'VERSION_ERROR', fis[-1], -1, msg, enmsg)
                        except:
                            pass


# 3 检测新引擎指定文件'main.scene'是否做二进制
def checktobinary(effectzip, effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    keyWord_1 = "b'%SerializedFormat%@"
    keyWord_2 = 'b"%SerializedFormat%@'
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'main.scene'):
            with open(fi, "rb") as f:
                fileStr = f.read()
                if keyWord_1 not in str(fileStr) and keyWord_2 not in str(fileStr):
                    msg = 'error:"main.scene"文件没有转二进制，请继续检查main.scene，Material和mesh三个文件都需要转二进制'
                    enmsg = 'error:"main.scene" did not to binary，please check main.scene，Material、mesh need to binary'
                    effectLog.addEnglishErrorThing(msg)
                    effectLog.addJsonData(1, 'ToBinary_ERROR', effectzip.zip_name, -1, msg, enmsg)


# 4 faceu中特效能力与loki设置版本信息的匹配检测
def checkFaceuVersion(effectzip, effectLog, lokiInformation):
    # 传入loki
    effect_data = json.loads(lokiInformation)
    # print("函数",effect_data)

    # 4.1 获取faceu资源包中特效能力列表
    # effect_data = EffectData.faceu_json_data
    json_data = json.dumps(effect_data)
    data = json.loads(json_data)
    effectFileTypes = data['effectFileTypes']
    effectRequirements = data['effectRequirements']
    systemList = data['systemList']
    faceu_effect_list = effectFileTypes + effectRequirements + systemList
    if len(faceu_effect_list) == 0:
        # print("传入特效信息为空")
        return
    appVersionIosMin = data['appVersionIosMin']
    # print("loki最低配置",appVersionIosMin)
    appVersionAndroidMin = data['appVersionAndroidMin']

    # 4.2.1 IOS：获取faceu特效能力中最大的版本配置
    verison_ios_list = {}
    effect_ios_version = EffectData.faceu_effect_ios_version
    for v in faceu_effect_list:
        if v not in effect_ios_version:
            verison_ios_list[v] = "00.00.00"
        else:
            verison_ios_list[v] = effect_ios_version[v]
    max_ios_version = max(verison_ios_list.values())
    # print("最大版本号：",max_ios_version)
    new_dict = {v: k for k, v in verison_ios_list.items()}
    max_ios_version_effect = new_dict[max_ios_version]
    # print("最大版本effect：",max_ios_version_effect)

    # 4.2.2 IOS：对资源包特效版本号限制与loki配置进行比较
    if LooseVersion(max_ios_version) > LooseVersion(appVersionIosMin):
        msg = 'error:ios最低版本号Loki配置错误，%s能力最低版本号限制%s，请将%s修改至%s及以上' % (
        max_ios_version_effect, max_ios_version, appVersionIosMin, max_ios_version)
        enmsg = 'error:ios Minimum version number configuration error，the feature:%s Minimum version %s，Please Change ≥ %s' % (
        max_ios_version_effect, max_ios_version, max_ios_version)
        effectLog.addEnglishErrorThing(msg)
        effectLog.addJsonData(1, 'Loki_appVersionIosMin_ERROR', effectzip.zip_name, -1, msg, enmsg)

    # 4.3.1 android：获取faceu特效能力中最大的版本配置
    verison_android_list = {}
    effect_android_version = EffectData.faceu_effect_android_version
    for v in faceu_effect_list:
        if v not in effect_android_version:
            verison_android_list[v] = "00.00.00"
        else:
            verison_android_list[v] = effect_android_version[v]
    max_android_version = max(verison_android_list.values())
    # print("最大版本号：",max_android_version)
    new_dict = {v: k for k, v in verison_android_list.items()}
    max_android_version_effect = new_dict[max_android_version]
    # print("最大版本effect：",max_android_version_effect)

    # 4.3.2 android：对资源包特效版本号限制与loki配置进行比较
    if LooseVersion(max_android_version) > LooseVersion(appVersionAndroidMin):
        msg = 'error:Android最低版本号Loki配置错误，%s能力最低版本号限制%s，请将%s修改至%s及以上' % (
        max_android_version_effect, max_android_version, appVersionAndroidMin, max_android_version)
        enmsg = 'error:Android Minimum version number configuration error，the feature:%s Minimum version %s，Please Change ≥ %s' % (
        max_android_version_effect, max_android_version, max_android_version)
        effectLog.addEnglishErrorThing(msg)
        effectLog.addJsonData(1, 'Loki_appVersionAndroidMin_ERROR', effectzip.zip_name, -1, msg, enmsg)


# 5.1 颜郑明 checkQingyanVersion中特效能力与loki设置版本信息的匹配检测
def checkQingyanVersion(effectzip, effectLog, lokiInformation):
    # 传入loki
    effect_data = json.loads(lokiInformation)
    # print("函数",effect_data)

    # 5.0_获取Qingyan资源包中特效能力列表
    # effect_data = EffectData.faceu_json_data
    json_data = json.dumps(effect_data)
    data = json.loads(json_data)
    effectFileTypes = data['effectFileTypes']
    effectRequirements = data['effectRequirements']
    systemList = data['systemList']
    Qingyan_effect_list = effectFileTypes + effectRequirements + systemList
    if len(Qingyan_effect_list) == 0:
        # print("传入特效信息为空")
        return
    appVersionIosMin = data['appVersionIosMin']
    # print("loki最低配置",appVersionIosMin)
    appVersionAndroidMin = data['appVersionAndroidMin']

    # 5.1.1_IOS：获取Qingyan特效能力中最大的版本配置
    verison_ios_list = {}
    effect_ios_version = EffectData.qingyan_effect_ios_version
    for v in Qingyan_effect_list:
        if v not in effect_ios_version:
            verison_ios_list[v] = "00.00.00"
        else:
            verison_ios_list[v] = effect_ios_version[v]
    max_ios_version = max(verison_ios_list.values())
    # print("最大版本号：",max_ios_version)
    new_dict = {v: k for k, v in verison_ios_list.items()}
    max_ios_version_effect = new_dict[max_ios_version]
    # print("最大版本effect：",max_ios_version_effect)

    # 5.1.2_IOS：对资源包特效版本号限制与loki配置进行比较
    if LooseVersion(max_ios_version) > LooseVersion(appVersionIosMin):
        msg = 'error:轻颜ios最低版本号Loki配置错误，%s能力最低版本号限制%s，请将%s修改至%s及以上' % (
        max_ios_version_effect, max_ios_version, appVersionIosMin, max_ios_version)
        enmsg = 'error:ios Minimum version number configuration error，the feature:%s Minimum version %s，Please Change ≥ %s' % (
        max_ios_version_effect, max_ios_version, max_ios_version)
        effectLog.addEnglishErrorThing(msg)
        effectLog.addJsonData(1, 'Loki_appVersionIosMin_ERROR', effectzip.zip_name, -1, msg, enmsg)

    # 5.2.1_android：获取Qingyan特效能力中最大的版本配置
    verison_android_list = {}
    effect_android_version = EffectData.qingyan_effect_android_version
    for v in Qingyan_effect_list:
        if v not in effect_android_version:
            verison_android_list[v] = "00.00.00"
        else:
            verison_android_list[v] = effect_android_version[v]
    max_android_version = max(verison_android_list.values())
    # print("最大版本号：",max_android_version)
    new_dict = {v: k for k, v in verison_android_list.items()}
    max_android_version_effect = new_dict[max_android_version]
    # print("最大版本effect：",max_android_version_effect)

    # 5.2.2_android：对资源包特效版本号限制与loki配置进行比较
    if LooseVersion(max_android_version) > LooseVersion(appVersionAndroidMin):
        msg = 'error:轻颜Android最低版本号Loki配置错误，%s能力最低版本号限制%s，请将%s修改至%s及以上' % (
        max_android_version_effect, max_android_version, appVersionAndroidMin, max_android_version)
        enmsg = 'error:Android Minimum version number configuration error，the feature:%s Minimum version %s，Please Change ≥ %s' % (
        max_android_version_effect, max_android_version, max_android_version)
        effectLog.addEnglishErrorThing(msg)
        effectLog.addJsonData(1, 'Loki_appVersionAndroidMin_ERROR', effectzip.zip_name, -1, msg, enmsg)


# 5.2 何泽 轻颜bach最低版本号≥970
def check_qingyan_bachversion(effectzip, effectLog):
    fi = get_Filepath(effectzip, 'config.json')
    if fi != None:
        with open(fi) as f:
            Config_string = json.loads(f.read())
            if ('bALG_BACH_CONFIG' in Config_string and Config_string['bALG_BACH_CONFIG'] == True):
                if LooseVersion(effectzip.version) < '9.7.0':
                    msg = '轻颜接入bach最低版本号要大于等于9.7.0，请修改configjson版本号'
                    enmsg = 'bach the min version is 970'
                    effectLog.addEnglishErrorThing(msg)
                    effectLog.addJsonData(1, 'Bach_Version_Error', effectzip.zip_name, -1, msg, enmsg)


# 6 西瓜mimo和mv资源包与loki面板配置检测
def checkXiguaPanelKey(effectzip, effectLog, lokiInformation):
    list_dir = os.listdir(effectzip.zip_path)
    XiaguaAttributes = ""
    pancelKey = ""
    if ('config.json' in list_dir):
        config_path = effectzip.zip_path + '/config.json'
        # print('独立config_path',config_path)
        with open(config_path, 'r') as f:
            config_string = json.loads(f.read())
            if ('effect' in config_string):
                effects = config_string['effect']
            if ('AmazingScene' in effects and effects['AmazingScene']['path'] != None):
                XiaguaAttributes = "MIMO"
            if ('AmazingAEAnimation' in config_string):
                XiaguaAttributes = "MV"
    if ('data.json' in list_dir and 'user_data.json' in list_dir):
        XiaguaAttributes = "MV"
    effect_data = json.loads(lokiInformation)
    # 6.0_获取xigua资源包中特效能力列表
    # effect_data = EffectData.faceu_json_data
    json_data = json.dumps(effect_data)
    data = json.loads(json_data)
    panelKey = data['panelKey']
    # print(XiaguaAttributes)
    # print(str(pancelKey))
    if (str(panelKey) == "propsindex"):
        if (XiaguaAttributes == "MIMO" or XiaguaAttributes == "MV"):
            msg = 'error:Loki面板配置错误,该资源包类型为%s,[首页道具propsindex]只支持非Mimo和非MV格式的道具包' % (
                XiaguaAttributes)
            enmsg = 'error:Loki panel configuration error, the resource pack type is%s,propsindex only supports non-Mimo and non-MV' % (
                XiaguaAttributes)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'Loki_PanelKey_ERROR', effectzip.zip_name, -1, msg, enmsg)
    elif (str(panelKey) == "prossynthesis"):
        if XiaguaAttributes != "MV":
            msg = 'error:Loki面板配置错误,该资源包类型为非MV格式道具,[合成道具prossynthesis]只支持MV格式的道具包'
            enmsg = 'error:Loki panel configuration error, the resource pack type is%s,prossynthesis only supports MV' % (
                XiaguaAttributes)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'Loki_PanelKey_ERROR', effectzip.zip_name, -1, msg, enmsg)
    elif (str(panelKey) == "props"):
        if XiaguaAttributes == "MV":
            msg = 'error:Loki面板配置错误,该资源包类型为%s,[拍摄道具props]只支持非MV格式的道具包' % (XiaguaAttributes)
            enmsg = 'error:Loki panel configuration error, the resource pack type is%s,props only supports non-MV' % (
                XiaguaAttributes)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'Loki_PanelKey_ERROR', effectzip.zip_name, -1, msg, enmsg)
    elif (str(panelKey) == "shoot-props-test"):
        if XiaguaAttributes == "MV":
            msg = 'error:Loki面板配置错误,该资源包类型为%s,[内测版拍摄道具test]只支持非MV格式的道具包' % (
                XiaguaAttributes)
            enmsg = 'error:Loki panel configuration error, the resource pack type is%s,shoot-props-test only supports non-MV' % (
                XiaguaAttributes)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'Loki_PanelKey_ERROR', effectzip.zip_name, -1, msg, enmsg)


"""
Start: 检测点7------检测图片大小及尺寸
"""


# 7 检测单张图片体积大小及尺寸
def get_size(path, unit='MB'):
    from PIL import Image
    f_size = os.path.getsize(path)
    if unit.lower() == 'mb':
        f_size = float(f_size) / float(1024 * 1024)
    elif unit.lower() == 'kb':
        f_size = float(f_size) / float(1024)
    else:
        f_size = float(f_size)
    return round(f_size, 2)


# 获取图片分辨率 长*宽
def get_img_size(img_path):
    from PIL import Image
    img = Image.open(img_path)
    return img.size


# 获取资源包所有后缀为png的图片列表详细信息
def effect_get_pics_info(effectzip, effectLog):
    from PIL import Image
    pic_list = effectzip.png + effectzip.gif

    pic_info_list = []
    try:
        for pic_path in pic_list:
            if '__MACOSX' in pic_path:
                continue
            # 获取实际的图片路径，注意不要把整体路径打印出来会有安全问题
            pic_related_path = pic_path.split('/', 4)[4]
            pic_size = get_size(pic_path, unit='KB')
            width, height = get_img_size(pic_path)
            pic_info = {
                'name': pic_related_path,
                'size': pic_size,
                'pixel': '{}*{}'.format(width, height)
            }
            pic_info_list.append(pic_info)
        return pic_info_list
    except:
        import traceback
        # print (traceback.format_exc())
        msg = "图片过大"
        enmsg = "Decompressed Data Too Large"
        effectLog.addEnglishErrorThing(msg)
        effectLog.addJsonData(1, 'PNG_SIZE_ERROR', effectzip.zip_name, -1, msg, enmsg)
        return pic_info_list


# 判定图片大小
def check_pics(pics, maxsize, standa, standb):
    abnormitypicsize = []
    if standa > standb:
        standa, standb = standb, standa
    for pic in pics:
        size = float(pic['size'])
        pixela = int(pic['pixel'].split('*')[0])
        pixelb = int(pic['pixel'].split('*')[1])
        if size > maxsize or pixela > standa or pixelb > standb:
            abnormitypicsize.append(pic)
    return abnormitypicsize


def check_pics_size(param, effectzip, effectLog, lokiInformation=None):
    if (param == 'DEFAULT'):
        max_size = EffectData.qingyan_max_size  # 表示图片大小上限, 需要调整的话修改data数据
        pixela = EffectData.qingyan_pixela  # 表示像素上限，需要调整的话修改data数据
        pixelb = EffectData.qingyan_pixela
    elif (param == 'FACEU'):
        max_size = EffectData.faceu_max_size
        pixela = EffectData.faceu_pixela
        pixelb = EffectData.faceu_pixela
    elif (param == 'QINGYAN'):
        max_size = EffectData.qingyan_max_size
        pixela = EffectData.qingyan_pixela
        pixelb = EffectData.qingyan_pixela
    elif (param == 'DOUYIN' or param == 'XIGUA'):
        max_size = EffectData.douyin_max_size
        pixela = EffectData.douyin_pixela
        pixelb = EffectData.douyin_pixela
    elif (param == 'TIKTOK'):
        max_size = EffectData.tiktok_max_size
        pixela = EffectData.tiktok_pixela
        pixelb = EffectData.tiktok_pixela
    elif (param == 'CAPCUT'):
        max_size = EffectData.capcut_max_size
        pixela = EffectData.capcut_pixela
        pixelb = EffectData.capcut_pixelb
    DYAME_prefab = ['effecttooldefault', 'effecttoolfirstobject', 'effecttoolsecondobject', 'effecttoolmakeup',
                    'effecttoolfilterprefab', 'effecttooleffect', 'effecttooldeformation', 'effecttoolliquify',
                    'ame_3d_accessory', 'ame_gan']
    DYAME_2D = ['ame_foreground_sticker', 'ame_face_tracking_sticker', 'ame_face_sticker']
    TTAME_prefab = ['effecttooldefault', 'effecttooltemplates', 'effecttoolfirstobject', 'effecttoolsecondobject',
                    'effecttoolliquify', 'effecttoolfacestretch', 'effecttoolmakeupstyle', 'effecttoolfilterprefab',
                    'effecttoolprefabeffect']
    TTAME_2D = ['ame_foreground_sticker', 'ame_face_tracking_sticker', 'ame_face_sticker', 'ame_background_sticker',
                'ame_hand_tracking_sticker']
    try:
        effect_data = json.loads(lokiInformation)
        panelKey = effect_data.get('panelKey')
        print(panelKey)
        if panelKey in DYAME_2D or panelKey in TTAME_2D:
            # AME-2D-静态贴纸
            if len(effectzip.png) == 1:
                max_size = EffectData.ame_max_png_size
                pixela = EffectData.ame_png_pixela
                pixelb = EffectData.ame_png_pixelb
            # AME-2D-序列帧贴纸、gif 贴纸
            else:
                max_size = EffectData.ame_max_pngs_size
                pixela = EffectData.ame_pngs_pixela
                pixelb = EffectData.ame_pngs_pixelb
            # 判断数量是否小于20
            if len(effectzip.png) >= 20 or len(effectzip.gif) >= 20:
                msg = "图片数量超出限制（20）"
                enmsg = "The number of pictures exceeded the limit (20)."
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(1, 'PNG_NUM_ERROR', effectzip.zip_name, -1, msg, enmsg)
        elif panelKey in DYAME_prefab or panelKey in TTAME_prefab:
            max_size = EffectData.ame_max_prefab_size
            pixela = EffectData.ame_prefab_pixela
            pixelb = EffectData.ame_prefab_pixelb
    except:
        pass
    # pic_info_list = []
    pics = effect_get_pics_info(effectzip, effectLog)
    # if len(pic_info_list) != 0:
    ret = check_pics(pics, max_size, pixela, pixelb)
    if len(ret) == 0:
        # print("图片大小检查通过")
        return
    else:
        # print("基准说明：大小：{}KB 分辨率：{}*{}".format(max_size, pixela, pixelb))
        # print("不通过详情：")
        # for r in ret:
        #     print(r)
        msg = "%s png基准说明：大小为%sKB,分辨率为%s*%s;该资源包中不通过PNG详情如下%s，请按标准重新修改" % (
        param, max_size, pixela, pixelb, ret)
        enmsg = "%s PNG Standard: The size %sKB, The resolution %s*%s;the fail png list is%s please re-edit" % (
        param, max_size, pixela, pixelb, ret)
        effectLog.addEnglishErrorThing(msg)
        effectLog.addJsonData(1, 'PNG_SIZE_ERROR', effectzip.zip_name, -1, msg, enmsg)
    """
End::------------------------
"""


"""
Start: 检测点8------检测轻颜和faceu的RT复用
"""


def check_effect_rt_reuse(effectzip):
    rt_abnormal = []
    check_type = ['2DStickerV3', '3DStickerV3', 'FaceMakeupV2', 'GeneralEffect', 'Filter']
    list_dir = os.listdir(effectzip.zip_path)
    if ('config.json' in list_dir):
        config_path = effectzip.zip_path + '/config.json'
        with open(config_path, "rb") as f:
            config_string = json.loads(f.read())
            try:
                link = config_string['effect']['Link']
                for item in link:
                    if 'type' in item and item['type'] in check_type:
                        if 'rtshare' in item:
                            rt_abnormal.append({
                                "type": item['type'],
                                "rtShare": "请修改大小写，rtshare->rtShare"
                            })
                        elif 'rtShare' not in item:
                            rt_abnormal.append({
                                "type": item['type'],
                                "rtShare": "无rtShare"
                            })
                        elif item["rtShare"] is not True:
                            rt_abnormal.append({
                                "type": item['type'],
                                "rtShare": item['rtShare']
                            })
            except:
                return
    return rt_abnormal


def check_rt_reuse(effectzip, effectLog):
    rtshare = check_effect_rt_reuse(effectzip)
    try:
        if len(rtshare) == 0:
            # print("RT复用检查通过")
            return
        else:
            # for rt in rtshare:
            # print(rt)
            msg = "RT复用检查错误，详细出错如下%s" % (rtshare)
            enmsg = "RT multiplexing check error, the detailed is%s" % (rtshare)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'RT_check_ERROR', effectzip.zip_name, -1, msg, enmsg)
    except:
        return


"""
End:------------------------
"""

"""
Start: 检测点9------美妆互斥,需要检测俩个文件，且同时满足
    1. config.json文件里需要有
        "exclusiveScene": [
            {
                "priority": 9999,
                "sceneKey": "FaceMakeup*",
                "tagName": [
                    "FaceMakeupV2_byTool/"
                ]
            }
        ]
    2. extra.json里有
        "settings":{
            "disableExtMakeup": 1
        }
    :param effect_path:
    :return:
"""


def check_makeup_opposite(effectzip):
    makeup_oppo = []
    config_path = effectzip.zip_path + '/config.json'
    extra_ptah = effectzip.zip_path + '/extra.json'
    # print("地址：",config_path,extra_ptah)

    if 'FaceMakeupV2' in effectzip.features:
        try:
            if os.path.exists(config_path):
                fconfig = open(config_path)
                config = json.load(fconfig)
                if 'exclusiveScene' in config['effect']:
                    comp_dict = config['effect']['exclusiveScene'][0]
                    if 'sceneKey' not in comp_dict:
                        makeup_oppo.append('config.json下exclusiveScene字段内没有sceneKey参数')
                    elif comp_dict['sceneKey'] != 'FaceMakeup*':
                        makeup_oppo.append('config.json下exclusiveScene字段格式错误，sceneKey={}'.format(
                            config['effect']['exclusiveScene'][0]['sceneKey']))
                else:
                    makeup_oppo.append('config.json下没有exclusiveScene字段')
                fconfig.close()
            if os.path.exists(extra_ptah):
                fextra = open(extra_ptah)
                extra = json.load(fextra)
                if 'disableExtMakeup' in extra['settings']:
                    if extra['settings']['disableExtMakeup'] != 1:
                        makeup_oppo.append(
                            'extra.json下disableExtMakeup值为{}'.format(extra['settings']['disableExtMakeup']))
                else:
                    makeup_oppo.append('extra.json下没有disableExtMakeup字段')
        except Exception as e:
            # print("美妆互斥解析出错: {}".format(e))
            return
        return makeup_oppo


def check_effect_makeup_opposite(effectzip, effectLog):
    makeup_oppo = check_makeup_opposite(effectzip)
    try:
        if len(makeup_oppo) == 0:
            return
            # print("美妆互斥检查通过")
        else:
            msg = "美妆互斥检查错误，详细出错如下%s" % (makeup_oppo)
            enmsg = "Makeup_opposite check error, the detailed is%s" % (makeup_oppo)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'Makeup_Opposite_ERROR', effectzip.zip_name, -1, msg, enmsg)
    except:
        return


"""
End::------------------------
"""
"""
Start: 检测点10------睫毛检查
"""


def get_json_files(effectzip):
    makeup_files_json = []
    for path in effectzip.files:
        # 获取所有文件路径的后缀，取出后缀为.json的文件
        makeup_files = os.path.splitext(path)[1]
        if makeup_files == ".json":
            makeup_files_json.append(path)
    # print("makeup_files文件是啥:",makeup_files_json)
    return makeup_files_json


def check_eyelash(effectzip, effectLog):
    """
    检查睫毛是否存在
    :param effect_path: 贴纸包路径(非zip包)
    :return: True/False
    """
    eyelash = []
    makeup_files = get_json_files(effectzip)
    makeup_jsons = []
    for file in makeup_files:
        if 'makeup.json' in file and '__MACOSX' not in file:
            makeup_jsons.append(file)
    # print("3次：",makeup_jsons)
    # 开始检查文件
    for file in makeup_jsons:
        with open(file) as f:
            makeup_detail = json.load(f)
            filters = makeup_detail['filters']
            for filter in filters:
                if '2d_sequence_resources' in filter and 'lash' in filter['2d_sequence_resources']['path']:
                    p = file.replace(effectzip.zip_path, '')
                    eyelash.append(
                        '{}睫毛检查：path={}, filterType={}'.format(p, filter['2d_sequence_resources']['path'],
                                                                   filter['filterType']))
                    # print("睫毛类型：",filter['filterType'])
                    if filter['filterType'] != "jiemao_faceu":
                        msg = "睫毛检查不通过，该睫毛类型为%s,应该修改为jiemao_faceu" % (filter['filterType'])
                        enmsg = "eyelash check does not pass, eyelash type is%s, please modify according to the standard" % (
                        filter['filterType'])
                        effectLog.addEnglishErrorThing(msg)
                        effectLog.addJsonData(1, 'eyelash_qingyan_ERROR', file, -1, msg, enmsg)
            return eyelash


"""
End:------------------------
"""


# 7 ObjectTrack字段检测
def checkObjectTrack(effectzip, effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    if ('config.json' in list_dir):
        config_path = effectzip.zip_path + '/config.json'
        with open(config_path, 'r') as f:
            config_string = json.loads(f.read())
            if ('effect' in config_string):
                effect = config_string['effect']
                if ('algorithmConfigs' in effect):
                    algorithmConfigs = effect['algorithmConfigs']
                    ObjectTrack_vakue = algorithmConfigs[0]['name']
                    if (ObjectTrack_vakue == 'ObjectTrack' and LooseVersion(effectzip.version) < '9.5.0'):
                        msg = "error file:%s ,资源包版本号为%s, 使用ObjectTrack算法的资源包版本需要≥9.5.0." % (
                        'config.json', effectzip.version)
                        enmsg = "error file:%s ,Config.json version number is %s, Please change the version number ≥ 9.5.0." % (
                        'config.json', effectzip.version)
                        effectLog.addEnglishErrorThing(msg)
                        effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)
    list_dir_lower = []
    for s in list_dir:
        list_dir_lower.append(s.lower())
    if ('amazingfeature' in list_dir_lower):
        for fi in effectzip.files:
            fis = fi.split('/')
            if (fis[-1] == 'content.json'):
                with open(fi) as f:
                    config_string = json.loads(f.read())
                    if ('requirement' in config_string):
                        requirement = config_string['requirement']
                        if ('ObjectTrack' in requirement and LooseVersion(effectzip.version) < '9.5.0'):
                            msg = "error file:%s ,资源包版本号为%s, 使用ObjectTrack算法的资源包版本需要≥9.5.0." % (
                            'content.json', effectzip.version)
                            enmsg = "error file:%s ,Config.json version number is %s, Please change the version number ≥ 9.5.0." % (
                            'config.json', effectzip.version)
                            effectLog.addEnglishErrorThing(msg)
                            effectLog.addJsonData(1, 'VERSION_ERROR', 'content.json', -1, msg, enmsg)


# 9 检测资源包体积
'''获取文件的大小,结果保留两位小数，单位为MB'''


def get_FileSize(effectzip, effectLog, param):
    filePath = effectzip.zip_path + '.zip'
    # print("文件路径：",filePath)
    fsize = os.path.getsize(filePath)
    fsize = float(fsize) / float(1024 * 1024)
    effect_size = round(fsize, 2)
    # print("资源包体积为:",effect_size)
    if (param == 'DEFAULT'):
        max_zip_size = EffectData.douyin_zip_size  # 表示图片大小上限, 需要调整的话修改data数据
    elif (param == 'FACEU'):
        max_zip_size = EffectData.faceu_zip_size
    elif (param == 'QINGYAN'):
        max_zip_size = EffectData.qingyan_zip_size
    elif (param == 'DOUYIN' or param == 'XIGUA'):
        max_zip_size = EffectData.douyin_zip_size
    elif (param == 'TIKTOK'):
        max_zip_size = EffectData.tiktok_zip_size
    elif (param == 'CAPCUT'):
        max_zip_size = EffectData.capcut_zip_size
    # print(max_zip_size)
    if effect_size > max_zip_size:
        msg = "资源包体积过大 %s业务线,zip资源包最大为限制%s, 该资源包为%s,请压缩包大小" % (
        param, max_zip_size, effect_size)
        enmsg = "package size to large %sthe size limit%s, this effect size is %s,please modify it according to the standard" % (
        param, max_zip_size, effect_size)
        effectLog.addEnglishErrorThing(msg)
        effectLog.addJsonData(1, 'ZIP_SIZE_ERROR', 'content.json', -1, msg, enmsg)


# 10 Tiktok版本号检测
def checkTiktokVersion(effectzip, effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    if ('config.json' in list_dir):
        if (LooseVersion(effectzip.version) >= '7.7.0' and LooseVersion(effectzip.version) <= '8.6.0'):
            msg = "error file:%s ,资源包版本号为%s, Tiktok无此版本号，请修正为8.7.0." % (
            'config.json', effectzip.version)
            enmsg = "error file:%s ,Config.json version number is %s, Please change the version number to 8.7.0." % (
            'config.json', effectzip.version)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)
        if (LooseVersion(effectzip.version) >= '7.3.0' and LooseVersion(effectzip.version) <= '7.5.0'):
            msg = "error file:%s ,资源包版本号为%s, Tiktok无此版本号，请修正为7.6.0." % (
            'config.json', effectzip.version)
            enmsg = "error file:%s ,Config.json version number is %s, Please change the version number to 7.6.0." % (
            'config.json', effectzip.version)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)

        # 11 config.json中zorder一致的检测


def checkSameZorder(effectzip, effectLog):
    zorder_list = effectzip.zorder
    set_zorder_list = set(zorder_list)
    if (len(set_zorder_list) != len(zorder_list)):
        msg = "config.json文件中zorder值存在一致，需要修改为不一致"
        enmsg = "config.json has same zorder,Please change it different"
        effectLog.addEnglishErrorThing(msg)
        effectLog.addJsonData(1, 'SAME_Zoder_ERROR', 'config.json', -1, msg, enmsg)


# 12 检测资源包的shader代码（老引擎：.vsh， .fsh，新引擎：.vert，.frag）
def check_shader(effectzip, effectLog):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR_tool_frag = BASE_DIR + " &&glslangValidator -S frag "
    BASE_DIR_tool_vert = BASE_DIR + " &&glslangValidator -S vert "

    for fsh in effectzip.fsh:
        # print(fsh)
        fsh_shell = "cd " + BASE_DIR_tool_frag + fsh
        # print(fsh_shell)
        # fsh_shell = "cd /Users/bytedance/Desktop/gitlab_luaauto/effect_file_utils/luaAuto/newLuaAuto &&glslangValidator -S frag "+fsh
        # print(fsh_shell)
        try:
            fsh_shell_error = os.popen(fsh_shell)
            fsh_shader_error = fsh_shell_error.read()
            # print(fsh_shader_error)
            if len(fsh_shader_error) != 0:
                msg = "fsh文件语法编译报错，详细如下%s请完成修复" % (fsh_shader_error)
                enmsg = "fsh_Shader_ERROR%s" % (fsh_shader_error)
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(1, 'fsh_Shader_ERROR', fsh, -1, msg, enmsg)
        except:
            pass
    for vsh in effectzip.vsh:
        # print(effectzip.vsh)
        # vsh_shell = "cd /Users/bytedance/Desktop/gitlab_luaauto/effect_file_utils/luaAuto/newLuaAuto &&glslangValidator -S vert "+vsh
        vsh_shell = "cd " + BASE_DIR_tool_vert + vsh
        vsh_shell_error = os.popen(vsh_shell)
        vsh_shader_error = vsh_shell_error.read()
        # print(vsh_shader_error)
        if len(vsh_shader_error) != 0:
            msg = "vsh文件语法编译报错，详细如下%s请完成修复" % (vsh_shader_error)
            enmsg = "vsh shader error%s" % (fsh_shader_error)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'vsh_Shader_ERROR', vsh, -1, msg, enmsg)
    for vert in effectzip.vert:
        # vert_shell = "cd /Users/bytedance/Desktop/gitlab_luaauto/effect_file_utils/luaAuto/newLuaAuto &&glslangValidator -S vert "+vert
        vert_shell = "cd " + BASE_DIR_tool_vert + vert
        vert_shell_error = os.popen(vert_shell)
        vert_shader_error = vert_shell_error.read()
        # print(vsh_shader_error)
        if len(vsh_shader_error) != 0:
            msg = "vert文件语法编译报错，详细如下%s请完成修复" % (vert_shader_error)
            enmsg = "vert shader error%s" % (fsh_shader_error)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'vert_Shader_ERROR', vert, -1, msg, enmsg)
    for frag in effectzip.frag:
        # frag_shell = "cd /Users/bytedance/Desktop/gitlab_luaauto/effect_file_utils/luaAuto/newLuaAuto &&glslangValidator -S frag "+frag
        fsh_shell = "cd " + BASE_DIR_tool_frag + frag
        frag_shader_error = frag_shell_error.read()
        # print(vsh_shader_error)
        if len(vsh_shader_error) != 0:
            msg = "frag文件语法编译报错，详细如下%s请完成修复" % (frag_shader_error)
            enmsg = "frag shader error%s" % (fsh_shader_error)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1, 'frag_Shader_ERROR', frag, -1, msg, enmsg)


# 12 调用Amaz.Guid函数最低版本号检测
def checkAmazGuidVersion(effectzip, effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    if ('AmazingFeature' in list_dir):
        AmazingFeature_path = effectzip.zip_path + '/AmazingFeature'
        list1_dir = os.listdir(AmazingFeature_path)
        if ('lua' in list1_dir):
            lua_path = AmazingFeature_path + '/lua'
            list2_dir = os.listdir(lua_path)
            if ('GraphSystem.lua' in list2_dir):
                GraphSystemlua_path = lua_path + '/GraphSystem.lua'
                with open(GraphSystemlua_path, 'r') as f:
                    file_string = f.read()
                    if ('Amaz.Guid' in file_string):
                        try:
                            # print(effectzip.version)
                            if (LooseVersion(effectzip.version) < '8.7.0'):
                                msg = "error file:%s ,资源包版本号为%s, 调用Amaz.Guid函数最低版本号需要≥8.7.0." % (
                                'config.json', effectzip.version)
                                enmsg = "error file:%s ,Config.json version number is %s, please change the version number ≥ 8.7.0." % (
                                'config.json', effectzip.version)
                                effectLog.addEnglishErrorThing(msg)
                                effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)
                        except:
                            pass

                        # 13 通用方法获取指定文件路径


def get_Filepath(effectzip, filename):
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == filename):
            # print(fi)
            return fi


# 14 剪映最低版本号检测：
# 字典合并，使用 **，函数将参数以字典的形式导入
def Merge(dict1, dict2, dict3):
    res = {**dict1, **dict2, **dict3}
    return res


def Merge_2(dict1, dict2):
    res = {**dict1, **dict2}
    return res


# config.json 确定走bach还是非bach
def check_is_bach(effectzip, effectLog):
    fi = get_Filepath(effectzip, 'config.json')
    if fi != None:
        with open(fi) as f:
            Config_string = json.loads(f.read())
            if ('bALG_BACH_CONFIG' in Config_string and Config_string['bALG_BACH_CONFIG'] == True):
                # print("bach")
                effect_version = Merge(EffectData.capcut_effect_requirement_version,
                                       EffectData.capcut_effect_bach_version, EffectData.capcut_effect_system_version)
            else:
                # print("not bach")
                effect_version = Merge_2(EffectData.capcut_effect_requirement_version,
                                         EffectData.capcut_effect_system_version)
            return effect_version


def check_capcut_version(effectzip, effectLog):
    effect_list = effectzip.features + effectzip.content_requirements + effectzip.algorithmConfig + effectzip.systemList
    if len(effect_list) == 0:
        # print("传入特效信息为空")
        return
    # 获取特效能力中最大的版本配置
    verison_list = {}
    effect_version = check_is_bach(effectzip, effectLog)
    for v in effect_list:
        if v not in effect_version:
            verison_list[v] = "00.00.00"
        else:
            verison_list[v] = effect_version[v]
    max_version = max(verison_list.values())
    # print("最大版本号：",max_version)
    new_dict = {v: k for k, v in verison_list.items()}
    max_version_effect = new_dict[max_version]
    # print("最大版本effect：",max_version_effect)

    if LooseVersion(effectzip.version) < LooseVersion(max_version):
        msg = '资源包版本号配置错误，%s能力最低版本号限制%s，请将%s修改至%s及以上' % (
        max_version_effect, max_version, effectzip.version, max_version)
        enmsg = 'effect version error: %s version is %s, please change it≥%s' % (
        max_version_effect, max_version, max_version)
        effectLog.addJsonData(1, 'VERSION_ERROR', effectzip.zip_name, -1, msg, enmsg)


# 15 竞品逆向资源，需要检测资源包MD5值与竞品值区别
def calculate_md5(file_path):
    """
        @desc: 对文件后缀为['jpg', 'png', 'gif', 'vsh', 'glb', 'webp']的md5核心算法
        @return: md5哈希值
    """
    m = hashlib.md5()
    with open(file_path, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def check_md5(effectzip, effectLog):
    file_path = effectzip.png + effectzip.jpg + effectzip.gif + effectzip.vsh + effectzip.glb + effectzip.webp
    if len(file_path) != 0:
        for fi in file_path:
            if calculate_md5(fi) in EffectData.MD5_database:
                msg = '该资源包存在竞品逆向资源,请删除的文件路径如下:%s' % (fi[27:])
                enmsg = 'The resource package has competing product reverse resources %s' % (fi[27:])
                effectLog.addJsonData(1, 'MD5_ERROR', effectzip.zip_name, -1, msg, enmsg)
    return


# 16 敏感词和告警词检测，敏感词维护在 EffectData.disable_keyword 字符串清单中后续新增字符串可以直接追加
def check_disable_keyword(effectzip, effectLog):
    for di in effectzip.files:
        # print(di)
        try:
            with open(di, encoding='utf-8') as di_path:
                file_string = di_path.read()
                # if EffectData.disable_string in file_string:
                # print(file_string)
                for disable_keyword in EffectData.disable_keyword:
                    if disable_keyword in file_string:
                        msg = '该资源包存在敏感词,请打开文件路径:%s，将敏感词【%s】改成SIDE_NOD' % (di, disable_keyword)
                        enmsg = 'The package has Disable Keyword,please open %s and change【%s】to SIDE_NOD' % (
                        di, disable_keyword)
                        effectLog.addJsonData(1, 'Disable_Keyword_ERROR', effectzip.zip_name, -1, msg, enmsg)
                for warning_keyword in EffectData.warning_keyword:
                    if warning_keyword in file_string:
                        msg = '该资源包存在安全接口,请打开文件路径:%s，确认安全接口【%s】是否有用' % (di, warning_keyword)
                        enmsg = 'The package has warning Keyword,please confirm'
                        effectLog.addJsonData(2, 'WARNING', effectzip.zip_name, -1, msg, enmsg)
        except:
            pass


def get_pathtest():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # print("地址：",BASE_DIR)


# 17 bach_algorithmConfig中Blit节点需要Size配置，且版本号>950
def check_algorithm_blit_version(effectzip, effectLog):
    fi = get_Filepath(effectzip, 'algorithmConfig.json')
    if fi != None:
        with open(fi) as f:
            algorithm_string = json.loads(f.read())
            # print(algorithm_string['nodes'])
            for items in algorithm_string['nodes']:
                if ('type' in items and 'blit' in items['type']):
                    # print(items['type'])
                    if ('size' not in items['config'] and LooseVersion(effectzip.version) < '9.5.0'):
                        msg = 'algorithmConfig.json文件中解析"type": "blit"，需要配置"size"或SDK版本大于等于950【%s】' % (
                            effectzip.version)
                        enmsg = 'effect version error: %s , please change it≥950' % (effectzip.version)
                        effectLog.addJsonData(1, 'VERSION_ERROR', effectzip.zip_name, -1, msg, enmsg)


# 18 bach_algorithmConfig中expression_detect需要添加stringparam和modelnames，且版本号>9.7.0
def check_algorithm_expression_model(effectzip, effectLog):
    # effectzip.model_names=str(effectzip.model_names)
    # print(effectzip.model_names)
    fi = get_Filepath(effectzip, 'algorithmConfig.json')
    # print(effectzip.model_names)
    # print(effectzip.features)
    # print(effectzip.zorder)
    # print(effectzip.version)
    if fi != None:
        with open(fi) as f:
            algorithm_string = json.loads(f.read())
            for items in algorithm_string['nodes']:
                if ('type' in items and 'expression_detect' in items['type']):
                    if ('config' in items and 'keyMaps' in items['config']):
                        if ('stringParam' in items['config']['keyMaps']):
                            if ('face_attr_age_gender_model_dir' in items['config']['keyMaps'][
                                'stringParam'] and 'face_attr_expression_model_dir' in items['config']['keyMaps'][
                                'stringParam']):
                                msg = 'algorithmConfig.json文件中包含type: expression_detect，需要将 face_attr_age_gender_model_dir和face_attr_expression_model_dir删除'
                                enmsg = 'please delete face_attr_age_gender_model_dir&face_attr_expression_model_dir in algorithmConfig.json'
                                effectLog.addJsonData(1, 'algorithmConfig_ERROR', effectzip.zip_name, -1, msg, enmsg)
                if ('type' in items and 'expression_detect' in items['type']):
                    if LooseVersion(effectzip.version) < '9.7.0':
                        if 'tt_face_attribute_age' not in effectzip.model_names and 'algo_ggl1pqhlpgg754kghlpah' not in effectzip.model_names:
                            if 'tt_face_attribute_exp' not in effectzip.model_names and 'algo_ggl1pqhlpgg754kghlhmi' not in effectzip.model_names:
                                msg = 'algorithmConfig.json文件中包含type: expression_detect，版本号要提升970及以上，config文件需要在model_names添加 tt_face_attribute_age 与 tt_face_attribute_exp'
                                enmsg = 'please change version≥970，config add tt_face_attribute_age and tt_face_attribute_exp in model_names'
                                effectLog.addJsonData(1, 'ModelName_ERROR', effectzip.zip_name, -1, msg, enmsg)
                    # if(LooseVersion(effectzip.version) < '9.7.0' or 'tt_face_attribute_age' not in effectzip.model_names or 'tt_face_attribute_exp' not in effectzip.model_names):
                    #     msg = 'algorithmConfig.json文件中包含type: expression_detect，版本号要提升970及以上，config文件需要在model_names添加 tt_face_attribute_age 与 tt_face_attribute_exp'
                    #     enmsg = 'please change version≥970，config add tt_face_attribute_age and tt_face_attribute_exp in model_names'
                    #     effectLog.addJsonData(1,'ModelName_ERROR',effectzip.zip_name,-1,msg,enmsg)


# 19 bach_algorithmConfig中带有tt_face配置的道具，且版本号小于等于1000是问题道具
def check_algorithm_face(effectzip, effectLog):
    fi = get_Filepath(effectzip, 'algorithmConfig.json')
    if fi != None:
        with open(fi) as f:
            algorithm_string = json.loads(f.read())
            for items in algorithm_string['nodes']:
                if ('type' in items and items['type'] == 'face' and 'stringParam' in items['config']['keyMaps']):
                    stringParam = items['config']['keyMaps']['stringParam']
                    # if(LooseVersion(effectzip.version) < 1010):
                    #     print('1')
                    if (LooseVersion(effectzip.version) < '10.1.0') and (
                        'face_base_model_key' in stringParam or 'face_extra_model_key' in stringParam):
                        msg = 'algorithmConfig.json中带‘face’,需要版本号要提升1010及以上，或将stringParam字段中ace_base_model_key&face_extra_model_key删除'
                        enmsg = 'algorithmConfig.json has‘face’，please change version≥1010 or delete ace_base_model_key and face_extra_model_key in stringParam'
                        effectLog.addJsonData(1, 'Face_VERSION_ERROR', effectzip.zip_name, -1, msg, enmsg)


# 20 西瓜AR检测是否type含有TouchGes
def check_AR_type(effectzip, effectLog):
    if ('AR' in effectzip.features and 'TouchGes' not in effectzip.features):
        msg = '此AR道具没有TouchGes的feature，无法透传手势实现触屏逻辑,需要在此道具包中添加TouchGes的feature'
        enmsg = 'This AR effect didnot have TouchGes, and cannot be transparently transmitted to directly touch the screen logic. please add the  TouchGes to this package'
        effectLog.addJsonData(1, 'AR_ERROR', effectzip.zip_name, -1, msg, enmsg)


# 21 befview应用道具版本号检测
def check_befview_version(effectzip, effectLog):
    fi = get_Filepath(effectzip, 'extra.json')
    if fi != None:
        with open(fi) as f:
            algorithm_string = json.loads(f.read())
            if ('befViewResRoot' in algorithm_string):
                if (LooseVersion(effectzip.version) < '10.4.0'):
                    msg = 'extra.json中应用了befViewResRoot，需要sdk提升至10.4.0及以上'
                    enmsg = 'extra.json has‘befViewResRoot’，please change version≥10.4.0'
                    effectLog.addJsonData(1, 'VERSION_ERROR', 'extra.json', -1, msg, enmsg)


# 22 特效算法groudseg检测
def check_groudseg_version(effectzip, effectLog):
    fi = get_Filepath(effectzip, 'config.json')
    if fi != None:
        with open(fi) as f:
            algorithm_string = f.read()
            if ('groundseg' in algorithm_string):
                if (LooseVersion(effectzip.version) < '7.1.0'):
                    msg = 'config.json中应用了groundseg，需要sdk提升至7.1.0及以上'
                    enmsg = 'config.json has‘groundseg’，please change sdk≥7.1.0'
                    effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)

    fi = get_Filepath(effectzip, 'content.json')
    if fi != None:
        with open(fi) as f:
            algorithm_string = f.read()
            if ('groundseg' in algorithm_string):
                if (LooseVersion(effectzip.version) < '7.1.0'):
                    msg = 'content.json中应用了groundseg，需要sdk提升至7.1.0及以上'
                    enmsg = 'content.json has‘groundseg’，please change sdk≥7.1.0'
                    effectLog.addJsonData(1, 'VERSION_ERROR', 'content.json', -1, msg, enmsg)


# 23 检查animatorControllerScript动画最低版本检测
def check_animatorControllerScript_version(effectzip, effectLog):
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'animatorControllerScript' or fis[-2] == 'animatorControllerScript' or fis[
            -3] == 'animatorControllerScript'):
            if (LooseVersion(effectzip.version) < '9.5.0'):
                msg = '使用了animatorControllerScript脚本，需要sdk提升至9.5.0及以上'
                enmsg = 'animatorControllerScript is used，please change sdk≥9.5.0'
                effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)
            break


# 24 剪映3d滤镜道具最低版本号检测
def capcut_3D_version(effectzip, effectLog):
    for fi in effectzip.files:
        fis = fi.split('/')
        fis_path = fis[-1].split('.')[-1]
        if (fis_path == '3dl' or fis_path == 'cube'):
            if (LooseVersion(effectzip.version) < '11.1.0'):
                msg = '使用了3D滤镜能力，需要sdk提升至11.1.0及以上'
                enmsg = '3D filter is used，please change sdk≥11.1.0'
                effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)
            break


# 25 新渲染链问题最低版本号检测
def AmazingScene_version(effectzip, effectLog):
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'config.json'):
            with open(fi) as f:
                algorithm_string = json.loads(f.read())
                if ('effect' in algorithm_string and 'AmazingScene' in algorithm_string['effect'] and 'asynLoad' in
                    algorithm_string['effect']['AmazingScene']):
                    if (algorithm_string['effect']['AmazingScene']['asynLoad'] == 1):
                        if (LooseVersion(effectzip.version) < '10.5.0'):
                            msg = '道具中使用了新渲染链，需要sdk提升至10.5.0及以上'
                            enmsg = 'new render chain is used，please change sdk≥10.5.0'
                            effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)
                        break


# 26 抖音版本回滚禁止版本有（1130、1140、1150）
def check_version_douyinbugfix(effectzip, effectLog):
    if (LooseVersion(effectzip.version) > '11.2.0'):
        msg = '抖音版本回滚，需要将effectsdk从 %s 降低至11.2.0及以下' % (effectzip.version)
        enmsg = 'douyin bugfix，please change sdk version from %s ≤11.2.0' % (effectzip.version)
        effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)


# 27 调用算法模型接口，检查资源包使用的modelname最低版本是否小于等于资源包版本
def check_modelname_version(effectzip, effectLog, url, access_key, secret_key):
    tce_env = os.getenv('TCE_HOST_ENV')
    modelNameList = []
    # boe 不做该类型检测
    if tce_env == 'boe':
        return

    # 解决存在多个config.json文件情况
    configList = []
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'config.json'):
            configList.append(fi)
    # 取path长度最短的config文件
    MinLen_config = len(configList[0])
    MinLen_config_index = 0
    for index, config in enumerate(configList):
        if len(config) < MinLen_config:
            MinLen_config = len(config)
            MinLen_config_index = index
    algorithm_path = None
    # 读取config.json文件
    with open(configList[MinLen_config_index]) as f:
        algorithm_string = json.loads(f.read())
    if ('effect' in algorithm_string and 'model_names' in algorithm_string['effect']):
        # 规避modelname为空情况
        if algorithm_string['effect']['model_names']:
            for key in algorithm_string['effect']['model_names']:
                modelNameList = algorithm_string['effect']['model_names'][key]
        # print(modelNameList)
        # 读取algorithmConfig.json文件，获取其中的model_name
    algorithm_path = None
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'algorithmConfig.json'):
            algorithm_path = fi
    if algorithm_path:
        with open(algorithm_path) as algorithm:
            algorithm_data = json.loads(algorithm.read())
        if algorithm_data.get('model_names'):
            for key in algorithm_data.get('model_names'):
                modelNameList.extend(algorithm_data.get('model_names')[key])
    if len(modelNameList) == 0:
        return

    now = str(int(time.time() * 1000))
    str_to_sign = ','.join([access_key, now, 'v1.0'])
    encrypted = hmac.new(secret_key.encode('utf-8'), str_to_sign.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    encrypted = hmac.new(encrypted.encode('utf-8'), b'', hashlib.sha256).hexdigest()
    x_signature_valid = '{0}/{1}/{2}/{3}'.format('v1.0', access_key, encrypted, now)

    headers = {
        'x-signature-valid': x_signature_valid,
        'Content-Type': 'application/json',
    }

    body = {
        "modelNameList": modelNameList,
        "scenarioId": 100
    }
    res = requests.post(url, headers=headers, json=body).json()
    # print(res)
    modelVersions = res['data']['modelList']
    for v in modelVersions:
        if LooseVersion(effectzip.version) < v['minEffectVersion']:
            msg = '使用的modelname %s 最低版本为 %s，需要将资源包从%s提高至 %s' % (
            v['name'], v['minEffectVersion'], effectzip.version, v['minEffectVersion'])
            enmsg = 'modelname %s min version is %s，please change effect %s into %s' % (
            v['name'], v['minEffectVersion'], effectzip.version, v['minEffectVersion'])
            effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)


# 28 检查algorithmConfig.json是否存在"type":  "nh_inference"字段，提醒用户进动态化及脚本模型review 群
def check_algorithmConfig_nh_inference(effectzip, effectLog):
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'algorithmConfig.json'):
            with open(fi) as f:
                algorithm_string = json.loads(f.read())
                for index in range(len(algorithm_string['nodes'])):
                    if algorithm_string['nodes'][index].get('type') == 'nh_inference':
                        msg = '道具使用了"nh_inference"动态化算法，请联系@诸葛晶晶 进行动态化模型review'
                        enmsg = 'dynamic algorithm is used，please call @诸葛晶晶 dynamic algorithm review group'
                        effectLog.addJsonData(1, 'VERSION_ERROR', 'algorithmConfig.json', -1, msg, enmsg)


# 29 JS代码关闭默认算法图中的blit_0节点检测
def checkBachGraphScript(effectzip, effectLog):
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'BachGraphScript.js'):
            with open(fi, 'r') as f:
                content = f.read()
                if re.search(r'algorthmManager.setAlgorithmEnable\("effectsdk_defaut_graph", "blit_0", false\);',
                             content):
                    msg = 'BachGraphScript.js文件中"algorthmManager.setAlgorithmEnable("effectsdk_defaut_graph", "blit_0", false);"会导致切换道具后，算法失效，请删除该行代码'
                    enmsg = '"algorthmManager.setAlgorithmEnable("effectsdk_defaut_graph", "blit_0", false);" in the BachGraphScript.js file will guide the algorithm to fail after switching effect, please delete this line of code'
                    effectLog.addJsonData(1, 'BachGraphScript.js', 'BachGraphScript.js', -1, msg, enmsg)
                    return


# 30 新渲染链道具搬运TT最低版本号检测
def TT_AmazingScene_version(effectzip, effectLog):
    # 解决存在多个config.json文件情况
    configList = []
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'config.json'):
            configList.append(fi)
    # 取path长度最短的config文件
    MinLen_config = len(configList[0])
    MinLen_config_index = 0
    for index, config in enumerate(configList):
        if len(config) < MinLen_config:
            MinLen_config = len(config)
            MinLen_config_index = index
    with open(configList[MinLen_config_index], 'r') as f:
        algorithm_string = json.loads(f.read())
        # print(algorithm_string)
        if ('effect' in algorithm_string and 'AmazingScene' in algorithm_string['effect']) and (
            LooseVersion(effectzip.version) < '13.1.0'):
            msg = '道具中使用了新渲染链，需要sdk提升至13.1.0及以上'
            enmsg = 'new render chain is used，please change sdk≥13.1.0'
            effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'sticker.json'):
            with open(fi) as f:
                algorithm_string = json.loads(f.read())
                if ('EffectNodeSystem' in algorithm_string['systemList']) and (
                    LooseVersion(effectzip.version) < '13.1.0'):
                    msg = '道具中使用了新渲染链，需要sdk提升至13.1.0及以上'
                    enmsg = 'new render chain is used，please change sdk≥13.1.0'
                    effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)


# 31 检测道具包内algorithmConfig.json里是否存在"script_path"字段,提醒用户需要打包脚本算法为模型，并进动态化及脚本模型review”群
def check_algorithmConfig_scriptPath(effectzip, effectLog):
    import re
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'algorithmConfig.json'):
            with open(fi) as f:
                if re.search('script_path', f.read()):
                    msg = '道具包内algorithmConfig.json里存在"script_path"字段,需要打包脚本算法为模型，找@诸葛晶晶'
                    enmsg = '道具包内algorithmConfig.json里存在"script_path"字段,需要打包脚本算法为模型，找@诸葛晶晶'
                    effectLog.addJsonData(1, 'NoticeInfo', 'config.json', -1, msg, enmsg)


# 32 检测道具包是否打开了麦克风权限
def check_open_mic_permission(effectzip, effectLog):
    '''
    检查打开麦克风设备权限
    '''
    extra_path = effectzip.zip_path + '/extra.json'
    if os.path.exists(extra_path):
        extra_file = open(extra_path, 'r+')
        # 以json格式读取extra.json
        extra_content = json.loads(extra_file.read())
        for key in extra_content.keys():
            if key == "audio_graph":
                audio_graph_content = extra_content["audio_graph"]
                for key in audio_graph_content.keys():
                    if key == "sources":
                        if "mic" in audio_graph_content["sources"]:
                            msg = "此特效会打开麦克风，请不要搬运到编辑页，否则会有安全风险！！！"
                            enmsg = "The effect will open the microphone, please do not transport it to the editing " \
                                    "page, otherwise there will be a security risk !!!"
                            effectLog.addJsonData(1, "NoticeInfo", "", -1, msg, enmsg)


# 33 检测压缩包zip文件内的所有entry数据。如果发现某个entry包含EXT descriptor，且其压缩方式不为DEFLATED，会导致android解压失败
def check_file_has_ext_descriptor_and_not_compression_by_deflated(effectzip, effectLog):
    with zipfile.ZipFile(effectzip.zip_path + '.zip', 'r') as zf:
        for entry in zf.infolist():
            if entry.flag_bits & 0x8 and entry.compress_type != 8:
                msg = "此特效是mac13系统生产的zip包，存在android平台解压失败问题，会导致特效应用失败"
                enmsg = "This effect is a zip package produced by the mac13 system. There is a problem that the android " \
                        "platform fails to decompress, which will cause the special effect application to fail. "
                effectLog.addJsonData(1, "ZIP_COMPRESS_ERROR", entry.filename, -1, msg, enmsg)


# 34 拦截缺失模型配置的道具
# 通过文件名获取文件路径,当有多个时，返回最短路径的
def fileNameGetfilePath(effectzip, fileName):
    filePath = []
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == fileName):
            filePath.append(fi)
    if len(filePath) == 1:
        return filePath[0]
    elif len(filePath) > 1:
        for f in filePath:
            minfilePath = filePath[0]
            if len(minfilePath) > len(f):
                minfilePath = f
            else:
                continue
        return minfilePath


book = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
key = "CQTZKHGJYMUWPBDEVRASONFILXp4qvh1a053s98cti27ugkrnm6_yjfbxdewozl"


def encode(s):
    if s.startswith("algo_"):
        # print("It has been already a confused model name.")
        return s
    encoded = ""
    for c in s:
        idx = book.find(c)
        if idx != -1:
            encoded += key[book.find(c)]
        else:
            encoded += c
    return "algo_" + encoded


def decode(s):
    if not s.startswith("algo_"):
        # print("It's not a confused model name.")
        return s
    else:
        s = s[len("algo_"):]  # delete prefix "algo_"
    decoded = ""
    for c in s:
        idx = key.find(c)
        if idx != -1:
            decoded += book[key.find(c)]
        else:
            decoded += c
    return decoded


# 判断模型是否存在缺失
def checkModelNameIntegrity(effectzip, effectLog):
    # 模型key的列表，后续会收敛成model_name，目前model_name是通用key，存在一些特殊key，需要存在这个列表
    modelNameKeys = ["audio_avatar_model_name", "ava_boost_model_name", "avatar_fit_model_name",
                     "avatar_fit_model_name", "avatar_fit_model_name", "car_series_model_name", " cloth_gan_model_key",
                     "compress_shot_detect_backbone_model_name", "compress_shot_detect_predhead_model_name",
                     "content_recommend_model_key", "deep_inpaint_model_key_coarse", "deep_inpaint_model_key_fine",
                     "licensecake_detection_model_name", "licensecake_detection_cake_landmark_model_name",
                     "licensecake_detection_person_recognition_model_name",
                     "licensecake_detection_cake_landmark_det_model_name", "lm_3d_network_weights",
                     "lm_3d_mean_face_info", "keypoint_name", "navi_avatar_drive_model_key",
                     "action_detect_static_model_key", "action_detect_sequence_model_key",
                     "action_recognition_tmpl_name", "auto_detection_object_model_name",
                     "auto_detection_human_model_name", " avatar3d_model_key", "avatar_drive_model_key",
                     " blockgan_model_key", "building_normal_scene_normal_model_path", "building_normal_reg_model_path",
                     "building_seg_model_key", "car_seg_model_key", "cloth_class_model_key", "clothset_model_key",
                     "clothseg_model_key", "depth_model_key", "face_attr_age_gender_model_dir",
                     "face_attr_expression_model_dir", "face_attr_extra_model_dir", "face_attr_model_dir",
                     "face_base_model_key", "face_extra_model_key", "face_extra_fast_model_name",
                     "face_beautify_model_key", "face_clusting_model_key", " face_gan_model_key", "face_mask_model_key",
                     "face_part_beauty_model_key", "face_pet_detect_model_key", "face_verify_model_key",
                     "female_gan_model_key", "food_comics_model_key", "foot_model", "forehead_seg_model_key",
                     "gaze_estimation_model_key", "ground_seg_model_key", "hp_model_name", "hair_flow_model_key",
                     " hand_object_seg_track_model_name", "hdr_net_model_key", "human_parsing_model_key",
                     "idream_model_key", "indoor_seg_model_name", "joints1_model_key", "joints2_model_key",
                     "license_plate_detect_model_key", "manga_model_key", "mug_model_key",
                     "multi_object_tracking_ar_model_key", "nail_model_key_seg", "nail_slam_normal_model_name",
                     "object_detect_model_key", "object_detection2_model_name", "object_tracking_model_name",
                     "saliency_model_key", "scene_normal_model_key", "scene_model_key", "skeleton_model_key",
                     "skeleton_pose_3d_model_key_skel", "skeleton_pose_3d_model_key_pose", "skin_seg_model_key",
                     "skyseg_model_key", "swap_live_model_name", "swapperme_model_key", "teeth_model_key",
                     "tracking_ar_model_key", "video_sr_model_key", "watch_tryon_model_name", "model_name"]
    # 默认模型名配置，如果算法节点type配置了，但是stringParam未配置模型，则需要根据type获取对应model默认model，判断默认model是否在modelListConfig中
    defaultModel = {'action_detect': ['tt_action_detection', 'tt_pose_detection'], 'after_effect': 'tt_after_effect',
                    'avacap': 'tt_avacap', 'avatar_3d': 'tt_avatar3dsticker', 'avatar_drive': 'tt_avatar_drive',
                    'avatar_score': ['tt_beauty_attr6', 'tt_face_beauty'], 'big_gan': 'tt_biggan',
                    'building_normal': 'bingo_building_normal', 'building_seg': 'bingo_building_seg',
                    'clothes_seg': 'tt_clothes_seg', 'content_recommend': 'tt_hashtag', 'depth': 'tt_depth_estimation',
                    'ear_seg': 'tt_earseg_kp', 'expression_detect': ['tt_face_attribute_age', 'tt_face_attribute_exp'],
                    'eye_fitting': 'tt_eyefitting', 'f_parsing': 'tt_f_parsing', 'face': ['tt_face', 'tt_face_extra'],
                    'face_attr': ['tt_face_attribute_age', 'tt_face_attribute_exp', 'tt_face_attribute_extra'],
                    'face_beautify': 'tt_facebeautify', 'face_clusting': 'tt_bigbrother',
                    'face_fitting': ['tt_facefitting1220', 'tt_facefitting1256', 'tt_facefitting845'],
                    'face_gan': 'tt_facegan_class', 'face_light': 'tt_face_light',
                    'face_new_landmark': 'tt_face_new_landmark', 'face_pet_detect': 'tt_petface',
                    'face_verify': 'tt_faceverify', 'facefitting_3d': 'tt_facefitting_3d', 'female_gan': 'female_gan',
                    'foot': 'tt_foot', 'freid': 'tt_freid', 'gender_gan': 'tt_gendergan', 'ground_seg': 'tt_ground_seg',
                    'hair': 'tt_hair', 'hair_flow': 'tt_hair_flow',
                    'hand': ['tt_hand_box_reg', 'tt_hand_det', 'tt_hand_gesture', 'tt_hand_kp', 'tt_hand_kp3d',
                             'tt_hand_lr', 'tt_hand_ring', 'tt_hand_seg'],
                    'havatar': ['tt_havatar_action_cls', 'tt_havatar_det', 'tt_havatar_lr_box', 'tt_havatar_lr_cls',
                                'tt_havatar_pose', 'tt_havatar_track'], 'hdr_net': 'tt_hdrnet_effect',
                    'head_fitting': ['tt_head3d_fitting_obj', 'tt_head3d_obj'], 'head_seg': 'tt_headseg',
                    'human_parsing': 'tt_human_parsing', 'idream': 'tt_idream', 'indoor_seg': 'tt_indoor_seg',
                    'manga': 'ap_manga',
                    'matting': ['tt_matting', 'tt_matting_video', 'tt_matting_subject', 'tt_matting_subjgpu',
                                'tt_matting_large'],
                    'memoji_match': ['tt_memoji_matchsafe_facial', 'tt_memoji_matchsafe_features',
                                     'tt_memoji_matchsafe_glasses', 'tt_memoji_matchsafe_hair',
                                     'tt_memoji_matchsafe_sun'], 'nail': ['tt_nail_kpts', 'tt_nail_seg'],
                    'navi_avatar_drive': 'navi_avatar_drive', 'neck': 'tt_neck_pose',
                    'object_tracking': 'bingo_objecttracking', 'old_gan': 'tt_old', 'porn_cls': 'tt_porn_classifier',
                    'saliency_seg': 'bingo_saliency_seg', 'salient_human': 'tt_salient_human',
                    'scene_normal': 'bingo_scene_normal', 'scene_recog_v3': 'tt_c3_cls',
                    'scene_recognition': ['tt_c1_det', 'tt_c1_small'], 'similarity': 'tt_sim',
                    'skeleton': 'tt_skeleton', 'skin_unified': ['tt_facebeautify', 'tt_skin_unified'],
                    'sky_seg': 'tt_skyseg', 'slam_nail': 'ttslammodel',
                    'smash_matting': ['tt_matting', 'tt_matting_video'],
                    'stop_motion': ['tt_matting', 'tt_matting_video'],
                    'swapperme': ['tt_face', 'tt_facebeautify', 'tt_facefitting1220'], 'video_cls': 'tt_videocls',
                    'video_matting': 'tt_matting', 'watch_tryon': 'tt_watch_tryon'}
    # AlgorithmConfig文件中node需要的model
    modelListAlgorithmConfig = []
    # config文件中的model和algorithmConfig文件中配置的model
    modelListConfig = []
    diffModelList = []
    # 读取算法配置文件，algorithmConfig.json文件
    algorithmConfigPath = fileNameGetfilePath(effectzip, 'algorithmConfig.json')
    if algorithmConfigPath is None:
        return
    with open(algorithmConfigPath) as f:
        algorithmConfigData = json.loads(f.read())
        # 遍历算法节点
        for node in algorithmConfigData.get('nodes'):
            # 获取node中的stringParam的值config->keyMaps->stringParam
            try:
                enable = node.get('enable')
                if enable == False:
                    continue
                stringParam = node.get('config').get('keyMaps').get('stringParam')
                if stringParam:
                    for key in stringParam:
                        if key in modelNameKeys:
                            if stringParam.get(key) not in modelListAlgorithmConfig:
                                if '/' in stringParam.get(key):
                                    modelListAlgorithmConfig.append(stringParam.get(key).split('/')[-1])
                                else:
                                    modelListAlgorithmConfig.append(stringParam.get(key))
                else:
                    modelType = node.get('type')
                    if defaultModel[modelType] not in modelListAlgorithmConfig:
                        modelListAlgorithmConfig.append(defaultModel[modelType])

            except:
                continue
    # 读取config.json文件
    configPath = fileNameGetfilePath(effectzip, 'config.json')
    with open(configPath) as f:
        configData = json.loads(f.read())
        effect = configData.get('effect')
        if effect.get('model_names') is None:
            modelListConfig = []
        else:
            for modelName in effect.get('model_names'):
                for model in effect.get('model_names').get(modelName):
                    modelListConfig.append(model)

    # algorithmConfig.json文件也配置了model_names,则需要取config.json文件于algorithmConfig.json文件的并集
    if algorithmConfigData.get('model_names'):
        for modelName in algorithmConfigData.get('model_names'):
            for model in algorithmConfigData.get('model_names').get(modelName):
                modelListConfig.append(model)
    # 判断modelListAlgorithmConfig中元素是否均存在于modelListConfig中
    for i in modelListAlgorithmConfig:
        # 一个算法名称对应多个模型名称，做特殊判断，如果有任一存在，则判断为存在
        if isinstance(i, list):
            diff = []
            for j in i:
                if j not in modelListConfig and encode(j) not in modelListConfig:
                    diff.append(j)
            if len(diff) == len(i):
                # 对"PXARStudio"进行tt_face豁免
                if configData.get('em_tool') == "PXARStudio" and i[0] == 'tt_face':
                    continue
                else:
                    diffModelList.append(i[0])
        elif i not in modelListConfig and encode(i) not in modelListConfig:
            diffModelList.append(i)
    if len(diffModelList) > 0:
        msg = f'模型{diffModelList}缺失，请修改道具包配置后重新上传'
        enmsg = f'Model {diffModelList} is missing, please modify the sticker and reupload'
        effectLog.addJsonData(1, 'algorithmConfig.json', 'algorithmConfig.json', -1, msg, enmsg)


# 35 音频资源包校验是否调用了stop和destroy（不调用会存在crash风险）
def checkAudioOnDestroy(effectzip, effectLog):
    import re
    # 遍历所有的lua文件和js文件
    for fi in effectzip.files:
        fis = fi.split('/')
        if fis[-1].endswith('.lua') or fis[-1].endswith('.js'):
            with open(fi, 'r') as file:
                # 去掉注释行
                s = ''
                for line in file.readlines():
                    if '--' in line or '//' in line:
                        continue
                    else:
                        s += line
            # 包含Amaz.AMGAudioModule.createAudioProxy为音频资源包
            if re.search('createAudioProxy', s):
                if re.search('stop()', s) and re.search('destroyAudioProxy', s):
                    continue
                else:
                    msg = '音频脚本需要在onDestroy函数中调用stop和destroy'
                    enmsg = 'The audio script needs to call stop and destroy in the onDestroy function'
                    effectLog.addJsonData(1, 'audio', 'lua/js', -1, msg, enmsg)


# 36 剪映js_path能力最小版本检测拦截
def check_js_path_min_version(effectzip, effectLog):
    config_path = fileNameGetfilePath(effectzip, 'config.json')
    try:
        with open(config_path) as f:
            config_data = json.loads(f.read())
            if config_data.get('js_path'):
                if LooseVersion(effectzip.version) < '15.1.0':
                    msg = '使用了js_path能力，最低版本为15.1.0'
                    enmsg = 'Using js_path abilities , with the minimum version of 15.1.0'
                    effectLog.addJsonData(1, 'VERSION_ERROR', 'config.json', -1, msg, enmsg)
    except:
        pass
    # 传入长度==3，存储所有的检测功能

