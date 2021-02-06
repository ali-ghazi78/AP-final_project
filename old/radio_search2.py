from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem,QLabel
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector_radio import *
import sys
import os
from PyQt5.QtGui import QPixmap
from save_image import *

ui_path = os.path.join(os.getcwd(), "gui/search_radio.ui")
Form = uic.loadUiType(ui_path)[0]

class RadioSearch(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)

        self.all_fields =  [self.first_name, self.last_name, self.father_name, self.pass_id, self.visit_date]
        self.show_all.clicked.connect(self._show_all)
        self.tableWidget.cellClicked.connect(self._show_cell_image)
        self.search.clicked.connect(self._search)
        self.clearField.clicked.connect(self._clearField)


    def _clearField(self):
        for i in self.all_fields:
            if(i.objectName()!="visit_date"):
                i.setText("")
    def _search(self):
        
        my_dict = {}
        for i in self.all_fields:
            if(i.text()!= ""):
                obj_name = i.objectName()
                my_dict[obj_name] = (i.text())
        rec = search_for_record(my_dict)
        self.show_on_table(rec)

    def _show_all(self):
        re = get_all_records()
        self.show_on_table(re)

    def show_on_table(self,re):
        if(len(re)!=0):
            self.tableWidget.setRowCount(len(re))
            self.tableWidget.setColumnCount(len(re[0])+1)
            # self.tableWidget.setItem(1, 1, QTableWidgetItem("TEXT"))
            for i in range(len(re)):
                for j in range(len(re[i])):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(re[i][j])))
            for i in range(len(re)):
                lb = QLabel(self)
                lb.setText('نمایش تصویر')
                self.tableWidget.setCellWidget(i, len(re[0]), lb)
        else:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(6)
            QMessageBox.warning(
                self, " ", "چیزی پیدا نشد ")    
    
    def _show_cell_image(self,row, col):
        if(col==5):# if show image col was called
            pa_id = self.tableWidget.item(row, 3).text() #pass_id
            vi_date = self.tableWidget.item(row, 4).text() #visit_date
            loadImage(pa_id,vi_date)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = RadioSearch()
    q.show()
    sys.exit(app.exec_())
