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

class CoreDoctor(QMainWindow, Form):
    def __init__(self,doctor_pass_id):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        self.doctor_pass_id = doctor_pass_id
        self.doctor_medium = empty()

        self.server_check = ConnectToServer("clinic",self)
        self.vertic_9.addWidget(self.server_check)
    

        self.tabWidget.removeTab( 1 )
        self.tabWidget.removeTab( 1 )
        self.tabWidget.removeTab( 3 )
        self.tabWidget.removeTab( 3)
        self.tabWidget.removeTab( 3 )

        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setTabEnabled(3, False)
        self.init = True

    def update_server_status(self,input,live_update=False):
        if(input["connection"]==False):
            print(input)
            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget.setTabEnabled(2, False)
            self.tabWidget.setTabEnabled(3, False)
            self.doctor_medium.stop()
            

        elif live_update==False:
            input["db_name"] = "clinic"
            self.doctor_pass_id = input["user_username"]

            if self.init:
                self.init = False
                self.booking_an_appointment = BookAP(db_info = input)
                self.vertic_4.addWidget(self.booking_an_appointment)

                self.patient_records = SearchPatientRecords(db_info=input)
                self.vertic_5.addWidget(self.patient_records)

                self.doctor_medium = Message(my_pass_id = self.doctor_pass_id,patient_or_doctor="doctor",db_info=input)
                self.vertic_8.addWidget(self.doctor_medium)

            self.doctor_medium.start()

            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setTabEnabled(2, True)
            self.tabWidget.setTabEnabled(3, True)
            
class empty():
    def __init__(self):
        pass
    def stop(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = CoreDoctor(doctor_pass_id="1234567890")
    q.show()
    sys.exit(app.exec_())

