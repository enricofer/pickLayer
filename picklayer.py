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
from PyQt4.QtGui import QAction, QIcon
from PyQt4 import uic
from qgis.core import *
from qgis.utils import plugins
from qgis.gui import QgsAttributeDialog
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
#from picklayer_dialog import pickLayerDialog
from identifygeometry import IdentifyGeometry
import os.path

class trace:

    def __init__(self):
        self.trace = None
        
    def ce(self,string):
        if self.trace:
            print string

class pickLayer:
    """QGIS Plugin Implementation."""

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
        #self.dlg = pickLayerDialog()
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
        contextMenu.addAction("")
        self.setCurrentAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","mSetCurrentLayer.png")),"Set current layer")
        self.hideAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","off.png")),"Hide")
        self.openPropertiesAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","settings.svg")),"Open properties dialog")
        self.setCurrentAction.triggered.connect(self.setCurrentFunc)
        self.hideAction.triggered.connect(self.hideFunc)
        self.openPropertiesAction.triggered.connect(self.openPropertiesFunc)
        if self.selectedLayer.type() == QgsMapLayer.VectorLayer:
            self.openAttributeTableAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","mActionOpenTable.png")),"Open attribute table")
            #self.openFilterAction = contextMenu.addAction("Open filter dialog")
            self.openAttributeTableAction.triggered.connect(self.openAttributeTableFunc)
            #self.openFilterAction.triggered.connect(self.openFilterFunc)
            if self.selectedLayer.isEditable():
                self.stopEditingAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","mIconEditableEdits.png")),"Stop editing")
                self.stopEditingAction.triggered.connect(self.stopEditingFunc)
            else:
                self.startEditingAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","mIconEditable.png")),"Start editing")
                self.startEditingAction.triggered.connect(self.startEditingFunc)
            self.editFeatureAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","mActionPropertyItem.png")),"Feature attributes edit")
            self.editFeatureAction.triggered.connect(self.editFeatureFunc)
        contextMenu.exec_(QCursor.pos())

    def setCurrentFunc(self):
        self.iface.setActiveLayer(self.selectedLayer)

    def hideFunc(self):
        self.iface.legendInterface().setLayerVisible(self.selectedLayer, False)
        
    def openPropertiesFunc(self):
        self.iface.showLayerProperties(self.selectedLayer)

    def openAttributeTableFunc(self):
        self.iface.showAttributeTable(self.selectedLayer)
        
#    def openFilterFunc(self):
#        pass
        
    def stopEditingFunc(self):
        self.iface.setActiveLayer(self.selectedLayer)
        self.iface.actionToggleEditing().trigger()
        
    def startEditingFunc(self):
        #self.selectedLayer.startEditing ()
        self.iface.setActiveLayer(self.selectedLayer)
        self.iface.actionToggleEditing().trigger()

    def editFeatureFunc(self):
        #dlg = QgsAttributeDialog(self.selectedLayer,self.selectedFeature,True)
        #dlg.show()
        self.iface.openFeatureForm(self.selectedLayer,self.selectedFeature,True)

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
        

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        #self.dlg.show()
        pass
