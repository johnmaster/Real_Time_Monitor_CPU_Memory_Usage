# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import sys
import socket
import threading
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(487, 263)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 0, 261, 51))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(40, 40, 371, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 131, 41))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 90, 181, 41))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(370, 100, 81, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(40, 150, 181, 41))
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(230, 150, 211, 41))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 210, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 210, 121, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(170, 210, 141, 31))
        self.label_5.setObjectName("label_5")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "文件客户端"))
        Form.setWindowIcon(QIcon("C:\\Users\\ThinkPad\\Desktop\\kehu.png"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt;\">接收的文件(放置在E盘下)</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt;\">已接受字节数</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt;\">BYTES</span></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt;\">文件服务器IP地址</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "建立TCP连接"))
        #建立TCP连接按钮与槽函数绑定
        self.pushButton.clicked.connect(self.establish_tcp_link)
        self.pushButton_2.setText(_translate("Form", "中断接收"))
        #建立中断发送与槽函数绑定
        self.pushButton_2.clicked.connect(self.interrupt_link)
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">连接没有建立...</span></p></body></html>"))

    #建立TCP连接的槽函数
    def establish_tcp_link(self):
        _translate = QtCore.QCoreApplication.translate
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.tcp_client_socket = socket.socket()
        self.tcp_client_socket.connect((self.ip_address, 8080))
        print("客户端连接成功")
        #显示IP地址
        self.lineEdit_3.setText(self.tcp_client_socket.getpeername()[0])
        self.label_5.setText(_translate("Form","<html><head/><body><p><span style=\" font-size:14pt;\">连接已经建立...</span></p></body></html>"))
        client_thread = threading.Thread(target=self.produce_data)
        client_thread.start()

    #接收文件名
    def produce_data(self):
        file_name_data = self.tcp_client_socket.recv(1024)
        print(file_name_data)
        file_name = file_name_data.decode()
        file_name = "E:\\" + file_name.split("/")[-1]
        self.lineEdit.setText(file_name)
        #存储数据
        client_thread_1 = threading.Thread(target=self.process_data, args=(file_name,))
        client_thread_1.start()

    #接收文件数据
    def process_data(self, file_name):
        i = 0
        try:
            with open(file_name, 'wb') as file:
                while True:
                    file_data = self.tcp_client_socket.recv(1024)
                    i+=len(file_data)
                    if file_data:
                        file.write(file_data)
                        self.lineEdit_2.setText(str(i))
                        time.sleep(0.0001)
                    else:
                        break
        except Exception as e:
            print("下载异常", e)
        else:
            print(file_name, "下载成功")
        self.tcp_client_socket.close()

    #启动中断连接的线程
    def interrupt_link(self):
        client_thread_2 = threading.Thread(target=self.interrupt_link_1)
        client_thread_2.start()

    #终端连接函数
    def interrupt_link_1(self):
        self.tcp_client_socket.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())