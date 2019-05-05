# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_rda.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1101, 381))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_rtm = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_rtm.setMinimumSize(QtCore.QSize(300, 300))
        self.label_rtm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_rtm.setObjectName("label_rtm")
        self.horizontalLayout.addWidget(self.label_rtm)
        self.label_dtm = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dtm.setMinimumSize(QtCore.QSize(300, 300))
        self.label_dtm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dtm.setObjectName("label_dtm")
        self.horizontalLayout.addWidget(self.label_dtm)
        self.label_atm = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_atm.setMinimumSize(QtCore.QSize(300, 300))
        self.label_atm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_atm.setObjectName("label_atm")
        self.horizontalLayout.addWidget(self.label_atm)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.RTM = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.RTM.setMinimumSize(QtCore.QSize(300, 10))
        self.RTM.setAlignment(QtCore.Qt.AlignCenter)
        self.RTM.setObjectName("RTM")
        self.horizontalLayout_2.addWidget(self.RTM)
        self.DTM = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.DTM.setMinimumSize(QtCore.QSize(300, 10))
        self.DTM.setAlignment(QtCore.Qt.AlignCenter)
        self.DTM.setObjectName("DTM")
        self.horizontalLayout_2.addWidget(self.DTM)
        self.ATM = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ATM.setMinimumSize(QtCore.QSize(300, 10))
        self.ATM.setAlignment(QtCore.Qt.AlignCenter)
        self.ATM.setObjectName("ATM")
        self.horizontalLayout_2.addWidget(self.ATM)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(460, 390, 181, 51))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_rtm.setText(_translate("Form", "label_rtm"))
        self.label_dtm.setText(_translate("Form", "label_dtm"))
        self.label_atm.setText(_translate("Form", "label_atm"))
        self.RTM.setText(_translate("Form", "TextLabel"))
        self.DTM.setText(_translate("Form", "TextLabel"))
        self.ATM.setText(_translate("Form", "TextLabel"))
        self.pushButton.setText(_translate("Form", "PushButton"))

