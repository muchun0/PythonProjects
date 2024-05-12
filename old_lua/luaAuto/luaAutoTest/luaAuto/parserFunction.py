#coding=utf-8
import data as EffectData
import os
import json
import struct
import sys
import shutil
import zipfile

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
    if (len(EffectData.classList) != len(EffectData.returnList) or len(EffectData.classList) != len(EffectData.funcList) or len(EffectData.classList) != len(
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
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].className = EffectData.classList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].funcName = EffectData.funcList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].version = EffectData.versionList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].parameter = EffectData.parameterList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].returnName = EffectData.returnList[i]
        else:
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].className = EffectData.classList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].funcName = EffectData.funcList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].version = EffectData.versionList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].parameter = EffectData.parameterList[i]
            myClassManager.classDic[EffectData.classList[i]].funcDic[EffectData.funcList[i]].returnName = EffectData.returnList[i]

        i += 1
    
    myClassManager.funcToVerion['getRenderProtocol'] = '4.6.0' #临时todo

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
                if (Strings[i+1] == '-'):
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
                if (Strings[i+1] == '-'):
                    i = i + 2
                    while (Strings[i] != '\n'):
                        i = i + 1
                    if(i == len(Strings)-1):
                        return ('null',[])
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
                    if(i == len(Strings)-1):
                        return ('null',[])
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
        "6C6F6361":"lua",
        "7B0A":"json",
        # "7B0A0922":"json"
        "23646566":"shader",
        "0A707265":"vert",
        "70726563":"frag",
        "0A236465":"vert",
        "0A202020":"glsl",
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
        "424D":"Bitmap",
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
    binfile = open(filename, 'rb') # 必需二制字读取 
    file_size = os.path.getsize(filename)
    if(file_size < 20):
        binfile.close() 
        return False
    ctl = check_type_list() 
    utl = un_check_type_list() 
    ftype = 'unknown'  
    checkChinese = True
    for hcode in ctl.keys():  
        numOfBytes = int(len(hcode) / 2) # 需要读多少字节  
        binfile.seek(0) # 每次读取都要回到文件头，不然会一直往后读取 
         
        hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes)) # 一个 "B"表示一个字节 
        f_hcode = bytes2hex(hbytes)  

        if f_hcode == hcode:  
            ftype = ctl[hcode] 
            checkChinese = True 
            break  
    for hcode in utl.keys():  
        numOfBytes = int(len(hcode) / 2) # 需要读多少字节  
        binfile.seek(0) # 每次读取都要回到文件头，不然会一直往后读取  
        hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes)) # 一个 "B"表示一个字节  
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
    if(type(check_str) == bytes):
        return chineseList
    for ch in check_str.encode().decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            chineseList.append(ch)
    return chineseList

#检测是否有中文
def checkChinese(effectzip,effectLog):
    for di in effectzip.dirs:
        temp_di = di.split('/')
        if('__MACOSX' not in temp_di and temp_di[-1] != '.DS_Store'):
            dir_path = di[len(effectzip.zip_path)+1:]
            # print(dir_path)
            checkList = check_contain_chinese(dir_path)
            if(len(checkList) > 0):
                msg = 'error: file:%s含有中文字符:%s\n'%(dir_path,checkList)
                enmsg = 'error: file:%s has chinese text is:%s\n'%(dir_path,checkList)
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(1,'HAS_CHINESE',effectzip.zip_name,-1,msg,enmsg)
                effectLog.setCode(4)

    for fi in effectzip.files:
        temp_fi = fi.split('/')
        if('__MACOSX' not in temp_fi and temp_fi[-1] != '.DS_Store' ):
            fi_path = fi[len(effectzip.zip_path)+1:]
            checkList = check_contain_chinese(fi_path)
            if(len(checkList) > 0):
                msg = 'error: file:%s has chinese text is:%s\n'%(fi_path,checkList)
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(1,'HAS_CHINESE',effectzip.zip_name,-1,msg)
            if(filetype(fi) == True):
                if(os.path.isfile(fi)):
                    with open(fi,'rb') as f:
                        try:
                            file_str = f.read().decode('utf-8')
                            checkList = check_contain_chinese(file_str)
                            if(len(checkList) > 0):
                                msg = 'error: file:%s 含有中文字符:%s\n'%(fi_path,checkList)
                                enmsg = 'error: file:%s has chinese text is:%s\n'%(fi_path,checkList)
                                effectLog.addEnglishErrorThing(msg)
                                effectLog.addJsonData(1,'HAS_CHINESE',effectzip.zip_name,-1,msg,enmsg)
                                effectLog.setCode(4)

                        except UnicodeDecodeError:
                            print('')

