from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem,QLabel
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector_radio import *
import sys
import os
from PyQt5.QtGui import QPixmap
from save_image import *

ui_path = os.path.join(os.getcwd(), "gui/edit_book_radio.ui")
Form = uic.loadUiType(ui_path)[0]

class EditBook(QMainWindow, Form):
    def __init__(self,parent=None):
        QMainWindow.__init__(self)
        Form.__init__(self)
        super(EditBook, self).__init__(parent)
        self.setupUi(self)
         
        self.input_record_fields = [
            self.first_name, self.last_name, self.father_name, self.pass_id, self.visit_date]
        self.input_record_fields_text = (self.first_name.text(), self.last_name.text(
        ), self.father_name.text(), self.pass_id.text(), self.visit_date.text())
        self.add_image.clicked.connect(self._import_image)

        self.image_path = ""
        self._image_done = False
        self.pre_first_name  =  " "
        self.pre_last_name   =  " "
        self.pre_father_name =  " "
        self.pre_pass_id     =  " "
        self.pre_visit_date     =  ""
        
        self.add_record.clicked.connect(self._add_record)



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


    def update_field(self):
        self.first_name.setText( self.pre_first_name)  
        self.last_name.setText( self.pre_last_name)   
        self.father_name.setText( self.pre_father_name)   
        self.pass_id.setText( self.pre_pass_id)     
        self.visit_date.setDateTime(self.pre_visit_date)

        self._image_done = loadImage(self.pre_pass_id, self.pre_visit_date, 0)
        if(self._image_done):
            im = QPixmap("output0.jpg")
            im = im.scaledToHeight(500)
            im = im.scaledToWidth(800)
            self.ImageBox.setPixmap(im)

    
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
            kw = {
                "first_name":self.pre_first_name,
                "last_name": self.pre_last_name,
                "father_name": self.pre_father_name,
                "pass_id": self.pre_pass_id,
                "visit_date": self.pre_visit_date
                }

            remove_from_table(kw)
            insert_into_table(self.first_name.text(), self.last_name.text(), self.father_name.text(), self.pass_id.text(), self.visit_date.text(), 0)
            QMessageBox.warning(self, " ", "دیتا عوض شد ")


            if(len(self.image_path) > 2 ):
                insertImage(self.image_path, self.pass_id.text(),
                            self.visit_date.text())
            elif(self._image_done):
                insertImage("./img/teeth.png", self.pass_id.text(),
                            self.visit_date.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = EditBook()
    q.show()
    sys.exit(app.exec_())
