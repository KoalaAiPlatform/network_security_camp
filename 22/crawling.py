from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Lock
import asyncio
import re
import random

main_url = "https://time.geekbang.org"  # 初始页面地址
domain = "geekbang.org"
urls = set()  # 爬取到的地址集合，通过set去重
task = set()  # 爬取任务，避免重复爬取
lock = Lock()
proxy_pool = [
    "134.35.254.250:8080",
    "177.93.36.81:999",
    "134.35.25.155:8080"
]


def register_task(craw_url):
    global lock
    global task
    with lock:
        if task.__contains__(craw_url):
            return False
        else:
            task.add(craw_url)
            return True


async def next_send(next_url):
    global urls
    global domain
    url_spilt = next_url.split('/')
    if len(url_spilt) > 2:
        temp_domain = url_spilt[2]
        if temp_domain.endswith(domain) and next_url.endswith('html'):
            await asyncio.create_task(crawling(next_url))


async def get_url_from_link(d):
    elements = d.find_elements(By.XPATH, "//link")  # 从link中获取
    global urls
    for element in elements:
        url = element.get_attribute("href")
        if url and not url.isspace():
            urls.add(url)
            await next_send(url)


async def get_url_from_a(d):
    elements = d.find_elements(By.XPATH, "//a")  # 从link中获取
    global urls
    for element in elements:
        href = element.get_attribute("href")
        if href and not href.isspace():
            urls.add(href)
            await next_send(href)


async def get_url_from_img(d):
    elements = d.find_elements(By.XPATH, "//img")  # 从link中获取
    global urls
    for element in elements:
        src = element.get_attribute("src")
        if src and not src.isspace():
            urls.add(src)
            await next_send(src)


async def get_url_from_script(d):
    elements = d.find_elements(By.XPATH, "//script")  # 从script中获取
    global urls
    for element in elements:
        src = element.get_attribute("src")
        if src and not src.isspace():
            urls.add(src)
            await next_send(src)


async def get_url_from_page_source(d):
    """
    解析页面源码，使用正则的方式匹配请求地址
    :param d:
    :return:
    """
    page_source = d.page_source
    pattern = r"(https?://\S+?)['\"\?]"
    source_urls = re.findall(pattern, page_source)
    for re_url in source_urls:
        if re_url and not re_url.isspace():
            urls.add(re_url)
            await next_send(re_url)


def is_intercept(d):
    pass


async def parse(d):
    await asyncio.create_task(get_url_from_link(d))  # 从link中获取地址
    await asyncio.create_task(get_url_from_a(d))  # 从a标签中获取地址
    await asyncio.create_task(get_url_from_img(d))  # 从img标签中获取地址
    await asyncio.create_task(get_url_from_script(d))  # 从script标签中获取地址
    await asyncio.create_task(get_url_from_page_source(d))  # 从源码内容中获取地址


async def crawling(craw_url, retry_times=3):
    """
    抓取主函数，获取到页面数据之后开启三个任务解析不同位置的url信息
    :param retry_times:  重试次数
    :param craw_url:  请求地址
    :return:
    """
    profile = webdriver.FirefoxOptions()  # 驱动设置
    profile.set_preference("general.useragent.override", "geektime.com")
    proxy = random.choice(proxy_pool)
    profile.add_argument('--proxy-server=%s' % proxy)
    driver = webdriver.Firefox(options=profile)
    if register_task(craw_url):
        with driver:
            driver.get(craw_url)  # 查看页面源码，可以找到拥有url信息的标签有link，script的src和js代码中
            if not is_intercept(driver):  # 查看是否被拦截了，如果被拦截了，则尝试随机代理，重新请求
                await asyncio.create_task(parse(driver))
            else:
                retry_times -= 1
                if retry_times > 0:
                    await crawling(craw_url, retry_times)


print("start crawling...")
asyncio.run(crawling(main_url, 3))

print(f'共爬取到链接{len(urls)}个')

for url in urls:
    print(url)
