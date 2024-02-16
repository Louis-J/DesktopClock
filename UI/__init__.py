import sys
import time
from .Frame import Frame
from PySide6.QtWidgets import QApplication
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(f'logs/{int(time.time())}.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

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
 