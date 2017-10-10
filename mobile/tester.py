from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import subprocess


def init_adb_server():
    print('===== START ADB SERVER =====')
    start_server = subprocess.Popen('adb start-server', stdout = subprocess.PIPE, shell = True)
    output = start_server.stdout.read()

    print(output)

def close_webdriver_port():
    close_port = subprocess.Popen('fuser -k -n tcp 9515', stdout = subprocess.PIPE, shell = True)
    output = close_port.stdout.read()

    print(output)


def kill_adb_server():
    print('===== KILL ADB SERVER =====')
    kill_server = subprocess.Popen('adb kill-server', stdout=subprocess.PIPE, shell=True)
    output = kill_server.stdout.read()

    print(output)

def run_chromedriver():

    command = subprocess.Popen('../mitmproxy/webdriver/chromedriver', stdout = subprocess.PIPE, shell = True)
    return command



def init_webdriver():


    options = webdriver.ChromeOptions()
    options.add_experimental_option('androidPackage', 'com.android.chrome')
    options.add_argument("--incognito")

    driver = webdriver.Chrome(chrome_options=options)

    return driver


def search_test():

    init_adb_server()

    chromedriver = run_chromedriver()

    keyword = 'iphone'

    for count in range(2):

        driver = init_webdriver()

        driver.get('https://www.yahoo.com')

        search_button = driver.find_element_by_id('uh-search-ph')

        search_button.send_keys(Keys.RETURN)

        search_box = driver.find_element_by_id('uh-search-box')

        search_box.send_keys(keyword)

        search_box.send_keys(Keys.RETURN)

        driver.quit()

        time.sleep(5)


    chromedriver.kill()

    kill_adb_server()

    close_webdriver_port()

search_test()

