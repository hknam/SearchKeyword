import subprocess
import os
import logging
import configparser

global config
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


def start_process(dumpfile_name):

    folder_path = os.path.expanduser('~') + "/" + "flowdump" + "/"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
      
    command = "mitmproxy -w " + folder_path + dumpfile_name

    run_command = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)


def kill_process(process):
    
    process_list_command = "ps"
    process_list_result = subprocess.check_output(process_list_command, shell=True)
    results = str(process_list_result).split('\\n')
    index = -1
    
    for result in results:
        if result.find('mitmproxy') > 0:
            lst = result.split(' ')
            index = lst[lst.index('?')-1]
            break
    
    process_kill_command = " kill " + str(index)
    run_command = subprocess.Popen(process_kill_command, stdout=subprocess.PIPE, shell=True)


def main():
    logger = init_logger()
    

    logger.info("TEST START")
    logger.debug("mitmproxy start")

    proc = start_process('test')
    logger.debug("mitmproxy run")

    kill_process(proc)
    logger.debug("mitmproxy stop")
   

if __name__ == "__main__":
    main()
