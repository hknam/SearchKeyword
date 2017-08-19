import sys
import linecache
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import configparser
import subprocess
import os
import logging
import datetime

config = configparser.ConfigParser()
config.read('config.ini')


proxy = config['proxy']['address']
port =  config['proxy']['port']
driver_path = config['webdriver']['path']
base_url = config['webdriver']['base_url']


def init_logger(file_name):

    logger = logging.getLogger(file_name)

    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    folder_path = os.path.expanduser('~') + "/" + "flowdump/logs/"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_handler = logging.FileHandler(folder_path + file_name)

    stream_handler = logging.StreamHandler()

    file_handler.setFormatter(fomatter)
    stream_handler.setFormatter(fomatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.setLevel(logging.DEBUG)

    return logger

def init_webdriver():
    """
        apply proxy preference to selenium webdriver
        get proxy, webdriver settring form config.ini            
    """
    
    try:       
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.ssl_port', int(port))
        profile.set_preference('network.proxy.ssl', proxy)
        profile.set_preference('network.proxy.http_port', int(port))
        profile.set_preference('network.proxy.http', proxy)
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('dom.popup_maximum', 0)
        
        driver = webdriver.Firefox(executable_path = driver_path, firefox_profile = profile)
        driver.set_page_load_timeout(60)
                
        return driver
    except Exception as e:
        print(e)
        driver.quit()


def find_external_url(driver):
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        current_url = driver.current_url

        #print(link.get_attribute('href'))


def find_input_tag(driver):
    try:
        tags = driver.find_elements_by_tag_name('input')
        for tag in tags:
            
            if tag.get_attribute('type') != 'text':
                continue
                
            prev_url = driver.current_url

            tag_id = find_id_tag(tag)
            tag_name = find_name_tag(tag)
            tag_class = find_class_tag(tag)

            if tag_id:
                elem = driver.find_element_by_id(tag_id)
                elem.send_keys('iphone')
                elem.send_keys(Keys.RETURN)
                time.sleep(10)

                next_url = driver.current_url
                if prev_url != next_url:
                    find_external_url(driver)
                break

            elif tag_name:
                elem = driver.find_element_by_name(tag_name)
                elem.send_keys('iphone')
                elem.send_keys(Keys.RETURN)
                time.sleep(10)

                next_url = driver.current_url
                if prev_url != next_url:
                    find_external_url(driver)
                break
                
            elif tag_class:
                elem = driver.find_element_by_class_name(tag_class)
                elem.send_keys('iphone')
                elem.send_keys(Keys.RETURN)
                time.sleep(10)

                next_url = driver.current_url
                if prev_url != next_url:
                    if next_url.startswith('https://'):
                        find_external_url(driver)
                break
            else:
                print("Doesn't find any input tags")
                
    except Exception as e:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj) )
        print(e)



def find_id_tag(tag):
    if tag.get_attribute('id'):
        return tag.get_attribute('id')
    else:
        return False

def find_class_tag(tag):
    if tag.get_attribute('class'):
        return tag.get_attribute('class')
    else:
        return False


def find_name_tag(tag):
    if tag.get_attribute('name'):
        return tag.get_attribute('name')
    else:
        return False


def start_process(dumpfile_name):
    folder_path = os.path.expanduser('~') + "/" + "flowdump/traffic/"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    command = "mitmdump -w " + folder_path + dumpfile_name

    run_command = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    return run_command


def kill_process(logger, process):
    process.kill()
    return process.pid

def close_mitmproxy_socket():
    http = "fuser -k -n tcp 8080"
    https = "fuser -k -n tcp 443"

    subprocess.Popen(http, stdout=subprocess.PIPE, shell=True)
    subprocess.Popen(https, stdout=subprocess.PIPE, shell=True)

def main():

    try:
        with open('gov_list.txt', 'r') as file:
            pages = file.read()


        for page in pages.split('\n'):
            dumpfile_name = page.split(',')[0]
            logger = init_logger(dumpfile_name)
            url = page.split(',')[1]
            mitm_proc = start_process(dumpfile_name)
            logger.info("mitmdump process start : pid " + str(mitm_proc.pid) )

            driver = init_webdriver()
            driver.get(base_url)
            logger.info("open web browser : " + base_url)
            driver.get(url)

            logger.info("current browser url : " + driver.current_url)
            logger.info("find input tag")
            find_input_tag(driver)
            driver.implicitly_wait(30)
            logger.debug(url)
            driver.quit()

            logger.info("close web browser")
            killed_pid = kill_process(logger, mitm_proc)

            logger.info("mitmdump process stop : pid " + str(killed_pid) )
            close_mitmproxy_socket()
            time.sleep(5)


    except Exception as e:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj) )
        print(e)
        sys.exit(1)


if __name__ == "__main__":
   main()
