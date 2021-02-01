from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QLabel, QBoxLayout
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector2 import *
import sys
import os
from PyQt5.QtGui import QPixmap
# from save_image import *
import datetime
from booking_rc import *

ui_path = os.path.join(os.path.dirname(os.getcwd()),
                       "gui\\new_gui\\booking\\booking_2.ui")
Form = uic.loadUiType(ui_path)[0]



class BookAP(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = BookAP()
    q.show()
    sys.exit(app.exec_())

