from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QLabel,QHeaderView
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector2 import *
import sys
import os
from PyQt5.QtGui import QPixmap
from booking_rc import *


ui_path = os.path.join(os.path.dirname(os.getcwd()),
                       "gui\\new_gui\\choose_patient\\choose_patient.ui")
Form = uic.loadUiType(ui_path)[0]

user_name = "ali"
password = "root"
my_host = "127.0.0.1"

class ChoosePerson(QMainWindow, Form):
    def __init__(self,partner_window=None,patient_or_doctor=None,db_info=None):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)
        self.partner_window = partner_window
        self.all_fields = [self.first_name,
                           self.last_name, self.father_name, self.pass_id]

        self.all_fields_selected = [self.first_name_s,
                           self.last_name_s, self.father_name_s, self.pass_id_s]
        self.show_all.clicked.connect(self._show_all)
        self.search.clicked.connect(self._search)
        self.clearField.clicked.connect(self._clearField)
        self.tableWidget.cellClicked.connect(self._choose_person)
        self.select_person.clicked.connect(self._select_person)
        self.tableWidget.verticalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.patient_or_doctor = patient_or_doctor
        if db_info!=None:
            self.c = SqlConnector(db_info["user"],db_info["password"],db_info["host"],db_info["db_name"])
        else:
            print("choose patient file error no init database")

    def _select_person(self):
        
        if(self.partner_window!=None):
            f = {
               (self.patient_or_doctor+"_last_name"):self.last_name_s.text(),
                (self.patient_or_doctor+"_pass_id"):self.pass_id_s.text(),
            }
            self.partner_window.update(f)
        self.close()


    def _clearField(self):
        for i in self.all_fields:
            i.setText("")
        for i in self.all_fields_selected:
            i.setText("")
            
    def _search(self):
        my_dict = {}
        for i in self.all_fields:
            if(i.text() != ""):
                obj_name = i.objectName()
                my_dict[obj_name] = (i.text())
        col = ["first_name", "last_name","father_name","pass_id", "image"]
        if(self.patient_or_doctor=="doctor"):
            re = self.c.search_for_record("clinic","doctor_info",my_dict,col)
        else:
            re = self.c.search_for_record("clinic","patient_info",my_dict,col)

        self.show_on_table(re,[4,])
        
    def _show_all(self):

        col = ["first_name", "last_name","father_name","pass_id", "image"]
        if(self.patient_or_doctor=="doctor"):
            re = self.c.search_for_record("clinic","doctor_info",{"first_name":".*"},col)
        else:
            re = self.c.search_for_record("clinic","patient_info",{"first_name":".*"},col)
        self.show_on_table(re,[4,])


    def show_on_table(self, re,image_col):
        if(len(re) != 0):
            self.tableWidget.setRowCount(len(re))
            self.tableWidget.setColumnCount(len(re[0]))
            for i in range(len(re)):
                for j in range(len(re[i])):
                    if j not in image_col:
                        self.tableWidget.setItem(
                            i, j, QTableWidgetItem(str(re[i][j])))
                    else:
                        if re[i][j] != None:
                            self.tableWidget.setCellWidget(
                            i, j, (ImgWidget1(re[i][j],0)))
                        else:
                            self.tableWidget.setCellWidget(
                            i, j, (ImgWidget1(re[i][j],1)))

        else:
            self.tableWidget.setRowCount(0)
            g = self.tableWidget.columnCount()
            self.tableWidget.setColumnCount(g)

            QMessageBox.warning(
                self, " ", "چیزی پیدا نشد ")

    def _choose_person(self,row, col):
        for i in range(len(self.all_fields_selected)):
            self.all_fields_selected[i].setText( self.tableWidget.item(row, i).text())
        

class ImgWidget1(QLabel):
    def __init__(self,data, reset,parent=None):
        super(ImgWidget1, self).__init__(parent)
        if(reset):
            self.clear()
        else:
            mp = QPixmap()
            mp.loadFromData(data)
            mp = mp.scaled(100,100)
            self.setPixmap(mp)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = ChoosePerson()
    q.show()
    sys.exit(app.exec_())
