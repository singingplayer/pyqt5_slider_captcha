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

class MySlider(QSlider):
    def __init__(self, orientation, parent=None):
        super(MySlider, self).__init__(orientation, parent)
        self.setFixedHeight(40)
        self.setMaximum(100)

        self.label = QLabel("向右滑动滑块验证", self)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.label.hide()

    def mouseMoveEvent(self, event):
        value = (event.pos().x() - self.x()) / (self.width() - self.x()) * 100
        self.setValue(value)

    def mouseReleaseEvent(self, event):
        pass
        # self.setValue(0)
        # self.label.show()

class SliderCaptchaDialog(QDialog):
    def __init__(self):
        try:
            super(SliderCaptchaDialog, self).__init__()
            # self.resize(300, 220)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("滑动验证码")

            # 随即图片
            width = random.randrange(300, 400, 2)
            height = width // 2
            url = f"http://placekitten.com/{width}/{height}"
            logging.debug(f"captcha image url: {url}")

            self.label_puzzle = QLabel("123")
            # try:
            #     image_data = requests.get(url).content
            # except:
            #     image_data = None
            # pixmap = QPixmap()
            # pixmap.loadFromData(image_data)
            # self.label_puzzle.setPixmap(pixmap)
            # self.label_puzzle.setScaledContents(True)

            self.slider = MySlider(Qt.Horizontal)

            self.vbox = QVBoxLayout(self)
            self.vbox.addWidget(self.label_puzzle)
            self.vbox.addWidget(self.slider)

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
	background:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
	border:2px solid #5C5C5C;
	border-radius:5px;
	width:18px;
	
	/* 滑块上下边与滑道重合 */
	margin:-2px 0;
}
      """)

        except:
            traceback.print_exc()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = SliderCaptchaDialog()
    main.show()
    sys.exit(app.exec_())
