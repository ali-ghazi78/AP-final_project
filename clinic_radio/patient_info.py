from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QLabel, QBoxLayout
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIntValidator
from sql_connector2 import *
import sys
import os
from PyQt5.QtGui import QPixmap
# from save_image import *
import datetime
from booking_rc import *
from image_connector import * 
ui_path = os.path.join(os.path.dirname(os.getcwd()),
                       "gui\\new_gui\\patient_info.ui")
Form = uic.loadUiType(ui_path)[0]

user_name = "ali"
password = "root"
my_host = "127.0.0.1"


class Patient_info(QMainWindow, Form):
    def __init__(self,db_info=None):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        if db_info!=None:
            self.c = SqlConnector(db_info["user"],db_info["password"],db_info["host"],db_info["db_name"])

        self.add_record.clicked.connect(self._add_record)
        self.add_image.clicked.connect(self._import_image)
        self.image_path = ""

        self.input_record_fields = [
            self.first_name, self.last_name, self.father_name, self.pass_id, self.birth_date, self.phone_number, self.address]
        
        self.input_record_fields_obligatory = [self.first_name, self.last_name, self.father_name, self.pass_id,self.password]
        
        self.onlyInt = QIntValidator()
        self.pass_id.setValidator(self.onlyInt)


    def _import_image(self):
        self.image_path = ""
        fname = QFileDialog.getOpenFileName(
            None, "Window name", "", "Image files (*.jpg *.png *.jpeg)")

        if(len(fname[0]) > 2):
            im = QPixmap(fname[0])
            im = im.scaledToHeight(500)
            im = im.scaledToWidth(800)
            self.ImageBox.setPixmap(im)
            self.image_path = fname[0]

    def _add_record(self):
        self._check_valid_input()

    def _check_valid_input(self):
        problemic_input = False
        for i in self.input_record_fields_obligatory:
            if len(i.text()) == 0 or len(self.pass_id.text())!=10  : 
                if(len(self.pass_id.text())!=10):
                    self.pass_id.setStyleSheet("color: red;")
                else:
                    i.setStyleSheet("color: red;")
                problemic_input = True
                break
            else:
                problemic_input = False
                i.setStyleSheet("color: black;")



        if problemic_input:
            QMessageBox.warning(
                self, " ", "لطفا فیلد  قرمز شده را تکمیل کنید ")
        else:
            k = {
                "pass_id": self.pass_id.text()
            }
            if(self.c.check_if_exist("clinic", "patient_info",k) ==False):
                my_dict = {}
                for i in self.input_record_fields:
                    obj_name = i.objectName()
                    if(obj_name=="address"):
                        my_dict[obj_name] = (i.toPlainText())
                    else:
                        my_dict[obj_name] = (i.text())
                
                my_dict2 = {
                    "username":self.pass_id.text(),
                    "password":self.password.text()
                }

                self.c.insert_into_table("clinic", "patient_info",my_dict)
                self.c.insert_into_table("clinic", "username_password",my_dict2)

                QMessageBox.warning(self, " ", "دیتا اضافه شد ")
                
                if(len(self.image_path) > 2 ):
                    img = convertToBinaryData(self.image_path)
                    prop = {
                        "pass_id":self.pass_id.text(),
                    }
                    imag_k = {
                        "image": img
                    }
                    self.c.edit_record("clinic", "patient_info",prop, imag_k )


            else:
                QMessageBox.warning(self, " ", "این کد ملی  قبلا ثبت شده است ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = Patient_info()
    q.show()
    sys.exit(app.exec_())

