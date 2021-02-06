from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem,QLabel,QBoxLayout
from PyQt5 import QtCore
from PyQt5 import uic
import sys
import os
from PyQt5.QtGui import QPixmap
import datetime
from booking_rc import *
from booking import * 
from patient_info import * 
from doctor_info import * 
from search_patient_records import *
from message import * 
from person_list import * 
from connect_to_server import * 
ui_path = os.path.join(os.path.dirname(os.getcwd()), "gui//core_radio.ui")
Form = uic.loadUiType(ui_path)[0]

class Core_page(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        self.patient_pass_id = "0123456789"
        self.doctor_pass_id = "1234567890" 
        
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

        self.patient_medium = Message(my_pass_id = self.patient_pass_id,patient_or_doctor="patient")
        self.vertic_7.addWidget(self.patient_medium)

        
        self.doctor_medium = Message(my_pass_id = self.doctor_pass_id,patient_or_doctor="doctor")
        self.vertic_8.addWidget(self.doctor_medium)

        self.server_check = ConnectToServer("clinic",self)
        self.vertic_9.addWidget(self.server_check)
    
    def update_server_status(self,input):
        # for key, val in input.iteritems() :
            print(input)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = Core_page()
    q.show()
    sys.exit(app.exec_())

