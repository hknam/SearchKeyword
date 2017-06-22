import subprocess
import time
import logging


def init_logger():

    logger = logging.getLogger('mitmproxy')

    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    file_name = './controller.log'

    file_handler = logging.FileHandler(file_name)
    stream_handler = logging.StreamHandler()

    file_handler.setFormatter(fomatter)
    stream_handler.setFormatter(fomatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.setLevel(logging.DEBUG)

    return logger

def start_process(dumpfile_name):

    cmd = "mitmproxy -w " + dumpfile_name
    mitmporxy_run = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    return mitmporxy_run

def kill_process(process):

    time.sleep(15)
    process.kill()


logger = init_logger()

logger.info("TEST START")
logger.debug("mitmproxy start")

proc = start_process('test')
logger.debug("mitmproxy run")

kill_process(proc)
logger.debug("mitmproxy stop")