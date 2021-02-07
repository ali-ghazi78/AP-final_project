from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QLabel
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector2 import *
import sys
import os
from PyQt5.QtGui import QPixmap
from booking_rc import *
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from image_connector import * 

ui_path = os.path.join(os.path.dirname(os.getcwd()),
                       "gui\\new_gui\\search_patient\\search_patient.ui")
Form = uic.loadUiType(ui_path)[0]

user_name = "ali"
password = "root"
my_host = "127.0.0.1"

class SearchPatientRecords(QMainWindow, Form):
    def __init__(self,individual=None,db_info=None):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        self.all_fields = [self.first_name,
                           self.last_name, self.father_name, self.pass_id]
        self.show_all.clicked.connect(self._show_all)
        self.search.clicked.connect(self._search)
        self.clearField.clicked.connect(self._clearField)
        self.tableWidget.cellClicked.connect(self._table_clicked)
        self.tableWidget.verticalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.refresh.clicked.connect(self._search)
        self.latest_search = []
        if db_info != None:
            print(db_info)
            self.c = SqlConnector(db_info["user"],db_info["password"],db_info["host"],db_info["db_name"])


        self.individual = individual
        if self.individual != None:
            self.pass_id.setText(self.individual)
            self._search()
            self.widgetlayout.hide()

    def _table_clicked(self,row,col):
        image_col  = [6,7,8]
        im_dict = {
            6:"image",
            7:"prescription",
            8:"radiology_image"
        }
        if(col in image_col) and self.editCheckbox.isChecked()!=True:
            if self.latest_search[row][col] != None :
                write_file(self.latest_search[row][col],"temp.jpg",1)
        elif col in image_col and col:
            self.image_path = ""
            fname = QFileDialog.getOpenFileName(
                None, "Window name", "", "Image files (*.jpg *.png *.jpeg)")
            if(len(fname[0]) > 2):
                image_path = fname[0]

                img = convertToBinaryData(image_path)
                prop_info = {
                    "pass_id":self.latest_search[row][3],
                }
                prop_book = {
                    "patient_pass_id":self.latest_search[row][3],
                    "visit_date": self.latest_search[row][4]
                }
                key = im_dict[col]
                imag_k = {
                    key: img
                }
                if(key=="image"):
                    self.c.edit_record("clinic", "patient_info",prop_info, imag_k )
                else:
                    self.c.edit_record("clinic", "booking",prop_book, imag_k )
                self._search()

        self._search()

    def _clearField(self):
        for i in self.all_fields:
            i.setText("")

    def _search(self):
        my_dict = {}
        for i in self.all_fields:
            if(i.text() != ""):
                obj_name = "p."+i.objectName()
                my_dict[obj_name] = (i.text())

        col = ["p.first_name", "p.last_name","p.father_name","p.pass_id", "b.visit_date","d.last_name","p.image","b.prescription","b.radiology_image"]
        rec  = self.c.search_with_join_where("clinic",["booking as b","patient_info as p","doctor_info as d"],["p.pass_id = b.patient_pass_id","d.pass_id = b.doctor_pass_id"],col,my_dict)
        self.latest_search  = rec.copy()
        self.show_on_table(rec,[6,7,8,])

    def _show_all(self):
        col = ["p.first_name", "p.last_name","p.father_name","p.pass_id", "b.visit_date","d.last_name","p.image","b.prescription","b.radiology_image"]
        re  = self.c.search_with_join("clinic",["booking as b","patient_info as p","doctor_info as d"],["p.pass_id = b.patient_pass_id","d.pass_id = b.doctor_pass_id"],col)
        self.show_on_table(re,[6,7,8,])
        self.latest_search  = re.copy()


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
    q = SearchPatientRecords()
    q.show()
    sys.exit(app.exec_())
