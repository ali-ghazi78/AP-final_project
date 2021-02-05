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
import icon_rc
from radio_search import * 
from radio_add import * 
from booking import * 
ui_path = os.path.join(os.getcwd(), "gui/core_radio.ui")
Form = uic.loadUiType(ui_path)[0]



class Core_page(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        self.add_window = RadioADD()
        self.vertic_1.addWidget(self.add_window)

        self.search_window = RadioSearch()
        self.vertic_2.addWidget(self.search_window)

        self.all_booking = Booking()
        self.vertic_4.addWidget(self.all_booking)

        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = Core_page()
    q.show()
    sys.exit(app.exec_())

