# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1185, 713)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(40, 40, 1111, 121))
        self.lineEditURL = QLineEdit(self.groupBox)
        self.lineEditURL.setObjectName(u"lineEditURL")
        self.lineEditURL.setGeometry(QRect(40, 50, 531, 25))
        self.btnAddJob = QPushButton(self.groupBox)
        self.btnAddJob.setObjectName(u"btnAddJob")
        self.btnAddJob.setGeometry(QRect(650, 50, 171, 29))
        self.btnSetting = QPushButton(self.groupBox)
        self.btnSetting.setObjectName(u"btnSetting")
        self.btnSetting.setGeometry(QRect(902, 50, 161, 29))
        self.label_info = QLabel(self.groupBox)
        self.label_info.setObjectName(u"label_info")
        self.label_info.setGeometry(QRect(40, 90, 531, 20))
        self.downloadJobList = QTableWidget(self.centralwidget)
        self.downloadJobList.setObjectName(u"downloadJobList")
        self.downloadJobList.setGeometry(QRect(40, 220, 1111, 491))
        self.label_info_2 = QLabel(self.centralwidget)
        self.label_info_2.setObjectName(u"label_info_2")
        self.label_info_2.setGeometry(QRect(40, 180, 531, 20))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1185, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Video Downloader", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Add Job", None))
        self.btnAddJob.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.btnSetting.setText(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.label_info.setText("")
        self.label_info_2.setText(QCoreApplication.translate("MainWindow", u"Right click on task for more actions", None))
    # retranslateUi

