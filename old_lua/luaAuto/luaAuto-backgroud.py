#coding=utf-8


import os
import zipfile
import sys
import shutil
from pathlib import Path
import json
import struct  


ErrorThing = ""
WarningThing = ""
IEThing = ""
ErrorEnglishThing = ""
JsonData = []
globalWarning = 0
globalError = 0
globalChinese = 0

versionList = ['3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.1.0','3.2.0','3.2.0','3.2.0','3.2.0','3.2.0','3.2.0','3.2.0','3.2.0','3.2.0','3.2.0','3.2.0','3.2.0','3.2.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.3.0','3.4.0','3.4.0','3.4.0','3.4.0','3.4.0','3.4.0','3.4.0','3.4.0','3.4.0','3.4.0','3.4.0','3.4.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.5.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.6.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.0','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.1','3.7.3','3.7.3','3.7.3','3.7.3','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.8.0','3.9.0','3.9.0','3.9.0','3.9.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.0.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.1.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.2.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.3.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.4.0','4.5.0','4.5.0','4.5.0','4.5.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.6.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.7.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.8.0','4.9.0','4.9.0','4.9.0','4.9.0','4.9.0','4.9.0','4.9.0','4.9.0','4.9.0','4.9.0','4.9.0','4.9.0','4.9.0','4.9.0','5.0.0','5.0.0','5.0.0','5.0.0','5.0.0','5.0.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.1.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.2.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.3.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.4.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.5.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.6.0','5.7.0','5.7.0','5.7.0','5.7.0','5.7.0','5.7.0','5.7.0','5.7.0','5.7.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.8.0','5.9.0','5.9.0','5.9.0','5.9.0','5.9.0','5.9.0','5.9.0','5.9.0','6.0.0','6.0.0','6.0.0','6.0.0','6.0.0','6.0.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.1.0','6.2.0','6.2.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.3.0','6.4.0','6.4.0','6.4.0','6.4.0','6.4.0','6.5.0','6.5.0','6.5.0','6.5.0','6.5.0','6.5.0','6.5.0','6.5.0','6.5.0','6.5.0','6.5.0','6.5.0','6.5.0','6.6.0','6.6.0','6.6.0','6.6.0','6.6.0','6.6.0','6.6.0','6.6.0','6.6.0','6.6.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.7.0','6.8.0','6.8.0','6.8.0','6.8.0','6.8.0','6.8.0','6.8.0','6.8.0','6.8.0','6.8.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','6.9.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.0.0','7.1.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.2.0','7.3.0','7.3.0','7.3.0']

classList = ['EffectSDK','EffectSDK','EffectSDK','EffectSDK','EffectSDK','EffectSDK','EffectSDK','EffectSDK','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','AudioManagerV2','AudioManagerV2','AudioManagerV2','AudioManagerV2','AudioManagerV2','AudioManagerV2','AudioManagerV2','AudioManagerV2','AudioManagerV2','AudioManagerV2','AudioManagerV2','AudioManagerV2','RenderInterface','EffectInterface','EffectInterface','EffectInterface','EffectInterface','EffectInterface','EffectInterface','EffectInterface','BEFEffect','BEFEffect','BEFEffect','BEFEffect','BEFEffect','BEFEffect','RenderManager','RenderManager','RenderManager','RenderManager','RenderManager','RenderManager','FaceReshapeFeature','FaceReshapeFeature','FaceReshapeFeature','FaceReshapeFeature','FaceReshapeFeature','FaceReshapeFeature','Game2Dfilter','Game2Dfilter','Game2Dfilter','Game2Dfilter','Game2Dfilter','Game2Dfilter','Game2Dfilter','Game2Dfilter','Game2Dfilter','MessageCenter','MessageCenter','Color','Vec2','Vec2','Vec2','Vec4','Vec4','Vec4','Line2D','Line2D','Line2DEmission','Parabola2DEmission','Box2D','Box2D','Box2D','Box2D','Box2D','Component2D','Component2D','Transform2D','Transform2D','Transform2D','Transform2D','Transform2D','Transform2D','Transform2D','Transform2D','Transform2D','Camera2D','Camera2D','Camera2D','Camera2D','AnimationCurve','AnimationPropertyKey','AnimationProperty','AnimationProperty','Animation2D','Animation2DState','Animation2DState','Animation2DState','Animation2DState','Animation2DState','Animation2DState','Animation2DState','Animation2DState','AnimatorController','AnimatorController','AnimatorController','AnimatorController','AnimatorController','AnimatorController','AnimatorController','AnimatorController','AnimatorController','AnimatorController','AnimatorController','AnimatorController','AnimatorController','AnimatorComponent','BoundingBox2D','BoundingBox2D','BoundingBox2D','BoundingBox2D','Point2DSprite','Point2DSprite','Entity2D','Entity2D','Entity2D','Entity2D','Entity2D','Scene2D','Scene2D','Scene2D','Scene2D','View2D','View2D','Viewer2D','Viewer2D','Viewer2D','Viewer2D','AtlasProtocol','SpriteManager','SpriteManager','SpriteManager','AnimationFactory','AnimationFactory','AnimationFactory','AnimationFactory','Sticker2DV3Feature','Sticker2DV3Feature','Sticker2DV3Feature','Sticker2DV3Feature','Sticker2DV3Feature','Sticker2DV3Feature','Sticker2DV3Feature','Sticker2DV3Feature','Sticker2DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','MultiViewLuaFilter','MultiViewLuaFilter','MultiViewLuaFilter','MultiViewLuaFilter','MultiViewLuaFilter','MultiViewLuaFilter','MultiViewLuaFilter','MultiViewLuaFilter','MultiViewLuaFilter','bef_base_param_st','bef_filter_target_st','bef_keyFrame_info_st','bef_keyFrames_info_st','bef_camera_info_st','bef_camera_info_st','bef_camera_info_st','bef_animation_st','bef_animation_st','bef_animation_st','bef_animation_st','bef_animation_v2_st','bef_animation_v2_st','bef_animation_v2_st','bef_animation_v2_st','bef_texture_info_st','bef_uv_animation_st','bef_uv_animation_st','bef_uv_animation_st','bef_shader_animation_st','bef_shader_animation_st','bef_shader_animation_st','bef_bone_animation_st','bef_bone_animation_st','bef_bone_animation_st','bef_viewport_scale_st','bef_viewport_scale_st','bef_viewport_scale_st','bef_protocol_param_st','bef_protocol_param_st','bef_protocol_param_st','bef_protocol_param_st','bef_base_filter_st','bef_base_filter_st','bef_base_filter_st','bef_base_group_st','bef_base_group_st','bef_base_group_st','bef_base_group_st','bef_base_group_st','bef_build_in_item_st','Viewport','Viewport','Viewport','Viewport','Viewport','InfoStickerDirector','InfoStickerDirector','Animation2DState','Sprite','Sprite','SpriteRenderer','SpriteRenderer','SpriteRenderer','SpriteRenderer','SpriteRenderer','SpriteRenderer','AnimationFactory','AnimationFactory','EffectSDK','EffectInterface','EffectInterface','EffectInterface','EffectInterface','EffectInterface','LuaFaceInfo','LuaFaceInfo','LuaGenderInfo','Sticker3DV3Feature','ARV3Feature','LuaScene','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','BEFBaseFeature','EffectInterface','ARV3Feature','ARV3Feature','FaceMakeupV2Filter','FaceMakeupV2Filter','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','EffectSDK','Sticker2DV3Feature','ARV3Feature','ARV3Feature','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','EffectInterface','EffectInterface','EffectInterface','EffectInterface','EffectInterface','EffectInterface','LuaSRTLine','LuaSRTLine','LuaSRTLine','LuaSRTLine','LuaSRTLine','LuaSRTLine','LuaSRTData','LuaSRTData','LuaObjectInfo','LuaObjectInfo','LuaObjectInfo','LuaJointInfo','LuaJointInfo','LuaJointInfo','LuaJointInfo','FaceMakeupV2Feature','FaceMakeupV2Filter','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','Vertex','Vertex','Vertex','Polygon','Polygon','Polygon','Polygon','Polygon','Canvas','Canvas','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','RectTransform','Sprite','Sprite','BoundingBox2D','Entity2D','Scene2D','AnimationFactory','AnimationFactory','AnimationFactory','AnimationFactory','AnimationFactory','AnimationFactory','AnimationFactory','AnimationFactory','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','GeneralEffectFeature','LuaAnimojiInfo','LuaAnimojiInfo','LuaAnimojiInfo','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','EffectSDK','InstrumentFeature','InstrumentFeature','InstrumentFeature','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','RenderInterface','EffectInterface','Sticker2DV3Feature','Sticker3DV3Feature','LuaScene','LuaScene','LuaScene','LuaScene','GeneralEffectFeature','GeneralEffectFeature','BEFProtocol','BEFProtocol','BEFProtocol','BEFProtocol','BEFProtocol','BEFProtocol','BEFProtocol','BEFProtocol','BEFProtocol','BEFProtocol','HookFilter','HookFilter','BEFEffect','LuaHandInfo','LuaHandInfo','LuaHandInfo','BEFBaseFeature','EffectInterface','EffectInterface','EffectInterface','EffectInterface','BEFEffect','LuaSceneInfo','LuaSceneInfo','LuaTextContent','LuaTextContent','LuaTextContent','LuaTextContent','LuaTextContent','LuaARScanInfo','LuaARScanInfo','LuaARScanInfo','LuaARScanInfo','LuaARScanInfo','Vec3','Vec3','Vec3','Sticker3DV3Feature','Sticker3DV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','ARV3Feature','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','EffectSDK','EffectManager','EffectManager','LuaFaceInfo','LuaFaceInfo','LuaFaceInfo','LuaFaceInfo','LuaSkeletonInfo','LuaSkeletonInfo','LuaSkeletonInfo','Sticker2DV3Feature','Sticker2DV3Feature','FaceStretchFeature','FaceStretchFeature','FaceStretchFeature','FaceStretchFeature','FaceStretchFeature','FaceStretchFeature','FaceStretchFeature','FaceStretchFeature','FaceStretchFeature','FaceStretchFeature','EffectSDK','LuaSkeletonInfo','Sprite','Sprite','Sticker3DV3Feature','Sticker3DV3Feature','AudioPlayer','AudioPlayer','AudioPlayer','AudioPlayer','AudioPlayer','ResourceManager','ResourceManager','ResourceManager','ResourceManager','Scheduler','Scheduler','GameDirector','GameDirector','GameDirector','GameDirector','GameDirector','EffectSDK','EffectSDK','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','Text2DFeature','EffectInterface','Sprite','Sticker2DV3Feature','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','Material','Material','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Quat','Vec2','Vec2','Vec2','Vec2','Vec2','Vec2','Vec2','Vec2','Vec2','Vec2','Vec2','Vec2','Vec2','Vec2','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','Vec3','EffectSDK','BEFBaseFeature','Image2DManager','Image2DManager','Image2DManager','Image2DManager','Image2DManager','Image2DManager','Image2DManager','EffectInterface','EffectInterface','BEFEffect','BEFEffect','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaScene','ElementDrawerFeature','ElementDrawerFeature','ElementDrawerFeature','ElementDrawerFeature','ElementDrawerFeature','ElementDrawerFeature','ElementDrawerFeature','ElementDrawerFeature','ElementDrawerFeature','FaceMakeupV2Feature','FaceMakeupV2Filter','bef_processor_info_st','Sticker3DV3Feature','Sticker3DV3Feature','FaceMakeupV2Filter','Texture','Image2DManager','LuaFaceFiveInfo','LuaFaceFiveInfo','MagnifierParams','Magnifier2D','Magnifier2D','Magnifier2D','Sticker3DV3Feature','LuaScene','LuaScene','LuaScene','GeneralEffectFeature','Mat3','Mat3','Mat3','Mat3','Mat3','Mat3','Mat3','Mat3','BEFProtocol','EffectSDK','EffectSDK','Image2DManager','EffectInterface','LuaHandInfo','LuaHandInfo','LuaHandInfo','AnimationFactory','Sticker2DV3Feature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','MattingFeature','MattingFeature','MattingFeature','MattingFeature','MattingFeature','MattingFeature','MattingFeature','MattingFeature','MattingFeature','ComposerFeature','EffectSDK','EffectSDK','EffectSDK','EffectManager','LuaFaceFittingInfo','Sticker3DV3Feature','LuaScene','LuaScene','LuaScene','LuaScene','LuaScene','MetaDataST','MetaDataST','MetaDataST','MetaDataST','MetaDataST','MetaDataST','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','GeneralEffectFeature','Vec3','EffectInterface','EffectInterface','LuaFaceInfo','LuaAudioSpectrumInfo','LuaAudioSpectrumInfo','LuaAudioSpectrumInfo','FaceMakeupV2Feature','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','EffectInterface','FaceMakeupV2Filter','FaceMakeupV2Filter','GeneralEffectFeature','BefRequirement','BefRequirement','EffectSDK','EffectInterface','EffectManager','LuaObjectTrackInfo','LuaObjectTrackInfo','LuaGazeInfo','LuaGazeInfo','LuaGazeInfo','LuaGazeInfo','LuaGazeInfo','LuaGazeInfo','LuaGazeInfo','LuaGazeInfo','LuaGazeInfo','LuaGazeInfo','LuaGazeInfo','LuaGazeInfo','Sticker2DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','Sticker3DV3Feature','LuaScene','FaceMakeupV2Feature','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','Text2DV2Feature','bef_protocol_merge_info','Mat3','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','Image2DManager','Image2DManager','Image2DManager','EffectInterface','EffectInterface','EffectInterface','EffectManager','CBundle','CBundle','LuaSkeletonInfo','LuaSkeletonInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaMugInfo','LuaMugInfo','LuaMugInfo','LuaMugInfo','LuaMugInfo','Sticker2DV3Feature','Sticker2DV3Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaFaceBeautyScoreInfo','LuaBlingInfo','LuaBlingInfo','LuaBlingInfo','Sprite','Sticker3DV3Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Filter','FaceMakeupV2Filter','FaceMakeupV2Filter','InfoStickerDirector','bef_compat_feature_info_st','bef_amazing_compat_info_st','bef_amazing_info_st','bef_effect_platform_config_st','EffectSDK','AudioManagerV2','EffectInterface','EffectInterface','EffectInterface','EffectInterface','EffectInterface','BEFGlobalFeatureV2','BEFGlobalFeatureV2','BEFGlobalFeatureV2','Mat3','Mat3','Quat','Quat','Vec3','HookFilter','HookFilter','EffectSDK','EffectSDK','BEFBaseFeature','BEFBaseFeature','EffectInterface','EffectInterface','EffectInterface','EffectInterface','EffectInterface','BEFEffect','BEFEffect','EffectManager','EffectManager','EffectManager','EffectManager','LuaTextLayoutInfo','LuaTextLayoutInfo','LuaTextLayoutInfo','Component2D','Transform2D','Transform2D','Transform2D','Transform2D','Transform2D','Transform2D','GeneralEffectAttr','GeneralEffectAttr','GeneralEffectAttr','GeneralEffectAttr','GeneralEffectAttr','GeneralEffectAttr','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectPass','GeneralEffectDraw','GeneralEffectDraw','GeneralEffectDraw','GeneralEffectDraw','GeneralEffectDraw','GeneralEffectDraw','GeneralEffectDraw','GeneralEffectTechnique','GeneralEffectTechnique','GeneralEffectTechnique','GeneralEffectTechnique','GeneralEffectTechnique','GeneralEffectRenderPipeline','GeneralEffectRenderPipeline','GeneralEffectRenderPipeline','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','GeneralEffectRenderer','Entity2D','Amazing3DStickerV3LuaEntry','AmazingBaseLuaEntry','GeneralEffectFeature','GeneralEffectFeature','InfoStickerDirector','InfoStickerDirector','InfoStickerDirector','InfoStickerDirector','InfoStickerDirector','InfoStickerDirector','LuaMusicTime','CE_SRTLine','CE_SRTLine','CE_SRTLine','CE_SRTData','CE_SRTData','CE_SRTData','ScriptComponent','Text2DComponent','Text2DComponent','Text2DComponent','Text2DComponent','Text2DComponent','Text2DComponent','Text2DComponent','SRTParser','SRTParser','SRTParser','SRTParser','Texture','Texture','HookFilter','ComposerFeature','RenderInterface','EffectInterface','LuaHistogramInfo','LuaHistogramInfo','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaScene','LuaSceneInterface','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','EffectInterface','EffectInterface','EffectInterface','EffectInterface','EffectInterface','LuaTeethInfo','LuaTeethInfo','LuaTeethInfo','GeneralEffectFeature','EffectSDK','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','Image2DManager','EffectInterface','BEFEffect','BEFEffect','BEFEffect','EffectManager','EffectManager','EffectManager','CBundle','CBundle','CBundle','CBundle','CBundle','CBundle','CBundle','CBundle','CBundle','CBundle','CBundle','CBundle','LuaTrackingArInfo','LuaTrackingArInfo','Sticker2DV3Feature','LuaScene','LuaScene','LuaScene','LuaScene','LuaSceneInterface','LuaSceneInterface','LuaSceneInterface','LuaSceneInterface','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','Vec3','Vec4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','ContourInfoVector','ContourInfoVector','ContourInfoVector','SegMaskInfo','BEFProtocol','BEFProtocol','HookFilter','HookFilter','EffectInterface','LuaNailInfo','LuaNailInfo','LuaNailInfo','FaceMakeupV2Filter','FaceMakeupV2Filter','GeneralEffectFeature','ContourInfoVector','EffectSDK','EffectSDK','EffectSDK','EffectSDK','EffectInterface','AgeGanSingleFaceFilter','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','BEFBaseFeature','RenderInterface','EffectInterface','BEFEffect','LuaFaceInfo','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','LuaBrush2dParam','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','GeneralEffectFeature','LuaModelInfo','LuaModelInfo','EffectSDK','EffectInterface','EffectManager','EffectManager','EffectManager','EffectManager','EffectManager','EffectManager','LuaTrackingArInfo','LuaTrackingArInfo','BaseLuaObject','BaseLuaObject','BaseLuaObject','FaceMakeupV2Filter','BEFGlobalFeatureV2','BefRequirement','BefRequirement','BefRequirement','BEFProtocol','EffectSDK','EffectSDK','EffectInterface','EffectInterface','bef_processor_info_st','ManualLiquefyFeature','EffectSDK','EffectManager','EffectManager','EffectManager','EffectManager','EffectManager','EffectManager','EffectManager','EffectManager','RenderManager','BefRequirement','BefRequirement','BefRequirement','EffectInterface','EffectInterface','LuaNailInfo','LuaScanningArInfo','LuaScanningArInfo','LuaScanningArInfo','LuaScanningArInfo','LuaScanningArInfo','AmazingLuaScene','GeneralEffectFeature','EffectInterface','EffectManager','EffectManager','EffectManager','LuaFaceInfo','LuaFaceInfo','LuaFaceExpressionInfo','LuaFaceExpressionInfo','LuaFaceExpressionInfo','LuaFaceExpressionInfo','BefRequirement','BefAlgorithmArrayExtParam','BefAlgorithmArrayExtParam','BefAlgorithmArrayExtParam','GeneralEffectFeature','EffectABConfig','EffectABConfig','EffectABConfig','EffectABConfig','EffectManager','AmazingFaceMakeupLuaEntry','FaceMakeupV2Feature','FaceMakeupV2Filter','GeneralEffectFeature','GeneralEffectFeature','NetworkManager','NetworkManager','EffectInterface','EffectManager','EffectManager','EffectManager','EffectManager','CBundle','LuaGenderInfo','LuaGenderInfo','algorithm_result_matting_st','LuaGeneralObjectDetectionInfo','LuaGeneralObjectDetectionInfo','LuaGeneralObjectDetectionInfo','BEFProtocol','BEFMVController','BEFMVFilter','AudioManagerV2','EffectInterface','EffectInterface','EffectInterface','EffectInterface','LuaTrackingArInfo','LuaClothesSegInfo','LuaClothesSegInfo','LuaClothesSegInfo','LuaClothesSegInfo','LuaClothesSegInfo','LuaClothesSegInfo','LuaClothesSegInfo','LuaClothesSegInfo','Sticker2DV3Feature','Sticker2DV3LuaInterface','EffectManager','BEFAudioNode','BEFAudioNode','BEFAudioNode','BEFAudioNode','BEFAudioNode','BEFAudioNode','BEFAudioNode','BEFAudioGraph','AudioInfo','AudioInfo','AudioInfo','AudioInfo','AudioInfo','AudioInfo','AudioInfo','AudioProxy','AudioProxy','AudioProxy','AudioProxy','AudioProxy','AudioProxy','EffectInterface','BEFEffect','EffectManager','LuaBuildingSegInfo','LuaBuildingSegInfo','LuaBuildingSegInfo','LuaBuildingSegInfo','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','FaceMakeupV2Feature','BEFGlobalFeatureV2','BEFGlobalFeatureV2','MattingFeature','MattingFeature','EffectSDK','EffectInterface','BefRequirement']

