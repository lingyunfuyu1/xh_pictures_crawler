# coding:utf-8

import logging
import os
import re

import requests


def get_target_strings_from_source_url(source_url, target_string_pattern, target_string_file_path="",
                                       target_string_file_name="", target_string_prefix="", encoding="utf-8"):
    if not source_url.strip():
        logging.error("参数source_url不能为空！")
        return None
    if not target_string_pattern.strip():
        logging.error("参数target_string_pattern不能为空！")
        return None
    if not re.search(".+://.+", source_url):
        logging.error("source_url非法，" + "source_url=" + source_url)
        return None
    request = requests.session()
    response = request.get(source_url, timeout=120)
    target_strings_initial = re.findall(target_string_pattern, response.text)
    # 修改查找失败的返回结果
    if not target_strings_initial:
        target_strings_initial.append("NoSuchTargetStringPattern")
    target_strings = []
    for target_string_initial in target_strings_initial:
        if target_string_initial not in target_strings:
            if encoding != "utf-8":
                # 如果页面不是utf-8编码，需要如下特殊处理
                target_string = target_string_prefix + target_string_initial.strip().encode(
                    'raw_unicode_escape').decode(
                    encoding).encode("utf-8") + "|" + source_url
            else:
                target_string = target_string_prefix + target_string_initial.strip() + "|" + source_url
            target_strings.append(target_string)
    if target_string_file_path and target_string_file_name:
        if not os.path.exists(target_string_file_path):
            os.makedirs(target_string_file_path)
        result_file = open(target_string_file_path + os.sep + target_string_file_name, 'a')
        for target_string in target_strings:
            result_file.write(target_string + "\n")
        result_file.close()
    return target_strings


def batch_get_target_strings_from_source_url_file(source_url_file_path, source_url_file_name, target_string_pattern,
                                                  target_string_file_path, target_string_file_name,
                                                  target_string_prefix="", encoding="utf-8"):
    if not source_url_file_path.strip():
        logging.error("参数source_url_file_path不能为空！")
        return None
    if not source_url_file_name.strip():
        logging.error("参数source_url_file_name不能为空！")
        return None
    if not target_string_pattern.strip():
        logging.error("参数target_string_pattern不能为空！")
        return None
    if not target_string_file_path.strip():
        logging.error("参数target_string_file_path不能为空！")
        return None
    if not target_string_file_name.strip():
        logging.error("参数target_string_file_name不能为空！")
        return None
    source_url_file = source_url_file_path + os.sep + source_url_file_name
    if not os.path.exists(source_url_file):
        logging.error("文件" + source_url_file + "不存在！")
        return None
    if not os.path.exists(target_string_file_path):
        os.makedirs(target_string_file_path)
    param_file = open(source_url_file, "r")
    result_file = open(target_string_file_path + os.sep + target_string_file_name, 'a')
    while True:
        lines = param_file.readlines(100)
        if not lines:
            break
        for line in lines:
            try:
                source_url = line.split("|")[0]
                logging.info("source_url:" + source_url)
                target_strings = get_target_strings_from_source_url(source_url, target_string_pattern,
                                                                    target_string_prefix=target_string_prefix,
                                                                    encoding=encoding)
                for target_string in target_strings:
                    result_file.write(target_string + "\n")
                result_file.flush()
            except Exception as e:
                logging.exception("发生未知异常，source_url:" + source_url)
    param_file.close()
    result_file.close()


if __name__ == "__main__":
    pass
