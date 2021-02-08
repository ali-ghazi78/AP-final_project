from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QLabel, QBoxLayout
from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector2 import *
import sys
import os
from PyQt5.QtGui import QPixmap
import datetime
from booking_rc import *
from image_connector import *
from core_secretary import *
from core_patient import * 
from core_doctor import * 
ui_path = os.path.join(os.path.dirname(os.getcwd()),
                       "gui\\new_gui\\welcome page\\welcome_page.ui")
Form = uic.loadUiType(ui_path)[0]

user_name = "ali"
password = "root"
my_host = "127.0.0.1"

class WelcomePage(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)
        self.btn_doctor.clicked.connect(self._doctor_core)
        self.btn_secretary.clicked.connect(self._secretary_core)
        self.btn_patient.clicked.connect(self._patient_core)

    def _doctor_core(self):
        self.secretary_page = CoreDoctor()
        self.secretary_page.show()
        self.hide()
        print("doctor")
    def _patient_core(self):
        self.secretary_page = CorePatient()
        self.secretary_page.show()
        self.hide()
    def _secretary_core(self):
        self.secretary_page = Core_page()
        self.secretary_page.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = WelcomePage()
    q.show()
    sys.exit(app.exec_())

