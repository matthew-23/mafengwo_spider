from collections import defaultdict
import time
import re
import json
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from configs import CITIE_IDS, POST_BASE_URL, PHOTO_BASE_URL, PROFILE_BASE_URL

driver = webdriver.PhantomJS(executable_path="phantomjs")


def get_posts_url_and_author_profile(city_id):
    """
    获取游记链接
    :param city_id:
    :return:
    """

    driver.get(POST_BASE_URL.format(city_id))

    time.sleep(5)
    _ = driver.find_elements_by_class_name("post-item")
    print("游记数量", len(_))

    post_info = []
    for post_element in _:
        post_id = post_element.find_element_by_tag_name("a").get_attribute(
            "href")
        post_id = re.compile("\d+").search(post_id)[0]
        post_url = PHOTO_BASE_URL.format(city_id, post_id)

        profile_url = post_element.find_element_by_class_name(
            "author").find_element_by_tag_name("a").get_attribute("href")

        print(post_url, profile_url)
        post_info.append((post_url, profile_url))
        if len(post_info) >= 10:
            break

    return post_info[:10]


def get_pic_urls_by_post_url(post_url):
    driver.get(post_url)
    time.sleep(5)

    p0 = driver.find_elements_by_class_name("part0")
    p1 = driver.find_elements_by_class_name("part1")
    p2 = driver.find_elements_by_class_name("part2")
    p3 = driver.find_elements_by_class_name("part3")
    pics = p0 + p1 + p2 + p3

    print(post_url, len(pics))

    pic_urls = []
    for pic in pics:
        pic_url = pic.find_element_by_css_selector("a > img").get_attribute(
            "data-original")
        pic_urls.append(pic_url)

    return pic_urls


def get_author_gender_by_profile_url(profile_url):
    """
    根据个人主页获取性别
    :param profile_url:
    :return:
    """
    driver.get(profile_url)
    time.sleep(5)

    try:
        driver.find_element_by_class_name("MGenderMale")
        return 'Male'
    except NoSuchElementException:
        return 'Female'


def process_city_posts(post_infos):
    """
    获取所有游记的图片
    :param post_urls:
    :return:
    """
    posts = []
    for post_url, profile_url in post_infos:
        _d = {}
        _d[post_url] = get_pic_urls_by_post_url(post_url)
        _d["gender"] = get_author_gender_by_profile_url(profile_url)

        posts.append(_d)
        print("图片数量", len(_d[post_url]))
    return posts


def process_city(city_name):
    """
    按城市处理
    :param city_name:
    :return:
    """
    print(city_name)
    city_id = CITIE_IDS[city_name]
    post_infos = get_posts_url_and_author_profile(city_id)
    city_data = process_city_posts(post_infos)

    file_name = "{}.json".format(city_name)
    file_name = os.path.join(os.getcwd(), 'data', file_name)

    with open(file_name, "w") as f:
        f.write(json.dumps(city_data))


if __name__ == '__main__':
    # process_city("香港")
    process_city("澳门")
    process_city("泰国")
    process_city("韩国")
    process_city("日本")

    # 关闭浏览器
    driver.close()
