# -*- coding: utf-8 -*-
"""
/***************************************************************************
 undoLayerChangesDialog
                                 A QGIS plugin
 undoLayerChanges
                             -------------------
        begin                : 2014-09-04
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

from qgis.core import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtXml import *
from ui_changeDSDialog import Ui_changeDataSourceDialog
from qgis.gui import QgsManageConnectionsDialog
import os.path
# create the dialog for zoom to point


class setDataSource(QtGui.QDialog, Ui_changeDataSourceDialog):

    def __init__(self,iface):
        QtGui.QDialog.__init__(self)
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.saveDataSource)
        self.buttonBox.rejected.connect(self.cancelDialog)
        self.selectDatasourceCombo.activated.connect(self.selectDS)
        self.openBrowser.clicked.connect(self.openFileBrowser)

    def openFileBrowser(self):
        exts = "All files (*.*);;ESRI shapefiles (*.shp);; Geojson (*.geojson);;Keyhole markup language (*.kml *.kmz)"
        fileName = QtGui.QFileDialog.getOpenFileName(None,"select OGR vector file", os.path.dirname(self.layer.source()), exts)
        if fileName:
            self.lineEdit.setText(fileName)

    def selectDS(self):
        if self.selectDatasourceCombo.currentIndex()==0:
            self.openBrowser.setEnabled(True)
        else:
            self.openBrowser.setDisabled(True)

    def changeDataSource(self,layer):
        self.layer = layer
        self.lineEdit.setText(self.layer.source())
        self.show()

    def cancelDialog(self):
        self.hide()

    def saveDataSource(self):
        self.hide()
        XMLDocument = QDomDocument("style")
        XMLMapLayers = QDomElement()
        XMLMapLayers = XMLDocument.createElement("maplayers")
        XMLMapLayer = QDomElement()
        XMLMapLayer = XMLDocument.createElement("maplayer")
        self.layer.writeLayerXML(XMLMapLayer,XMLDocument)
        self.iface.setActiveLayer(self.layer)
        datasourceType = self.selectDatasourceCombo.currentText().lower().replace(' ','')
        print datasourceType
        nlayer = QgsVectorLayer(self.lineEdit.text(),self.layer.name(), datasourceType)
        QgsMapLayerRegistry.instance().addMapLayer(nlayer)
        print XMLMapLayer.firstChildElement("datasource").firstChild().nodeValue()
        XMLMapLayer.firstChildElement("datasource").firstChild().setNodeValue(os.path.relpath(nlayer.source(),QgsProject.instance().readPath("./")).replace('\\','/'))
        XMLMapLayer.firstChildElement("id").firstChild().setNodeValue(os.path.relpath(nlayer.id()))
        print XMLMapLayer.firstChildElement("datasource").firstChild().nodeValue()
        XMLMapLayers.appendChild(XMLMapLayer)
        XMLDocument.appendChild(XMLMapLayers)
        #print XMLDocument.toString()
        nlayer.readLayerXML(XMLMapLayer)
        self.iface.actionDraw().trigger()
        self.canvas.refresh()
        self.iface.legendInterface().refreshLayerSymbology(nlayer)
        self.iface.setActiveLayer(nlayer)
        QgsMapLayerRegistry.instance().removeMapLayer(self.layer.id())