#检测自定义文字是否送审核
def checkTextIsOk(effectzip,effectLog):
    for fi in effectzip.files:
        temp_fi = fi.split('/')
        if('__MACOSX' not in temp_fi and temp_fi[-1][-4:] == '.lua' and temp_fi[-1][0] != '.'):
            with open(fi,'r') as lua_file:
                lua_string = lua_file.read()
                if(lua_string.find('handleKeyboardInput') > 0): #说明是新引擎文字贴纸
                    if(lua_string.find('getTextContent') > 0 and lua_string.find('Amaz.StringVector') > 0):
                        lua_textset = True #ok
                    else:
                        msg = 'error: file:%s text2DV2 handleKeyboardInput 送审文字接口需要添加接口getLuaTextContent()请添加 \n'%(fi)
                        enmsg ='error: file:%s text2DV2 handleKeyboardInput  need getTextContent() and use Amaz.StringVector Conversion String ,please use\n'%(fi)
                        effectLog.addEnglishErrorThing(msg)
                        effectLog.addJsonData(1,'TEXT_2DV2',effectzip.zip_name,-1,msg,enmsg)
                elif(lua_string.find('handleInputText') > 0): #说明是旧引擎文字贴纸
                    if(lua_string.find('getLuaTextContent') <= 0 ):
                        msg = 'error: file:%s text2DV2 handleInputText  送审文字接口需要添加接口getLuaTextContent()请添加'%(fi)
                        enmsg = 'error: file:%s text2DV2 handleInputText  need getLuaTextContent(),please use\n'%(fi)
                        effectLog.addEnglishErrorThing(msg)
                        effectLog.addJsonData(1,'TEXT_2DV2',effectzip.zip_name,-1,msg,enmsg)


#检测函数是否是内建函数
# def checkFunctionIsIn(effectzip,effectLog):
#     return

#检测是否有ARKIt 版本号
def checkARkitVersion(effectzip,effectLog):
    if('ARKit' in effectzip.features):
        for fi in effectzip.files:
            temp_fis = fi.split('/')
            if('extra.json' in temp_fis and '__MACOSX' not in temp_fis and temp_fis[-1] != '.DS_Store'):
                with open(fi,'r') as f:
                    json_string = json.loads(f.read())
                    if('worldTracking' in json_string and effectzip.verison < '6.8.0'):
                        msg = "error file:%s 版本号错误. Config.json 版本号是 %s, ARKit+需要提高到 6.8.0."%(effectzip.zip_name,effectzip.version) 
                        enmsg = "error file:%s Wrong config version number. Config.json version number is %s, ARKit+worldTracking Please change the version number to 6.8.0."%(effectzip.zip_name,effectzip.version) 
                        effectLog.addEnglishErrorThing(msg)
                        effectLog.addJsonData(1,'VERSION_ERROR',effectzip.zip_name,-1,msg,enmsg)
            

    return

#检测AERender版本号
def checkAERenderVersion(effectzip,effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    if('data.json' in list_dir and 'user_data.json' in list_dir and effectzip.version < '6.3.0'):
        msg = "error file:%s版本号错误 %s, AERender能力的版本号高于6.3.0."%(effectzip.zip_name,effectzip.version)
        enmsg = "error file:%s Wrong config version number. Config.json version number is %s, AERender Please change the version number to 6.3.0."%(effectzip.zip_name,effectzip.version)
        effectLog.addEnglishErrorThing(msg)
        effectLog.addJsonData(1,'VERSION_ERROR',effectzip.zip_name,-1,msg,enmsg)



#检测3dFaceMeshPerspective版本号
def check3dFaceMeshPerspectiveVersion(effectzip,effectLog):
    return
#检测是否有禁止feature列表
def checkFeatureDisable(effectzip,effectLog,featureList):   
    for feature in effectzip.features:
        if(feature in featureList):
            msg = 'error file:%s feature:%s 不能被使用'%(effectzip.zip_name,feature)
            enmsg = 'error file:%s feature:%s not be use'%(effectzip.zip_name,feature)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1,'DISABLE_FEATURE',effectzip.zip_name,-1,msg,enmsg)

    #features 是否amazingFeature
