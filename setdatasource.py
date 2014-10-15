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
from ui_changeDSDialog import Ui_changeDataSourceDialog
# create the dialog for zoom to point


class setDataSource(QtGui.QDialog, Ui_changeDataSourceDialog):

    def __init__(self,iface):
        QtGui.QDialog.__init__(self)
        self.iface = iface
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.saveDataSource)
        self.buttonBox.rejected.connect(self.cancelDialog)

    def changeDataSource(self,layer):
        self.layer = layer
        self.lineEdit.setText(self.layer.source())
        self.show()

    def cancelDialog(self):
        self.hide()

    def saveDataSource(self):
        print "apply"
        self.hide()
        self.iface.setActiveLayer(self.layer)
        nlayer = QgsVectorLayer(self.lineEdit.text(),self.layer.name() , "ogr")
        nlayer.setRendererV2(self.layer.rendererV2())
        print nlayer.name()
        QgsMapLayerRegistry.instance().removeMapLayer(self.layer.id())
        QgsMapLayerRegistry.instance().addMapLayer(nlayer)
        self.iface.setActiveLayer(self.nlayer)