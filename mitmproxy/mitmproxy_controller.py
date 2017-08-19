import subprocess
import os
import logging
import configparser

global config

def init_logger(file_name):

    global config
    global logger


    logger = logging.getLogger('mitmproxy')

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


def start_process(dumpfile_name):

    folder_path = os.path.expanduser('~') + "/" + "flowdump/traffic/"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
      
    command = "mitmdump -w " + folder_path + dumpfile_name

    run_command = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    logger.info("start mitmproxy pid : ", run_command.pid)
    return run_command



def kill_process(process):
    

    process.kill()
    logger.info("kill process pid : ", process.pid)

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
