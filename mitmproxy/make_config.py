import platform
import configparser
config = configparser.ConfigParser()


def detect_os():
    platform_name = platform.system()
    if platform_name == 'Linux':
        return 'geckodriver_linux'
    elif platform_name == 'Darwin':
        return 'geckodriver_macos'
    else:
        print('Do not support this platform')
        sys.exit(1)

config['filename'] = {}


config['filename']['controller'] = 'controller.log'
config['filename']['browser'] = 'browser.log'
config['filename']['reader'] = 'reader.log'
config['filename']['finder'] = 'finder.log'
config['filename']['keyword'] = 'iphone'

config['proxy'] = {}


config['proxy']['address'] = '127.0.0.1'
config['proxy']['port'] = '8080'
config['proxy']['name'] = 'mitmproxy'


config['webdriver'] = {}


config['webdriver']['path'] = './webdriver/' + detect_os()
config['webdriver']['base_url'] = 'about:blank'



with open('config.ini', 'w') as configfile:
    config.write(configfile)