returnList = ['EffectManager','RenderManager','BEFGlobalFeatureV2','FaceReshapeFeature','FaceMakeupV2Feature','Sticker3DV3Feature','Sticker2DV3Feature','void','bool','int','bool','int','BEFProtocol','EffectInterface','void','void','void','void','void','bool','bool','void','void','void','int','float','BEFEffect','bool','RenderInterface','void','void','void','float','float','BEFBaseFeature','bool','BEFBaseFeature','AudioManagerV2','EffectInterface','bool','void','void','void','bool','bool','bool','null','int','int','void','void','void','Viewer2D','int','Texture','AtlasProtocol','Vec2','int','int','GameFaceInfo','EffectInterface','void','void','null','null','null','null','null','null','null','Line2D','Line2D','Line2DEmission','Parabola2DEmission','null','null','bool','bool','bool','void','bool','Vec2&','void','void','void','void','void','bool','bool','void','void','void','void','void','void','AnimationPropertyKey','AnimationCurve','void','AnimationProperty','void','void','float','bool','bool','bool','bool','void','Animation2D','Animation2DState','Animation2DState','void','short','void','void','void','void','void','void','void','void','AnimatorController','void','void','Box2D&','Box2D&','void','void','bool','Transform2D','void','T','T','Entity2D','void','void','void','Scene2D','void','View2D','RenderEngine','int','int','bool','SpriteManager','bool','bool','Animation2D','Animation2D','Animation2D','Animation2D','void','null','null','int','BEFProtocol','void','void','void','void','void','null','null','int','BEFProtocol','LuaScene','bool','bool','bool','bool','bool','void','null','null','void','int','BEFProtocol','LuaScene','EffectInterface','bool','bool','bool','null','bool','bool','bool','void','void','null','null','int','int','BEFProtocol','bool','bool','bool','bool','bool','bool','bool','float','null','null','int','void','bool','void','uint64_t','Texture','bool','bool','bool','bool','bool','bool','bool','float','std::unique_ptr<MakeupBaseV2Filter>','int','void','bool','null','void','int','BEFProtocol','int','int','int','int','int','int','void','int','char','int','float','float','void','void','void','void','void','void','void','null','null','bool','void','void','void','void','void','bool','null','null','null','void','null','null','void','null','null','bool','void','null','null','bool','void','void','null','null','void','null','null','void','null','null','void','null','null','void','null','null','null','void','null','null','void','null','null','null','bef_base_group_st','void','null','null','null','bool','bool','bool','Viewer2D','Texture','void','void','void','Material','void','Color&','void','Sprite','void','Animation2D','Animation2D','GeneralEffectFeature','void','void','float','float','float','bef_fpoint','bef_rect','float','std::string','std::string','bool','void','null','null','int','BEFProtocol','void','int','double','bool','bool','void','bool','bool','bool','bool','bool','bool','bool','char','bool','bool','bool','bool','bool','bool','bool','bool','bool','bool','void','bool','bool','bool','float','bool','bool','void','LuaSRTData','bef_rectf','int','float','float','int','int','int','LuaSRTLine','int','int','int','bef_rect','int','int','int','bool','int','void','int','bool','bool','null','null','null','null','void','void','void','void','void','CanvasRenderMode','void','Vec2&','void','void','Vec2&','void','Vec2&','bool','void','float','void','float','Vec4','void','void','Vec3&','void','Vec3&','void','Vec3&','bool','bool','RectTransform','void','void','void','bool','void','Entity2D','Animation2D','Animation2D','Animation2D','Animation2D','Animation2D','Animation2D','Animation2D','Animation2D','int','int','int','int','int','bool','int','int','int','void','void','void','int','EntityGUID','void','bool','bool','bool','EntityGUID','EntityGUID','bool','InstrumentFeature','int','int','bool','int','void','void','void','void','void','BEFBaseFeature','bool','bool','bool','bool','void','void','void','bool','bool','void','void','void','Texture','void','bool','void','void','void','void','null','null','BEFBaseFeature','LuaKeyPoint','bef_rect','int','bool','int','int','double','int','bool','bef_fpoint','int','void','char','void','int','long','int','char','float','float','int','null','null','null','void','void','LuaTextContent','void','void','std::vector<std::string>','int','void','bool','void','void','void','void','void','void','bool','bool','bool','bool','bool','bool','Vec3','Vec3','Vec4','Vec3','Vec3','bool','bool','EntityGUID','bool','EntityGUID','bool','bool','bool','bool','bool','bool','bool','FaceStretchFeature','long','void','int','float','float','float','LuaKeyPoint','bef_rect','int','void','void','null','null','void','BEFProtocol','int','std::vector<BRC::Vec2>','std::vector<BRC::Vec2>','std::vector<BRC::Vec2>','std::vector<BRC::Vec2>','void','Text2DFeature','int','Texture','void','void','void','void','void','void','void','void','void','void','Texture','std::string','void','bool','Viewer2D','Interactor','AudioPlayer','ResourceManager','Scheduler','void','GameDirector','null','null','void','BEFProtocol','bool','bool','bool','bool','bool','void','void','LuaTextContent','void','void','std::vector<std::string>','int','void','char','void','char','void','bool','Vec3','Quat','Vec3','bool','Texture','float','bool','null','null','null','null','null','null','void','void','Real','Real','void','void','Real','Real','Real','Real','Vec3','bool','Quat','Quat','Quat','Quat','void','void','null','null','null','null','Real','Real','Real','Real','Real','Real','Real','Vec2','bool','bool','null','null','null','null','Real','Real','Real','Real','Real','Vec3','Vec3','Vec3','Real','Vec3','bool','bool','Vec2','Vec2','Vec2','ElementDrawerFeature','BEFBaseFeature','void','void','void','void','void','void','void','void','bool','BEFBaseFeature','Image2DManager','float','float','float','float','float','float','float','float','float','float','float','float','FaceBeautyScore','int','bool','void','null','null','BEFProtocol','void','void','void','void','void','bool','bool','void','void','void','int','void','void','int','int','null','void','MagnifierParams','void','bool','bool','float','bool','bool','null','null','null','null','Mat3&','void','Mat3&','Mat3&','void','MattingFeature','','null','Texture','LuaKeyPoint','int','int','Animation2D','std::vector<BRC::Vec2>','bool','bool','bool','void','null','null','int','int','int','void','void','BEFProtocol','','carrays.i','null','null','int','bef_fpoint','bool','void','void','Texture','void','double','null','null','void','void','void','void','Image2DManager','void','void','bool','float','effect_result','bool','int','int','float','float','int','void','void','std::string','int','void','int','int','double','void','BefRequirement','bool','null','null','Text2DV2Feature','char','effect_result','int','float','int','LuaKeyPoint','LuaKeyPoint','LuaKeyPoint','LuaKeyPoint','LuaKeyPoint3D','LuaKeyPoint3D','LuaKeyPoint3D','LuaKeyPoint3D','LuaKeyPoint3D','LuaKeyPoint3D','LuaKeyPoint3D','bool','void','void','void','bool','void','void','bool','int','int','int','void','void','int','void','void','bool','int','null','null','void','BEFProtocol','bool','bool','bool','bool','LuaTextContent','void','void','std::vector<std::string>','int','void','char','void','LuaTextLayoutInfo','char','null','Real','BEFProtocol','double','int','int','void','void','void','char','int','CBundle','CBundle&','std::vector<float>','void','int','int','float','float','float','float','float','float','float','float','int','bef_rectf','bef_fpoint','float','int','void','void','bool','bool','bool','bool','bool','bool','float','float','float','float','int','bef_fpoint','float','int','bool','void','bool','bool','int','bool','&','void','void','void','void','HookFilter','void','effect_result','double','double','int','bool','int','int','int','null','Mat3&','void','Quat','void','float','void','ARV3Feature','ComposerFeature','std::string','BefRequirement','LuaFaceInfo','void','float','int','std::string','std::string&','BefRequirement','void','BefRequirement','void','BefRequirement','int','BEFCharLayoutInfo','int','Entity2D','Vec2&','float','void','Transform2D','int','Transform2D','void','void','void','void','void','void','void','void','void','bool','void','void','void','void','void','void','void','void','void','void','void','void','void','void','void','bool','void','void','void','void','char','GeneralEffectPass','GeneralEffectAttr','char','void','int','bool','void','GeneralEffectDraw','GeneralEffectDraw','void','void','char','void','void','void','GeneralEffectTechnique','GeneralEffectTechnique','GeneralEffectTechnique','void','void','void','int','void','void','Color&','void','&','GeneralEffectRenderPipeline','void','void','void','char','bool','bool','char','GeneralEffectFeature','char','LuaMusicTime&','char','bool','void','Vec2','null','int','double','char','char','CE_SRTLine','int','void','void','bool','bool','Texture','LuaTextLayoutInfo','void','char','bool','CE_SRTData','bool','void','int','int','std::vector<float>','BEFEffect','BEFEffect','void','int','float','void','int','void','float','void','float','void','float','void','float','void','float','bool','bool','bool','bool','bool','void','int','bool','bool','bool','int','bef_fpoint','int','bool','AmazingBaseLuaEntry','bool','bool','void','void','SegMaskInfo','bool','bool','void','CBundle&','effect_result','void','bool','bool','int','float','double','std::string','CBundle','void','void','void','void','void','int','float','void','bool','bool','Mat4','Mat4','bool','bool','Mat4','Mat4','bool','bool','bool','bool','null','null','null','null','null','null','null','null','Mat4&','void','Mat4&','Mat4&','Mat4&','Mat4&','Mat4&','Mat4&','Mat4&','Mat4&','Mat4&','Mat4&','Mat4&','Real','void','Real','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','Mat4','ContourInfo&','int','ContourInfo&','Texture','Viewport&','void','void','SegMaskInfo','int','int','bef_rectf','bef_fpoint','void','void','bool','std::vector<BRC::Vec2>&','AgeGanSingleFaceFilter','std::bitset<N>','std::bitset<N>','std::bitset<N>','bool','public:void','std::string','int','void','int','std::vector<BEFBaseFeature*>','double','bool','bef_face_info&','bef_brush2d_param','void','void','void','void','bool','bool','bool','bool','int','char','int','BaseLuaObject','void','void','void','void','BaseLuaObject','BaseLuaObject','int','bool','char','BaseLuaObject','null','std::string&','void','null','null','long','Texture','int','ManualLiquefyFeature','std::vector<float>&','std::string','null','void','std::vector<BRC::Vec3>','int','int','std::vector<BRC::Vec4>','void','int','int','void','Mat3','BEFBaseFeature','null','null','long','std::string&','effect_result','int','int','int','int','float','int','bool','bool','void','effect_result','void','BaseLuaObject','float','int','int','float','float','int','null','null','null','null','bool','char','void','char','bool','std::string','void','void','void','Vec4','bool','int','int','bef_local_edit_info','BaseLuaObject','std::string','BEFMVController','NetworkManager','void','int','Vec4','algorithm_image_result_buffer','int','bef_rectf','int','Texture','BEFMVFilter','Texture','void','bool','Texture','Texture','bool','int','float','float','int','int','int','int','int','int','void','void','CBundle','void','void','void','void','void','void','int','BEFAudioNode','std::string','std::string','std::string','size_t','mammon_midi_note','std::string','std::string','AudioInfo','BEFAudioGraph','void','void','int','int','double','AudioProxy','void','float','float','int','int','int','int','int','int','int','int','int','int','int','Texture','void']

