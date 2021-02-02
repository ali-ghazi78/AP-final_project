from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QLabel
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector2 import *
import sys
import os
from PyQt5.QtGui import QPixmap
from search_patient_rc import *


ui_path = os.path.join(os.path.dirname(os.getcwd()),
                       "gui\\new_gui\\search_patient\\search_patient.ui")
Form = uic.loadUiType(ui_path)[0]


class SearchPatient(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        self.all_fields = [self.first_name,
                           self.last_name, self.father_name, self.pass_id]
        self.show_all.clicked.connect(self._show_all)
        self.search.clicked.connect(self._search)
        self.clearField.clicked.connect(self._clearField)
        # self.tableWidget.cellClicked.connect(self._show_cell_image)

    def _clearField(self):
        for i in self.all_fields:
            i.setText("")

    def _search(self):
        my_dict = {}
        for i in self.all_fields:
            if(i.text() != ""):
                obj_name = "p."+i.objectName()
                my_dict[obj_name] = (i.text())

        col = ["p.first_name", "p.last_name","p.father_name","p.pass_id", "b.visit_date","d.last_name","p.image","b.comments","b.prescription","b.radiology_image"]
        rec  = search_with_join_where("clinic",["booking as b","patient_info as p","doctor_info as d"],["p.pass_id = b.patient_pass_id","d.pass_id = b.doctor_pass_id"],col,my_dict)
        self.show_on_table(rec)

    def _show_all(self):
        col = ["p.first_name", "p.last_name","p.father_name","p.pass_id", "b.visit_date","d.last_name","p.image","b.comments","b.prescription","b.radiology_image"]
        re  = search_with_join("clinic",["booking as b","patient_info as p","doctor_info as d"],["p.pass_id = b.patient_pass_id","d.pass_id = b.doctor_pass_id"],col)
        self.show_on_table(re)


    def show_on_table(self, re):
        if(len(re) != 0):
            self.tableWidget.setRowCount(len(re))
            self.tableWidget.setColumnCount(len(re[0]))
            # self.tableWidget.setItem(1, 1, QTableWidgetItem("TEXT"))
            for i in range(len(re)):
                for j in range(len(re[i])):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(re[i][j])))
            # for i in range(len(re)):
            #     lb = QLabel(self)
            #     lb.setText('نمایش تصویر')
            #     self.tableWidget.setCellWidget(i, len(re[0]), lb)
        else:
            self.tableWidget.setRowCount(0)
            g = self.tableWidget.columnCount()
            self.tableWidget.setColumnCount(g)

            QMessageBox.warning(
                self, " ", "چیزی پیدا نشد ")

    # def _show_cell_image(self,row, col):
    #     if(col==5):# if show image col was called
    #         pa_id = self.tableWidget.item(row, 3).text() #pass_id
    #         vi_date = self.tableWidget.item(row, 4).text() #visit_date
    #         loadImage(pa_id,vi_date)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = SearchPatient()
    q.show()
    sys.exit(app.exec_())