#判断lua 版本号是不是正确的
def checkLuaVersion(effectzip,effectLog):
    
    list_dir = os.listdir(effectzip.zip_path)
    i = -1
    version = '4.0.0'
    function = ''
    line = 0
    if('event.lua' in list_dir):
        lua_path = effectzip.zip_path + '/event.lua'
        stringList = []
        numList = {}
        with open(lua_path, 'r') as f:
            try:
                file_string = f.read()
                (stringList,numList) = participle(file_string)
            except:
                msg = "file:%s event.lua particple Error"%(effectzip.zip_name)
                effectLog.addEnglishErrorThing(msg)
        if(len(stringList) == 0 and effectzip.version < '4.0.0'):
            msg = 'config.json version is %s please change it to 4.0.0'%(effectzip.version)
            return
            
        myClassManager = parseFunction()
        name2ClassDic = {}
        #处理eventHandles
        while(i < len(stringList)):
            #判断function 是eventHandles function 还是外面的functions
            if(stringList[i] == 'MattingEffect'):
                i += 1
                if(version < '6.0.0'):
                    version = '6.0.0'
                    continue
            if (stringList[i] == ':' and stringList[i + 2] == '('):
                if(stringList[i+1] in EffectData.coordinateList):
                    msg = ('warning: 贴纸是用了坐标的贴纸，确认一下有没有用归一化处理 function = %s, line = %d \n'%(stringList[i+1],numList[i+1]))
                    effectLog.addEnglishErrorThing(msg)
            
                if (stringList[i + 1] in EffectData.featureList): #effect 调用基础函数
                    j = i -1
                    while (stringList[j] != '=' and stringList[j] != '(' and stringList[j] != ')' and j > 0):
                        j -= 1
                    if (stringList[j] == '(' or stringList[j] == ')' or j == 0):
                        i += 1
                        continue
                    className = myClassManager.getfuncToReturnName(stringList[i + 1])
                    
                    knum = i+3
                    while(knum < len(stringList)):
                        while(stringList[knum] != ')'):
                            knum = knum +1
                        if(stringList[knum+1] == ':' and stringList[knum+3] == '('):
                            tempClass = myClassManager.getClass(className)
                            if(tempClass != None):
                                className = tempClass.getFunc(stringList[knum+2])
                                knum = knum+4
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
                        knum = i+3
                        while(True and knum < len(stringList)):
                            while(stringList[knum] != ')'):
                                knum = knum +1
                            if(stringList[knum+1] == ':' and stringList[knum+3] == '('):
                                tempClass = myClassManager.getClass(className)
                                if(tempClass != None):
                                    className = tempClass.getFunc(stringList[knum+2])
                                    knum = knum+4
                                    
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
                                if (stringList[i - 2] == '='):  #在name2ClassDic 重新建立二阶查询
                                    if (myClassManager.getClass(tempFunc.returnName) != None):
                                        name2ClassDic[stringList[i - 3]] = myClassManager.getClass(tempFunc.returnName)

                                if (version < tempFunc.version):
                                    version = tempFunc.version
                                    function = stringList[i + 1]
                                    line = numList[i + 1]
                    elif(stringList[i-1] in EffectData.confirmFiled): #某些特殊字段还是当作二阶查询处理
                        tempClass = myClassManager.getClass(EffectData.confirmFiled[stringList[i-1]])
                        tempFunc = tempClass.getFunc(stringList[i+1])
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

        if(effectzip.version < version):
            msg = 'error: config.json版本 %s, line = %d function = %s 请提高版本到 %s'%(effectzip.version,line,function,version)
            enmsg = 'error: config.json version %s, line = %d function = %s please change version to %s'%(effectzip.version,line,function,version)
            effectLog.addEnglishErrorThing(msg)
            effectLog.addJsonData(1,'VERISON_ERROR',effectzip.zip_name,line,msg,enmsg)



                

    

