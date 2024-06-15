import logging.config

# 定义日志配置字典
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '我的玩家好凶猛.log',  # 日志文件名
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '我的玩家好凶猛': {  # 你可以根据需要设置多个logger，这里只是一个示例
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}




# 根据book_name创建一个logger实例
def get_logger(book_name):
    # 使用字典配置日志
    logging.config.dictConfig(LOGGING)
    return logging.getLogger(book_name)

# # main.py 或其他需要日志的模块
#
# import logging.config
# import logging_config  # 导入包含日志配置的模块
#
# # 使用字典配置日志
# logging.config.dictConfig(logging_config.LOGGING)
#
# # 创建一个logger实例
# logger = logging.getLogger('my_app')
#
# # 记录一些日志
# logger.debug('这是一条debug级别的日志')
# # ...
