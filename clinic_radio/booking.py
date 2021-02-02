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


class BookAP(QMainWindow, Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)
        self.select_patient.clicked.connect(self._select_patient)
        self.select_doctor.clicked.connect(self._select_doctor)
        self.book_ap.clicked.connect(self._book_ap)

        self.patient_pass_id = ""
        self.doctor_pass_id = ""

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
            insert_into_table("clinic", "booking", k)
            QMessageBox.warning(
                self, " ", "رزور با موفقیت انجام شد ")
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
