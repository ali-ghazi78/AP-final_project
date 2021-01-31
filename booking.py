from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem,QLabel
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector_radio import *
import sys
import os
from PyQt5.QtGui import QPixmap
from save_image import *
import datetime
from  radio_add import * 

ui_path = os.path.join(os.getcwd(), "gui/booking.ui")
Form = uic.loadUiType(ui_path)[0]


class Booking(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)
        self.calendar.clicked[QtCore.QDate].connect(self.showDate)
        self.tableWidget.setColumnWidth(1, 650)
        self.tableWidget.cellClicked.connect(self._show_cell_image)
        self.edit_window = RadioADD(self)
        
    def showDate(self):
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        rec = search_for_booking(date)
        self.show_on_table(rec)
    
    
    def show_on_table(self,re):
        if(len(re)!=0):
            self.tableWidget.setRowCount(len(re))
            self.tableWidget.setColumnCount(len(re[0])+1)
            # self.tableWidget.setItem(1, 1, QTableWidgetItem("TEXT"))
            for i in range(len(re)):
                for j in range(len(re[i])):
                    if(j==4): #visit_date
                        t = str(re[i][j].time())
                        self.tableWidget.setItem(i, j, QTableWidgetItem(t))
                    else:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(re[i][j])))
            for i in range(len(re)):
                lb = QLabel(self)
                image_path = "img//edit.png"

                im = QPixmap(image_path)
                im = im.scaledToHeight(25)
                im = im.scaledToWidth(25)
                lb.setPixmap(im)
                self.tableWidget.setCellWidget(i, len(re[0]), lb)
        
        else:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(6)
            QMessageBox.warning(
                self, " ", "هیچ ویزیتی در این روز ست نشده است. ")    
    
    def _show_cell_image(self,row, col):
        if(col==5):# if show image col was called
            date = self.calendar.selectedDate().toString("yyyy-MM-dd")
            rec = search_for_booking(date)
            pa_id = self.tableWidget.item(row, 3).text() #pass_id
            vi_date = rec[row][4]

            self.edit_window.first_name.setText(rec[row][0])
            self.edit_window.last_name.setText(rec[row][1])
            self.edit_window.father_name.setText(rec[row][2])
            self.edit_window.pass_id.setText(rec[row][3])
            
            self.edit_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = Booking()
    q.show()
    sys.exit(app.exec_())

