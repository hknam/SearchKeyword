
# coding: utf-8

# In[1]:

import configparser
config = configparser.ConfigParser()


# In[2]:

config['filename'] = {}


# In[3]:

config['filename']['controller'] = 'controller.log'
config['filename']['browser'] = 'browser.log'
config['filename']['reader'] = 'reader.log'
config['filename']['finder'] = 'finder.log'


# In[4]:

config['proxy'] = {}


# In[5]:

config['proxy']['address'] = '172.17.0.2'
config['proxy']['port'] = '8080'
config['proxy']['name'] = 'mitmproxy'


# In[6]:

config['webdriver'] = {}


# In[7]:

config['webdriver']['path'] = './geckodriver'
config['webdriver']['base_url'] = 'http://www.google.com'


# In[8]:

with open('config.ini', 'w') as configfile:
    config.write(configfile)


# In[ ]:



