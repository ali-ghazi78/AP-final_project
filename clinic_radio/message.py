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
from icon_rc import *
import datetime  
    
receive_style = '''
    width: 300px;
    margin: 50px auto;
    background: #00bfb6;
    padding: 20px;
    text-align: center;
    font-weight: 900;
    color: #fff;
    font-family: arial;
    position:relative; 
'''
send_style = '''
    width: 300px;
    margin: 50px auto;
    background: #e74c3c;
    padding: 20px;
    text-align: center;
    font-weight: 900;
    color: #fff;
    font-family: arial;
    position:relative; 
'''

ui_path = os.path.join(os.path.dirname(os.getcwd()),
                       "gui\\new_gui\\messaging\\message.ui")
Form = uic.loadUiType(ui_path)[0]


class Message(QMainWindow, Form):
    def __init__(self,my_pass_id="1234567890",patient_or_doctor="doctor"):
        QMainWindow.__init__(self)
        Form.__init__(self)
        self.setupUi(self)
        self.chooseReceiver.clicked.connect(self._choose_patient)
        self.send.clicked.connect(self._send)

        self.reciever_pass_id = ""
        
        self.patient_last_name = " "
        self.doctor_last_name  = " "
        self.patient_pass_id = " "
        self.doctor_pass_id = " "
        self.my_pass_id = my_pass_id
        self.all_recieved  = []
        self.all_sent = [] 
        
        self.scroll_bar = self.scrollArea.verticalScrollBar()
        self.scroll_bar.rangeChanged.connect(lambda: self.scroll_bar.setValue(self.scroll_bar.maximum()))

        self.timer = QTimer()
        self.timer.timeout.connect(self._check_new_message)
        self.timer.start(2000)
        
        self.patient_or_doctor = patient_or_doctor
    
    def _check_new_message(self):
        self.timer.stop()
        if  not len(self.reciever_pass_id)<=1 :
            self._init_show()

        k = {
            "receiver_pass_id":self.my_pass_id,
            "seen":"unseen"
        }
        received = search_for_record_exact("clinic", "message_server", k,["sender_pass_id",])
        if(len(received)!=0):
            myset = set(received)
            self.tableWidgetReceive.setRowCount(len(myset))
            self.tableWidgetReceive.setColumnCount(2)
            for id,val in enumerate(myset): 
                k = {
                    "pass_id":val[0], # val 0 is pass_id of patient or doctor 
                }
                last_name1 = search_for_record_exact("clinic", "patient_info", k,["last_name",])             
                last_name2 = search_for_record_exact("clinic", "doctor_info", k,["last_name",])             
                last_name = last_name1
                if(last_name1 == None):
                    last_name =last_name2 # one one these 2 is empty

                self.tableWidgetReceive.setItem(id ,0, QTableWidgetItem(str(last_name[0][0])))
                self.tableWidgetReceive.setItem(id ,1, QTableWidgetItem(str(received.count(val))))
        else:
            self.tableWidgetReceive.setRowCount(0)
            self.tableWidgetReceive.setColumnCount(2)


        self.timer.start(2000)

    def _send(self):
        message = self.plainTextEditMessage.toPlainText()
        current = datetime.datetime.now()
        k = {
            "sender_pass_id":self.my_pass_id,
            "receiver_pass_id":self.reciever_pass_id,
            "text_message":message,
            "message_date":current
        }
        self.plainTextEditMessage.setPlainText(" ")


        if not len(self.reciever_pass_id)<1 :
            insert_into_table("clinic","message_server",k)
            self._init_show()
            
        else:
             QMessageBox.warning(
                self, " ", "گیرنده ای انتخاب نشده است ")


    def _init_show(self):
        for i in reversed(range(self.scrollAreaLayout.count())): 
            self.scrollAreaLayout.itemAt(i).widget().deleteLater()

        kargs_send = {
            "receiver_pass_id" : self.reciever_pass_id,
            "sender_pass_id" : self.my_pass_id    
        }
        kargs_receive = {
            "receiver_pass_id" : self.my_pass_id  ,
            "sender_pass_id" : self.reciever_pass_id     
        }
        
        received = search_for_record_exact("clinic", "message_server", kargs_receive)
        sent = search_for_record_exact("clinic", "message_server", kargs_send)
        # now we see unseed  messages
        k_prop = {
            "sender_pass_id":self.reciever_pass_id,
            "receiver_pass_id":self.my_pass_id,
        }
        k_set = {
            "seen":"seen"
        }
        edit_record("clinic", "message_server", k_prop, k_set)

        all_message = received + sent
        all_message = sorted(all_message,key=lambda x: x[3])
        for i in range(len(all_message)):
            hint = " "
            label = QLabel()
            self.scrollAreaLayout.addWidget(label)
            if(all_message[i][0]==self.my_pass_id ):
                label.setStyleSheet(send_style)
                hint = "ارسال شده"
            else:
                label.setStyleSheet(receive_style)
                hint = "دریافت شده"
            hint += " "+":\n"+all_message[i][3].strftime("%Y/%m/%d , %H:%M") + "\n"
            label.setText(hint+all_message[i][2])

    def _real_time_show(self):
        pass

    def _choose_patient(self):
        person = "patient"
        if (self.patient_or_doctor=="patient"):
            person = "doctor"
        
        self.choose_patient_window = ChoosePerson(self, person)
        self.choose_patient_window.show()


    def update(self,inputs):
        if("patient_last_name" in inputs):
            self.patient_last_name = inputs["patient_last_name"]
            self.patient_pass_id = inputs["patient_pass_id"]
            self.reciever_pass_id  = self.patient_pass_id
            self.last_name.setText("گیرنده" + " : " + self.patient_last_name)

        elif("doctor_last_name" in inputs):
            self.doctor_last_name  = inputs["doctor_last_name"]
            self.doctor_pass_id = inputs["doctor_pass_id"]
            self.reciever_pass_id  = self.doctor_pass_id
            self.last_name.setText("گیرنده" + " : " + self.doctor_last_name)
            
        self._init_show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    q = Message()
    q.show()
    sys.exit(app.exec_())
