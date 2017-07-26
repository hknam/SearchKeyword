
import configparser
config = configparser.ConfigParser()


config['filename'] = {}


config['filename']['controller'] = 'controller.log'
config['filename']['browser'] = 'browser.log'
config['filename']['reader'] = 'reader.log'
config['filename']['finder'] = 'finder.log'


config['proxy'] = {}


config['proxy']['address'] = '172.17.0.2'
config['proxy']['port'] = '8080'
config['proxy']['name'] = 'mitmproxy'


config['webdriver'] = {}


config['webdriver']['path'] = './geckodriver'
config['webdriver']['base_url'] = 'about:blank'

with open('config.ini', 'w') as configfile:
    config.write(configfile)



