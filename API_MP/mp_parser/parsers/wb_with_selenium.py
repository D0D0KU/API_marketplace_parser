from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


fake_useragent = UserAgent().chrome


def create_browser(user_agent, chromedriver):
    """
    Создает вебдрайвер и добавляет необходимые опции
    :param user_agent:
    :param chromedriver:
    :return:
    """
    opts = webdriver.ChromeOptions()
    opts.add_argument(user_agent)  # Добавляет юзер-агента в опции
    opts.add_argument("--disable-blink-features=AutomationControlled")  # Отключает видимость автоматизации для сайта
    service = Service(executable_path=chromedriver)
    browser = webdriver.Chrome(
        service=service,
        options=opts
    )
    return browser


def parse_links(parse_data):
    url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={parse_data}"
    br = create_browser(fake_useragent, r"chromedriver\chromedriver.exe")


    br.get(url)
    tpl = (By.CSS_SELECTOR, "[class='pagination']")
    element = WebDriverWait(br, 10).until(EC.visibility_of_element_located(tpl))

    for _ in range(10):
        # прокрутка страницы до элемента
        br.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)


    html = br.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    all_teg_a = soup.find_all('a')
    for i in all_teg_a:
        if 'detail.aspx' in i.attrs["href"]:
            links.append(i.attrs["href"])
    br.quit()
    return links