funcList = ['EffectSdk.castEffectManager','EffectSdk.castRenderManager','EffectSdk.castBEFGlobalFeatureV2','EffectSdk.castFaceReshapeFeature','EffectSdk.castFaceMakeupV2Feature','EffectSdk.castSticker3DV3Feature','EffectSdk.castSticker2DV3Feature','EffectSdk.LOG_LEVEL','setFeatureStatus','getFeatureStatus','addTimer','setIntensity','getRenderProtocol','getEffectManager','startPlay','restartPlay','stopPlay','pause','resume','isPlaying','seek','setLoop','setVolume','setPlayerIndex','getPlayerIndex','getCurrentPlayTime','getActiveEffect','getBgmEnable','getRenderManager','setMusicBeatType','setMusicBeatStep','processMusicBeatData','getMusicBeatIntensity','getMusicBeatDuration','addFeature','removeFeature','getFeature','getAudioManager','getEffectManager','addTimer','setShouldRebuildChain','setShouldRebuildChainActive','setEnableBuildInItems','isShouldRebuildChain','isShouldRebuildChainActive','checkFeatureStatusisSuccess','FaceReshapeFeature','setFeatureEnable','getFeatureEnable','setIntensity','setIntensityByType','setIntensityEyeAndCheek','getViewer','luaCallback','getTextureById','getAtlasProtocolById','getFacePosition','addGameTimer','removeGameTimer','getFaceInfo','getEffectManager','sendMessage','postMessage','Color','Vec2','Vec2','Vec2','Vec4','Vec4','Vec4','create','create','create','create','Box2D','Box2D','intersects','contain','containPoint','setEnable','isEnabled','getPosition','setPosition','setScale','rotate','setRotation','setAnchor','addChild','removeChild','clearChilds','setZoomX','setZoomY','setNear','setFar','setCurve','create','getAnimationCurveClip','addKey','getProperty','setLoop','setSpeed','getSpeed','isPlaying','isPaused','isStoped','isWaiting','reset','getAnimation','getAnimationState','getAnimationState','setFps','getFps','playAnimation','pauseAnimation','restartAnimation','stopAnimation','playAnimation','pauseAnimation','restartAnimation','stopAnimation','getController','setColor','setLocalBox2D','getLocalBox2D','getWorldBox2d','setPoints','setPoints','isVisible','getTransform','setVisible','addComponent','getComponent','createEntity','removeEntity','onPause','onResume','getScene','setCamera','getView','getRenderEngine','getWidth','getHeight','setAtlasTexture','getInstance','attachAltas','attachSingleFrame','createPositionAnimation','createRotationAnimation','createScaleAnimation','createFrameClampAnimation','registerFeature','Sticker2DV3Feature','~Sticker2DV3Feature','initWithConfig','getRenderProtocol','playClip','resumeClip','resetClip','appearClip','registerFeature','Sticker3DV3Feature','~Sticker3DV3Feature','initWithConfig','getRenderProtocol','getLuaScene','play','pause','resume','stop','setDeviceOrientation','registerFeature','ARV3Feature','~ARV3Feature','InitEventSystem','initWithConfig','getRenderProtocol','getLuaScene','getEffectManager','handleDistanceEvent','handleVisualEvent','handleActionEvent','LuaScene','play','isAnimPlaying','setDeviceOrientation','setVisible','registerFeature','FaceMakeupV2Feature','~FaceMakeupV2Feature','initWithConfig','setIntensity','getRenderProtocol','play','pause','seek','show','hide','isInit','setUniform','getUniform','FaceMakeupV2Filter','~FaceMakeupV2Filter','checkResExistOrLoaded','initialize','draw','setIntensity','getRequirement','getOutputTexture','play','pause','seek','show','hide','isInit','setUniform','getUniform','createFilterByType','updateFaceParam','initFaceParam','checkSDKResultAvailable','BEFGlobalFeatureV2','registerFeature','checkResExistOrLoaded','getRenderProtocol','initWithFile','setFeatureEnable','getFeatureEnable','setIntensity','setOneColorFilter','setTwoColorFilter','parseResourceforGestureControl','getFilterPathNum','getFirstLoadFilterPath','setTwoColorFilter','getFeatureViewPortWidth','getFeatureViewPortHeight','clearAllFilterProtocol','checkResExistOrLoadedforNormal','clearAllFeaturePar','checkAttributeforNormal','checkAttributeforTwoColor','checkAttributeforColorShift','checkAttributeforTwoShaderPool','MultiViewLuaFilter','~MultiViewLuaFilter','draw','setColRow','setMixViewPort','setTargetTextureSize','active','initialize','handleTimerEvent','~bef_base_param_st','~bef_filter_target_st','~bef_keyFrame_info_st','clear','bef_camera_info_st','~bef_camera_info_st','clear','bef_animation_st','~bef_animation_st','isValid','clear','bef_animation_v2_st','~bef_animation_v2_st','isValid','clear','clear','bef_uv_animation_st','~bef_uv_animation_st','clear','bef_shader_animation_st','~bef_shader_animation_st','clear','bef_bone_animation_st','~bef_bone_animation_st','clear','bef_viewport_scale_st','~bef_viewport_scale_st','clear','bef_protocol_param_st','bef_base_param_st','~bef_protocol_param_st','clear','bef_base_filter_st','~bef_base_filter_st','clear','bef_base_group_st','~bef_base_group_st','bef_base_group_st','&operator=','clear','bef_build_in_item_st','Viewport','Viewport','operator==','operator!=','isValid','getViewer','getTextureById','setFreeze','setAtlasFrame','setTexture','getDefaultSpriteMaterial','setColor','getColor','setSprite','getSprite','setAtlasFrame','createFrameClampAnimation','createFrameAnimation','EffectSdk.castGeneralEffectFeature','setMusicBeatRadius','setMusicBeatOffset','getMusicBeatMaxPitch','getMusicBeatMinPitch','getMusicBeatCurPitch','getFace106Point','getFaceRect','isMan','getDebugInfoString','getDebugInfoString','isVisible','registerFeature','GeneralEffectFeature','~GeneralEffectFeature','initWithConfig','getRenderProtocol','setFeatureGeneralStatus','setIntensity','getTimeStamp','handleEffectEvent','handleARTouchEvent','InitEventSystem','handleFace3DMeshEvent','setUniformRenderCache','setUniformInt','setUniformFloat','setUniformVec2','setUniformVec3','setUniformVec4','EffectSdk.getSDKVersion','setClipRenderCache','handleTouchEvent','handleManipulateEvent','pause','resume','stop','setEntityScreenPosition','setEntityScreenPosition','setEntityRotationIncrement','setEntityScaleIncrement','InitEventSystem','pushCommandMove','pushCommandRemove','pushCommandGrab','getMusicCurrentTime','getFontStatus','getSRTStatus','swapSRTIndex','getSRTData','getRenderCacheSize','index','startTime','endTime','text','charAt','length','data','count','getCount','getType','getObjectRect','getNumber','getPositionX','getPositionY','getDetect','setIntensity','setIntensity','setIntensity','pushCommandHistogram','pushRefHistogram','Vertex','Vertex','Vertex','Polygon','setDirty','setIndexDirty','insertVertex','reset','setRenderMode','getRenderMode','setPivot','getPivot','setAnchor','setAnchorMin','getAnchorMin','setAnchorMax','getAnchorMax','isAnchorPolymeric','setWidth','getWidth','setHeight','getHeight','getRect','setRect','setPosition','getPosition','setScale','getScale','setRotation','getRotation','addTransform','removeTransform','getParentTransform','setParentTransform','setGeometryMesh','setGeometry','isOutOfFrustum','setOrderInLayer','getEntity','createMoveToAnimation','createMoveToAnimationWithKeys','createScaleToAnimation','createScaleToAnimationWithKeys','createRotateToAnimation','createRotateByAnimation','createClampToAnimation','createAlphaToAnimation','initWithFile','checkResExistOrLoaded','setMakeupResource','setFeatureEnable','getFeatureEnable','setUniformImagePath','getAnimojiInfoState','getAnimojiInfoID','getAnimojiCount','InitEventSystem','bindEntityToFaceID','unbindEntityToAnyFaceID','getBindedFaceIDForEntity','getEntityGUIDWithName','setVisibleWithGUID','isVisibleWithGUID','setEntityComponentEnableWithName','setEntityComponentEnableWithGUID','cloneEntity','removeEntityWithName','removeEntityWithGUID','EffectSdk.castInstrumentFeature','getInstrumentActionIdByIndex','getInstrumentActionLen','checkInstrumentPositionReady','getOrderKey','setOrderKey','addTarget','removeTarget','removeAllTargets','setInputTexture','getRenderChainFeatureByOrderKey','checkMusicBeatEmpty','setClipFps','handlePoint2DTransEvent','forceStop','setPosition','setOrientation','setScale','pushCommandGrabAlgorithm','pushCommandPutAlgorithm','addTarget','removeTarget','removeAllTargets','getOutputTexture','setEnable','isEnable','setViewport','setNeedBlend','setInputTexture','replaceInputTexture','HookFilter','HookFilter','addBaseFeature','getHandKeyPoint','getHandRect','getHandCount','removeTimer','getInputWidth','getInputHeight','getInputAspectRatio','getOrientation','removeTimer','getScene','getResult','setTextContent','getTextContent','removeTextContent','getEntityCount','getEntityGUID','getNthLogoState','getNthLogoName','getNthLogoXYArray','getNthLogoXYElement','getLogosCount','Vec3','Vec3','Vec3','showInputKeyboard','hideInputKeyboard','getLuaTextContent','showInputKeyboard','hideInputKeyboard','getTextContent','getTextMaxCount','setLanguage','removeEntityWithGUIDRecursively','setWorldPosition','setWorldOrientation','setWorldScale','setPositionGUID','setOrientationGUID','setScaleGUID','setEntityScreenPositionPlaneName','setEntityScreenPositionPlaneNormal','setEntityScreenPositionOffsetZ','setEntityRotationIncrementWithGUID','setEntityScaleIncrementWithGUID','makeEntityFaceCamera','getEntityScreenPosition','getWorldPosition','getWorldOrientation','getWorldScale','getText3DParagraphBoundingBox','followEntity','unfollowEntity','createText3DEntities','updateText3DEntities','pickEntityGroup','createEntityGroup','removeEntityGroup','setUniformInt','setUniformFloat','setUniformVec2','setUniformVec3','setUniformVec4','EffectSdk.castFaceStretchFeature','getRequirment','disableAlgorithm','getFaceCount','getFaceRoll','getFacePitch','getFaceYaw','getSkeletonKeyPoint','getSkeletonRect','getSkeletonCount','setVertices','unsetVertices','FaceStretchFeature','~FaceStretchFeature','registerFeature','getRenderProtocol','setIntensity','getStretchQ','getStretchP','getTemplateQ','getTemplateP','setDirty','EffectSdk.castText2DFeature','getSkeletonID','getTexture','setAlpha','setARScanType','setARScanAnchors','play','replay','stop','pause','resume','loadAsset','loadAssetDeep','getTexture','getAudio','schedule','removeSchedule','getViewer','getInteractor','getAudioPlayer','getResourceManager','getScheduler','EffectSdk.print','EffectSdk.getSharedDirector','Text2DFeature','~Text2DFeature','registerFeature','getRenderProtocol','pushCommandGenerate','pushCommandGenerateUTF8','pushCommandGenerate','pushCommandMove','pushCommandRemove','updateFontPath','updateFontPath','getLuaTextContent','showInputKeyboard','hideInputKeyboard','getTextContent','getTextMaxCount','setLanguage','getLanguage','setMaxCount','getPlatform','setAssetPath','setClipStartPlayTimestamp','getLocalPosition','getLocalOrientation','getLocalScale','setUniformTex','getUniformTex','getFloat','setFloat','Quat','Quat','Quat','Quat','Quat','~Quat','set','set','dot','normalize','inverse','unitInverse','roll','pitch','yaw','normLength','QuaternionToEuler','isNaN','slerp','nlerp','squad','rotation','fromAngleAxis','fromMat3','Vec2','Vec2','Vec2','~Vec2','length','squaredLength','distance','squaredDistance','dotProduct','crossProduct','normalize','reflect','isNaN','isZeroLength','Vec3','Vec3','Vec3','~Vec3','length','squaredLength','distance','squaredDistance','dotProduct','crossProduct','perpendicular','randomDeviat','normalize','reflect','isNaN','isZeroLength','xy','xz','yz','EffectSdk.castElementDrawerFeature','clone','play','resume','reset','appear','setFps','addProcessor','removeProcessor','enableAudioEffect','setAudioEffectIndex','addFeature','getImage2DManager','getLeftPlump','getRightPlump','getLeftDouble','getRightDouble','getFace','getFaceLong','getEye','getJaw','getFaceWidth','getFaceSmooth','getNoseWidth','getForeHead','getFaceBeautyScore','getFaceCount','reset','registerFeature','ElementDrawerFeature','~ElementDrawerFeature','getRenderProtocol','setColor','addLine','setLinePoint','removeLine','formLines','setOptimize','setOptimize','clear','setExtraInfo','setUpdateStartTime','updateFaceParam','addUVFrame','updateProcessorImagePaths','getFacePartScore','getBeautyID','MagnifierParams','setParams','getParams','setBgTexture','handleDeviceOrientEvent','setCameraOrientation','getDeviceFovy','setCameraFovy','setUniformTextureStar','Mat3','Mat3','Mat3','~Mat3','identity','set','transpose','inverse','insertRequiresInputsIndex','EffectSdk.castMattingFeature','EffectSdk.castComposerFeature','Image2DManager','getRenderCacheTexture','getHandExtensionPoints','getHandId','getAction','createRotateToAnimationWithKeys','getVertices','pushCommandGrabCPUAlgorithm','setAttributeFromRenderCache','setBrcData','registerFeature','MattingFeature','~MattingFeature','initWithConfig','setIntensity','setIntensity','playClip','resetClip','getRenderProtocol','getGameEffect','EffectSdk.%array_class','EffectSdk.%array_class','EffectSdk.%array_class','getRenderCacheIntValue','getFace106Point','handleFaceFittingEvent','setOrientationGUID','updateMeshCooking','getAttachedRenderTexture','getCurrentTime','getCostTime','MetaDataST','MetaDataST','setVertexListPos','setVertexListUV','setNormalList','setIndiceList','getImage2DManager','getResourcesFilesName','addSequenceProcessor','pushCommandGrabCPUAlgorithm','dotProduct','setAudioSpectrumLength','getUseAmazing','getFaceID','getSpecLen','getSpec','getSpecTime','setOpacity','setActiveIntensity','setIntensityOpacity','translateFilterType','checkResExistOrLoaded','resetProtocol','setFeatureEnable','getFeatureEnable','getTransitionDuration','buildParam','getRequirement','setBrcAttributeData','BefRequirement','BefRequirement','EffectSdk.castText2DV2Feature','getInputText','setAlgorithmExtParam','getStatus','getPose','getFaceId','getLeftEyePos2D','getRightEyePos2D','getLeftEyeGaze2D','getRightEyeGaze2D','getLeftEyePos3D','getRightEyePos3D','getLeftEyeGaze3D','getRightEyeGaze3D','getMidEyeGaze3D','getHeadR3D','getHeadT3D','setClipAlpha','removeFeaturesIfNeed','mergeFeature','addFeatureToRemove','hasMergedFeature','mergeFeaturesEnd','sendEventsIfNeed','estimateCamPos','getIntensity','getIntensity','getActiveIntensity','setExclusive','clearExclusive','getIntensity','setExclusive','clearExclusive','getUniformFloat','_setIntensity','Text2DV2Feature','~Text2DV2Feature','registerFeature','getRenderProtocol','generateBitmapUTF32','generateBitmapUTF8','moveRenderCache','removeRenderCache','getLuaTextContent','showInputKeyboard','hideInputKeyboard','getTextContent','getTextMaxCount','setLanguage','getLanguage','setMaxCount','getTextLayoutWithKey','getRootDir','~bef_protocol_merge_info','at','getRenderProtocol','getTimeStamp','getDisplayWidth','getDisplayHeight','play','playFromTo','setHideWhenPlayEnd','getFontPath','getFontFaceIndex','getBundleInfo','getRenderInfo','GetFloatArray','SetFloatArray','getWidth','getHeight','getChin','getWrinkle','getEyebag','getFaceratio','getMouthwidth','getEyeshape','getEyedist','getEyebrowdist','getMugCount','getMugRect','getPoint','getProb','getId','playClipFromTo','setHideWhenPlayEnd','playClip','playClipFromTo','setHideWhenPlayEnd','setHideWhenPlayEnd','playClip','playClipFromTo','getLWrinkle','getLEyebag','getRWrinkle','getREyebag','getCornersCount','getCornersPoint','getCornersQuality','setGifFile','mergeFeature','setUseAmazing','getUseAmazing','draw','updateFaceParam','checkSDKResultAvailable','getCurrentInfoStickerDir','clear','clear','clear','clear','EffectSdk.castHookFilter','set3DAudioPos','processMusicBeatData','getEffectStartTime','getEffectEndTime','getCameraPosition','getMaleMakeupState','setOneColorFilterIntensityV3','setTwoColorFilter','getFilterIntensity','Mat3','makeRotation','ToAngleAxis','lookRotation','orthoNormalize','getFloatData','pushHookCommand','EffectSdk.castARV3Feature','EffectSdk.castComposerFeature','getAbsPath','getRequirement','getMVRenderCacheLuaFaceInfo','setRenderCacheFloat','getRenderCacheFloat','getCurrentClipIndex','getMVAlgorithmResultKey','BEFEffect::getResRoot','getRequirement','setFeatureAlgorithmPairs','getFeatureAlgorithmPairs','setEffectAlgorithmPairs','getEffectAlgorithmPairs','getCount','getCharLayout','getLineCount','getAttachedEntity','getScale','getRotation','setScale','getParent','getChildCount','getChild','setAttributeArray','setAttributeArray','setAttributeArray','setIndexArray','setIndexArray','setBeginMode','setShaderSource','setShaderFilePath','setDirty','isDirty','setUniformTexture','setUniformTexture','setUniformRenderTexture','setUniformRenderTexture','setUniformBool','setUniformInt','setUniformFloat','setUniformVec2','setUniformVec3','setUniformVec4','setUniformIntArray','setUniformFloatArray','setUniformVec2Array','setUniformVec3Array','setUniformVec4Array','addUniformType','removeUniform','setBlendFunc','setBlendFunc','clearUniforms','getName','getPass','getAttr','getName','setRenderTargetId','getRenderTargetId','isEnable','setEnable','getDraw','addDraw','removeDraw','clearDraws','getName','setClearColor','setClearDepth','setClearType','addTechnique','getTechnique','getActiveTechnique','setActiveTechnique','removeTechnique','clearTechniques','getZOrder','setZOrder','setColor','getColor','setBoundingBoxVerts','getBoundingbox','getRenderPipeline','addRenderPipeline','addScreenRenderPipeline','removeRenderPipeline','getEntityName','handleDeviceOrientEvent','handleDeviceOrientEvent','getClassName','getClassPtr','getCurrentInfoStickerDir','getCurrentMusicTime','getInfoStickerName','getManipulateState','setOffset','getOffset','LuaMusicTime','getIndex','getStartTime','getText','getHeaderItem','data','getSize','setLuaScript','initText2DComponent','createTexture','removeTexture','getTextureWithKey','getTextLayoutWithKey','setFontPath','getFontPath','setSRTInfo','getSRTData','isDirty','setDirty','getWidth','getHeight','getFloatArray','getGameEffect','getEffectByName','resetFaceClusting','getCount','histogramAtHueIndex','setBrushType','getBrushType','setStrokeSize','getStrokeSize','setStrokeStep','getStrokeStep','setFeatherSize','getFeatherSize','setSpeedInfluence','getSpeedInfluence','setBrushColor','getBrushColor','setRenderToTexturePassEnabled','setRenderToTexturePassEnabled','setBrush2DParam','getBrush2DParam','pushCommandHistogramCalculation','setTeethParam','getRenderCacheIntValue','setAlgorithmParamInt','setAlgorithmParamFloat','setAlgorithmParamStr','getFaceCount','getPoint','getId','pushCommandHistogramCalculation','EffectSdk.castAmazingFeature','registerHandle','unregisterHandle','unregisterAllHandles','gotoFrame','getRenderCacheSegMaskInfo','registerHandle','unregisterHandle','unregisterAllHandles','getRenderInfo','setAlgorithmRuntimeParam','modifyAlgorithmConfigs','ContainsKey','GetBool','GetInt','GetFloat','GetDouble','GetString','GetBundle','SetBool','SetInt','SetFloat','SetDouble','SetString','getStatus','getPose','seek','reset','resetBoneAnim','getProjectionMatrix','getViewMatrix','reset','resetBoneAnim','getProjectionMatrix','getViewMatrix','setUniformMat3','pushCommandGrabSegMaskInfo','setLuaAttributeData','setLuaRenderObject','Vec3','Vec4','Mat4','Mat4','Mat4','Mat4','Mat4','~Mat4','identity','set','makeTranslation','makeRotation','makeScale','makeTransform','makeLookAt','makeOrtho','makePerspective','makePerspectiveByCameraIntrinsic','addTranslation','transpose','inverse','at','decomposition','determinant','translation','rotation','scale','transform','lookAt','ortho','perspective','project','get','size','__getitem__','getTexture','getViewport','setInputRenderCache','pushHookCommand','getSegMaskInfo','getClientState','getNailCount','getNailRect','getPoint','clearRTTextureIn','setRTTextureFlagMakeupV2','setLuaRenderObjectByVertexVec2','mergeContourPoints','EffectSdk.castAgeGanSingleFaceFilter','EffectSdk.operator&','EffectSdk.operator','EffectSdk.operator^','getEnableNativeBuffer','setAgeGanFaceID','getType','getMinorOrderKey','setMinorOrderKey','getCloneType','getRenderChain','getDeltaTime','removeFeature','getFaceInfo','getAllParams','setCurveType','setNoiseInfluence','setUseOrientation','setOrient','setBrush2DParameters','getBrush2DParameters','setUniformInputEffectIndex','setUniformLocalInput','getModelLevel','getVersion','EffectSdk.autoCastBaseLuaObject','getAlgorithmResultFromRenderCache','clearAllPhotoAlgorithmResults','clearPhotoAlgorithmResult','processTextureWithAlgorithm','processImageWithAlgorithm','getPhotoAlgorithmResult','getVideoFrameAlgorithmResult','getAccuracy','isMirrored','getClassName','getClassPtr','~BaseLuaObject','translateFilterType','loadResource','BefRequirement','BefRequirement','ToULLong','getInputTextureFromMap','EffectSdk.autoCastBaseLuaObject','EffectSdk.castManualLiquefyFeature','getMusicMetadata','getRenderCacheStringValue','bef_processor_info_st','setTouchInfo','EffectSdk.getFitVertexCoord','getDuetWidth','getDuetHeight','getDuetStickerForbid','setDuetStickerForbid','setDuetMode','getDuetMode','setDuetTouchTransform','getDuetTouchTransform','getTerminalFeature','BefRequirement','BefRequirement','ToULLong','getMusicBeatFilePath','setMusicBeatFilePath','getCls','getObjectId','getStatus','getAccuracy','getPose','getUniformScanCode','resetBoneAnim','pushCommandHistogramCalculation','enableAudioProcessByType','setAlgorithmExtParam','setRenderCacheTexture','getFrameAlgorithmResult','getFaceOcclusion','getFaceAction','getFaceCount','getAge','getAttractive','getExpressionType','BefRequirement','BefAlgorithmArrayExtParam','BefAlgorithmArrayExtParam','BefAlgorithmArrayExtParam','pushCommandGrabCPUAlgorithmByOffset','requestABInfo','configABValue','requestABInfoWithLicense','getABValue','getABLicense','getAMGScene','getAMGScene','getAMGScene','getPixelColor','downloadPixel','get','post','getXTLocalEditParam','getPhotoNativeAlgorithmResult','getCacheDir','getMVController','getNetworkManager','SetHandle','getRacial','getRacialPros','getUnRealTimeModeBuffer','getObjNum','getObjBbox','getObjLabel','getInputTextureFromMap','getMVFilter','getInputTexture','setDataSource','reverseAudioWav','createRenderCacheTexture','getCurDstTexture','captureTexture2Bitmap','getObjectId','getShiftX','getShiftY','getLeft','getTop','getRight','getBottom','getWidth','getHeight','updateClipImagePaths','updateClipImagePaths','getFrameTaskRenderInfo','connect','op','op','op','op','op','opInt','createNode','getAccompanyPath','getSamiResDir','getSamiDescFile','getMidiSize','getMidiNote','getNotePitchPath','getGraphPresetString','getAudioInfo','createGraph','useGraph','start','getTime','getUnderRunCount','getRecordCurrentTime','getAudioProxy','disableRequirement','getShiftX','getShiftY','getWidth','getHeight','initWithConfig','initWithConfig','initWithFile','initWithFile','initWithFile','initWithFile','initWithConfig','initWithConfig','EffectSdk.uploadImageByTexture','getCurSrcTexture','setRequirement']

