import logging
import sys


def set_logger(log_path):
    """
    将日志输出到日志文件和控制台
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')

    # 创建一个handler，用于from utils import set_logger写入日志文件
    # 增加对logger.info中文乱码的处理
    # python3.9以上才可以设置encoding
    if sys.version_info.major == 3 and sys.version_info.minor >= 9:
        file_handler = logging.FileHandler(filename=log_path, encoding='utf-8')
    else:
        file_handler = logging.FileHandler(filename=log_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # 创建一个handler，用于将日志输出到控制台
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger

