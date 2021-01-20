import sys
import traceback
import random
import time
import logging

import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# 设置日志级别
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class SliderCaptchaDialog(QDialog):
    def __init__(self):
        try:
            super(SliderCaptchaDialog, self).__init__()
            self.resize(380, 220)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("滑动验证码")

            self.label_puzzle = QLabel()
            self.thread_load_image = LoadImageThread()  # 创建线程
            self.thread_load_image.start()
            self.thread_load_image.trigger.connect(self.load_image)

            self.slider = QSlider(Qt.Horizontal)
            self.slider.setFixedHeight(40)

            self.vbox = QVBoxLayout(self)
            self.vbox.addWidget(self.label_puzzle)
            self.vbox.addWidget(self.slider)
            self.vbox.setStretch(0, 1)
            self.vbox.setStretch(1, 0)

            self.setStyleSheet("""
QDialog {
    background: #ffffff;
}

QLabel {
}

QSlider::groove {
    border: 1px solid #999999;
    height: 30px;
}

QSlider::handle:horizontal {
    image: url(./icons/arrow.png);
    border:1px solid #999999;
    background: #ffffff;
    width:30px;
    margin: -1px ;
}

QSlider::handle:hover {
    image: url(./icons/arrow-hover.png);
    border:1px solid #999999;
    background: #1991FA;
}

QSlider::add-page:horizontal {
}

QSlider::sub-page:horizontal {
    border: 1px solid  #1991FA;
    background: #D1E9FE;
}
      """)

        except:
            traceback.print_exc()

    def load_image(self, content):
        try:
            pixmap = QPixmap()
            pixmap.loadFromData(content)
            pixmap = pixmap.scaled(self.label_puzzle.size())
            self.label_puzzle.setPixmap(pixmap)
            self.label_puzzle.setScaledContents(True)
        except:
            traceback.print_exc()

class LoadImageThread(QThread):

    trigger =pyqtSignal(bytes)

    def __init__(self):
        super(LoadImageThread, self).__init__()

    def run(self):
        width = random.randrange(300, 400, 2)
        height = width // 2
        url = f"http://placekitten.com/{width}/{height}"
        logging.debug(f"captcha image url: {url}")

        try:
            image_data = requests.get(url).content
        except:
            image_data = None
        self.trigger.emit(image_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = SliderCaptchaDialog()
    main.show()
    sys.exit(app.exec_())
