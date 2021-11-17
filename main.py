
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QThread, QThreadPool, QRunnable, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage

import threading
import time
from ui import Ui_Dialog
import sys
import cv2
import platform

class RenderCamera(QObject):
    finished = pyqtSignal()
    def __init__(self, capture, label):
        super().__init__()
        self.label = label
        self.capture = capture

    def run(self):
        while self.capture.isOpened():
            ret, frame = self.capture.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, channel = frame.shape
            bytesPerLine = channel * w
            #qImg = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888).scaled(self.label.width() - 15, self.label.height() - 15)
            #print(self.label.width())
            qImg = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888).scaledToHeight(self.label.height() - 10)
            self.label.setPixmap(QPixmap(qImg))
            time.sleep(400)

        self.finished.emit()

class Application(QtWidgets.QDialog):
    def __init__(self):
        super(Application, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)
        self.ui.groupBox.setLayout(self.ui.horizontalLayout)
        self.workers = []
        self.threads = []
        self.count = 1
        self.capture = []
        self.label = [self.ui.cam1, self.ui.cam2, self.ui.cam3, self.ui.cam4, self.ui.cam5, self.ui.cam6, self.ui.cam7, self.ui.cam8]
        self.capture.append(cv2.VideoCapture('rtsp://jewell:Jennydog14@jewellfamily.ddns.net/stream1')
        self.capture.append(cv2.VideoCapture('rtsp://jewell:Jennydog14@jewellfamily.ddns.net/stream2')
    def readyPlay(self):
        for index in range(self.count):
            self.capture.append(cv2.VideoCapture('rtsp://jewell:Jennydog14@jewellfamily.ddns.net/stream1'))
            self.threads.append(QThread())
            self.workers.append(RenderCamera(self.capture[index], self.label[index]))
 
            self.workers[index].moveToThread(self.threads[index])
            self.threads[index].started.connect(self.workers[index].run)
            self.workers[index].finished.connect(self.workers[index].deleteLater)
            self.threads[index].finished.connect(self.threads[index].deleteLater)
            self.threads[index].start()

            # self.mediaplayer.append(self.instance.media_player_new())
            # self.media.append(self.instance.media_new('rtsp://jewell:Jennydog14@jewellfamily.ddns.net/stream1'))
 
            # self.mediaplayer[index].set_media(self.media[index])
            # self.media[index].parse()
            # print(self.media[index].get_meta(0))
            # if platform.system() == "Linux": # for Linux using the X Server
            #     self.mediaplayer[index].set_xwindow(int(self.label[index].winId()))
            # elif platform.system() == "Windows": # for Windows
            #     self.mediaplayer[index].set_hwnd(int(self.label[index].winId()))
            # elif platform.system() == "Darwin": # for MacOS
            #     self.mediaplayer[index].set_nsobject(int(self.label[index].winId()))
            # self.mediaplayer[index].play()

    def startPlay(self):
        pass        

def main():

    app = QtWidgets.QApplication(sys.argv)
    mainDlg = Application()

    mainDlg.showFullScreen()
    mainDlg.readyPlay()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()



