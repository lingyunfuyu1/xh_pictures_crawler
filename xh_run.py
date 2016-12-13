# coding:utf-8

import ConfigParser
import logging
import os
import shutil

import xh_image_download_tool
import xh_string_spider_tool


def get_post_url(category_url, post_url_pattern, post_url_prefix, encoding, post_url_file_path, post_url_file_name,
                 start_post_number, end_post_number):
    logging.info("----------------------------------------------------------------------")
    logging.info("PID-" + str(os.getpid()) + "\tScanning post_url(s). Please waiting...")
    post_urls = xh_string_spider_tool.get_target_strings_from_source_url(category_url, post_url_pattern,
                                                                         target_string_prefix=post_url_prefix,
                                                                         encoding=encoding)
    result_file = open(post_url_file_path + os.sep + post_url_file_name, 'a')
    for post_url in post_urls[int(start_post_number) - 1:int(end_post_number)]:
        result_file.write(post_url + "\n")
    result_file.close()


def get_post_category(post_url_file_path, post_url_file_name, post_category_pattern, post_category_file_path,
                      post_category_file_name, post_category_prefix, encoding):
    logging.info("----------------------------------------------------------------------")
    logging.info("PID-" + str(os.getpid()) + "\tScanning post_category(s). Please waiting...")
    xh_string_spider_tool.batch_get_target_strings_from_source_url_file(post_url_file_path, post_url_file_name,
                                                                        post_category_pattern, post_category_file_path,
                                                                        post_category_file_name,
                                                                        target_string_prefix=post_category_prefix,
                                                                        encoding=encoding)


def get_image_url(post_url_file_path, post_url_file_name, image_url_pattern, image_url_file_path, image_url_file_name,
                  image_url_prefix, encoding):
    logging.info("----------------------------------------------------------------------")
    logging.info("PID-" + str(os.getpid()) + "\tScanning image_url(s). Please waiting...")
    xh_string_spider_tool.batch_get_target_strings_from_source_url_file(post_url_file_path, post_url_file_name,
                                                                        image_url_pattern, image_url_file_path,
                                                                        image_url_file_name,
                                                                        target_string_prefix=image_url_prefix,
                                                                        encoding=encoding)


def download_image_file(image_url_file_path, image_url_file_name, root_image_directory_path):
    logging.info("----------------------------------------------------------------------")
    logging.info("PID-" + str(os.getpid()) + "\tDownloading image(s). Please waiting...")
    xh_image_download_tool.batch_download_images_from_image_url_file(image_url_file_path, image_url_file_name,
                                                                     root_image_directory_path)


def classify(post_category_file_path, post_category_file_name, root_image_directory_path, image_directory_path_prefix):
    logging.info("----------------------------------------------------------------------")
    logging.info("PID-" + str(os.getpid()) + "\tClassifying image(s). Please waiting...")
    param_file = open(post_category_file_path + os.sep + post_category_file_name, 'r')
    while True:
        lines = param_file.readlines(500)
        if not lines:
            break
        for line in lines:
            try:
                post_url = line.split("|")[1]
                logging.info("post_url:" + post_url)
                post_category = line.split("|")[0]
                image_file_directory = filter(str.isalnum, line.split("|")[1].split("/")[-1].strip())
                source_image_directory_path = root_image_directory_path + os.sep + image_file_directory
                target_image_directory_path = root_image_directory_path + os.sep + image_directory_path_prefix + post_category
                if not os.path.exists(source_image_directory_path):
                    logging.info("The image directory " + image_file_directory + " does not exist!")
                    continue
                if not os.path.exists(target_image_directory_path):
                    os.makedirs(target_image_directory_path)
                shutil.move(source_image_directory_path, target_image_directory_path)
            except Exception as e:
                logging.exception("Exception! post_url:" + post_url)
    param_file.close()


