# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\DEMO\Documents\dev\pickLayer\ui_changeDSDialog.ui'
#
# Created: Wed Oct 15 16:28:06 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_changeDataSourceDialog(object):
    def setupUi(self, changeDataSourceDialog):
        changeDataSourceDialog.setObjectName(_fromUtf8("changeDataSourceDialog"))
        changeDataSourceDialog.resize(657, 127)
        self.buttonBox = QtGui.QDialogButtonBox(changeDataSourceDialog)
        self.buttonBox.setGeometry(QtCore.QRect(300, 80, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(changeDataSourceDialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 171, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(changeDataSourceDialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 621, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))

        self.retranslateUi(changeDataSourceDialog)
        QtCore.QMetaObject.connectSlotsByName(changeDataSourceDialog)

    def retranslateUi(self, changeDataSourceDialog):
        changeDataSourceDialog.setWindowTitle(_translate("changeDataSourceDialog", "undoLayerChanges", None))
        self.label.setText(_translate("changeDataSourceDialog", "DATASOURCE:", None))