parameterList = ['1','1','1','1','1','1','1','2','2','0','3','2','0','0','0','0','0','0','0','0','1','1','1','1','0','0','0','0','0','1','1','0','2','2','2','1','1','0','0','3','1','1','2','0','0','0','0','1','0','1','2','2','0','1','1','1','0','3','1','0','0','4','4','4','0','1','2','0','1','4','2','2','3','4','0','2','1','1','1','1','0','0','1','1','1','1','1','1','1','0','1','1','1','1','1','2','1','1','1','1','1','0','0','0','0','0','0','1','1','1','1','0','1','1','1','1','1','1','1','1','0','1','1','0','0','1','2','0','0','1','0','0','1','1','0','0','0','1','1','0','0','0','1','0','4','3','6','6','6','6','0','0','0','2','0','4','3','2','3','0','0','0','2','0','1','3','3','3','3','7','0','0','0','1','2','0','0','0','1','1','1','1','4','3','5','2','0','0','0','2','1','0','1','1','3','1','1','1','3','2','0','0','0','0','1','1','0','0','1','1','3','1','1','1','3','2','1','2','2','2','0','0','0','0','2','1','0','1','1','3','1','0','0','3','0','0','0','1','0','0','0','0','0','0','0','1','2','1','2','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','0','4','1','1','0','0','1','1','1','1','0','1','0','1','0','1','6','2','1','1','1','0','0','1','2','1','1','0','0','1','0','0','0','2','0','1','1','0','1','1','1','1','4','4','4','5','6','7','0','3','1','1','3','3','3','4','7','5','2','1','3','2','8','0','0','0','0','0','1','0','0','0','0','1','0','1','0','0','0','1','0','1','1','1','2','2','2','1','2','1','1','2','0','1','1','1','1','1','0','1','0','1','1','0','1','0','0','1','0','1','0','0','4','1','0','1','0','1','0','1','1','0','1','1','1','1','1','1','5','4','5','4','5','4','5','5','2','0','1','1','0','4','1','1','0','1','2','1','1','1','2','1','3','3','2','1','1','1','1','0','0','0','1','2','1','0','2','2','0','3','1','3','4','5','4','4','4','2','1','0','0','1','0','1','1','2','2','0','1','3','2','1','0','3','0','0','0','0','3','1','0','3','1','1','0','1','1','1','1','2','0','0','1','3','3','3','0','3','3','0','0','1','1','4','5','4','4','5','4','4','7','4','5','2','1','1','1','1','1','2','2','1','2','3','2','1','1','4','4','5','6','7','1','0','1','0','1','1','1','2','1','0','5','2','0','0','0','0','1','0','0','0','0','0','1','1','0','1','1','1','2','2','1','1','1','1','1','1','1','6','1','0','0','0','0','0','1','0','0','0','0','0','10','9','3','2','1','0','2','0','3','3','0','0','1','0','1','0','1','3','1','1','1','4','2','1','2','0','1','1','4','2','0','1','2','1','0','0','0','1','1','1','0','1','0','4','4','6','3','2','1','1','1','2','0','0','0','1','1','1','1','0','1','0','1','1','1','3','0','0','0','1','1','1','1','0','2','0','1','0','1','0','0','0','1','2','3','3','2','3','3','5','2','1','1','2','0','1','1','1','1','1','1','1','1','1','1','1','1','1','0','3','0','0','0','0','4','4','4','1','0','1','1','0','1','1','3','2','4','1','0','0','1','0','1','1','4','0','1','4','0','1','9','0','0','9','0','0','1','1','1','1','1','2','1','1','4','2','1','2','7','0','0','0','2','1','2','2','0','0','0','2','2','2','1','2','1','4','2','1','0','0','3','0','1','1','1','1','0','2','3','3','1','1','0','1','0','1','0','2','3','2','1','0','0','1','0','0','0','0','3','0','2','1','0','1','0','1','1','1','1','1','1','1','1','1','1','1','1','1','3','0','1','1','1','0','1','5','2','2','2','2','0','2','2','0','4','2','0','0','0','0','5','4','2','1','0','3','3','0','0','1','0','1','1','0','0','2','0','0','0','0','3','6','3','0','0','0','0','1','2','0','0','1','1','1','1','1','1','1','1','0','1','2','1','1','6','3','2','5','2','2','2','5','1','1','1','1','0','1','1','3','1','1','0','1','3','2','0','0','0','0','0','1','3','0','0','0','0','0','2','5','2','1','1','2','2','2','1','2','1','1','0','0','1','2','1','1','2','0','0','2','1','2','1','0','1','0','0','0','0','1','0','0','1','3','3','3','2','2','1','2','2','1','0','2','8','2','8','2','2','2','2','2','2','2','2','2','2','2','2','1','1','3','0','0','0','0','0','1','0','0','1','1','2','1','0','0','4','1','1','1','1','0','1','1','0','0','1','1','0','1','0','1','5','4','1','0','1','1','0','0','0','0','1','1','2','1','0','0','0','0','1','1','0','3','1','4','1','1','1','1','0','1','0','0','1','0','0','1','0','1','0','0','1','1','0','1','0','1','0','1','0','1','0','4','0','2','2','2','2','2','1','1','3','3','3','0','2','1','3','1','3','3','0','3','1','3','3','0','0','2','2','1','1','1','1','1','1','1','2','2','2','2','2','0','1','3','3','3','0','0','3','3','0','0','4','3','3','7','1','1','0','1','1','1','16','0','0','16','1','1','1','3','3','6','4','8','1','0','0','2','3','0','1','1','1','3','3','6','4','8','1','0','1','0','0','2','6','1','0','0','1','2','0','1','7','0','1','2','2','2','0','1','0','0','1','0','0','0','1','0','0','1','1','1','1','2','2','4','3','0','0','1','2','0','2','6','5','2','2','0','0','0','0','0','1','0','2','1','1','1','1','1','1','1','0','2','3','0','0','0','1','1','0','1','0','0','2','1','1','0','1','1','0','0','0','1','0','3','7','2','1','2','2','1','1','0','1','1','1','1','0','1','1','5','0','3','1','3','0','0','0','0','2','0','3','4','2','1','0','0','0','2','1','1','0','0','1','1','1','0','1','1','3','3','0','3','0','0','0','0','0','0','0','0','0','4','4','0','1','1','2','2','2','6','1','1','0','0','0','0','1','1','1','1','0','1','0','0','0','0','0','2','0','0','0','0','1','2','1','2','1','2','1','2','8','0','1']



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
    if (len(classList) != len(returnList) or len(classList) != len(funcList) or len(classList) != len(
            versionList) or len(classList) != len(parameterList)):
        print("error:   列表个数不相等 ")
        exit(0)
    myClassManager = ClassManager()
    while (i < len(classList)):
        myClassManager.funcToClass[funcList[i]] = classList[i]
        myClassManager.funcToReturnName[funcList[i]] = returnList[i]
        myClassManager.funcToVerion[funcList[i]] = versionList[i]
        if (classList[i] not in myClassManager.classDic):
            myClassManager.classDic[classList[i]] = MyClass()
            myClassManager.classDic[classList[i]].className = classList[i]

        if (funcList[i] not in myClassManager.classDic[classList[i]].funcDic):
            myClassManager.classDic[classList[i]].funcDic[funcList[i]] = MyFunc(i)
            myClassManager.classDic[classList[i]].funcDic[funcList[i]].className = classList[i]
            myClassManager.classDic[classList[i]].funcDic[funcList[i]].funcName = funcList[i]
            myClassManager.classDic[classList[i]].funcDic[funcList[i]].version = versionList[i]
            myClassManager.classDic[classList[i]].funcDic[funcList[i]].parameter = parameterList[i]
            myClassManager.classDic[classList[i]].funcDic[funcList[i]].returnName = returnList[i]
        else:
            myClassManager.classDic[classList[i]].funcDic[funcList[i]].className = classList[i]
            myClassManager.classDic[classList[i]].funcDic[funcList[i]].funcName = funcList[i]
            myClassManager.classDic[classList[i]].funcDic[funcList[i]].version = versionList[i]
            myClassManager.classDic[classList[i]].funcDic[funcList[i]].parameter = parameterList[i]
            myClassManager.classDic[classList[i]].funcDic[funcList[i]].returnName = returnList[i]

        i += 1
    
    myClassManager.funcToVerion['getRenderProtocol'] = '4.6.0' #临时todo

    return myClassManager


