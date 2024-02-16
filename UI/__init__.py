import sys
import time
import logging
import os
from .Frame import Frame
from PySide6.QtWidgets import QApplication


log_dir = 'logs'
keep_time = 30*24*3600
keep_num = 20

def set_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(f'logs/{int(time.time())}.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info('logger start!')
    return logger

def clear_logs():
    cur_time = time.time()
    file_list = []
    for file in os.listdir(log_dir):
        file_path = os.path.join(log_dir, file)
        modified_time = os.path.getmtime(file_path)
        if cur_time - modified_time > keep_time:
            os.remove(file_path)
            logger.info(f'clear log file: {file_path}')
        else:
            file_list.append((modified_time, file_path))
    if len(file_list) > keep_num:
        file_list.sort(key = lambda x: -x[0])
        for file_path in (i[1] for i in file_list[keep_num:]):
            os.remove(file_path)
            logger.info(f'clear log file: {file_path}')

logger = set_logger()
clear_logs()

class UI:
    def __init__(self):
        app = QApplication(sys.argv)

        logger.info('isSessionRestored: %s', app.isSessionRestored())
        logger.info('sessionId: %s', app.sessionId())
        logger.info('sessionKey: %s', app.sessionKey())

        self.frame = Frame()
        self.frame.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    UI()
 