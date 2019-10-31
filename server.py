# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
import socket
import os
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(527, 220)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 0, 121, 31))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(60, 30, 331, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(390, 30, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(70, 80, 111, 41))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 80, 171, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(350, 80, 81, 41))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(70, 130, 101, 51))
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(170, 130, 181, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 180, 121, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(370, 180, 131, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(190, 190, 171, 21))
        self.label_5.setObjectName("label_5")
        #显示本机IP地址
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.lineEdit_3.setText(self.ip_address)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "文件服务器"))
        Form.setWindowIcon(QIcon("C:\\Users\\ThinkPad\\Desktop\\server.png"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt;\">发送的文件</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "选择文件"))
        #将pushButton与选择文件函数进行信号和槽函数绑定
        self.pushButton.clicked.connect(self.select_file)
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt;\">文件大小</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt;\">BYTES</span></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt;\">本机IP</span></p></body></html>"))
        self.pushButton_2.setText(_translate("Form", "开始侦听"))
        #点击开始侦听按钮将开始侦听与槽函数绑定
        self.pushButton_2.clicked.connect(self.start)
        #点击开始发送按钮将开始发送与槽函数绑定
        self.pushButton_3.setText(_translate("Form", "开始发送"))
        self.pushButton_3.clicked.connect(self.process_data_thread)
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">连接还没有建立...</span></p></body></html>"))

    #选择文件函数并显示文件大小
    def select_file(self):
        #选择文件
        self.fname = QFileDialog.getOpenFileName()
        #在第一个LineEdit中显示文件的位置
        self.lineEdit.setText(self.fname[0])
        #在第二个LineEdit中显示选择的文件大小
        self.lineEdit_2.setText(str(os.path.getsize(self.fname[0])))

    def start(self):
        start_1 = threading.Thread(target=self.start_listen)
        start_1.start()

    def start_listen(self):
        self.tcp_server_socket = socket.socket()
        self.tcp_server_socket.bind((self.ip_address, 8080))
        self.tcp_server_socket.listen(3)
        #创建一个线程，用于处理socket连接
        server_thread = threading.Thread(target=self.socket_connect)
        server_thread.start()
        print("开始监听")

    def socket_connect(self):
        _translate = QtCore.QCoreApplication.translate
        try:
            client_socket, client_addr = self.tcp_server_socket.accept()
        except Exception as e:
            print(e)
        self.base_connect = client_socket
        print("客户端：", client_addr, "链接成功")
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">连接已经建立...</span></p></body></html>"))

    def process_data_thread(self):
        server_thread_2 = threading.Thread(target=self.start_send)
        server_thread_2.start()

    def start_send(self):
        #首先发送文件名
        self.base_connect.send(self.fname[0].encode())
        #发送文件
        try:
            with open(self.fname[0], 'rb') as file:
                while True:
                    file_data = file.read(1024)
                    if file_data:
                        self.base_connect.send(file_data)
                    else:
                        print(self.fname[0] + "传输成功")
                        break
        except Exception as e:
            print("传输异常：", e)
        self.base_connect.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())

