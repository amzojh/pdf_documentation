import os
import sys
import glob

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication


from util.pdf_util import pdfUtil
from util.gui_util import GUIWidget

from logger.deafult_logger import defaultLogger
# 각 File마다 들어갈 문구가 다를 것이기 때문에 엑셀로 입력받는 것도 좋을 듯 


def main():
    app = QApplication(sys.argv)
    gui_class = GUIWidget()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()