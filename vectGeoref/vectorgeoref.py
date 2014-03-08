# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VectorGeoref
								 A QGIS plugin
 A visual tool to georeferencing vector layers
							  -------------------
		begin                : 2013-11-11
		copyright            : (C) 2013 by Giuliano Curti
		email                : giulianc51@gmail.com
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
#tets aggiunta linea
import os.path
import os

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Initialize Qt resources from file resources.py
import resources_rc

# Import the code for the dialog
from vectorgeorefdialog import VectorGeorefDialog


class VectorGeoref:

	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		# initialize plugin directory
		self.plugin_dir = os.path.dirname(__file__)
		# initialize locale
		locale = QSettings().value("locale/userLocale")[0:2]
		localePath = os.path.join(self.plugin_dir, 'i18n', 'vectorgeoref_{}.qm'.format(locale))
		if os.path.exists(localePath):
			self.translator = QTranslator()
			self.translator.load(localePath)
			if qVersion() > '4.3.3':
				QCoreApplication.installTranslator(self.translator)
		# Create the dialog (after translation) and keep reference
		self.dlg = VectorGeorefDialog(self.iface)

	def initGui(self):
		# Create action that will start plugin configuration
		self.plugin_dir = os.path.dirname(__file__)
		icoDir = self.plugin_dir + os.sep + "/icon.png"
		self.action = QAction(QIcon(icoDir),u"Vector Georeferencer", self.iface.mainWindow())
		# connect the action to the run method
		self.action.triggered.connect(self.run)
		# Add toolbar button and menu item
		self.iface.addToolBarIcon(self.action)
		self.iface.addPluginToMenu(u"&vectorgeoref", self.action)

	def unload(self):
		# Remove the plugin menu item and icon
		self.iface.removePluginMenu(u"&vectorgeoref", self.action)
		self.iface.removeToolBarIcon(self.action)

	# run method that performs all the real work
	def run(self):
		self.dlg.show()
		# Run the dialog event loop
		result = self.dlg.exec_()
		# See if OK was pressed
		if result == 1:
			# do something useful (delete the line containing pass and
			# substitute with your code)
			pass
