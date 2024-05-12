# 根据不同业务线，对Rules进行调用
import Rules
import json

with open('config.json', 'r') as f:
    config_info = json.load(f)

def checkEffectZip(effectzip, effectLog, param, lokiInformation=None):
    # 非标资源包， 只检测中文
    # 非标资源包， 只检测中文
    for feature in effectzip.features:
        if (feature[0:2] == "NS" or feature[0:2] == 'ns'):
            effectLog.jsonErrorData.clear()
            if (param == 'ALL' or param == 'TikTok'):
                checkChinese(effectzip, effectLog)
                return
    if (param == 'DEFAULT'):
        # checkChinese(effectzip,effectLog)
        featureDisableList = ['FaceDistortion']
        checkFeatureDisable(effectzip, effectLog, featureDisableList)
        checkARkitVersion(effectzip, effectLog)
        checkAERenderVersion(effectzip, effectLog)
        checkLuaVersion(effectzip, effectLog)
        checkLuaIsNotNil(effectzip, effectLog)
        disableFiles = []
        disableDirs = ['.vscode']
        checkFileDisable(effectzip, effectLog, disableFiles, disableDirs)
        checkTextIsOk(effectzip, effectLog)
        checktobinary(effectzip, effectLog)
        # 检测图片大小，分辨率
        # check_pics_size(param,effectzip,effectLog)
        # get_FileSize(effectzip,effectLog,param)
        checkObjectTrack(effectzip, effectLog)
        checkSameZorder(effectzip, effectLog)
        checkAmazGuidVersion(effectzip, effectLog)
        # check_md5(effectzip,effectLog)
        check_disable_keyword(effectzip, effectLog)
        # check_shader(effectzip,effectLog)
        # get_pathtest()
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))
        # print(BASE_DIR)
        # print(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        check_algorithm_blit_version(effectzip, effectLog)
        check_algorithm_expression_model(effectzip, effectLog)
        check_algorithm_face(effectzip, effectLog)
        check_algorithmConfig_nh_inference(effectzip, effectLog)
        check_modelname_version(effectzip, effectLog,
                                url='https://model-dispatcher.bytedance.net/openapi/model/getModelMinimumVersion',
                                access_key='4269ab2e88c8657c284cae87d55e41a5',
                                secret_key='9dcb30681e192565b32bbc9d628d8873')
        checkBachGraphScript(effectzip, effectLog)
        check_algorithmConfig_scriptPath(effectzip, effectLog)
        check_open_mic_permission(effectzip, effectLog)
        check_file_has_ext_descriptor_and_not_compression_by_deflated(effectzip, effectLog)
        checkModelNameIntegrity(effectzip, effectLog)
        checkAudioOnDestroy(effectzip, effectLog)
    elif (param == 'DEFAULT_I18N'):
        checkChinese(effectzip, effectLog)
        featureDisableList = ['FaceDistortion']
        checkFeatureDisable(effectzip, effectLog, featureDisableList)
        checkARkitVersion(effectzip, effectLog)
        checkAERenderVersion(effectzip, effectLog)
        checkLuaVersion(effectzip, effectLog)
        checkLuaIsNotNil(effectzip, effectLog)
        disableFiles = []
        disableDirs = ['.vscode']
        checkFileDisable(effectzip, effectLog, disableFiles, disableDirs)
        checkTextIsOk(effectzip, effectLog)
        checktobinary(effectzip, effectLog)
        # 检测图片大小，分辨率
        # check_pics_size('DEFAULT',effectzip,effectLog)
        # get_FileSize(effectzip,effectLog,'DEFAULT')
        checkObjectTrack(effectzip, effectLog)
        # print("值",effectzip.zorder)
        checkSameZorder(effectzip, effectLog)
        checkAmazGuidVersion(effectzip, effectLog)
        # check_md5(effectzip,effectLog)
        check_disable_keyword(effectzip, effectLog)
        check_algorithm_blit_version(effectzip, effectLog)
        check_algorithm_expression_model(effectzip, effectLog)
        check_algorithm_face(effectzip, effectLog)
        check_modelname_version(effectzip, effectLog,
                                url='https://model-dispatcher-us.byteintl.net/openapi/model/getModelMinimumVersion',
                                access_key='727280b4edb9892605848e1988359f0a',
                                secret_key='038b392d4f2b1d05fe84db2aaf6a245e')
        check_algorithmConfig_nh_inference(effectzip, effectLog)
        checkBachGraphScript(effectzip, effectLog)
        TT_AmazingScene_version(effectzip, effectLog)
        check_algorithmConfig_scriptPath(effectzip, effectLog)
        check_open_mic_permission(effectzip, effectLog)
        check_file_has_ext_descriptor_and_not_compression_by_deflated(effectzip, effectLog)
        checkModelNameIntegrity(effectzip, effectLog)
        checkAudioOnDestroy(effectzip, effectLog)
    elif (param == 'DOUYIN'):
        # checkChinese(effectzip,effectLog)
        featureDisableList = ['FaceDistortion']
        checkFeatureDisable(effectzip, effectLog, featureDisableList)
        checkARkitVersion(effectzip, effectLog)
        checkAERenderVersion(effectzip, effectLog)
        checkLuaVersion(effectzip, effectLog)
        checkLuaIsNotNil(effectzip, effectLog)
        disableFiles = []
        disableDirs = ['.vscode']
        checkFileDisable(effectzip, effectLog, disableFiles, disableDirs)
        get_FileSize(effectzip, effectLog, param)
        checkTextIsOk(effectzip, effectLog)
        checktobinary(effectzip, effectLog)
        # from PIL import Image
        check_pics_size(param, effectzip, effectLog, lokiInformation=lokiInformation)
        # checkObjectTrack(effectzip,effectLog)
        checkSameZorder(effectzip, effectLog)
        # check_shader(effectzip,effectLog)
        # check_md5(effectzip,effectLog)
        check_disable_keyword(effectzip, effectLog)
        check_algorithm_blit_version(effectzip, effectLog)
        check_algorithm_expression_model(effectzip, effectLog)
        check_algorithm_face(effectzip, effectLog)
        check_befview_version(effectzip, effectLog)
        check_groudseg_version(effectzip, effectLog)
        check_animatorControllerScript_version(effectzip, effectLog)
        AmazingScene_version(effectzip, effectLog)
        # 代码已经下架：check_version_douyinbugfix(effectzip, effectLog)
        check_modelname_version(effectzip, effectLog,
                                url='https://model-dispatcher.bytedance.net/openapi/model/getModelMinimumVersion',
                                access_key='4269ab2e88c8657c284cae87d55e41a5',
                                secret_key='9dcb30681e192565b32bbc9d628d8873')
        check_algorithmConfig_nh_inference(effectzip, effectLog)
        checkBachGraphScript(effectzip, effectLog)
        check_algorithmConfig_scriptPath(effectzip, effectLog)
        # check_open_mic_permission(effectzip, effectLog)
        checkModelNameIntegrity(effectzip, effectLog)
        checkAudioOnDestroy(effectzip, effectLog)
    elif (param == 'TIKTOK'):
        featureDisableList = ['FaceDistortion']
        checkFeatureDisable(effectzip, effectLog, featureDisableList)
        checkIsFaceMakeup(effectzip, effectLog)
        checktobinary(effectzip, effectLog)
        get_FileSize(effectzip, effectLog, param)
        check_pics_size(param, effectzip, effectLog, lokiInformation=lokiInformation)
        disableFiles = []
        disableDirs = ['.vscode']
        checkFileDisable(effectzip, effectLog, disableFiles, disableDirs)
        checkObjectTrack(effectzip, effectLog)
        checkLuaIsNotNil(effectzip, effectLog)
        checkTiktokVersion(effectzip, effectLog)
        checkSameZorder(effectzip, effectLog)
        checkChinese(effectzip, effectLog)
        checkAmazGuidVersion(effectzip, effectLog)
        # check_md5(effectzip,effectLog)
        check_disable_keyword(effectzip, effectLog)
        # check_shader(effectzip,effectLog)
        check_algorithm_blit_version(effectzip, effectLog)
        check_algorithm_expression_model(effectzip, effectLog)
        check_algorithm_face(effectzip, effectLog)
        check_befview_version(effectzip, effectLog)
        check_groudseg_version(effectzip, effectLog)
        check_animatorControllerScript_version(effectzip, effectLog)
        AmazingScene_version(effectzip, effectLog)
        check_modelname_version(effectzip, effectLog,
                                url='https://model-dispatcher-us.byteintl.net/openapi/model/getModelMinimumVersion',
                                access_key='727280b4edb9892605848e1988359f0a',
                                secret_key='038b392d4f2b1d05fe84db2aaf6a245e')
        check_algorithmConfig_nh_inference(effectzip, effectLog)
        checkBachGraphScript(effectzip, effectLog)
        TT_AmazingScene_version(effectzip, effectLog)
        check_algorithmConfig_scriptPath(effectzip, effectLog)
        check_open_mic_permission(effectzip, effectLog)
        checkModelNameIntegrity(effectzip, effectLog)
        checkAudioOnDestroy(effectzip, effectLog)
    elif (param == 'QINGYAN'):
        check_pics_size(param, effectzip, effectLog, lokiInformation=lokiInformation)
        disableFiles = []
        disableDirs = ['.vscode']
        checkFileDisable(effectzip, effectLog, disableFiles, disableDirs)
        check_rt_reuse(effectzip, effectLog)
        check_effect_makeup_opposite(effectzip, effectLog)
        checktobinary(effectzip, effectLog)
        checkLuaIsNotNil(effectzip, effectLog)
        checkChinese(effectzip, effectLog)
        check_eyelash(effectzip, effectLog)
        get_FileSize(effectzip, effectLog, param)
        checkSameZorder(effectzip, effectLog)
        # check_md5(effectzip,effectLog)
        check_disable_keyword(effectzip, effectLog)
        # check_shader(effectzip,effectLog)
        check_algorithm_blit_version(effectzip, effectLog)
        check_algorithmConfig_scriptPath(effectzip, effectLog)
    elif (param == 'FACEU'):
        check_pics_size(param, effectzip, effectLog, lokiInformation=lokiInformation)
        disableFiles = []
        disableDirs = ['.vscode']
        checkFileDisable(effectzip, effectLog, disableFiles, disableDirs)
        check_rt_reuse(effectzip, effectLog)
        check_effect_makeup_opposite(effectzip, effectLog)
        checktobinary(effectzip, effectLog)
        checkLuaIsNotNil(effectzip, effectLog)
        checkChinese(effectzip, effectLog)
        get_FileSize(effectzip, effectLog, param)
        checkSameZorder(effectzip, effectLog)
        # check_md5(effectzip,effectLog)
        check_disable_keyword(effectzip, effectLog)
        # check_shader(effectzip,effectLog)
        check_algorithm_blit_version(effectzip, effectLog)
        check_algorithmConfig_scriptPath(effectzip, effectLog)
    elif (param == 'CAPCUT'):
        check_pics_size(param, effectzip, effectLog, lokiInformation=lokiInformation)
        disableFiles = []
        disableDirs = ['.vscode']
        checkFileDisable(effectzip, effectLog, disableFiles, disableDirs)
        checktobinary(effectzip, effectLog)
        checkLuaIsNotNil(effectzip, effectLog)
        get_FileSize(effectzip, effectLog, param)
        checkSameZorder(effectzip, effectLog)
        check_capcut_version(effectzip, effectLog)
        # check_md5(effectzip,effectLog)
        check_disable_keyword(effectzip, effectLog)
        # check_shader(effectzip,effectLog)
        check_algorithm_blit_version(effectzip, effectLog)
        capcut_3D_version(effectzip, effectLog)
        check_algorithmConfig_scriptPath(effectzip, effectLog)
        check_js_path_min_version(effectzip, effectLog)
    elif (param == 'XIGUA'):
        check_pics_size(param, effectzip, effectLog, lokiInformation=lokiInformation)
        disableFiles = []
        disableDirs = ['.vscode']
        checkFileDisable(effectzip, effectLog, disableFiles, disableDirs)
        checktobinary(effectzip, effectLog)
        checkLuaIsNotNil(effectzip, effectLog)
        get_FileSize(effectzip, effectLog, param)
        checkSameZorder(effectzip, effectLog)
        check_disable_keyword(effectzip, effectLog)
        check_AR_type(effectzip, effectLog)
        check_algorithm_blit_version(effectzip, effectLog)
        check_algorithmConfig_scriptPath(effectzip, effectLog)


# 传入长度==4，存储检测loki配置功能
def checkLokiEffectZip(effectzip, effectLog, param, lokiInformation):
    if (param == 'FACEU'):
        #    print(param)
        #    print("传入json：",json.loads(lokiInformation))
        checkFaceuVersion(effectzip, effectLog, lokiInformation)
    elif (param == 'QINGYAN'):
        checkQingyanVersion(effectzip, effectLog, lokiInformation)
    elif (param == 'XIGUA'):
        checkXiguaPanelKey(effectzip, effectLog, lokiInformation)

