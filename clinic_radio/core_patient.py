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

class CorePatient(QMainWindow, Form):
    def __init__(self,patient_pass_id):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        self.patient_pass_id = patient_pass_id
    
        self.server_check = ConnectToServer("clinic",self)
        self.vertic_9.addWidget(self.server_check)
            
        self.tabWidget.removeTab( 1 )
        self.tabWidget.removeTab( 1 )
        self.tabWidget.removeTab( 1 )
        self.tabWidget.removeTab( 2 )
        self.tabWidget.removeTab( 2 )
        self.tabWidget.removeTab( 3 )
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)

    def update_server_status(self,input):
        if(input["connection"]==False):
            print(input)
            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget.setTabEnabled(2, False)
        else:
            input["db_name"] = "clinic"

            self.patient_records = SearchPatientRecords(individual=self.patient_pass_id,db_info=input)
            self.vertic_5.addWidget(self.patient_records)

            self.patient_medium = Message(my_pass_id = self.patient_pass_id,patient_or_doctor="patient",db_info = input)
            self.vertic_7.addWidget(self.patient_medium)

            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setTabEnabled(2, True)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = CorePatient(patient_pass_id="0123456789")
    q.show()
    sys.exit(app.exec_())

