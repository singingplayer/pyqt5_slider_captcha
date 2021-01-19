import sys
import traceback
import random
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
            self.resize(300, 220)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("滑动验证码")

            # 随即图片
            width = random.randrange(300, 400, 2)
            height = width // 2
            url = f"http://placekitten.com/{width}/{height}"
            logging.debug(f"captcha image url: {url}")

            self.label = QLabel("123")
            # self.label.setStyleSheet("color: blue")
            try:
                image_data = None#requests.get(url).content
            except:
                image_data = None
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.label.setPixmap(pixmap)
            self.label.setStyleSheet(""" """)

            self.slider = QSlider(Qt.Horizontal)
            self.slider.setStyleSheet(""" """)

            self.vbox = QVBoxLayout(self)
            self.vbox.addWidget(self.label)
            self.vbox.addWidget(self.slider)


        except:
            traceback.print_exc()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = SliderCaptchaDialog()
    main.show()
    sys.exit(app.exec_())
