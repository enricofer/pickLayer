# -*- coding: utf-8 -*-
"""
/***************************************************************************
 autoSaver
                                 A QGIS plugin
 auto save current project
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QTimer
from PyQt4.QtGui import *
from PyQt4.QtGui import QAction, QIcon, QClipboard
from PyQt4 import uic
from qgis.core import *
from qgis.utils import plugins
from qgis.gui import QgsAttributeDialog
from functools import *
# Initialize Qt resources from file resources.py
#import resources_rc
# Import the code for the dialog
from snappingdialog import snappingDialog
from identifygeometry import IdentifyGeometry
from setdatasource import setDataSource
import os.path

def stringToPythonNames(string):
    validPyChars="1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_"
    stringOK=""
    for char in string.encode('ascii', 'ignore'):
        if char in validPyChars:
            stringOK += char
    return "action_"+stringOK

class trace:

    def __init__(self):
        self.trace = None
        
    def ce(self,string):
        if self.trace:
            print string

class pickLayer:
    """QGIS Plugin Implementation."""

    def registerActions(self,layer):
        acts=[]
        actionOrder = 0
        for action in layer.actions().listActions():
            actionCode = """
@self
def %s(self):
    self.selectedLayer.actions().doAction(%s)""" % (stringToPythonNames(action.name()),actionOrder)
            acts.append([action.name(),stringToPythonNames(action.name())])
            print actionCode
            exec actionCode
        return acts
    

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.mapCanvas = iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        self.snapDlg = snappingDialog()
        self.DsDialog = setDataSource(iface)
        self.tra = trace()


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        #icon_path = ':/plugins/pickLayer/icon.png'
        icon_path = os.path.join(self.plugin_dir,"icons","pickLayer.png")
        # map tool action
        self.mapToolAction = QAction(QIcon(icon_path),"Pick to Layer", self.iface.mainWindow())
        self.mapToolAction.setCheckable(True)
        self.mapTool = IdentifyGeometry(self.mapCanvas)
        self.mapTool.geomIdentified.connect(self.editFeature)
        self.mapTool.setAction(self.mapToolAction)
        self.mapToolAction.triggered.connect(self.setMapTool)
        self.iface.addToolBarIcon(self.mapToolAction)
        self.iface.addPluginToMenu("&Pick to Layer", self.mapToolAction)


    def contextMenuRequest(self):
        contextMenu = QMenu()
        self.clipboardLayerAction = contextMenu.addAction("Layer: "+self.selectedLayer.name())
        contextMenu.addSeparator()
        self.setCurrentAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","mSetCurrentLayer.png")),"Set current layer")
        self.hideAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","off.png")),"Hide")
        self.openPropertiesAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","settings.svg")),"Open properties dialog")
        self.zoomToLayerAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","zoomToLayer.png")),"Zoom to layer extension")
        self.setDataSourceAction = contextMenu.addAction("Change Data source")
        self.setCurrentAction.triggered.connect(self.setCurrentFunc)
        self.hideAction.triggered.connect(self.hideFunc)
        self.openPropertiesAction.triggered.connect(self.openPropertiesFunc)
        self.setDataSourceAction.triggered.connect(self.setDataSourceFunc)
        self.zoomToLayerAction.triggered.connect(self.zoomToLayerFunc)
        if self.selectedLayer.type() == QgsMapLayer.VectorLayer:
            contextMenu.addSeparator()
            self.openAttributeTableAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","mActionOpenTable.png")),"Open attribute table")
            self.openAttributeTableAction.triggered.connect(self.openAttributeTableFunc)
            self.zoomToFeatureAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","zoomToFeature.png")),"Zoom to feature")
            self.zoomToFeatureAction.triggered.connect(self.zoomToFeatureFunc)
            if self.selectedLayer.isEditable():
                self.stopEditingAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","mIconEditableEdits.png")),"Stop editing")
                self.stopEditingAction.triggered.connect(self.stopEditingFunc)
            else:
                self.startEditingAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","mIconEditable.png")),"Start editing")
                self.startEditingAction.triggered.connect(self.startEditingFunc)
            self.snappingOptionsAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","snapIcon.png")),"Snapping options")
            self.snappingOptionsAction.triggered.connect(self.snappingOptionsFunc)
            if len(QgsApplication.clipboard().text().splitlines()) > 1:
                clipFeatLineTXT = QgsApplication.clipboard().text().splitlines()[1]
                clipFeatsTXT = clipFeatLineTXT.split('\t')
                self.clipAttrsFieldnames = QgsApplication.clipboard().text().splitlines()[0].split('\t')[1:]
                self.clipAttrsValues = clipFeatsTXT[1:]
                self.clipGeom = QgsGeometry.fromWkt(clipFeatsTXT[0])
                #if self.clipGeom.isGeosValid():
                if self.selectedLayer.isEditable() and self.clipGeom:
                    self.pasteGeomAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","pasteIcon.png")),"Paste geometry on feature")
                    self.pasteGeomAction.triggered.connect(self.pasteGeomFunc)
                    self.pasteAttrsAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","pasteIcon.png")),"Paste attributes on feature")
                    self.pasteAttrsAction.triggered.connect(self.pasteAttrsFunc)
            self.copyFeatureAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","copyIcon.png")),"Copy feature")
            self.copyFeatureAction.triggered.connect(self.copyFeatureFunc)
            self.editFeatureAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","mActionPropertyItem.png")),"Feature attributes edit")
            self.editFeatureAction.triggered.connect(self.editFeatureFunc)
            if self.selectedLayer.actions().listActions():
                actionOrder = 0
                contextMenu.addSeparator()
                for action in self.selectedLayer.actions().listActions():
                    try:
                        customIcon = action.icon()
                    except:
                        customIcon = QIcon(os.path.join(self.plugin_dir,"icons","customAction.png"))
                    newActionItem = contextMenu.addAction(customIcon,action.name())
                    newActionItem.triggered.connect(partial(self.customAction,actionOrder))
                    actionOrder += 1
        contextMenu.exec_(QCursor.pos())

    def zoomToFeatureFunc(self):
        featureBox = self.selectedFeature.geometry().boundingBox()
        self.mapCanvas.setExtent(featureBox)
        self.mapCanvas.refresh()
        
    def zoomToLayerFunc(self):
        layerBox = self.selectedLayer.extent()
        self.mapCanvas.setExtent(layerBox)
        self.mapCanvas.refresh()

    def setCurrentFunc(self):
        self.iface.setActiveLayer(self.selectedLayer)

    def setDataSourceFunc(self):
        self.DsDialog.changeDataSource(self.selectedLayer)

    def customAction(self,actionId):
        self.selectedLayer.actions().doActionFeature(actionId,self.selectedFeature)

    def hideFunc(self):
        self.iface.legendInterface().setLayerVisible(self.selectedLayer, False)
        
    def openPropertiesFunc(self):
        self.iface.showLayerProperties(self.selectedLayer)

    def openAttributeTableFunc(self):
        self.iface.showAttributeTable(self.selectedLayer)
        
    def stopEditingFunc(self):
        self.iface.setActiveLayer(self.selectedLayer)
        self.iface.actionToggleEditing().trigger()
        
    def startEditingFunc(self):
        self.iface.setActiveLayer(self.selectedLayer)
        self.iface.actionToggleEditing().trigger()

    def snappingOptionsFunc(self):
        self.snapDlg.getSnappingOptionsDialog(self.selectedLayer)

    def editFeatureFunc(self):
        self.iface.openFeatureForm(self.selectedLayer,self.selectedFeature,True)

    def copyFeatureFunc(self):
        bakActiveLayer = self.iface.activeLayer()
        self.iface.setActiveLayer(self.selectedLayer)
        self.selectedLayer.setSelectedFeatures([self.selectedFeature.id()])
        self.iface.actionCopyFeatures().trigger()
        self.iface.setActiveLayer(bakActiveLayer)

    def pasteGeomFunc(self):
        #self.selectedLayer.startEditing()
        #self.selectedFeature.setGeometry(self.clipGeom)
        self.selectedLayer.changeGeometry(self.selectedFeature.id(), self.clipGeom)
        self.selectedLayer.updateExtents()
        self.selectedLayer.setCacheImage(None)
        self.selectedLayer.triggerRepaint()

    def pasteAttrsFunc(self):
        for attrId in range(0,len(self.clipAttrsValues)):
            if self.selectedLayer.pendingFields().field(str(self.clipAttrsFieldnames[attrId])):
                self.selectedLayer.changeAttributeValue(self.selectedFeature.id(),attrId,self.clipAttrsValues[attrId])

    def editFeature(self,layer,feature):
        self.selectedLayer = layer
        self.selectedFeature = feature
        self.contextMenuRequest()
        pass

    def unload(self):
        self.iface.removePluginMenu("&Pick to Layer", self.mapToolAction)
        self.iface.removeToolBarIcon(self.mapToolAction)

    def setMapTool(self):
        self.mapCanvas.setMapTool(self.mapTool)
        
