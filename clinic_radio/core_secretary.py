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

        self.tabs = [i for i in range(1,8)]
        self.doctor_pass_id = "1234567890" 
        

        self.server_check = ConnectToServer("clinic",self)
        self.vertic_9.addWidget(self.server_check)
         
        self.tabWidget.removeTab( 7 )

        for i in self.tabs:
                self.tabWidget.setTabEnabled(i, False)

    def update_server_status(self,input):
        if(input["connection"]==False):
            print(input)
            for i in self.tabs:
                self.tabWidget.setTabEnabled(i, False)
    
        else:
            input["db_name"] = "clinic"

            for i in self.tabs:
                self.tabWidget.setTabEnabled(i, True)

            self.add_patient = Patient_info(db_info=input)
            self.vertic_1.addWidget(self.add_patient)

            self.search_window = Doctor_info(db_info=input)
            self.vertic_2.addWidget(self.search_window)

            self.patient_List = PersonList(patient_or_doctor="patient",db_info=input)
            self.vertic_3.addWidget(self.patient_List)

            self.booking_an_appointment = BookAP(db_info=input)
            self.vertic_4.addWidget(self.booking_an_appointment)

            self.patient_records = SearchPatientRecords(db_info=input)
            self.vertic_5.addWidget(self.patient_records)

            
            self.patient_List = PersonList(patient_or_doctor="doctor",db_info=input)
            self.vertic_6.addWidget(self.patient_List)

            self.doctor_medium = Message(my_pass_id = self.doctor_pass_id,patient_or_doctor="doctor",db_info=input)
            self.vertic_8.addWidget(self.doctor_medium)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = Core_page()
    q.show()
    sys.exit(app.exec_())

