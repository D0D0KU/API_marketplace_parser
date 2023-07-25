from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time


fake_useragent = UserAgent().chrome


def create_browser(user_agent, chromedriver):
    """
    Создает вебдрайвер и добавляет необходимые опции
    :param user_agent:
    :param chromedriver:
    :return:
    """
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(user_agent)  # Добавляет юзер-агента в опции
    options.add_argument("--disable-blink-features=AutomationControlled")  # Отключает видимость автоматизации для сайта
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    service = Service(executable_path=chromedriver)
    browser = webdriver.Chrome(
        service=service,
        options=options
    )
    return browser

def solve_captcha(br):
    try:
        tuple_captcha_button = (By.CSS_SELECTOR, "[class='CheckboxCaptcha-Anchor']")
        captcha_button = WebDriverWait(br, 5).until(EC.visibility_of_element_located(tuple_captcha_button))
        captcha_button.click()
    except:
        print('no captcha')


def cheсk_last_page(br):
    tpl = (By.CSS_SELECTOR, '[data-baobab-name="next"]')
    try:
        last_page = WebDriverWait(br, 15).until(EC.visibility_of_element_located(tpl))
        return True
    except:
        return False
    

def check_pagination(br):
    tpl = (By.CSS_SELECTOR, '[class="CPS7s"]')
    try:
        pagination = WebDriverWait(br, 15).until(EC.visibility_of_element_located(tpl))
        br.execute_script("arguments[0].scrollIntoView();", pagination)
        return True
    except:
        return False

def save_products(br):
    all_products = []
    html = br.page_source

    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find('main', id="searchResults")

    all_products_groups = products.find_all('div', class_="_HcxN _1oMZn _1nwni")
    all_products_cards = []
    for i in all_products_groups:
        all_products_cards.extend(i.find_all('article'))

    for i in all_products_cards:
        product = {'name': f'{i.find("h3").text}',
                    'price': f'''{i.find("h3").findNext("h3").find("span").findNext("span").text}.00''',
                    'link': f'''https://market.yandex.ru{i.find("a").attrs["href"]}'''
                    }
        all_products.append(product)
    return all_products

def parse_products(parse_data, parse_page=100):
    url = f"https://market.yandex.ru/search?cvredirect=1&text={parse_data}"
    br = create_browser(fake_useragent, r"chromedriver\chromedriver.exe")

    br.get(url)
    solve_captcha(br)

    all_products = []
    flag_page = True
    for _ in range(1, parse_page + 1):
        if flag_page:
            flag_page = False
            check_pagination(br)
            all_products.extend(save_products(br))
        else:
            if cheсk_last_page(br):
                tpl = (By.CSS_SELECTOR, '[data-baobab-name="next"]')
                last_page = WebDriverWait(br, 10).until(EC.visibility_of_element_located(tpl))
                last_page.click()
                time.sleep(5)
                check_pagination(br)
                all_products.extend(save_products(br))
            else:
                break
    br.quit()
    return all_products
