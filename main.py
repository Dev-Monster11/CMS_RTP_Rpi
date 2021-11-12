
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
import rtsp
from ui import Ui_Dialog
import sys
class Application(QtWidgets.QDialog):
    def __init__(self):
        super(Application, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)
        self.ui.groupBox.setLayout(self.ui.horizontalLayout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.refreshCamera)
        self.timer.start(40)
        self.client1 = rtsp.Client(rtsp_server_uri='rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')
    def setURL(self):
        pass
    def refreshCamera(self):
        _image1 = self.client1.read(raw=True)
        h, w, channel = _image1.shape
        bytesPerLine = 3 * w
        qImg = QImage(_image1.data, w, h, bytesPerLine, QImage.Format_RGB888)
        # print(qImg)
        self.ui.cam1.setPixmap(QPixmap(qImg))
def main():
    app = QtWidgets.QApplication(sys.argv)
    mainDlg = Application()
    mainDlg.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()



