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
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class SliderCaptchaDialog(QDialog):
    def __init__(self):
        try:
            super(SliderCaptchaDialog, self).__init__()
            self.setStyleSheet("""
QDialog {background: #ffffff;
}

QPushButton{
    background-image: url(./icons/refresh.png);
    background-repeat: no-repeat;
    border: none;
}
QPushButton:hover{
    background-image: url(./icons/refresh-hover.png);
}


QSlider::groove {
    border: 1px solid #999999;
}

QSlider::handle:horizontal {
    image: url(./icons/arrow.png);
    border:1px solid #999999;
    background: #ffffff;
    width: 45px;
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
            self.setFixedSize(330, 230)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("滑动验证码")

            self.label = QLabel(self)
            self.label.setGeometry(10, 10, 310, 155)

            self.pushButton = QPushButton(self)
            self.pushButton.setGeometry(280, 20, 310, 30)
            self.pushButton.clicked.connect(self.refresh_image)

            self.slider = QSlider(Qt.Horizontal, self)
            self.slider.setGeometry(10, 180, 310, 40)
            self.slider.sliderMoved.connect(self.move_slider)

            self.thread = LoadImageThread()
            self.thread.start()
            self.thread.trigger.connect(self.load_image)

            self.label_puzzle = QLabel(self)
            self.label_puzzle.setGeometry(10, 10, 45, 45)
            self.label_puzzle.raise_()
        except:
            traceback.print_exc()

    def refresh_image(self):
        try:
            self.slider.setValue(0)
            self.label.clear()
            self.label_puzzle.clear()
            self.thread.start()
        except:
            traceback.print_exc()

    def load_image(self, content):
        try:
            # 滑块复位
            self.slider.setValue(0)

            width = self.label.width()
            height = self.label.height()

            block_width = 42
            block_radius = 10

            min_x = block_width + (block_radius * 2) + 15
            max_x = width - block_width - ( block_radius * 2) - 15
            random_x = random.randint(min_x, max_x)

            min_y = block_radius * 2 + 15
            max_y = height - block_width
            random_y = random.randint(min_y, max_y)

            # 背景图
            pixmap = QPixmap()
            pixmap.loadFromData(content)
            self.label.setPixmap(pixmap)

            # 拼图
            pixmap_puzzle = pixmap.copy(QRect(10, 20, 45, 45))
            self.label_puzzle.setPixmap(pixmap_puzzle)
            self.label_puzzle.move(10, random_y)
        except:
            traceback.print_exc()

    def move_slider(self, value):
        x = int(value / self.slider.maximum() * (self.label.width() - 45)) + 10
        y = self.label_puzzle.y()
        self.label_puzzle.move(x, y)


class LoadImageThread(QThread):

    trigger = pyqtSignal(bytes)

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
