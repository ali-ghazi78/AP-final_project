from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem,QLabel
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector_radio import *
import sys
import os
from PyQt5.QtGui import QPixmap
from save_image import *

ui_path = os.path.join(os.getcwd(), "gui/admin_radio.ui")
Form = uic.loadUiType(ui_path)[0]

class RadioADD(QMainWindow, Form):
    def __init__(self,parent=None):
        QMainWindow.__init__(self)
        Form.__init__(self)
        super(RadioADD, self).__init__(parent)
        self.setupUi(self)

        self.add_record.clicked.connect(self._add_record)

        self.input_record_fields = [
            self.first_name, self.last_name, self.father_name, self.pass_id, self.visit_date]
        self.input_record_fields_text = (self.first_name.text(), self.last_name.text(
        ), self.father_name.text(), self.pass_id.text(), self.visit_date.text())
        self.add_image.clicked.connect(self._import_image)

        self.image_path = ""

    def _import_image(self):
        self.image_path = ""
        fname = QFileDialog.getOpenFileName(
            None, "Window name", "", "Image files (*.jpg *.png *.jpeg)")
        
        self.ImageBox.clear()            
        self.ImageBox.setText("no image loaded \n (optional)")      
        if(len(fname[0])>2):
            im = QPixmap(fname[0])
            im = im.scaledToHeight(500)
            im = im.scaledToWidth(800)
            
            
            self.ImageBox.setPixmap(im)
            self.image_path = fname[0]

    def _add_record(self):
        self._check_valid_input()

    def _check_valid_input(self):
        problemic_input = False
        for i in self.input_record_fields:
            if len(i.text()) == 0:
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
            print(check_if_exist("12","1992-06-20 23:59:59"))
            if(check_if_exist(self.pass_id.text(),self.visit_date.text() ) ==False):
                insert_into_table(self.first_name.text(), self.last_name.text(
                ), self.father_name.text(), self.pass_id.text(), self.visit_date.text(), 0)
                QMessageBox.warning(self, " ", "دیتا اضافه شد ")
                if(len(self.image_path) > 2 ):
                    insertImage(self.image_path, self.pass_id.text(),
                                self.visit_date.text())
                    self.image_path = ""
            else:
                QMessageBox.warning(self, " ", "این بیمار در این ساعت در سیستم قبلا ثبت شده است ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = RadioADD()
    q.show()
    sys.exit(app.exec_())
