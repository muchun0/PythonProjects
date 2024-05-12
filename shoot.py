# 一个半小时后关机
import os
import sys
import datetime

if __name__ == '__main__':
    os.system("shutdown -s -t 5400")
    print("系统将在一个半小时后关机")
