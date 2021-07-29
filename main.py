import sys
import modules.app_functions
import threading

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from modules.ui_mainwidow import Ui_Form
from pathlib import Path
from modules import *

widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._homeFolder = modules.app_functions.AppFunctions.saveLocation(self)

        global widgets
        widgets = self.ui
        self.widgets = widgets

        widgets.location.clicked.connect(self.click)
        widgets.download.clicked.connect(self.click)

        widgets.location_var.setPlaceholderText(f'{self._homeFolder}')
        widgets.location_var.setText(f'{self._homeFolder}')


    def click(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == 'location':
            filename = QFileDialog()
            filename.setOption(QFileDialog.DontUseNativeDialog)
            filename.setOption(QFileDialog.ShowDirsOnly)
            filename.setFileMode(QFileDialog.Directory)
            filename.setDirectory(self._homeFolder)
            filename.exec()
            widgets.location_var.setText(filename.directory().path())

        if btnName == 'download':
            link = widgets.link_var.text()
            if link:
                widgets.link_var.setText(link)
                downloadFolder = f'{widgets.location_var.text()}/'
                title = modules.app_functions.AppFunctions.getTitle(link)
                widgets.video_title.setText(f'{title}')
            downloader = threading.Thread(target=modules.app_functions.AppFunctions.downloadVideo, args=(link, downloadFolder, self), daemon=True)
            downloader.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
