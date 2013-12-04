# -*- coding: utf-8 -*-

"""
001	2012-07-28
"""

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class genericDlg(QDialog):	#QtGui.
	""" Dialogo per N parametri """

	def __init__(self,title,fields):
		"""
			Inizializza la maschera per l'editing di N parametri.
			I nomi dei parametri sono dati dalla lista fields.
		"""
		QDialog.__init__(self)	#QtGui.
		# impostazione interfaccia utente
		self.setWindowTitle(title)
		num = len(fields)
		self.resize(280, 40+30*num)

		self.entries = []
		for i,l in enumerate(fields):
			label = QLabel(self)	#QtGui.
			label.setGeometry(QRect(10, 10+30*i, 100, 20))	#QtCore.
			label.setText(l)
			entry = QLineEdit(self)	#QtGui.
			entry.setGeometry(QRect(120, 10+30*i, 150, 20))	#QtCore.
			self.entries.append(entry)

		buttonBox = QDialogButtonBox(self)	#QtGui.
		buttonBox.setGeometry(QRect(120, 40+30*i, 150, 30))	#QtCore.
		buttonBox.setOrientation(Qt.Horizontal)	#QtCore.
		buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)	#QtGui.	#QtGui.
		buttonBox.setObjectName("buttonBox")
		QObject.connect(buttonBox,SIGNAL("accepted()"),self.accept)	#QtCore.	#QtCore.
		QObject.connect(buttonBox,SIGNAL("rejected()"),self.reject)	#QtCore.	#QtCore.
		QMetaObject.connectSlotsByName(self)	#QtCore.

	def setValues(self,params):
		""" Inizializza i parametri nella maschera di input  """
		for i,v in enumerate(self.entries):
			v.setText(str(params[i]))

	def clearValues(self):
		""" Azzera i parametri nella maschera di input  """
		for i,v in enumerate(self.entries):
			v.setText('')

	def getValues(self):
		""" Restituisce il parametro  """
		val = []
		for v in self.entries:
			val.append(v.text())
		return val