def main():
    website_dict = {"1": "jxxxx", "2": "txxxx"}
    print "-----------------------"
    print "Choose Website:"
    keys = website_dict.keys()
    keys.sort()
    for key in keys:
        print key, "-", website_dict[key]
    print "-----------------------"
    while True:
        website_id = raw_input("website_id:").strip()
        if website_id in website_dict.keys():
            section = website_dict[website_id]
            break
        else:
            print "Error input! Please retry."

    option_dict = {"1": "scan post_url", "2": "scan post_category", "3": "scan image_url", "4": "download image",
                   "5": "classify", "6": "ALL", "7": "ALL but Classify"}
    print "-----------------------"
    print "Choose Option:"
    keys = option_dict.keys()
    keys.sort()
    for key in keys:
        print key, "-", option_dict[key]
    print "-----------------------"
    while True:
        option_id = raw_input("option_id:").strip()
        if option_id in option_dict.keys():
            break
        else:
            print "Error input! Please retry."

    if website_id == "1" and option_id in ["1", "6", "7"]:
        start_page_number = "1"
        end_page_number = "1"
        while True:
            start_post_number = raw_input("start_post_number:").strip()
            if not start_post_number:
                start_post_number = "1"
            if int(start_post_number) in range(1, 101):
                break
            else:
                print "Error input! Please retry."
        while True:
            end_post_number = raw_input("end_post_number:").strip()
            if not end_post_number:
                end_post_number = "20"
            if int(end_post_number) in range(1, 101) and int(end_post_number) >= int(start_post_number):
                break
            else:
                print "Error input! Please retry."
    elif website_id == "2" and option_id in ["1", "6", "7"]:
        while True:
            start_page_number = raw_input("start_page_number:").strip()
            if not start_page_number:
                start_page_number = "1"
            if int(start_page_number) in range(1, 101):
                break
            else:
                print "Error input! Please retry."
        while True:
            end_page_number = raw_input("end_page_number:").strip()
            if not end_page_number:
                end_page_number = "1"
            if int(end_page_number) in range(1, 101) and int(end_page_number) >= int(start_page_number):
                break
            else:
                print "Error input! Please retry."
        while True:
            start_post_number = raw_input("start_post_number:").strip()
            if not start_post_number:
                start_post_number = "1"
            if int(start_post_number) in range(1, 21):
                break
            else:
                print "Error input! Please retry."
        while True:
            end_post_number = raw_input("end_post_number:").strip()
            if not end_post_number:
                end_post_number = "20"
            if int(end_post_number) in range(1, 21) and int(end_post_number) >= int(start_post_number):
                break
            else:
                print "Error input! Please retry."
    else:
        pass

    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    work_directory = cf.get(section, "work_directory")
    logfile_name = cf.get(section, "logfile_name")
    category_url = cf.get(section, "category_url")
    encoding = cf.get(section, "encoding")
    post_url_pattern = cf.get(section, "post_url_pattern")
    post_category_pattern = cf.get(section, "post_category_pattern")
    image_url_pattern = cf.get(section, "image_url_pattern")
    post_url_prefix = cf.get(section, "post_url_prefix")
    post_category_prefix = cf.get(section, "post_category_prefix")
    image_url_prefix = cf.get(section, "image_url_prefix")

    post_url_file_path = work_directory + os.sep + "param"
    post_url_file_name = "post_url.txt"
    post_category_file_path = work_directory + os.sep + "param"
    post_category_file_name = "post_category.txt"
    image_url_file_path = work_directory + os.sep + "param"
    image_url_file_name = "image_url.txt"
    root_image_directory_path = work_directory + os.sep + "image"
    image_directory_path_prefix = section + "-"

    if not os.path.exists(work_directory):
        os.makedirs(work_directory)
    if not os.path.exists(post_url_file_path):
        os.makedirs(post_url_file_path)
    if not os.path.exists(post_category_file_path):
        os.makedirs(post_category_file_path)
    if not os.path.exists(image_url_file_path):
        os.makedirs(image_url_file_path)
    if not os.path.exists(root_image_directory_path):
        os.makedirs(root_image_directory_path)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(filename)s(%(lineno)d): %(funcName)s] PID-%(process)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=work_directory + os.sep + logfile_name,
        filemode="a")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s]  PID-%(process)d  %(funcName)s - %(message)s")
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    if option_id == "1" or option_id == "6" or option_id == "7":
        if category_url.find("${page_number}") != -1:
            category_url_init = category_url
            for page_number in range(int(start_page_number), int(end_page_number) + 1):
                category_url = category_url_init.replace("${page_number}", str(page_number))
                get_post_url(category_url, post_url_pattern, post_url_prefix, encoding, post_url_file_path,
                             post_url_file_name, start_post_number, end_post_number)
        else:
            get_post_url(category_url, post_url_pattern, post_url_prefix, encoding, post_url_file_path,
                         post_url_file_name, start_post_number, end_post_number)

    if option_id == "2" or option_id == "6" or option_id == "7":
        get_post_category(post_url_file_path, post_url_file_name, post_category_pattern, post_category_file_path,
                          post_category_file_name, post_category_prefix, encoding)

    if option_id == "3" or option_id == "6" or option_id == "7":
        get_image_url(post_url_file_path, post_url_file_name, image_url_pattern, image_url_file_path,
                      image_url_file_name, image_url_prefix, encoding)

    if option_id == "4" or option_id == "6" or option_id == "7":
        download_image_file(image_url_file_path, image_url_file_name, root_image_directory_path)

    if option_id == "5" or option_id == "6":
        classify(post_category_file_path, post_category_file_name, root_image_directory_path, image_directory_path_prefix)


if __name__ == "__main__":
    main()
