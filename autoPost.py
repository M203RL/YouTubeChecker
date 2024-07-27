from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webbrowser
import pyperclip
import time
import re

UserData = r''

##場外
link1 = ''

##專版
link2 = ''


def initial(test):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("disable-infobars") 

    # path of the chrome's profile parent directory - change this path as per your system
    options.add_argument(f"user-data-dir={UserData}")

    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument('--no-sandbox')
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    if test:
        ##場外
        driver.get(link1)
    else:
        ##專版
        driver.get(link2)

        select = Select(driver.find_element("name", 'nsubbsn'))
        select.select_by_value('3')

        select = Select(driver.find_element("name", 'subject'))
        select.select_by_value('2')
    time.sleep(0.1)
    if test:
        driver.find_element("id", 'editor').click()
    else:
        driver.find_element("id", 'postTips').click()


    try:
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'editor-button fe_source') and not(contains(@class, 'editor-button fe_source is-active'))]"))).click()
    except:
        pass
    text = driver.find_element("id", 'source')
    text.clear()
    return driver

def post(driver, test, title, article):
    # ts = time.time()
    if not test:
        ##標題
        tt = driver.find_element("name", 'title')
        pyperclip.copy(title)
        tt.send_keys(Keys.CONTROL, 'v')

    ##內文
    text = driver.find_element("id", 'source')
    pyperclip.copy(article)
    text.send_keys(Keys.CONTROL, 'v')
    
    ##發文
    target = driver.find_element(By.CSS_SELECTOR, 'a[href="javascript:Forum.Post.post();"]')
    target.click()
    

    target = driver.find_element(By.CSS_SELECTOR, 'button[class="btn btn-insert btn-primary"]')
    target.click()
    get_url = driver.current_url
    if test:
        while get_url == link1:
            get_url = driver.current_url
            time.sleep(0.01)
        driver.quit()
        return get_url
    if not test:
        while get_url == link2:
            get_url = driver.current_url
            time.sleep(0.01)
        driver.get('https://forum.gamer.com.tw/B.php?bsn=23805&subbsn=3')
        posted = str(driver.find_element(By.XPATH,f'//p[text()="【情報】{title}"]').get_attribute('href'))
        webbrowser.open(f'https://forum.gamer.com.tw/{posted}',1)
        driver.get(f'https://forum.gamer.com.tw/{posted}')
        id1 = re.findall(r'\d+', str(driver.find_element(By.CSS_SELECTOR, 'section[class="c-section"]').get_attribute('id')))[0]
        id2 = str(re.search(r'.*?bsn=23805&snA=(.*?)&tnum', posted).group(1))
        driver.quit()
        driver.quit()
        return f'https://forum.gamer.com.tw/{posted}'


if __name__ == '__main__':
    ts = time.time()
    initial(True)
    post(True, 'title', 'adsad')
    tf = time.time()
    dt = round(tf - ts, 2)
    print('Total Time: ' + str(dt) + 's')
