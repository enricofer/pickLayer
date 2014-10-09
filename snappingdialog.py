# -*- coding: utf-8 -*-
"""
/***************************************************************************
 pickLayerSnappingDialog
                                 A QGIS plugin
 pick layer
                             -------------------
        begin                : 2014-06-16
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Enrico Ferreguti
        email                : enricofer@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


from PyQt4 import QtCore, QtGui, uic
from qgis.core import *
from ui_picksnapdialog import Ui_pickSnapDialog


class trace:

    def __init__(self):
        self.trace = None
        
    def ce(self,string):
        if self.trace:
            print string

class snappingDialog(QtGui.QDialog, Ui_pickSnapDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.tra = trace()
        self.buttonOkNo.accepted.connect(self.saveSnappingOptions)
        self.buttonOkNo.rejected.connect(self.cancelSnappingOptions)

    def cancelSnappingOptions(self):
        self.hide()

    def saveSnappingOptions(self):
        # hide the dialog
        self.hide()
        if self.snapStateCombo.currentIndex() == 0:
            self.enabledList[self.idLayer] = u'enabled'
        else:
            self.enabledList[self.idLayer] = u'disabled'
        if self.snapModeCombo.currentIndex() == 0:
            self.snapToList[self.idLayer] = u'to_vertex'
        elif self.snapModeCombo.currentIndex() == 1:
            self.snapToList[self.idLayer] = u'to_segment'
        else:
            self.snapToList[self.idLayer] = u'to_vertex_and_segment'
        if self.snapModeCombo.currentIndex() == 1:
            self.toleranceUnitList[self.idLayer] = u'1'
        else:
            self.toleranceUnitList[self.idLayer] = u'0'
        self.toleranceList[self.idLayer] = self.toleranceCombo.currentText()
        self.tra.ce(self.layerSnappingList)
        self.tra.ce(self.enabledList)
        self.tra.ce(self.toleranceUnitList)
        self.tra.ce(self.snapToList)
        self.tra.ce(self.toleranceList)
        proj = QgsProject.instance()
        proj.writeEntry("Digitizing", "/LayerSnappingEnabledList", self.layerSnappingList)
        proj.writeEntry("Digitizing", "/LayerSnappingEnabledList", self.enabledList)
        proj.writeEntry("Digitizing", "/LayerSnappingToleranceUnitList", self.toleranceUnitList)
        proj.writeEntry("Digitizing", "/LayerSnapToList", self.snapToList)
        proj.writeEntry("Digitizing", "/LayerSnappingToleranceList", self.toleranceList)
        proj.writeEntry("Digitizing", "/AvoidIntersectionsList", self.avoidIntersectionsList)
        

    def getSnappingOptionsDialog(self,layer):
        self.selectedLayer = layer
        proj = QgsProject.instance()
        self.layerSnappingList = proj.readListEntry("Digitizing", "/LayerSnappingList")[0]
        self.enabledList = proj.readListEntry("Digitizing", "/LayerSnappingEnabledList")[0]
        self.toleranceList = proj.readListEntry("Digitizing", "/LayerSnappingToleranceList")[0]
        self.toleranceUnitList = proj.readListEntry("Digitizing", "/LayerSnappingToleranceUnitList")[0]
        self.snapToList = proj.readListEntry("Digitizing", "/LayerSnapToList")[0]
        self.avoidIntersectionsList = proj.readListEntry("Digitizing", "/AvoidIntersectionsList")[0]
        self.tra.ce(self.layerSnappingList)
        self.tra.ce(self.enabledList)
        self.tra.ce(self.toleranceUnitList)
        self.tra.ce(self.snapToList)
        self.tra.ce(self.toleranceList)
        if not self.selectedLayer.id() in self.layerSnappingList:
            return
            #self.layerSnappingList.append(self.selectedLayer.id())
            #self.enabledList.append(u'disabled')
            #self.toleranceUnitList.append(u'1')
            #self.snapToList.append(u'to_vertex')
            #self.toleranceList.append(u'0.0000')
        self.idLayer = self.layerSnappingList.index(self.selectedLayer.id())
        self.compileSnapForm(self.idLayer)
        self.label.setText(self.selectedLayer.name())
        self.show()

    def compileSnapForm(self,layerIndex):
        if self.enabledList[layerIndex] == u'enabled':
            self.snapStateCombo.setCurrentIndex(0)
        else:
            self.snapStateCombo.setCurrentIndex(1)
        if self.snapToList[layerIndex] == u'to_vertex':
            self.snapModeCombo.setCurrentIndex(0)
        elif self.snapToList[layerIndex] == u'to_segment':
            self.snapModeCombo.setCurrentIndex(1)
        else:
            self.snapModeCombo.setCurrentIndex(2)
        if self.toleranceUnitList[layerIndex] == u'1':
            self.snapModeCombo.setCurrentIndex(1)
        else:
            self.snapModeCombo.setCurrentIndex(0)
        self.toleranceCombo.insertItem(0,self.toleranceList[layerIndex])
        self.toleranceCombo.setCurrentIndex(0)