listCast = {'EffectSdk.castEffectManager', 'EffecctSdk.castRenderManager', 'EffectSdk.castBEFGlobalFeatureV2',
            'EffectSdk.castFaceReshapeFeature', "EffectSdk.castSticker2DV3Feature",
            "EffectSdk.castGeneralEffectFeature", "EffectSdk.castFaceMakeupV2Feature",
            "EffectSdk.castSticker3DV3Feature", "EffectSdk.castElementDrawerFeature", "EffectSdk.castText2DFeature","EffectSdk.castText2DV2Feature","EffectSdk.castAmazingFeature"}

handleFuncList = {'handleFaceActionEvent': '3.1.0', 'handleHandGestureEvent': '3.1.0',
                  'handleHandDistanceEvent': '3.1.0', 'handleAnimationEvent': '3.1.0', 'handleTouchEvent': '3.5.0',
                  'handleTimerEvent': '3.1.0', 'handleFeatureEvent': '3.1.0', 'handleEffectEvent': '3.1.0',
                  'handleUpdate': '3.1.0', 'handleAudioEvent': '3.1.0', 'handleClientMsgEvent': '3.1.0',
                  'handleRecodeVedioEvent': '3.2.0', 'handleActionDetectStaticEvent': '4.2.0',
                  'handleActionDetectSequenceEvent': '4.2.0', 'handleFaceAttributeEvent': '3.3.0',
                  'handleFaceInfoEvent': '3.3.0', 'handleGenderEvent': '3.3.0',
                  'handleFacePetActionDetectEvent': '3.3.0', 'handleManipulateEvent': '3.5.0',
                  'handleHandSeqActionEvent': '3.6.0', 'handleJointInfoEvent': '3.6.0', 'handleObjectEvent': '3.6.0',
                  'handleCarDoorOpenDetectEvent': '3.7.0', 'handleAnimojiInfoEvent': '3.7.1',
                  'handleHandInfoEvent': '3.9.0', 'handleComposerUpdateNodeEvent': '3.9.0',
                  'handleSceneInfoEvent': '4.0.0', 'setKeyboardHide': '4.0.0', 'handleInputText': '4.0.0',
                  'handleLicensePlateDetectEvent': '4.0.0', 'handleSkeletonInfoEvent': '4.1.0',
                  'handleCaptureEvent': '4.2.0'}

featureList = {'getFeature': '3.1.0', 'getEffectManager': '3.1.0', 'getAudioManager': '3.1.0'}

name2ClassDic = {}

confirmFiled ={'audio':'AudioManagerV2','scene':'LuaScene'} #手动添加的字段，用于二阶查找， {字段:类}

#判断贴纸包里是否有坐标
coordinateList = {'getFace106Point','setVertices','getInputWidth','getInputHeight','getSkeletonKeyPoint'}

'''
file_bin 是文本文件的二进制
文件头是AMGS， 用ascall 比较
'''
def isencrypt(file_bin):
    if(len(file_bin) > 11):
        validHeader = file_bin[0] == 65 and file_bin[1] == 77 and file_bin[2] == 71 and file_bin[3] == 83 and file_bin[4] == 0x17 and file_bin[5] == 0x1E and file_bin[6] == 0x0A and file_bin[7] == 0x0E;
        validVersion = file_bin[8] == 1

        return validHeader and validVersion

    return False

#解密函数 传入加密的str 文件， 输出解密str 文件
def decrypt(file_str):
    if(isencrypt(file_str)):
        keyA = 0X28
        keyB = 0x5A
        i = 16 #开头长度
        key_str = ""
        bytes_str = bytearray(file_str)
        while i < len(bytes_str):
            key = (file_str[i]^keyB) - keyA
            # print(type(key))
            # print(type(key.to_bytes(4,byteorder='little', signed=True)))
            # print(type(file_str[i]))
            # print(type(file_str))
            bytes_str[i] = key
            i += 1
        bytes_str = bytes_str[20:]
        decrpt_str = bytes_str.decode('utf-8')
        return decrpt_str
    else:
        return file_str.decode('utf-8')






def participle(Strings, file_name):
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

    #


def parseConfigFile(configFile, dir_name):
    global ErrorThing
    global ErrorEnglishThing
    global JsonData
    global globalError
    global globalWarning

    with open(configFile, 'r') as f:
        json_string = json.loads(f.read())
        version = ''
        if('version' in json_string):
            version = json_string['version']
            if(version < '4.0.0'):
                ErrorThing = ErrorThing + "error： config 版本号低于4.0.0，应改成4.0.0\n"
                ErrorEnglishThing = ErrorEnglishThing + "error: config.json version < 4.0.0 please change to 4.0.0 \n"
                tempData = {}
                tempData['code'] = 1
                tempData['type'] = 'VERSION_ERROR'
                tempData['file'] = dir_name
                tempData['line'] = '-1'
                tempData['msg'] = 'config.json version:%s 应改成4.0.0'%(version)
                JsonData.append(tempData)
                globalError = 1
        else:
            ErrorThing = ErrorThing + "error： config文件没有识别版本号\n"
            ErrorEnglishThing = ErrorEnglishThing + "error: config.json dose't recognize version number\n"
            tempData = {}
            tempData['code'] = 1
            tempData['type'] = 'NO_VERSION'
            tempData['file'] = dir_name
            tempData['line'] = '-1'
            tempData['msg'] = 'config.json没有识别版本号'
            JsonData.append(tempData)
            globalError = 1
        

        features = []
        requirements = []
        config_path = []
        req = {}
        effects = {}
        if('effect' in json_string):
            effects = json_string['effect']
        ARKit = False
        if('requirement' in effects and effects['requirement'] != None):
            req = effects['requirement']
            for key in req:
                if(req[key] == 'true'):
                    requirements.append(key)
        if('Link' in effects):
            link = effects['Link']
            for eff in link:
                if('type' in eff):
                    features.append(eff['type'])
                    if(eff['type'][0:2] == "NS" or eff['type'][0:2] == "ns"):
                        #跳过除中文外的检测
                        JsonData.clear()
                        globalError = 0
                        return ("1.0.0",[],False,[])
                if('path' in eff):
                    config_path.append(eff['path'])
        if('bgms' in effects):
            bgms = effects['bgms']
            for bgm in bgms:
                if(isinstance(bgm,dict)):
                    if('music_path' in bgm):
                        config_path.append(bgm['music_path'])
        
        
        if('FaceDistortion' in features):
            ErrorThing = ErrorThing + "error： FaceDistortion Feature has been Forbid, please delete in your config.json\n"
            ErrorEnglishThing = ErrorEnglishThing + "error： FaceDistortion Feature has been Forbid, please delete in your config.json\n"
            tempData = {}
            tempData['code'] = 1
            tempData['type'] = 'FEATURE_FORBID'
            tempData['file'] = dir_name
            tempData['line'] = '-1'
            tempData['msg'] = ' FaceDistortion Feature has been Forbid'
            JsonData.append(tempData)
            globalError = 1
    
        if('ARKit' in features):
            ARKit = True
        
        config_file = []
        for path in config_path:
            tempString = path
            tempString = tempString.split('/', 1)
            tempString = tempString[0].split('\\', 1)
            if (tempString not in config_file):
                config_file.append(tempString[0])
            
        if("InfoSticker" in features):
            version = '1.0.0'
    
    return version,config_file,ARKit,requirements
        





