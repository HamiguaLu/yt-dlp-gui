# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SettingUI(object):
    def setupUi(self, SettingUI):
        if not SettingUI.objectName():
            SettingUI.setObjectName(u"SettingUI")
        SettingUI.resize(577, 174)
        self.buttonBox = QDialogButtonBox(SettingUI)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(40, 120, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.lineEditDownloadFolder = QLineEdit(SettingUI)
        self.lineEditDownloadFolder.setObjectName(u"lineEditDownloadFolder")
        self.lineEditDownloadFolder.setGeometry(QRect(20, 30, 371, 25))
        self.btn_sel_folder = QPushButton(SettingUI)
        self.btn_sel_folder.setObjectName(u"btn_sel_folder")
        self.btn_sel_folder.setGeometry(QRect(412, 30, 151, 29))
        self.label_info = QLabel(SettingUI)
        self.label_info.setObjectName(u"label_info")
        self.label_info.setGeometry(QRect(70, 80, 361, 20))

        self.retranslateUi(SettingUI)
        self.buttonBox.accepted.connect(SettingUI.accept)
        self.buttonBox.rejected.connect(SettingUI.reject)

        QMetaObject.connectSlotsByName(SettingUI)
    # setupUi

    def retranslateUi(self, SettingUI):
        SettingUI.setWindowTitle(QCoreApplication.translate("SettingUI", u"Please select the download folder", None))
        self.btn_sel_folder.setText(QCoreApplication.translate("SettingUI", u"Browse", None))
        self.label_info.setText("")
    # retranslateUi

