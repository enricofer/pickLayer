# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'picksnapdialog.ui'
#
# Created: Thu Oct 09 10:07:05 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_pickSnapDialog(object):
    def setupUi(self, pickSnapDialog):
        pickSnapDialog.setObjectName(_fromUtf8("pickSnapDialog"))
        pickSnapDialog.resize(178, 189)
        self.label = QtGui.QLabel(pickSnapDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.snapStateCombo = QtGui.QComboBox(pickSnapDialog)
        self.snapStateCombo.setGeometry(QtCore.QRect(10, 30, 161, 22))
        self.snapStateCombo.setObjectName(_fromUtf8("snapStateCombo"))
        self.snapStateCombo.addItem(_fromUtf8(""))
        self.snapStateCombo.addItem(_fromUtf8(""))
        self.snapModeCombo = QtGui.QComboBox(pickSnapDialog)
        self.snapModeCombo.setGeometry(QtCore.QRect(10, 60, 161, 22))
        self.snapModeCombo.setObjectName(_fromUtf8("snapModeCombo"))
        self.snapModeCombo.addItem(_fromUtf8(""))
        self.snapModeCombo.addItem(_fromUtf8(""))
        self.snapModeCombo.addItem(_fromUtf8(""))
        self.snapUnitsCombo = QtGui.QComboBox(pickSnapDialog)
        self.snapUnitsCombo.setGeometry(QtCore.QRect(10, 90, 161, 22))
        self.snapUnitsCombo.setObjectName(_fromUtf8("snapUnitsCombo"))
        self.snapUnitsCombo.addItem(_fromUtf8(""))
        self.snapUnitsCombo.addItem(_fromUtf8(""))
        self.toleranceCombo = QtGui.QComboBox(pickSnapDialog)
        self.toleranceCombo.setGeometry(QtCore.QRect(10, 120, 161, 22))
        self.toleranceCombo.setEditable(True)
        self.toleranceCombo.setObjectName(_fromUtf8("toleranceCombo"))
        self.toleranceCombo.addItem(_fromUtf8(""))
        self.toleranceCombo.addItem(_fromUtf8(""))
        self.toleranceCombo.addItem(_fromUtf8(""))
        self.toleranceCombo.addItem(_fromUtf8(""))
        self.toleranceCombo.addItem(_fromUtf8(""))
        self.toleranceCombo.addItem(_fromUtf8(""))
        self.buttonOkNo = QtGui.QDialogButtonBox(pickSnapDialog)
        self.buttonOkNo.setGeometry(QtCore.QRect(0, 150, 171, 32))
        self.buttonOkNo.setOrientation(QtCore.Qt.Horizontal)
        self.buttonOkNo.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonOkNo.setObjectName(_fromUtf8("buttonOkNo"))

        self.retranslateUi(pickSnapDialog)
        QtCore.QMetaObject.connectSlotsByName(pickSnapDialog)

    def retranslateUi(self, pickSnapDialog):
        pickSnapDialog.setWindowTitle(_translate("pickSnapDialog", "Dialog", None))
        self.label.setText(_translate("pickSnapDialog", "TextLabel", None))
        self.snapStateCombo.setItemText(0, _translate("pickSnapDialog", "enabled", None))
        self.snapStateCombo.setItemText(1, _translate("pickSnapDialog", "disabled", None))
        self.snapModeCombo.setItemText(0, _translate("pickSnapDialog", "to vertex", None))
        self.snapModeCombo.setItemText(1, _translate("pickSnapDialog", "to segment", None))
        self.snapModeCombo.setItemText(2, _translate("pickSnapDialog", "to vertex and segment", None))
        self.snapUnitsCombo.setItemText(0, _translate("pickSnapDialog", "map units", None))
        self.snapUnitsCombo.setItemText(1, _translate("pickSnapDialog", "pixels", None))
        self.toleranceCombo.setItemText(0, _translate("pickSnapDialog", "0.00", None))
        self.toleranceCombo.setItemText(1, _translate("pickSnapDialog", "2.50", None))
        self.toleranceCombo.setItemText(2, _translate("pickSnapDialog", "5.00", None))
        self.toleranceCombo.setItemText(3, _translate("pickSnapDialog", "10.0", None))
        self.toleranceCombo.setItemText(4, _translate("pickSnapDialog", "20.0", None))
        self.toleranceCombo.setItemText(5, _translate("pickSnapDialog", "50.0", None))

