import sys
import linecache
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import time
import configparser
import subprocess
import os
import logging
import datetime

config = configparser.ConfigParser()
config.read('config.ini')

keyword = config['filename']['keyword']
proxy = config['proxy']['address']
port =  config['proxy']['port']
driver_path = config['webdriver']['path']
base_url = config['webdriver']['base_url']


def init_logger(file_name):

    logger = logging.getLogger(file_name)

    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    folder_path = os.path.expanduser('~') + "/flowdump/logs/"

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
    logger = init_logger('init_webdriver')

    try:       
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.ssl_port', int(port))
        profile.set_preference('network.proxy.ssl', proxy)
        profile.set_preference('network.proxy.http_port', int(port))
        profile.set_preference('network.proxy.http', proxy)
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('dom.popup_maximum', 0)


        driver = webdriver.Firefox(executable_path = driver_path, firefox_profile = profile)
        driver.set_page_load_timeout(120)


        return driver
    except Exception as e:
        logger.error(e)
        sys.exit(1)




def find_external_url(driver):
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        current_url = driver.current_url

        #print(link.get_attribute('href'))


def find_input_tag(driver):

    logfile_name = driver.current_url.split("://")[1].split("/")[0]
    logger = init_logger('find_input_tag : ' + logfile_name)
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
                elem.send_keys(keyword)
                elem.send_keys(Keys.RETURN)
                time.sleep(10)

                next_url = driver.current_url
                if prev_url != next_url:
                    find_external_url(driver)
                break

            elif tag_name:
                elem = driver.find_element_by_name(tag_name)
                elem.send_keys(keyword)
                elem.send_keys(Keys.RETURN)
                time.sleep(10)

                next_url = driver.current_url
                if prev_url != next_url:
                    find_external_url(keyword)
                break
                
            elif tag_class:
                elem = driver.find_element_by_class_name(tag_class)
                elem.send_keys(keyword)
                elem.send_keys(Keys.RETURN)
                time.sleep(10)

                next_url = driver.current_url
                if prev_url != next_url:
                    if next_url.startswith('https://'):
                        find_external_url(driver)
                break
            else:
                logger.error("Doesn't find any input tags")
                
    except TimeoutException as e:
        logger.error(e)
        driver.close()


    except Exception as e:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        logger.error('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj) )




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


def start_process(logger, dumpfile_name):
    folder_path = os.path.expanduser('~') + "/flowdump/traffic/"
    full_file_path = folder_path + dumpfile_name

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if os.path.exists(full_file_path):
        os.remove(full_file_path)

    command = "mitmdump -w " + full_file_path

    run_command = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    outs, errs = run_command.communicate(timeout=30)

    logger.info("subprocess open outs : " + str(outs))
    logger.info("subprocess open errors : " + str(errs))

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
    logger = init_logger('url, page number')

    urls = 'gov_list.txt'
    with open(urls, 'r') as file:
        pages = file.read()

    page_list = pages.split('\n')

    logger.info("total pages : " + str(len(page_list)))

    try:
        start_page_number = int(sys.argv[1])
        end_page_number = int(sys.argv[2])

        if end_page_number > len(page_list):
            end_page_number = len(page_list)
            logger.info("end page number : " + str(end_page_number))

        if start_page_number > end_page_number:
            logger.error("page number out of range error")
            sys.exit(1)

    except IndexError as e:
        start_page_number = 0
        end_page_number = len(page_list)
        logger.info("no input number, start page number : 0, end page number : " + str(end_page_number))

    logger.info("start page number : " + str(start_page_number) + " end page number : " + str(end_page_number))



    for index in range(start_page_number, end_page_number):
        url = page_list[index].split(',')[1]
        try:
            url = page_list[index].split(',')[1]
            dumpfile_name = url.split("://")[1].split("/")[0]
        except IndexError as e:
            logger.error(e)
            continue


        logger = init_logger(dumpfile_name)

        mitm_proc = start_process(logger, dumpfile_name)
        logger.info("mitmdump process start : pid " + str(mitm_proc.pid))


        driver = init_webdriver()
        logger.info("open selenium webdriver")


        # url = 'http://' + page

        try:
            driver.get(base_url)
            logger.info("open web browser : " + base_url)
            driver.get(url)

            logger.info("current browser url : " + driver.current_url)
            logger.info("find input tag")
            find_input_tag(driver)
            driver.implicitly_wait(30)
            logger.debug(url)
            driver.quit()

        except TimeoutException as e:
            logger.error("timeout exception : " + driver.current_url)


        except Exception as e:
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            logger.error('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj) )
            logger.error("error page number : " + str(index) )


        finally:
            logger.info("close web browser")
            killed_pid = kill_process(logger, mitm_proc)
            logger.info("mitmdump process stop : pid " + str(killed_pid))
            close_mitmproxy_socket()
            logger.info("close mitmproxy port")
            time.sleep(5)


if __name__ == "__main__":
   main()
