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
import mysql.connector

ui_path = os.path.join(os.path.dirname(os.getcwd()), "gui\\new_gui\\connect to server\\connect_to_server.ui")
Form = uic.loadUiType(ui_path)[0]

class ConnectToServer(QMainWindow, Form):
    def __init__(self,dbname="clinic",partner_window=None):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)
        self.dbname = dbname
        self.connectToServer.clicked.connect(self._connect_to_server)
        self.partner_window = partner_window
    
    def _connect_to_server(self):
        if self.connectToServer.text() == "disconnect":
            self.connectToServer.setText("connect")
        else:
            try :
                db = mysql.connector.connect(host = self.lineEdit_host_address.text(), user = self.lineEdit_2_user.text(), passwd = self.lineEdit_3_password.text(), db = self.dbname)
                if (db):
                    print ("Connection successful")
                    self.connectToServer.setText("disconnect")
                    if self.partner_window != None:
                        f={
                            "connection":True,
                            "host": self.lineEdit_host_address.text(),
                            "user": self.lineEdit_2_user.text(),
                            "password": self.lineEdit_3_password.text()
                        }
                        self.partner_window.update_server_status(f)     
                    QMessageBox.warning(
                        self, " ", "اتصال به سرور برقرار شد")
   
                else:
                    if self.partner_window != None:
                        f={
                            "connection":False,
                        }
                        self.partner_window.update_server_status(f) 
                    self.connectToServer.setText("connect")
                    QMessageBox.warning(
                    self, " ", "اطلاعات وارد شده صحیح نیست یا سرور قطع است")
            except:
                if self.partner_window != None:
                        f={
                            "connection":False,
                        }
                        self.partner_window.update_server_status(f)
                print("problem occured")
                self.connectToServer.setText("connect")
                QMessageBox.warning(
                    self, " ", "اطلاعات وارد شده صحیح نیست یا سرور قطع است")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = ConnectToServer()
    q.show()
    sys.exit(app.exec_())

