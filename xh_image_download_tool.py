# coding:utf-8

import logging
import os
import re

import requests


def download_image_from_url(image_url, image_file_path, image_file_name=""):
    """请求图片URL下载图片，保存为指定的路径下的指定文件名。

    参数：
    image_url：要下载的图片的url
    image_file_path：下载图片存放的路径，如果不存在则自动创建
    image_file_name：下载图片保存的文件名，如果为空则自动从image_url中截取设置

    返回：
    下载到路径image_file_path下的图片文件image_file_name

    异常：
    无
    """
    if not image_url.strip():
        logging.error("参数image_url不能为空！")
        return None
    if not image_file_path.strip():
        logging.error("参数image_file_path不能为空！")
        return None
    if not os.path.exists(image_file_path):
        os.makedirs(image_file_path)
    if not re.search(".+://.+", image_url):
        logging.error("image_url非法，" + "image_url=" + image_url)
        return None
    if not image_file_name.strip():
        image_file_name = filter(lambda ch: ch in '._-' or str.isalnum, image_url.split("/")[-1])
    if os.path.exists(image_file_path + os.sep + image_file_name):
        logging.warn("图片" + image_file_path + os.sep + image_file_name + "已存在，跳过！")
        return None
    request = requests.session()
    response = request.get(image_url, stream=True, verify=False, timeout=120)
    if response.status_code != 200:
        logging.error("返回码为 " + str(response.status_code) + "，image_url=" + image_url)
        return None
    with open(image_file_path + os.sep + image_file_name, "wb") as fd:
        for chunk in response.iter_content(chunk_size=10240):
            fd.write(chunk)


def batch_download_images_from_image_url_file(image_url_file_path, image_url_file_name, root_image_file_path):
    """从指定路径下读取指定源文件获取image_url，遍历得到的image_url去下载图片，保存为指定的路径下的指定文件名。

    参数：
    image_url_file_path：image_url参数文件的路径，也是下载图片文件存放路径的上级路径
    image_url_file_name：存放图片URL的文件名
    root_image_file_path：存放下载的图片文件的上级路径

    返回：
    下载到路径root_image_file_path下的按目录分别存放的图片文件

    异常：
    无
    """
    if not image_url_file_path.strip():
        logging.error("参数image_url_file_path不能为空！")
        return None
    if not image_url_file_name.strip():
        logging.error("参数image_url_file_name不能为空！")
        return None
    image_url_file = image_url_file_path + os.sep + image_url_file_name
    if not os.path.exists(image_url_file):
        logging.error("文件" + image_url_file + "不存在！")
        return None
    param_file = open(image_url_file, "r")
    while True:
        lines = param_file.readlines(100)
        if not lines:
            break
        for line in lines:
            try:
                image_url = line.split("|")[0]
                logging.info("image_url:" + image_url)
                # 从post_url取图片目录名称，根据反斜杠/逆序取，直到有值
                # 目录名称和图片名称中只保留合法的字符
                i = 1
                while True:
                    image_file_directory = filter(str.isalnum, line.split("|")[1].split("/")[-i].strip())
                    if image_file_directory.strip():
                        break
                    else:
                        i += 1
                image_file_path = root_image_file_path + os.sep + image_file_directory
                image_file_name = filter(lambda ch: ch in '._-' or str.isalnum, image_url.split("/")[-1])
                download_image_from_url(image_url, image_file_path, image_file_name)
            except Exception as e:
                logging.exception("发生未知异常，image_url:" + image_url)
    param_file.close()


if __name__ == '__main__':
    pass
