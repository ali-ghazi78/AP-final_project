from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem,QLabel,QBoxLayout
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import sys
import os
from PyQt5.QtGui import QPixmap
import datetime
import icon_rc
from booking import * 
from patient_info import * 
from doctor_info import * 
from search_patient_records import *
from person_list import * 
ui_path = os.path.join(os.path.dirname(os.getcwd()), "gui//core_radio.ui")
Form = uic.loadUiType(ui_path)[0]



class Core_page(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        self.add_patient = Patient_info()
        self.vertic_1.addWidget(self.add_patient)

        self.search_window = Doctor_info()
        self.vertic_2.addWidget(self.search_window)

        self.patient_List = PersonList(patient_or_doctor="patient")
        self.vertic_3.addWidget(self.patient_List)

        self.booking_an_appointment = BookAP()
        self.vertic_4.addWidget(self.booking_an_appointment)

        self.patient_records = SearchPatientRecords()
        self.vertic_5.addWidget(self.patient_records)

        
        self.patient_List = PersonList(patient_or_doctor="doctor")
        self.vertic_6.addWidget(self.patient_List)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = Core_page()
    q.show()
    sys.exit(app.exec_())