def analyze(stringList, file_name, numList):
    i = 0
    global ErrorThing
    global ErrorEnglishThing
    global WarningThing
    global JsonData
    global globalError
    global globalWarning
    while (i < len(stringList)):
        temp_str = stringList[i]
        if (temp_str == 'getFeature' or temp_str == 'addFeature'):
            j = i - 1
            while (stringList[j] != '='):
                j -= 1
            feature = stringList[j - 1]
            i += 1
            if ((stringList[i + 5] in listCast) or (stringList[i + 6] in listCast)):
                i += 5
            while (stringList[i] != feature and stringList[i] != '}' and i < len(stringList) - 1  ):
                i += 1
            if(i >= len(stringList) - 1):
                continue
            if (stringList[i + 1] == ':'):
                # print("文件%s: error feature %s 没有判空, 行数%d" % (file_name, feature, numList[i + 1]))
                ErrorThing = ErrorThing + ''
                ErrorThing = ErrorThing + "文件:"+file_name+"error feature " +  feature + "没有判空,请将问题反馈给资源生产同学修复 对应lua文件行数" + str(numList[i+1]) + "\n"
                ErrorEnglishThing =  ErrorEnglishThing + "file: " + file_name + " error feature : " + feature + " doesn't check empty variable, please ask the developer to fix" + "Error line number in Lua: " + str(numList[i+1]) + "\n"
                tempData = {}
                tempData['code'] = 1
                tempData['type'] = 'FEATURE_NOT_NIL'
                tempData['file'] = file_name
                tempData['line'] = numList[i+1]
                tempData['msg'] = feature + "没有判空,请将问题反馈给资源生产同学修复"
                JsonData.append(tempData)
                globalError = 1
                i += 1
                continue
            if (stringList[i - 1] == 'if'):
                tempj = i - 1
                tempString = ''
                while (stringList[tempj] != 'then'):
                    tempString += stringList[tempj]
                    tempj += 1
                string1 = 'if' + feature
                string2 = 'if' + feature + '==' + 'nil'
                string3 = 'if' + feature + '~=' + 'nil'
                if (tempString != string1 and tempString != string2 and tempString != string3):
                    # print("文件%s: warning1 feature : %s" % (file_name, tempString))
                    WarningThing = WarningThing+  '文件' + file_name + 'warning1 feature :' + tempString+'\n'
            elif (stringList[i - 2] == 'if'):
                tempj = i - 2
                tempString = ''
                while (stringList[tempj] != 'then'):
                    # print(stringList[tempj])
                    tempString += stringList[tempj]
                    tempj += 1
                string1 = 'if' + '(' + feature + ')'
                string2 = 'if' + 'not' + feature
                string3 = 'if' + '(' + feature + '~=' + 'nil' + ')'
                string4 = 'if' + '(' + feature + '==' + 'nil' + ')'
                if (tempString != string1 and tempString != string2 and tempString != string3 and tempString != string4):
                    # print("文件%s: feature warning2: %s" % (file_name, tempString))
                    WarningThing = WarningThing + '文件' + file_name + 'warning2 feature :' + tempString + '\n'
            elif (stringList[i - 3] == 'if'):
                tempj = i - 3
                tempString = ''
                while (stringList[tempj] != 'then'):
                    tempString += stringList[tempj]
                    tempj += 1
                string1 = 'if' + '(' + 'not' + feature + ')'
                if (tempString != string1):
                    # print("文件%s: feature warning3: %s" % (file_name, tempString))
                    WarningThing = WarningThing + '文件' + file_name + 'warning3 feature :' + tempString + '\n'
            elif (stringList[i - 2] in listCast):  # 经过cast
                j = i - 1
                while (stringList[j] != '='):
                    j -= 1
                feature1 = stringList[j - 1]
                while (stringList[i] != feature):
                    i += 1
                i += 1
                while (stringList[i] != feature1 and stringList[i] != feature and stringList[i] != '}'):
                    i += 1
                if(stringList[i] == '}' or i >= len(stringList)-1):
                    continue

                if (stringList[i + 1] == ':'):
                    i += 1
                    # print("文件%s: error feature %s 没有判空，行数%d" % (file_name, feature1, numList[i + 1]))
                    ErrorThing = ErrorThing + "文件%s: error feature %s 没有判空，请将问题反馈给资源生产同学修复 lua文件行数%d\n" % (file_name, feature1, numList[i + 1])
                    ErrorEnglishThing =  ErrorEnglishThing + "file: " + file_name + " error feature : " + feature1 + " doesn't check empty variable, please ask the developer to fix" + "Error line number in Lua: " + str(numList[i+1]) + "\n"

                    tempData = {}
                    tempData['code'] = 1
                    tempData['type'] = 'FEATURE_NOT_NIL'
                    tempData['file'] = file_name
                    tempData['line'] = numList[i + 1]
                    tempData['msg'] = feature1 + "没有判空，请将问题反馈给资源生产同学修复"
                    JsonData.append(tempData)
                    globalError = 1
                    continue
                if (stringList[i - 1] == 'if'):
                    tempj = i - 1
                    tempString = ''
                    while (stringList[tempj] != 'then'):
                        tempString += stringList[tempj]
                        tempj += 1
                    string1 = 'if' + feature1
                    string2 = 'if' + feature1 + '==' + 'nil'
                    string3 = 'if' + feature1 + '~=' + 'nil'
                    if (tempString != string1 and tempString != string2 and tempString != string3):
                        # print("文件%s: feature warning1: %s" % (file_name, tempString))
                        WarningThing = WarningThing + "文件%s: feature warning1: %s\n" % (file_name, tempString)
                elif (stringList[i - 2] == 'if'):
                    tempj = i - 2
                    tempString = ''
                    while (stringList[tempj] != 'then'):
                        tempString += stringList[tempj]
                        tempj += 1
                    string1 = 'if' + '(' + feature1 + ')'
                    string2 = 'if' + 'not' + feature1
                    string3 = 'if' + '(' + feature1 + '~=' + 'nil' + ')'
                    string4 = 'if' + '(' + feature1 + '==' + 'nil' + ')'
                    if (tempString != string1 and tempString != string2):
                        # print("文件%s: feature warning2: %s" % (file_name, tempString))
                        WarningThing = WarningThing + "文件%s: feature warning2: %s" % (file_name, tempString)
                elif (stringList[i - 3] == 'if'):
                    tempj = i - 3
                    tempString = ''
                    while (stringList[tempj] != 'then'):
                        tempString += stringList[tempj]
                        tempj += 1
                    string1 = 'if' + '(' + 'not' + feature1 + ')'
                    if (tempString != string1):
                        # print("文件%s: feature warning3: %s" % (file_name, tempString))
                        WarningThing = WarningThing + "文件%s: feature warning3: %s" % (file_name, tempString)
                else:
                    tempj = i - 7
                    while (stringList[tempj] != 'if' and tempj < i):
                        tempj += 1
                    if (tempj == i):
                        # print("文件%s: feature error3:不符合格式需要查看一下 %s,行数:%d" % (file_name, feature, numList[i]))
                        ErrorThing = ErrorThing + "文件%s: feature:%s error3:不符合格式需要查看一下,行数:%d\n" % (file_name, feature, numList[i]) + '\n'
                        ErrorEnglishThing = ErrorEnglishThing + "file: %s feature: %s Unknown format errors, please check. Error line in Lua: %d\n" %(file_name, feature, numList[i])

                        tempData = {}
                        tempData['code'] = 2
                        tempData['type'] = 'FEATURE_NOT_KNOW'
                        tempData['file'] = file_name
                        tempData['line'] = numList[i + 1]
                        tempData['msg'] = feature + "不符合格式，需要查看一下"
                        # globalWarning = 1
                        # JsonData.append(tempData)
                    else:
                        tempString = ''
                        while (stringList[tempj] != 'then'):
                            tempString += stringList[tempj]
                            tempj += 1
                        # print("%s: feature warning3: %s" % (file_name, tempString))
                        WarningThing = WarningThing + "%s: feature warning3: %s" % (file_name, tempString)
            else:
                tempj = i - 10
                while (stringList[tempj] != 'if' and tempj < i):
                    tempj += 1
                if (tempj == i):
                    # print("文件%s: feature error4:不符合格式需要查看一下 %s,行数%d" % (file_name, feature, numList[i + 1]))
                    ErrorThing = ErrorThing + "文件%s: feature error4:不符合格式需要查看一下 %s,行数%d\n" % (file_name, feature, numList[i + 1]) 
                    ErrorEnglishThing = ErrorEnglishThing + "error4: file:%s feature:%s unknown format errors,please check,Error line number in Lua:%s +\n"%(file_name,feature,numList[i + 1])
                    tempData = {}
                    tempData['code'] = 2
                    tempData['type'] = 'FEATURE_NOT_KNOW'
                    tempData['file'] = file_name
                    tempData['line'] = numList[i + 1]
                    tempData['msg'] = feature + "不符合格式，需要查看一下"
                    # JsonData.append(tempData)
                    # globalWarning = 1
                else:
                    tempString = ''
                    while (stringList[tempj] != 'then'):
                        tempString += stringList[tempj]
                        tempj += 1
                    # print("%s: feature warning4: %s" % (file_name, tempString))
                    WarningThing = WarningThing + "%s: feature warning4: %s\n" % (file_name, tempString)

       
        elif (temp_str == 'getAudioManager'):
            j = i - 1
            while (stringList[j] != '='):
                j = j - 1
            audioManager = stringList[j - 1]
            i = i + 1
            while (stringList[i] != audioManager  and stringList[i] != '}' and i < len(stringList)-1 ):
                i = i + 1
            if(i == len(stringList)-1):
                ErrorThing = ErrorThing + "文件%s error: audioManager %s 没有判空，请将问题反馈给资源生产同学修复 lua文件行数%d\n" % (file_name, audioManager, numList[j - 1]) 
                ErrorEnglishThing = ErrorEnglishThing + "error: File:%s audioManager %s doesn't check empty variable, please ask the developer to fix Error line number in Lua:%d"%(file_name,audioManager, numList[j - 1])
                tempData = {}
                tempData['code'] = 2
                tempData['type'] = 'AUDIO_MANAGER_NOT_USE'
                tempData['file'] = file_name
                tempData['line'] = numList[j - 1]
                tempData['msg'] = audioManager + "getAudioManger 不要连用"
                # globalError = 1
                # JsonData.append(tempData)
                continue
            if (stringList[i + 1] == ':'):
                i += 1
                # print("文件%serror: audioManager %s 没有判空 行数%d" % (file_name, audioManager, numList[i + 1]))
                ErrorThing = ErrorThing + "文件%s error: audioManager %s 没有判空，请将问题反馈给资源生产同学修复 lua文件行数%d\n" % (file_name, audioManager, numList[i + 1])
                ErrorEnglishThing = ErrorEnglishThing + "error: File:%s audioManager %s doesn't check empty variable, please ask the developer to fix Error line number in Lua:%d"%(file_name,audioManager, numList[j - 1])
                tempData = {}
                tempData['code'] = 1
                tempData['type'] = 'FEATURE_NOT_NIL'
                tempData['file'] = file_name
                tempData['line'] = numList[i + 1]
                tempData['msg'] = audioManager + "audioManger 没有判空，请将问题反馈给资源生产同学修复"
                globalError = 1
                JsonData.append(tempData)
                continue
            if (stringList[i - 1] == 'if'):
                tempj = i - 1
                tempString = ''
                while (stringList[tempj] != 'then'):
                    tempString += stringList[tempj]
                    tempj += 1
                string1 = 'if' + audioManager
                string2 = 'if' + audioManager + '==' + 'nil'
                string3 = 'if' + audioManager + '~=' + 'nil'
                if (tempString != string1 and tempString != string2 and tempString != string3):
                    # print("文件%s: audioManager warning1: %s" % (file_name, tempString))
                    WarningThing = WarningThing + "文件%s: audioManager warning1: %s" % (file_name, tempString)
            elif (stringList[i - 2] == 'if'):
                tempj = i - 2
                tempString = ''
                while (stringList[tempj] != "then"):
                    tempString += stringList[tempj]
                    tempj += 1
                string1 = 'if' + '(' + audioManager + ')'
                string2 = 'if' + '(' + audioManager + '==' + 'nil' + ')'
                string3 = 'if' + '(' + audioManager + '~=' + 'nil' + ')'
                string4 = 'if' + 'not' + audioManager
                if (
                        tempString != string1 and tempString != string2 and tempString != string3 and tempString != string4):
                    # print("文件%s: audioManager warning2: %s" % (file_name, tempString))
                    WarningThing = WarningThing + "文件%s: audioManager warning2: %s\n" % (file_name, tempString)
            elif (stringList[i - 3] == 'if'):
                tempj = i - 3
                tempString = ''
                while (stringList[tempj] != 'then'):
                    tempString += stringList[tempj]
                    tempj += 1
                string1 = 'if' + '(' + 'not' + audioManager + ')'
                if (tempString != string1):
                    # print("文件%s: audioManager warning3: %s" % (file_name, tempString))
                    WarningThing = WarningThing + "文件%s: audioManager warning3: %s\n" % (file_name, tempString)
            else:
                tempj = i - 5
                while (stringList[tempj] != 'if' and tempj < i):
                    tempj += 1
                if (tempj == i):
                    # print("文件%s: audioManager error4: 不符合格式需要查看一下 %s, 行数%d" % (file_name, audioManager, numList[i]))
                    ErrorThing = ErrorThing + "文件%s: audioManager error4: 不符合格式需要查看一下 %s, 行数%d\n" % (file_name, audioManager, numList[i])
                    ErrorEnglishThing = ErrorEnglishThing + "error4: file:%s audioManager:%s unknown format errors,please check,Error line number in Lua:%s +\n"%(file_name,audioManager,numList[i])

                    tempData = {}
                    tempData['code'] = 2
                    tempData['type'] = 'FEATURE_NOT_KNOW'
                    tempData['file'] = file_name
                    tempData['line'] = numList[i]
                    tempData['msg'] = audioManager + "不符合格式，需要查看一下"
                    # globalWarning = 1
                    # JsonData.append(tempData)
                else:
                    tempString = ''
                    while (stringList[tempj] != 'then'):
                        tempString += stringList[tempj]
                        tempj += 1
                    # print("文件%s: audioManager warning3: %s" % (file_name, tempString))
                    WarningThing = WarningThing + "文件%s: audioManager warning3: %s" % (file_name, tempString)

        elif(temp_str == 'getRenderCacheTexture'):  
            j = i - 1
            while (stringList[j] != '='):
                j = j - 1
            audioManager = stringList[j - 1]
            i = i + 1
            while (stringList[i] != audioManager  and stringList[i] != '}' and i < len(stringList)-1 ):
                i = i + 1
            if(i == len(stringList)-1):
                ErrorThing = ErrorThing + "文件%s error: getRenderCacheTexture %s 没有判空，请将问题反馈给资源生产同学修复 lua文件行数%d\n" % (file_name, audioManager, numList[j - 1]) 
                ErrorEnglishThing = ErrorEnglishThing + "error: File:%s getRenderCacheTexture %s doesn't check empty variable, please ask the developer to fix Error line number in Lua:%d"%(file_name,audioManager, numList[j - 1])
                tempData = {}
                tempData['code'] = 2
                tempData['type'] = 'GET_RENDER_CACHE_TEXTURE_NOT use'
                tempData['file'] = file_name
                tempData['line'] = numList[j - 1]
                tempData['msg'] = audioManager + "getRenderCacheTexture 不要连用"
                globalError = 1
                JsonData.append(tempData)
                continue
            if (stringList[i + 1] == ':'):
                i += 1
                # print("文件%serror: audioManager %s 没有判空 行数%d" % (file_name, audioManager, numList[i + 1]))
                ErrorThing = ErrorThing + "文件%s error: getRenderCacheTexture %s 没有判空，请将问题反馈给资源生产同学修复 lua文件行数%d\n" % (file_name, audioManager, numList[i + 1])
                ErrorEnglishThing = ErrorEnglishThing + "error: File:%s getRenderCacheTexture %s doesn't check empty variable, please ask the developer to fix Error line number in Lua:%d"%(file_name,audioManager, numList[j - 1])
                tempData = {}
                tempData['code'] = 1
                tempData['type'] = 'FEATURE_NOT_NIL'
                tempData['file'] = file_name
                tempData['line'] = numList[i + 1]
                tempData['msg'] = audioManager + "getRenderCacheTexture 没有判空，请将问题反馈给资源生产同学修复"
                globalError = 1
                JsonData.append(tempData)
                continue
            if (stringList[i - 1] == 'if'):
                tempj = i - 1
                tempString = ''
                while (stringList[tempj] != 'then'):
                    tempString += stringList[tempj]
                    tempj += 1
                string1 = 'if' + audioManager
                string2 = 'if' + audioManager + '==' + 'nil'
                string3 = 'if' + audioManager + '~=' + 'nil'
                if (tempString != string1 and tempString != string2 and tempString != string3):
                    # print("文件%s: audioManager warning1: %s" % (file_name, tempString))
                    WarningThing = WarningThing + "文件%s: getRenderCacheTexture warning1: %s" % (file_name, tempString)
            elif (stringList[i - 2] == 'if'):
                tempj = i - 2
                tempString = ''
                while (stringList[tempj] != "then"):
                    tempString += stringList[tempj]
                    tempj += 1
                string1 = 'if' + '(' + audioManager + ')'
                string2 = 'if' + '(' + audioManager + '==' + 'nil' + ')'
                string3 = 'if' + '(' + audioManager + '~=' + 'nil' + ')'
                string4 = 'if' + 'not' + audioManager
                if (
                        tempString != string1 and tempString != string2 and tempString != string3 and tempString != string4):
                    # print("文件%s: audioManager warning2: %s" % (file_name, tempString))
                    WarningThing = WarningThing + "文件%s: getRenderCacheTexture warning2: %s\n" % (file_name, tempString)
            elif (stringList[i - 3] == 'if'):
                tempj = i - 3
                tempString = ''
                while (stringList[tempj] != 'then'):
                    tempString += stringList[tempj]
                    tempj += 1
                string1 = 'if' + '(' + 'not' + audioManager + ')'
                if (tempString != string1):
                    # print("文件%s: audioManager warning3: %s" % (file_name, tempString))
                    WarningThing = WarningThing + "文件%s: audioManager warning3: %s\n" % (file_name, tempString)
            else:
                tempj = i - 5
                while (stringList[tempj] != 'if' and tempj < i):
                    tempj += 1
                if (tempj == i):
                    # print("文件%s: audioManager error4: 不符合格式需要查看一下 %s, 行数%d" % (file_name, audioManager, numList[i]))
                    ErrorThing = ErrorThing + "文件%s: getRenderCacheTexture error4: 不符合格式需要查看一下 %s, 行数%d\n" % (file_name, audioManager, numList[i])
                    ErrorEnglishThing = ErrorEnglishThing + "error4: file:%s getRenderCacheTexture:%s unknown format errors,please check,Error line number in Lua:%s +\n"%(file_name,audioManager,numList[i])

                    tempData = {}
                    tempData['code'] = 2
                    tempData['type'] = 'FEATURE_NOT_KNOW'
                    tempData['file'] = file_name
                    tempData['line'] = numList[i]
                    tempData['msg'] = audioManager + "不符合格式，需要查看一下"
                    # globalWarning = 1
                    # JsonData.append(tempData)
                else:
                    tempString = ''
                    while (stringList[tempj] != 'then'):
                        tempString += stringList[tempj]
                        tempj += 1
                    # print("文件%s: audioManager warning3: %s" % (file_name, tempString))
                    WarningThing = WarningThing + "文件%s: getRenderCacheTexture warning3: %s" % (file_name, tempString)
  

        i += 1


