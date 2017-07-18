
# coding: utf-8

# In[ ]:

import sys
import linecache
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import configparser
import mitmproxy_controller as controller


# In[ ]:

config = configparser.ConfigParser()
config.read('config.ini')


# In[ ]:

proxy = config['proxy']['address']
port =  config['proxy']['port']
driver_path = config['webdriver']['path']
base_url = config['webdriver']['base_url']


# In[ ]:

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
        
        driver = webdriver.Firefox(executable_path = driver_path, firefox_profile = profile)
        driver.set_page_load_timeout(60)
                
        return driver
    except Exception as e:
        print(e)
        driver.quit()


# In[ ]:

def find_external_url(driver):
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        print(link.text)


# In[ ]:

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


# In[ ]:

def find_id_tag(tag):
    if tag.get_attribute('id'):
        return tag.get_attribute('id')
    else:
        return False


# In[ ]:

def find_class_tag(tag):
    if tag.get_attribute('class'):
        return tag.get_attribute('class')
    else:
        return False


# In[ ]:

def find_name_tag(tag):
    if tag.get_attribute('name'):
        return tag.get_attribute('name')
    else:
        return False


# In[ ]:

def main():
    try:
        driver = init_webdriver()
        #mitm_proc = controller.start_process('test')
        
        driver.get(base_url)
        
        
        with open('gov_list.txt', 'r') as file:
            pages = file.read()
        for page in pages.split('\n'):
            url = page.split(',')[1]
            driver.get(url)
            find_input_tag(driver)
            driver.implicitly_wait(30)
            
        '''
        driver.get('http://gc.jbpolice.go.kr/index.police')
        driver.implicitly_wait(30)
        find_input_tag(driver)
        '''
        #controller.kill_process(mitm_proc)
        
    except Exception as e:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj) )
        print(e)
        driver.quit()
        sys.exit(1)


# In[ ]:

if __name__ == "__main__":
    main()


# In[ ]:



