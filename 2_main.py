
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QThread, QThreadPool, QRunnable, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
import rtsp
import threading
import time
from ui import Ui_Dialog
import sys
import vlc
import platform

# class RenderCamera(QObject):
#     finished = pyqtSignal()
#     def __init__(self, client, label):
#         super().__init__()
#         self.label = label
#         self.instance = vlc.Instance()
#         self.media = self.instance.media_nen('rtsp://jewell:Jennydog14@jewellfamily.ddns.net/stream1')
#     def run(self):
#         while True:           
#             h, w, channel = _frame.shape
#             print(h)
#             bytesPerLine = 3 * w

#             self.label.setPixmap(QPixmap(qImg))
#             time.sleep(0.01)

#         self.finished.emit()
class Application(QtWidgets.QDialog):
    def __init__(self):
        super(Application, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)
        self.ui.groupBox.setLayout(self.ui.horizontalLayout)

        self.count = 8
        self.media = []
        self.mediaplayer = []
        self.label = [self.ui.cam1, self.ui.cam2, self.ui.cam3, self.ui.cam4, self.ui.cam5, self.ui.cam6, self.ui.cam7, self.ui.cam8]

    def setInstance(self, instance):
        self.instance = instance
    def readyPlay(self):
        for index in range(self.count):
            self.mediaplayer.append(self.instance.media_player_new())
            self.media.append(self.instance.media_new('rtsp://jewell:Jennydog14@jewellfamily.ddns.net/stream1'))
        
            self.mediaplayer[index].set_media(self.media[index])
            self.media[index].parse()
            print(self.media[index].get_meta(0))
            if platform.system() == "Linux": # for Linux using the X Server
                self.mediaplayer[index].set_xwindow(int(self.label[index].winId()))
            elif platform.system() == "Windows": # for Windows
                self.mediaplayer[index].set_hwnd(int(self.label[index].winId()))
            elif platform.system() == "Darwin": # for MacOS
                self.mediaplayer[index].set_nsobject(int(self.label[index].winId()))
            self.mediaplayer[index].play()

    def startPlay(self):
        pass        

def main():
    instance = vlc.Instance()
    app = QtWidgets.QApplication(sys.argv)
    mainDlg = Application()
    mainDlg.setInstance(instance)
    mainDlg.readyPlay()
    mainDlg.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()



