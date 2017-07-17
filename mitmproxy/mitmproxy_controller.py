
# coding: utf-8

# In[22]:

import subprocess
import time
import logging
import configparser

global config
global logger


# In[23]:

def init_logger():
    
    global config
    global logger
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    logger = logging.getLogger('mitmproxy')

    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    
    file_name = config['filename']['browser']

    file_handler = logging.FileHandler(file_name)
    stream_handler = logging.StreamHandler()

    file_handler.setFormatter(fomatter)
    stream_handler.setFormatter(fomatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.setLevel(logging.DEBUG)

    return logger


# In[24]:

def start_process(dumpfile_name):
    #global config
    #container_name = config['proxy']['name']
    container_name = 'mitmproxy'
    
    file_path = '/home/' + dumpfile_name
      
    command = "docker exec " + container_name + " mitmproxy -w " + file_path
    #logger.debug(command)

    run_command = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)


# In[28]:

def kill_process(process):
    
    #container_name = config['proxy']['name']
    container_name = 'mitmproxy'
    process_list_command = "docker exec " + container_name + " ps"
    process_list_result = subprocess.check_output(process_list_command, shell=True)
    results = str(process_list_result).split('\\n')
    index = -1
    
    for result in results:
        if result.find('mitmproxy') > 0:
            lst = result.split(' ')
            index = lst[lst.index('?')-1]
            break
    
    process_kill_command = "docker exec " + container_name + " kill " + str(index)
    #logger.debug(process_kill_command)
    run_command = subprocess.Popen(process_kill_command, stdout=subprocess.PIPE, shell=True)


# In[26]:

def main():
    logger = init_logger()
    

    logger.info("TEST START")
    logger.debug("mitmproxy start")

    proc = start_process('test')
    logger.debug("mitmproxy run")

    kill_process(proc)
    logger.debug("mitmproxy stop")
   


# In[ ]:

if __name__ == "__main__":
    main()


# In[ ]:



