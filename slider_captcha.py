import sys
import traceback
import random
import time
import logging
import urllib.request

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import icons_rc
# 设置日志级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class SliderCaptchaDialog(QDialog):
    def __init__(self):
        try:
            super(SliderCaptchaDialog, self).__init__()
            # 是否验证通过
            self.pass_verify = False
            # 样式
            self.setStyleSheet("""
QDialog {background: #ffffff;
}

QPushButton{
    background-image: url(:/icons/refresh.png);
    background-repeat: no-repeat;
    border: none;
}
QPushButton:hover{
    background-image: url(:/icons/refresh-hover.png);
}


QSlider::groove {
    border: 1px solid #999999;
}

QSlider::handle:horizontal {
    image: url(:/icons/arrow.png);
    border:1px solid #999999;
    background: #ffffff;
    width: 45px;
    margin: -1px ;
}

QSlider::handle:hover {
    image: url(:/icons/arrow-hover.png);
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

            # 左上角
            self.left_x = 10
            self.left_y = 10

            # 背景图
            self.width = 310
            self.height = 155
            self.label_background = QLabel(self)
            self.label_background.setGeometry(self.left_x, self.left_y, self.width, self.height)

            # 前景图
            self.side = 45
            self.radius = 8
            self.label_foreground = QLabel(self)
            self.label_foreground.setGeometry(self.left_x, self.left_y, self.side + self.radius * 2, self.side + self.radius * 2)
            self.label_foreground.raise_()
            
            # 拼图位置取值范围
            self.min_x = self.side + self.radius * 2
            self.max_x = self.width - self.side - (self.radius * 2)

            self.min_y = self.side + self.radius * 2 
            self.max_y = self.height - self.side - (self.radius * 2)

            # 刷新按钮
            self.pushButton = QPushButton(self)
            self.pushButton.setGeometry(280, 20, 310, 30)
            self.pushButton.clicked.connect(self.refresh_captcha)

            # 滑块
            self.slider = QSlider(Qt.Horizontal, self)
            self.slider.setEnabled(False)
            self.slider.setGeometry(10, 180, 310, 40)
            self.slider.sliderMoved.connect(self.move_slider)
            self.slider.sliderReleased.connect(self.release_slider)

            # 图片加载线程
            self.thread = LoadImageThread()
            self.thread.trigger.connect(self.load_image)
            self.thread.start()
        except:
            traceback.print_exc()

    def reset_slider(self):
        """滑块重置"""
        try:
            self.slider.setValue(0)
            self.slider.setStyleSheet("QSlider::handle:horizontal {image: url(:/icons/arrow.png); background: #ffffff;} QSlider::handle:hover {image: url(:/icons/arrow-hover.png);background: #1991FA;}")

            self.label_foreground.move(self.left_x, self.left_y + self.dst_y - self.radius * 2)
        except:
            traceback.print_exc()

    def reset_label(self):
        """图片重置"""
        try:
            self.slider.setEnabled(False)
            self.label_background.clear()
            self.label_foreground.clear()
        except:
            traceback.print_exc()

    def refresh_captcha(self):
        """刷新验证码"""
        try:
            self.reset_slider()
            self.reset_label()
            self.thread.start()
        except:
            traceback.print_exc()

    def load_image(self, content):
        """加载图片"""
        try:
            self.dst_x = random.randint(self.min_x, self.max_x)
            self.dst_y = random.randint(self.min_y, self.max_y)
            logging.debug(f"dst_x:{self.dst_x}, dst_y:{self.dst_y}")

            pixmap = QPixmap()
            pixmap.loadFromData(content)
            pixmap = pixmap.scaled(self.width, self.height)

            # 背景图
            pixmap_background = pixmap.copy()
            painter = QPainter(pixmap_background)
            painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            painter.drawRect(QRect(self.dst_x, self.dst_y, self.side, self.side))
            painter.drawEllipse(self.dst_x + self.side, self.dst_y + self.side//2 - self.radius, self.radius * 2, self.radius * 2)
            painter.drawEllipse(self.dst_x + self.side // 2 - self.radius, self.dst_y - self.radius*2, self.radius * 2, self.radius * 2)
            painter.end()

            self.label_background.setPixmap(pixmap_background)

            # 前景图
            pixmap_foreground = QPixmap(self.side + self.radius * 2, self.side + self.radius * 2)
            pixmap_foreground.fill(Qt.transparent)
            painter = QPainter(pixmap_foreground)

            path = QPainterPath()
            path.addEllipse(self.side // 2 - self.radius, 0, self.radius * 2, self.radius * 2)
            path.addEllipse(self.side, self.radius * 2 + self.side//2 - self.radius, self.radius * 2, self.radius * 2)
            path.addRect(0, self.radius*2, self.side, self.side)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, self.side + self.radius * 2, self.side + self.radius * 2, pixmap)

            painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
            painter.drawEllipse(self.side // 2 - self.radius, 0, self.radius * 2, self.radius * 2)
            painter.drawEllipse(self.side, self.radius * 2 + self.side//2 - self.radius, self.radius * 2, self.radius * 2)
            painter.drawRect(0, self.radius*2, self.side, self.side)

            painter.end()

            self.label_foreground.setPixmap(pixmap_foreground)
            self.label_foreground.move(self.left_x, self.left_y + self.dst_y - self.radius * 2)

            # 滑块
            self.slider.setEnabled(True)
        except:
            traceback.print_exc()

    def move_slider(self, value):
        """移动滑块"""
        try:
            x = self.left_x + int(value / self.slider.maximum() * (self.width - 45))

            self.label_foreground.move(x, self.left_y + self.dst_y - self.radius * 2)
        except:
            traceback.print_exc()

    def release_slider(self):
        """释放滑块"""
        try:
            if -3 < self.label_foreground.x() - self.dst_x - 10 < 3:
                self.pass_verify = True
                self.slider.setStyleSheet("QSlider::handle:horizontal {image: url(:/icons/right.png); background: #52CCBA;} ")
                QTimer.singleShot(1000, self.refresh_captcha)
            else:
                self.pass_verify = False
                self.slider.setStyleSheet("QSlider::handle:horizontal {image: url(:/icons/wrong.png); background: #f57a7a;}")
                QTimer.singleShot(1000, self.reset_slider)
            print(f"pass {self.pass_verify}")
        except:
            traceback.print_exc()

class LoadImageThread(QThread):

    trigger = pyqtSignal(bytes)

    def __init__(self):
        super(LoadImageThread, self).__init__()

    def run(self):
        url = "https://unsplash.it/400/200?random"
        logging.debug(f"captcha image url: {url}")

        try:
            image_data = urllib.request.urlopen(url).read()
        except:
            image_data = b''
        self.trigger.emit(image_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = SliderCaptchaDialog()
    main.show()
    sys.exit(app.exec_())