def analyzeFunction(stringList, file_name, numList):
    global ErrorThing
    global ErrorEnglishThing
    global WarningThing
    global name2ClassDic
    global JsonData
    global globalError
    global globalWarning
    global IEThing 
    i = -1
    version = '4.0.0'
    function = ''
    line = 0
    myClassManager = parseFunction()
    functionDic = {}
    paramsDic = {}
    if(len(stringList) == 0):
        return (version, function, line)
    #先存储eventHandles 的数据
    # while(i < len(stringList)):
    #     i  += 1
    #     if (stringList[i] == 'MattingEffect'):
    #         i += 1
    #         if (version < '6.0.0'):
    #             version = '6.0.0'
    #         continue
    #     if (stringList[i] == 'EventHandles'):
    #         print('lalala eventHandles')
    #         handleFlag = True
    #         i += 1
    #         break
    #     #增加 name 判断函数参数类型
    #     if(stringList[i] == 'function'):
    #         i = i + 1
    #         functionCount = 1
    #         functionName = stringList[i]
    #         i = i + 1
    #         if(stringList[i] != '('):
    #             print('function name is error')
    #         paramsDic[functionName] = []
    #         while(functionCount != 0):
    #             i = i + 1
    #             if(stringList[i] == ')'):
    #                 functionCount -= 1
    #             elif(stringList[i] == '(' ):
    #                 functionCount += 1
    #             else:
    #                 if(stringList[i] != ','):
    #                     paramsDic[functionName].append(stringList[i])


    #         functionCount = 1
    #         addList = ['if','for','while']
    #         functionDic[functionName] = []
    #         while(functionCount != 0):
    #             i += 1
    #             functionDic[functionName].append(stringList[i])
    #             if(stringList[i] == 'end'):
    #                 functionCount -= 1
    #             elif(stringList[i] in addList):
    #                 functionCount += 1               
                
         

    #处理Eventhandles        
    while (i < len(stringList)):
        # 判断fcuntion 是eventHandles 里面的fcuntion 还是外面的function
        
        if (stringList[i] == 'MattingEffect'):
            i += 1
            if (version < '6.0.0'):
                version = '6.0.0'
            continue

        if (stringList[i] == ':' and stringList[i + 2] == '('):
            if(stringList[i+1] in coordinateList):
                IEThing = IEThing + ('贴纸是用了坐标的贴纸，确认一下有没有用归一化处理 function = %s, line = %d \n'%(stringList[i+1],numList[i+1]))
                IEThing = IEThing + ('The effect uses coordinates, please check if the position values get normalized, function = %s, line = %d \n'%(stringList[i+1],numList[i+1]))
            
            if (stringList[i + 1] in featureList):
                j = i - 1
                while (stringList[j] != '=' and stringList[j] != '(' and stringList[j] != ')' and j > 0):
                    j -= 1
                if (stringList[j] == '(' or stringList[j] == ')' or j == 0):
                    # print("warning: 文件%s stringList[j] = %s 行数%d 写的不符合规范，需要人工查看一下 " % (file_name, stringList[i + 1], numList[i + 1]))
                    WarningThing = WarningThing + "warning: 文件%s stringList[j] = %s 行数%d 写的不符合规范，需要人工查看一下\n" % (file_name, stringList[i + 1], numList[i + 1])
                    tempData = {}
                    tempData['code'] = 2
                    tempData['type'] = 'FEATURE_NOT_KNOW'
                    tempData['file'] = file_name
                    tempData['line'] = numList[i + 1]
                    tempData['msg'] =  "stringList[j] = %s 写的不符合规范，需要人工查看一下"%(stringList[i+1])
                    # globalWarning = 1
                    i += 1

                    continue
                #增加连续调用函数 临时todo 
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
                
                name2ClassDic[stringList[j - 1]] = myClassManager.getClass(className)
                if (version < featureList[stringList[i + 1]]):
                    version = featureList[stringList[(i + 1)]]
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
                    # print('文件%serror:  BEFEfeect 没有函数 %s 行数%d' % (file_name, stringList[i + 1], numList[i + 1]))
                    # ErrorThing = ErrorThing + "文件%serror:  BEFEfeect 没有函数 %s 行数%d\n" % (file_name, stringList[i + 1], numList[i + 1])
                    tempData = {}
                    tempData['code'] = 2
                    tempData['type'] = 'CLASS_NO_FUNCTION'
                    tempData['file'] = file_name
                    tempData['line'] = numList[i + 1]
                    tempData['msg'] =  "BEFEffect 没有对应函数 %s"%(stringList[i+1])
                    # globalWarning  = 1
                    # JsonData.append(tempData)
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
                        else:
                            # print("文件%s error: 类%s 没有对应函数%s 行数:%d" % (file_name, name2ClassDic[stringList[i - 1]].className, stringList[i + 1], numList[i + 1]))
                            # ErrorThing = ErrorThing + "文件%s error: 类%s 没有对应函数%s 行数:%d" % (
                            # file_name, name2ClassDic[stringList[i - 1]].className, stringList[i + 1], numList[i + 1])
                            tempData = {}
                            tempData['code'] = 2
                            tempData['type'] = 'CLASS_NO_FUNCTION'
                            tempData['file'] = file_name
                            tempData['line'] = numList[i + 1]
                            tempData['msg'] = "类%s 没有对应函数%s" % (name2ClassDic[stringList[i - 1]].className,stringList[i + 1])
                            # globalWarning = 1
                            # JsonData.append(tempData)
                    else:
                        # print("文件%s warning: info %s 没有对应的类  行数%d, 可能超出版本范围 " % (file_name, stringList[i - 1], numList[i - 1]))
                        WarningThing = WarningThing + "文件%s warning: info %s 没有对应的类  行数%d, 可能超出版本范围 " % (
                        file_name, stringList[i - 1], numList[i - 1])
                        tempData['code'] = 2
                        tempData['type'] = 'FUNCTION_NOT_KNOW_CLASS'
                        tempData['file'] = file_name
                        tempData['line'] = numList[i - 1]
                        tempData['msg'] =  "info %s 没有对应的类"%(stringList[i-1])
                        # globalWarning  = 1
                        # JsonData.append(tempData)
                elif(stringList[i-1] in confirmFiled): #某些特殊字段还是当作二阶查询处理
                    tempClass = myClassManager.getClass(confirmFiled[stringList[i-1]])
                    tempFunc = tempClass.getFunc(stringList[i+1])
                    if (tempFunc != None):
                        if (version < tempFunc.version):
                            version = tempFunc.version
                            function = stringList[i + 1]
                            line = numList[i + 1]
                    else:
                        # print("文件%s error: 类%s 没有对应函数%s 行数:%d" % (file_name, tempClass, stringList[i + 1], numList[i + 1]))
                        # ErrorThing = ErrorThing + "文件%s error: 类%s 没有对应函数%s 行数:%d" % (
                        # file_name, tempClass, stringList[i + 1], numList[i + 1])
                        tempData = {}
                        tempData['code'] = 2
                        tempData['type'] = 'CLASS_NO_FUNCTION'
                        tempData['file'] = file_name
                        tempData['line'] = numList[i + 1]
                        tempData['msg'] = "类%s 没有对应函数%s" % (tempClass,stringList[i + 1])
                        # globalWarning = 1
                        # JsonData.append(tempData)
                else:
                    # 当作一阶函数处理
                    tempVersion = myClassManager.getFuncVersion(stringList[i + 1])
                    if (tempVersion != None):
                        if (version < tempVersion):
                            version = tempVersion
                            function = stringList[i + 1]
                            line = numList[i + 1]
                        # print("文件%swarning: 在一阶列表查询函数，是以函数最高版本号查询，同名函数可能会有问题，关键字 %s %s, 行数：%d" % (file_name, stringList[i - 1], stringList[i + 1], numList[i + 1]))
                        WarningThing = WarningThing + "文件%swarning: 在一阶列表查询函数，是以函数最高版本号查询，同名函数可能会有问题，关键字 %s %s, 行数：%d" % (
                        file_name, stringList[i - 1], stringList[i + 1], numList[i + 1])
                        tempData = {}
                        tempData['code'] = 2
                        tempData['type'] = 'FIRST_FUNCTION'
                        tempData['file'] = file_name
                        tempData['line'] = numList[i + 1]
                        tempData['msg'] =  " %s 在一阶段函数列表查询"%(stringList[i+1])
                        # globalWarning  = 1
                        # JsonData.append(tempData)
                    else:
                        # 说明函数是lua自定义的函数或者是数学库函数
                        # print("文件%swarning: function  versionlist 列表没有这个函数,可能是数学库函数或者自己定义的函数 关键字%s %s" % (file_name, stringList[i - 1], stringList[i + 1]))
                        WarningThing = WarningThing + "文件%swarning: function  versionlist 列表没有这个函数,可能是数学库函数或者自己定义的函数 关键字%s %s" % (
                        file_name, stringList[i - 1], stringList[i + 1])
                        WarningThing = WarningThing + "文件%swarning: 在一阶列表查询函数，是以函数最高版本号查询，同名函数可能会有问题，关键字 %s %s, 行数：%d" % (
                        file_name, stringList[i - 1], stringList[i + 1], numList[i + 1])
                        tempData = {}
                        tempData['code'] = 2
                        tempData['type'] = 'NOT_FOUND'
                        tempData['file'] = file_name
                        tempData['line'] = numList[i + 1]
                        tempData['msg'] =  " %s 在数据库里没有查询到"%(stringList[i+1])
                        # globalWarning  = 1
                        # JsonData.append(tempData)
        elif (stringList[i] in listCast):
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
        elif (stringList[i] in handleFuncList):  # 对handleFunction 处理
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

            if (version < handleFuncList[stringList[i]]):
                version = handleFuncList[stringList[i]]
                function = stringList[i]
                line = numList[i]

        i += 1
    return (version, function, line)




def parserLuaFile(luaFile, dir_name):
    global ErrorThing
    with open(luaFile, 'rb') as f:
        file_string = f.read()
        file_string = decrypt(file_string)
        stringList = []
        numList = {} 
        try:
            (stringList, numList) = participle(file_string, dir_name)
        except:
            ErrorThing = ErrorThing + "file:%s configFile particple Error"%(dir_name)
        analyze(stringList, dir_name,numList)
        # funcs = getFunction(stringList,dir_name)

        (version, function, line)= analyzeFunction(stringList,dir_name,numList)
        return (version , function, line)
        

def check_contain_chinese(check_str):
    for ch in check_str.encode().decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True,ch
    return False,''

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

