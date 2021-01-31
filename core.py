from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem,QLabel,QBoxLayout
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector_radio import *
import sys
import os
from PyQt5.QtGui import QPixmap
from save_image import *
import datetime
from  edit_book_radio import * 

ui_path = os.path.join(os.getcwd(), "gui/booking.ui")
Form = uic.loadUiType(ui_path)[0]



class Booking(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = Booking()
    q.show()
    sys.exit(app.exec_())