#检查资源包的lua 是不是判空了
def checkLuaIsNotNil(effectzip,effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    if('event.lua' in list_dir):
        lua_path = effectzip.zip_path + '/event.lua'
        with open(lua_path, 'r') as f:
            file_string = f.read()
            stringList = []
            numList = {}
            try:
                (stringList,numList) = participle(file_string)
            except:
                msg ="file:%s event.lua particple Error"%(effectzip.zip_name)
                effectLog.addEnglishErrorThing(msg)
            functionList = ['getFeature','addFeature','getAudioManager','getRenderCacheTexture']
            i = 0
            while(i < len(stringList)):
                temp_str = stringList[i]
                if(temp_str in functionList):
                    j = i -1
                    while(stringList[j] != '='):
                        j -= 1
                    feature = stringList[j-1]
                    i += 1
                    if (stringList[i+5] in EffectData.listCast) or (stringList[i + 6] in EffectData.listCast):
                        i += 5
                    while (stringList[i] != feature and stringList[i] != '}' and i < len(stringList) - 1  ):
                        i += 1
                    if(i >= len(stringList) - 1):
                        continue
                    if(stringList[i+1] == ':'):
                        msg = "file:%s event.lua function %s 文件没有判空, 函数路径=%d"%(effectzip.zip_name,temp_str,numList[i+1])
                        enmsg ="file:%s event.lua function %s doesn't check empty variable,please add, function line=%d"%(effectzip.zip_name,temp_str,numList[i+1])
                        effectLog.addEnglishErrorThing(msg)
                        effectLog.addJsonData(1,'FEATURE_NOT_JUDGE_NIL',effectzip.zip_name,numList[i+1],msg,enmsg)
                        i += 1
                        continue

                    if(stringList[i-2] in EffectData.listCast):
                        j = i - 1
                        while(stringList[j] != '='):
                            j -= 1
                        castFeature = stringList[j -1]    
                        while(stringList[i] != feature):
                            i += 1
                        i += 1
                        while (stringList[i] != castFeature and stringList[i] != feature and stringList[i] != '}'):
                            i += 1
                        if(stringList[i] == '}' or i >= len(stringList)-1):
                            continue
                        if (stringList[i + 1] == ':'):
                            i += 1
                            msg = "file:%s event.lua function %s 文件没有判空, 函数路径为%d"%(effectzip.zip_name,castFeature,numList[i+1])
                            enmsg ="file:%s event.lua function %s doesn't check empty variable,please add, function line=%d"%(effectzip.zip_name,temp_str,numList[i+1])
                            effectLog.addEnglishErrorThing(msg)
                            effectLog.addJsonData(1,'FEATURE_NOT_JUDGE_NIL',effectzip.zip_name,numList[i+1],msg,enmsg)

                i += 1

    return

def checkFileDisable(effectzip,effectLog,disableFiles,disableDirs):
    for di in effectzip.dirs:
        temp_di = di.split('/')
        for disDir in disableDirs:
            if(disDir in temp_di):
                msg = 'error: file:%s 文件夹含多余文件%s'%(effectzip.zip_name,disDir)
                enmsg = 'error: file:%s has diable dir%s'%(effectzip.zip_name,disDir)
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(1,'FILE_DISABLE',effectzip.zip_name,-1,msg,enmsg)
    for fi in effectzip.files:
        temp_di = fi.split('/')
        for disfi in disableFiles:
            if(disfi in temp_di):
                msg = 'error: file:%s 文件夹含多余文件%s'%(effectzip.zip_name,disfi)
                enmsg = 'error: file:%s has diable dir%s'%(effectzip.zip_name,disDir)
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(1,'FILE_DISABLE',effectzip.zip_name,-1,msg,enmsg)

    
    return

#1 西瓜新渲染连资源包检测
def checkIsAmazingScene(effectzip,effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    if('config.json' in list_dir):
        config_path = effectzip.zip_path + '/config.json'
        #print('独立config_path',config_path)
        with open(config_path,'r') as f:
            config_string = json.loads(f.read())
            if('effect' in config_string):
                effects = config_string['effect']
            if('AmazingScene' in effects and effects['AmazingScene']['path'] != None):
                msg ='error:这是新渲染链资源包'
                enmsg ='this is a sticker package with New RenderChain mode'
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(2,'Mino',effectzip.zip_name,-1,msg,enmsg)
            else:
                msg ='error:这不是新渲染链资源包'
                enmsg ='this is a sticker package with New RenderChain mode'
                effectLog.addEnglishErrorThing(msg)
                effectLog.addJsonData(2,'Mino',effectzip.zip_name,-1,msg,enmsg)
#2  Tik Tok轻颜妆容搬运sdk版本检测   
def checkIsFaceMakeup(effectzip,effectLog):
    # 打印出第一层文件名字
    list_dir = os.listdir(effectzip.zip_path)
    if('FaceMakeupV2_byTool' in list_dir ):
        for fi in effectzip.files:
            fis =fi.split('/')
            if (fis[-1] == 'makeup.json'):
                with open(fi) as f:
                    makeup_string = json.loads(f.read())
                    if('filters' in makeup_string):
                        filters = makeup_string['filters']
                        try:
                            fragShaderPath_value = filters[0]['fragShaderPath']
                            #print("轻颜妆",effectzip.version)
                            keyWord = "b'%Shader%@"
                            if ('Shader' in fragShaderPath_value and effectzip.version < '8.7.0'):
                                msg = "error file:%s ,资源包版本号为%s, 轻颜妆版本号需要> 8.7.0."%(fis[-1],effectzip.version)
                                enmsg = "error file:%s ,Config.json version number is %s, fragShaderPath Please change the version number > 8.7.0."%(fis[-1],effectzip.version)
                                effectLog.addEnglishErrorThing(msg)
                                effectLog.addJsonData(1,'VERSION_ERROR',fis[-1],-1,msg,enmsg)
                        except:
                            print('')

#3 检测新引擎指定文件是否做二进制
def checktobinary(effectzip,effectLog):
    list_dir = os.listdir(effectzip.zip_path)
    keyWord = "b'%SerializedFormat%@"
    for fi in effectzip.files:
        fis = fi.split('/')
        if (fis[-1] == 'main.scene'):
            with open(fi,"rb")as f:
                fileStr = f.read()
                if keyWord not in str(fileStr):
                    msg ='error:"main.scene"文件没有转二进制，请继续检查main.scene，Material和mesh三个文件都需要转二进制'
                    enmsg = 'error:"main.scene" did not to binary，please check main.scene，Material、mesh need to binary'
                    effectLog.addEnglishErrorThing(msg)
                    effectLog.addJsonData(1,'ERROR',effectzip.zip_name,-1,msg,enmsg)


#存储所有的检测功能
def checkEffectZip(effectzip,effectLog,param):
    #test

    #非标资源包， 只检测中文
    for feature in effectzip.features:
        if(feature[0:2] == "NS" or feature[0:2] == 'ns'):
            effectLog.jsonErrorData.clear()
            if(param == 'ALL' or param == 'TikTok'):
                checkChinese(effectzip,effectLog)
                return
    if(param == 'DEFAULT'):
        # checkChinese(effectzip,effectLog)
        featureDisableList = ['FaceDistortion']
        checkFeatureDisable(effectzip,effectLog,featureDisableList)
        checkARkitVersion(effectzip,effectLog)
        checkAERenderVersion(effectzip,effectLog)
        checkLuaVersion(effectzip,effectLog)
        checkLuaIsNotNil(effectzip,effectLog)
        disableFiles = []
        disableDirs = ['.vscode']
        #checkFileDisable(effectzip,effectLog,disableFiles,disableDirs)
        checkTextIsOk(effectzip,effectLog)
        checktobinary(effectzip,effectLog)
    elif(param == 'DOUYIN'):
        featureDisableList = ['FaceDistortion']
        checkFeatureDisable(effectzip,effectLog,featureDisableList)
        checkARkitVersion(effectzip,effectLog)
        checkAERenderVersion(effectzip,effectLog)
        checkLuaVersion(effectzip,effectLog)
        checkLuaIsNotNil(effectzip,effectLog)
        disableFiles = []
        disableDirs = ['.vscode']
        #checkFileDisable(effectzip,effectLog,disableFiles,disableDirs)
        checkTextIsOk(effectzip,effectLog)
        checktobinary(effectzip,effectLog)
    elif(param == 'TIKTOK'):
        checkChinese(effectzip,effectLog)
        featureDisableList = ['FaceDistortion']
        checkFeatureDisable(effectzip,effectLog,featureDisableList)
        checkIsFaceMakeup(effectzip,effectLog)
        checktobinary(effectzip,effectLog)
    elif(param == 'XIGUA'):
        checkIsAmazingScene(effectzip,effectLog)