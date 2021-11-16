
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QThread, QThreadPool, QRunnable, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
import rtsp
import threading
import time
from ui import Ui_Dialog
import sys


class RenderCamera(QObject):
    finished = pyqtSignal()
    def __init__(self, client, label):
        super().__init__()
        self.label = label
        self.client = client

    def run(self):
        while True:
            _frame = self.client.read(raw=True)
            h, w, channel = _frame.shape
            print(h)
            bytesPerLine = 3 * w
            qImg = QImage(_frame.data, w, h, bytesPerLine, QImage.Format_RGB888).scaled(self.label.width() - 50, self.label.height() - 50)
            self.label.setPixmap(QPixmap(qImg))
            time.sleep(0.001)

        self.finished.emit()
class Application(QtWidgets.QDialog):
    def __init__(self):
        super(Application, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)
        self.ui.groupBox.setLayout(self.ui.horizontalLayout)
        self.ui.pushButton.clicked.connect(self.startPlay)
        self.count = 8
        self.client = []
        self.workers = []
        self.threads = []
        for index in range(self.count):
            print(index)
            self.client.append(rtsp.Client(rtsp_server_uri='rtsp://jewell:Jennydog14@jewellfamily.ddns.net/stream2'))
            # self.client.append(rtsp.Client(rtsp_server_uri='rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'))
        self.labels = [self.ui.cam1, self.ui.cam2, self.ui.cam3, self.ui.cam4, self.ui.cam5, self.ui.cam6, self.ui.cam7, self.ui.cam8]

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.refreshCamera)
        # self.timer.start(10)
        self.refreshCamera()
        # self.client1 = rtsp.Client(rtsp_server_uri='rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')
        # self.client2 = rtsp.Client(rtsp_server_uri='rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')
        # self.client3 = rtsp.Client(rtsp_server_uri='rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4')

        # rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen02.stream

        # rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream
    def setURL(self):
        pass
    def startPlay(self):
        self.timer.start(40)
    def refreshCamera(self):
        ww = self.ui.cam1.width()
        hh = self.ui.cam1.height()
        
        for index in range(self.count):
            self.threads.append(QThread())
            self.workers.append(RenderCamera(self.client[index], self.labels[index]))
            
            self.workers[index].moveToThread(self.threads[index])
            self.threads[index].started.connect(self.workers[index].run)
            self.workers[index].finished.connect(self.workers[index].deleteLater)
            self.threads[index].finished.connect(self.threads[index].deleteLater)
            self.threads[index].start()
        # pool = QThreadPool.globalInstance()

        # ww = self.ui.cam1.width()
        # hh = self.ui.cam2.height()

        # for index in range(self.count):
        #     runnable = RenderCamera(self.client[index], labels[index], ww, hh)
        #     pool.start(runnable)

        
        # for index in range(self.count):
        #     _image = self.client[index].read(raw=True)
        #     h, w, channel = _image.shape
        #     bytesPerLine = 3 * w
        #     qImg = QImage(_image.data, w, h, bytesPerLine, QImage.Format_RGB888).scaled(ww - 50, hh - 50)
        #     self.labels[index].setPixmap(QPixmap(qImg))

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainDlg = Application()
    mainDlg.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()



