from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QLabel, QBoxLayout
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from sql_connector2 import *
import sys
import os
from PyQt5.QtGui import QPixmap
from choose_patient import *
import datetime
from booking_rc import *

ui_path = os.path.join(os.path.dirname(os.getcwd()),
                       "gui\\new_gui\\booking\\booking_2.ui")
Form = uic.loadUiType(ui_path)[0]

user_name = "ali"
password = "root"
my_host = "127.0.0.1"


class BookAP(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.con = SqlConnector(user_name,password,my_host)
        self.setupUi(self)
        self.select_patient.clicked.connect(self._select_patient)
        self.select_doctor.clicked.connect(self._select_doctor)
        self.book_ap.clicked.connect(self._book_ap)
        self.visit_date.clicked.connect(self._today_appointment)
        self._today_appointment()
        self.patient_pass_id = ""
        self.doctor_pass_id = ""
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget.cellClicked.connect(self._table_clicked)

    def _table_clicked(self,row,col):
        if col == 4:
            qm = QMessageBox()
            ret = qm.question(self,'', "آیا واقعا میخواهید ویزیت را لغو کنید ؟", qm.Yes | qm.No)
            if ret == qm.Yes:
                datetime = self.tableWidget.item(row,3).text()
                patient_id = self.tableWidget.item(row,1).text()
                k={
                    "patient_pass_id":patient_id,
                    "visit_date":datetime
                }
                self.con.remove_from_table("clinic", "booking", k)
                self._today_appointment()


    def _today_appointment(self):
        date  = self.visit_date.selectedDate().toString("yyyy-MM-dd")
        my_dict = {
            "visit_date": date,
        }
        col = ["p.last_name","p.pass_id","d.last_name","b.visit_date"]
        sort_col="b.visit_date"
        rec  = self.con.search_with_join_where("clinic",["booking as b","patient_info as p","doctor_info as d"],["p.pass_id = b.patient_pass_id","d.pass_id = b.doctor_pass_id"],col,my_dict,sort_col)
        self.show_on_table(rec)

    def show_on_table(self, re,image_col=[]):
        if(len(re) != 0):
            self.tableWidget.setRowCount(len(re))
            self.tableWidget.setColumnCount(len(re[0])+1)
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
            for i in range(len(re)):
                l = QLabel()
                l.setText(" حذف ویزیت")
                self.tableWidget.setCellWidget(
                            i, len(re[i]), l)

        else:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(4)


    def _book_ap(self):
        if(self.patient_pass_id != "" and self.doctor_pass_id !=""):
            time = self.visit_time.time().toString("hh:mm:ss")
            date = self.visit_date.selectedDate().toString("yyyy-MM-dd")
            datetime = date + " " + time
            k = {

                "patient_pass_id": self.patient_pass_id,
                "doctor_pass_id": self.doctor_pass_id,
                "visit_date" : datetime
            }
            self.con.insert_into_table("clinic", "booking", k)
            QMessageBox.warning(
                self, " ", "رزور با موفقیت انجام شد ")
            self._today_appointment()
        else:
          QMessageBox.warning(
                self, " ", "دکتر یا بیمار به درستی انتخاب نشده است ")


    def _select_patient(self):
        self.choose_patient_window = ChoosePerson(self, "patient")
        self.choose_patient_window.show()

    def _select_doctor(self):
        self.choose_doctor_window = ChoosePerson(self, "doctor")
        self.choose_doctor_window.show()

    def update(self, kargs):
        if("patient_last_name" in kargs):
            self.patient_last_name.setText(kargs["patient_last_name"])
            self.patient_pass_id = (kargs["patient_pass_id"])
        elif("doctor_last_name" in kargs):
            self.doctor_last_name.setText(kargs["doctor_last_name"])
            self.doctor_pass_id = (kargs["doctor_pass_id"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = BookAP()
    q.show()
    sys.exit(app.exec_())
