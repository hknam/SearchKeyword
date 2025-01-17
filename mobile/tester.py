from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import subprocess
import sys
import platform
import signal
import os
import argparse

def detect_os():
    platform_name = platform.system()
    if platform_name == 'Linux':
        return '../webdriver/chromedriver_linux'
    elif platform_name == 'Darwin':
        return '../webdriver/chromedriver_macos'
    else:
        print('Do not support this platform')
        sys.exit(1)


def add_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='test page path')
    parser.add_argument('--start', help='start page index')
    parser.add_argument('--end', help='end page index')

    return parser

def init_adb_server():
    print('===== START ADB SERVER =====')
    start_server = subprocess.Popen('adb start-server', stdout = subprocess.PIPE, shell = True)
    output = start_server.stdout.read()

    print(output)

def close_webdriver_port():
    get_port_number = subprocess.Popen(['lsof -i :9515'], stdout = subprocess.PIPE, shell = True)
    output = str(get_port_number.stdout.read())
    pid_line = output.split('\\n')[1]
    pid = int(pid_line.split(' ')[1])
    os.kill(pid, signal.SIGTERM)


def kill_adb_server():
    print('===== KILL ADB SERVER =====')
    kill_server = subprocess.Popen('adb kill-server', stdout=subprocess.PIPE, shell=True)
    output = kill_server.stdout.read()

    print(output)

def run_chromedriver():

    driver_path = detect_os()
    command = subprocess.Popen(driver_path, stdout = subprocess.PIPE, shell = True)
    return command



def init_webdriver():

    driver_path = detect_os()
    options = webdriver.ChromeOptions()
    options.add_experimental_option('androidPackage', 'com.android.chrome')
    options.add_argument("--incognito")

    driver = webdriver.Chrome(driver_path, chrome_options=options)

    return driver


def search_test():

    parser = add_argument()


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

        time.sleep(5)

        print( driver.execute_script('return window.document.referrer') )

        driver.quit()

        time.sleep(5)


    chromedriver.kill()

    kill_adb_server()

    close_webdriver_port()
    

search_test()