def parseDstDir(dstDir, dir_name):
    global name2ClassDic
    global JsonData
    global globalError
    global globalWarning
    global ErrorThing
    global ErrorEnglishThing
    global IEThing
    global globalChinese

    file_list = os.listdir(dstDir)
    file_list.sort()

    #找到所有路径
    dir_list = os.walk(dstDir)
    all_files = []
    all_dirs = []
    for root, dirs, files in dir_list:
        for name in files:
            all_files.append(os.path.join(root,name))
        for name in dirs:
            all_dirs.append(os.path.join(root,name))


     #检测.vscode 文件夹
    for di in all_dirs:
        temp_di = di.split('/')
        if('.vscode' in temp_di):
            ErrorThing = ErrorThing + ('error: There is a hidden .vscode folder in the effect. If you confirm that the file is useless, please open the effect in the vscode tool and delete\n')
            tempData = {}
            tempData['code'] = 1
            tempData['type'] = 'VSCODE'
            tempData['file'] = dstDir
            tempData['line'] = 0
            tempData['msg'] = 'There is a hidden .vscode folder in the effect. If you confirm that the file is useless, please open the effect in the vscode tool and delete'
            globalError = 1
            JsonData.append(tempData)
            break
    for di in all_dirs:
        temp_di = di.split('/')
        if('__MACOSX' not in temp_di and temp_di[-1] != '.DS_Store'):
            dir_path = di[len(dstDir)+1:]
            check,ch = check_contain_chinese(dir_path)
            if(check):
                chk_chi = True
                #重命名
                # os.rename(di,di[0:len(dstDir)+1]+dir_str) 
                ErrorThing = ErrorThing + ('error: file:%s has chinese in %s text is:%s\n'%(dstDir,di,ch))
                ErrorEnglishThing = ErrorEnglishThing + ('error: file:%s has chinese in %s text is:%s\n'%(dstDir,di,ch))
                tempData = {}
                tempData['code'] = 4
                tempData['type'] = 'HAS_CHINESE'
                tempData['file'] = dir_name
                tempData['line'] = 0
                tempData['msg'] = 'error: file:%s has chinese in %s text is:%s\n'%(dstDir,di,ch)
                globalError = 1
                globalChinese = 1
                JsonData.append(tempData)
    
    # 解析文字贴纸有没有送审
    lua_textset = True
    for fi in all_files:
        temp_fi = fi.split('/')
        if('__MACOSX' not in temp_fi and temp_fi[-1][-4:] == '.lua'):
            with open(fi,'r') as lua_file:
                lua_string = lua_file.read()
                if(lua_string.find('handleKeyboardInput') > 0): #说明是新引擎文字贴纸
                    # print('lsh: find:',lua_string.find('getTextContent'),lua_string.find('Amaz.StringVector'))
                    if(lua_string.find('getTextContent') > 0 and lua_string.find('Amaz.StringVector') > 0):
                        lua_textset = True
                    else:
                        lua_textset = False
                    break
                elif(lua_string.find('handleInputText') > 0): #说明是旧引擎文字贴纸
                    # print('lsh: find old:',lua_string.find('getLuaTextContent'))
                    if(lua_string.find('getLuaTextContent') > 0 ):
                        lua_textset = True
                    else:
                        lua_textset = False
                    break

                       
    if(lua_textset == False):
        ErrorThing = ErrorThing + ('error: file:%s text2DV2 not use getLuaTextContent,please use\n'%(dstDir))
        ErrorEnglishThing = ErrorEnglishThing + ('error: file:%s text2DV2 not use getLuaTextContent,please use\n'%(dstDir))
        tempData = {}
        tempData['code'] = 1
        tempData['type'] = 'TEXT_2DV2'
        tempData['file'] = dir_name
        tempData['line'] = 0
        tempData['msg'] = 'error: file:%s text2DV2 not use getLuaTextContent,please use\n'%(dstDir)
        globalError = 1
        JsonData.append(tempData)

    for fi in all_files:
        temp_fi = fi.split('/')
        if('__MACOSX' not in temp_fi and temp_fi[-1] != '.DS_Store' ):
            fi_path = fi[len(dstDir)+1:]
            check,ch = check_contain_chinese(fi_path)
            if(check):
                ErrorThing = ErrorThing + ('error: file:%s has chinese in %s text is:%s\n'%(dstDir,fi,ch))
                ErrorEnglishThing = ErrorEnglishThing + ('error: file:%s has chinese in %s text is:%s\n'%(dstDir,fi,ch))
                tempData = {}
                tempData['code'] = 1
                tempData['type'] = 'HAS_CHINESE'
                tempData['file'] = dir_name
                tempData['line'] = 0
                tempData['msg'] = 'error: file:%s has chinese in %s text is:%s\n'%(dstDir,fi,ch)
                globalError = 1
                globalChinese = 1
                JsonData.append(tempData)
            if(filetype(fi)== True):
                if(os.path.isfile(fi)):
                    with open(fi,'rb') as f:
                        try:
                            file_str = f.read()
                            file_str = decrypt(file_str)
                            check,ch = check_contain_chinese(file_str)
                            if(check):
                                tempData = {}
                                tempData['code'] = 1
                                tempData['type'] = 'HAS_CHINESE'
                                tempData['file'] = dir_name
                                tempData['line'] = 0
                                tempData['msg'] = 'error: file:%s has chinese in %s text:%s\n'%(dstDir,fi,ch)
                                globalError = 1
                                globalChinese = 1
                                JsonData.append(tempData)
                                ErrorThing = ErrorThing + ('error: file:%s has chinese in %s text:%s\n'%(dstDir,fi,ch))
                                ErrorEnglishThing = ErrorEnglishThing + 'error: file:%s has chinese in %s text:%s\n'%(dstDir,fi,ch)
                        except UnicodeDecodeError:
                            print('')


    version = ""
    versionLua = "0.0.0"
    function = '0.0.0'
    line = -1
    config_file = []
    requirement = []
    not_detect_zip = ['infoSticker.lua','template.json','fontPath.json'] #如果资源包有这些文件就过滤掉， 目前有背景贴纸和歌词贴纸,直播贴纸

    if('config.json' in file_list):
        config_path = dstDir + '/' + 'config.json'
        version,config_file,ARKit,requirement = parseConfigFile(config_path,dir_name)
        if(ARKit and 'extra.json' in file_list):
            extra_path = dstDir + '/' + 'extra.json'
            with open(extra_path, 'r') as f:
                json_string = json.loads(f.read())
                if('worldTracking' in json_string):
                    if(version < '6.8.0'):
                        ErrorThing = ErrorThing + "error：文件%s 版本号错误: config.json版本号是%s, ARKit+worldTracking  版本号应该改为 6.8.0 "%(dir_name,version) + '\n'
                        ErrorEnglishThing = ErrorEnglishThing + "error file:%s Wrong config version number. Config.json version number is %s, ARKit+worldTracking Please change the version number to 6.8.0."%(dir_name,version) + '\n'
                        tempData = {}
                        tempData['code'] = 1
                        tempData['type'] = 'VERSION_ERROR'
                        tempData['file'] = dir_name
                        tempData['line'] = line
                        tempData['msg'] = "config 版本号错误 config.json版本号是 %s, ARKit+worldTracking   ,版本号应该改成6.8.0"%(version)
                        globalError = 1
                        JsonData.append(tempData)
    
    if('data.json' in file_list and 'user_data.json' in file_list):
        if(version < '6.3.0'):
            ErrorThing = ErrorThing + "error：文件%s 版本号错误: config.json版本号是%s, AERender  版本号应该改为 6.3.0 "%(dir_name,version) + '\n'
            ErrorEnglishThing = ErrorEnglishThing + "error file:%s Wrong config version number. Config.json version number is %s, AERender Please change the version number to 6.3.0."%(dir_name,version) + '\n'
            tempData = {}
            tempData['code'] = 1
            tempData['type'] = 'VERSION_ERROR'
            tempData['file'] = dir_name
            tempData['line'] = line
            tempData['msg'] = "config 版本号错误 config.json版本号是 %s, AERender   ,版本号应该改成6.3.0"%(version)
            globalError = 1
            JsonData.append(tempData)


    

     
        
        if('__MACOSX' not in temp_fi and temp_fi[-1] == 'content.json'):
            with open(fi,'r') as f:
                json_string = json.loads(f.read())
                if('requirement' in json_string):
                    req = json_string['requirement']

                    for key in req:
                        if((req[key] == True  or req[key] == 'true') and key not in requirement):
                            requirement.append(key)
                            

    if('3dFaceMeshPerspective' in requirement or '3dFaceMesh' in requirement):
        if(version < '6.4.1'):
            ErrorThing = ErrorThing + "error：文件%s 版本号错误: config.json版本号是%s, 3dFaceMeshPerspective,3dFaceMesh  版本号应该改为 6.5.0 "%(dir_name,version) + '\n'
            ErrorEnglishThing = ErrorEnglishThing + "error file:%s Wrong config version number. Config.json version number is %s, 3dFaceMeshPerspective,3dFaceMesh Please change the version number to 6.5.0."%(dir_name,version) + '\n'
            tempData = {}
            tempData['code'] = 1
            tempData['type'] = 'VERSION_ERROR'
            tempData['file'] = dir_name
            tempData['line'] = line
            tempData['msg'] = "config 版本号错误 config.json版本号是 %s, 3dFaceMeshPerspective   ,版本号应该改成6.8.0"%(version)
            globalError = 1
            JsonData.append(tempData)

    if('event.lua' not in file_list): #没有event.lua 文件直接过
        return
    if('config.json' in file_list):
            fileName = dstDir + '/' + 'config.json'
            # version,config_file,ARKit,requirement = parseConfigFile(fileName,dir_name)
            if(version == '1.0.0' ): #不检测
                tempData = {}
                tempData['code'] = 2
                tempData['type'] = 'VERSION_NOT_CHECK'
                tempData['file'] = dir_name
                tempData['line'] = 0
                tempData['msg'] = "版本号超出，不检测"
                # globalWarning = 1
                # JsonData.append(tempData)
                return
    for i in range(len(file_list)):
        #先检测config.json
        if(file_list[i] == 'event.lua'):
            fileName = dstDir +'/'+ file_list[i]
            (versionLua,function,line) = parserLuaFile(fileName, dir_name)
        # elif(file_list[i] == 'config.json'):
        #     fileName = dstDir + '/' + file_list[i]
        #     version,config_file = parseConfigFile(fileName,dir_name)
        #     version = version[1:len(version)-1]
        #     if(version == '1.0.0'): #不检测
        #         return
    
    if version < versionLua:
        tempData = {}
        tempData['code'] = 1
        tempData['type'] = 'VERSION_ERROR'
        tempData['file'] = dir_name
        tempData['line'] = line
        tempData['msg'] = "config 版本号错误 config.json版本号是 %s,   函数版本 %s 对应版本 %s ,版本号应该改成%s"%(version,function,versionLua, versionLua)
        globalError = 1
        JsonData.append(tempData)
        # print("文件%s error version:%s, function %s %s is error config版本号错误, 行数:%d"%(dir_name,version,function,versionLua,line))
        ErrorThing = ErrorThing + "error：文件%s 版本号错误: config.json版本号是%s, 函数 %s 对应版本 %s ,版本号应该改成%s lua文件行数:%d"%(dir_name,version,function,versionLua,versionLua, line) + '\n'
        ErrorEnglishThing = ErrorEnglishThing + "error file:%s Wrong config version number. Config.json version number is %s, (%s) is (%s) version function. Please change the version number to %s. lua line number is: %d \n "%(dir_name,version,function,versionLua,versionLua,line) + '\n'
    else:
    #     print("文件%s version is ok"%(dir_name))
        ErrorThing = ErrorThing + "文件%s version is ok"%(dir_name) + '\n'
        ErrorEnglishThing = ErrorEnglishThing + "file:%s version is ok  \n "%(dir_name)


    # 比较config_file 和 config_file的区别
    deleteString = ['__MACOSX','event.lua','config.json','trigger.json','resource','extra.json']
    for name in deleteString:
        if(name in file_list):
            file_list.remove(name)
    file_list.sort()
    config_file.sort()
    if(file_list != config_file):
        for config in config_file:
            if(config not in file_list):
                tempData = {}
                tempData['code'] = 2
                tempData['type'] = 'FILE_NOT_EQUEAL'
                tempData['file'] = dir_name
                tempData['line'] = 0
                tempData['msg'] = "config中%s在资源包不存在"%(config)
                # globalWarning = 1
                # JsonData.append(tempData)
                # print("资源包%s error:  config中%s 在资源包不存在，请确认一下"%(dir_name,config))
                IEThing = IEThing + "资源包%s error:  config.json中%s 在资源包不存在，请确认一下，如果是多余的建议删除后再提交"%(dir_name,config) +'\n'
                IEThing = IEThing + "error: file:%s  %s in config.json  is unnecessary Unnecessary files please check it. \n "%(dir_name,config)

        for fileString in file_list:
            if(fileString not in config_file):
                tempData = {}
                tempData['code'] = 2
                tempData['type'] = 'FILE_NOT_EQUEAL'
                tempData['file'] = dir_name
                tempData['line'] = 0
                tempData['msg'] = "资源文件中%s是多余的，多余内容会增加资源包大小，导致资源下载失败率升高，浪费用户流量，建议删除后再提交"%(fileString)
                # globalWarning = 1
                # JsonData.append(tempData)
                # print("资源包%s error:  资源文件中%s 是多余的，请确认一下"%(dir_name,fileString))
                IEThing = IEThing + "资源包%s error:  资源文件中%s 是多余的，请确认一下，如果是多余的建议删除后再提交"%(dir_name,fileString) + '\n'
                IEThing = IEThing + "error: file:%s effect file %s is unnecessary Unnecessary files will increase the size of effect package. It causes higher download failure rate and wastes user's cellular data \n "%(dir_name,fileString)
def parserFileName(stringName):
    return stringName[0:len(stringName)-4]


#解压缩文件
def unzip_file(zip_src, dir, file_name):
    global name2ClassDic
    global JsonData
    global globalError
    global globalWarning
    global globalFilePath
    r = zipfile.is_zipfile(zip_src)
    file_name = parserFileName(file_name)
    os.chdir(dir)
    dst_dir = dir + file_name
    if(os.path.exists(dst_dir)):
        shutil.rmtree(dst_dir)
    os.mkdir(file_name)
    
    if r:
        fz = zipfile.ZipFile(zip_src,'r')
        #参考 https://blog.csdn.net/u010099080/article/details/79829247
        renamePath = {}
        for file in fz.namelist():
            fz.extract(file,dst_dir)
            # file_newname = dst_dir + "/" + file.encode('cp437').decode('utf-8')
            path = os.getcwd()+"/"+file
            check_contain_chinese(path)
        parseDstDir(dst_dir,file_name)
        globalFilePath = dst_dir

    else:
        tempData = {}
        tempData['code'] = 1
        tempData['type'] = 'error'
        tempData['file'] = 'error'
        tempData['line'] = 0
        tempData['msg'] = "不是zip包"
        globalError = 1
        JsonData.append(tempData)
        # print( '%s is not zip' %(zip_src))


## hash tag
count = 0

def genTag(origin, count):

    ss = origin + str(count) + str(int(time.time()))
    m2 = hashlib.md5()
    m2.update(ss.encode('utf-8'))
    token = m2.hexdigest()
    #print(token)
    return token

def setTag(path, filename, count):
    filePath = os.path.join(path, filename)
    if (not os.path.exists(filePath)):
        print("file not find!\n")
        return False
    with open(filePath,"r") as f:
        doc = json.load(f)
        if filename == "config.json" and "effect" in doc.keys():
            if "name" in doc.keys():
                tag = doc["name"]
                doc["name"] = genTag(tag, count)
            else:
                print("Can't find name key in file : "+filePath)
                return False
        elif (filename == "content.json"):
            if "tag" in doc.keys():
                tag = doc["tag"]
                doc["tag"] = genTag(tag, count)
            else:
                print("Can't find name key in file : "+filePath)
                return False
    with open(filePath,"w") as f:  
        json.dump(doc,f)
    f.close()

def deleteOSFile(dir):
    list = os.listdir(dir)
    for i in range(0,len(list)):
        if list[i] == "__MACOSX" :
            path = os.path.join(dir,list[i])
            print("delete folder " + path)
            shutil.rmtree(path)
    



def checkDir(rootdir):
    global count
    list = os.listdir(rootdir)
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isdir(path):
            if checkDir(path) == False:
                return False
        elif '.json' in list[i]:
            count = count + 1
            if setTag(rootdir, list[i], count) == False:
                return False
    return True

__all__ = ["test_data"]

def test_data(path):
    global ErrorThing
    global WarningThing 
    global ErrorEnglishThing 
    global JsonData 
    global globalWarning 
    global globalError
    ErrorThing = ""
    WarningThing = ""
    ErrorEnglishThing = ""
    JsonData = []
    globalWarning = 0
    globalError = 0 
    if(path[-4:] == '.zip'): #说明是zip包
            i = len(path)
            while(i >0):
                if(path[i-1] == '/'):
                    uzip_path = path[0:i]
                    file_index = path[i:]
                    unzip_file(path,uzip_path,file_index)
                    break
                i -= 1
    else:
        print('test error')
            
    info = {}
    if(globalError == 1):
        info['status_code'] = 1
    elif(globalWarning == 1):
        info['status_code'] = 2
    else:
        info['status_code'] = 0
    info['data'] = JsonData

    # if(len(json.dumps(info,ensure_ascii = False)) < 1000):
    #     print(json.dumps(info,ensure_ascii = False))
    # else:
    #     res_json_sub = {}
    #     res_json_sub['status_code'] = info['status_code']
    #     res_json_sub['data'] = []
    #     for js in JsonData:
    #         if(len(res_json_sub)+len(js) < 1000):
    #             res_json_sub['data'].append(js)
    #         else:
    #             break
    #     print(json.dumps(res_json_sub,ensure_ascii = False))
    return info

if __name__ == '__main__':
    if(len(sys.argv) == 2):
        globalError = 0
        globalWarning = 0
        path = sys.argv[1]
        if(path[-4:] == '.zip'): #说明是zip包
            i = len(path)
            while(i >0):
                if(path[i-1] == '/'):
                    uzip_path = path[0:i]
                    file_index = path[i:]
                    unzip_file(path,uzip_path,file_index)
                    break
                i -= 1
        else: #说明是文件夹
            folder_path = path
            file_list = os.listdir(folder_path)
            file_list.sort()
            uzip_path = folder_path+'/../unzip'
            if(not os.path.exists(uzip_path)):
                os.mkdir(uzip_path)

            os.chdir(folder_path)
            if(uzip_path[-1] != '/'):
                uzip_path += '/'
            for index in range(len(file_list)):
                lenString = len(file_list[index])
                stringName = file_list[index][lenString-4:lenString]
                if(stringName != '.zip'):
                    continue
                src_path = folder_path + '/' + file_list[index]
                # print(src_path)
                unzip_file(src_path,uzip_path, file_list[index])

    else:
        ErrorThing = ErrorThing+("输入的参数不对： 请输入： python3 luaAuto.py Path, Path 为zip包路径或者zip包文件夹对应的路径\n")
        ErrorThing = ErrorThing+('Usage: python3 luaAuto.py <zip_file_path> \n')
    info = {}
    if(globalChinese == 1):
        info['status_code'] = 4
    elif(globalError == 1):
        info['status_code'] = 1
    elif(globalWarning == 1):
        info['status_code'] = 2
    else:
        info['status_code'] = 0
    info['data'] = JsonData
    #QA使用+TA
    # print(ErrorThing)
    # print(ErrorEnglishThing)
    # print(IEThing)

    #TA使用
    # if (globalFilePath != ""):
    #     print("######################gen random tag part #########################")
    #     print("hash all tag in " + globalFilePath)
    #     deleteOSFile(globalFilePath)
    #     checkDir(globalFilePath)
    #     print("######################gen random tag part #########################")
    #后台使用
    if(len(json.dumps(info,ensure_ascii = False)) < 1000):
        print(json.dumps(info,ensure_ascii = False))
    else:
        res_json_sub = {}
        res_json_sub['status_code'] = info['status_code']
        res_json_sub['data'] = []
        for js in JsonData:
            if(len(json.dumps(res_json_sub,ensure_ascii = False))+len(js) < 1000):
                res_json_sub['data'].append(js)
            else:
                break
        print(json.dumps(res_json_sub,ensure_ascii = False))
