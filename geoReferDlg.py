# -*- coding: utf-8 -*-

"""
001	2013-11-11
"""

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class geoReferDlg(QDialog):
	"""
		Dialogo per la gestione del vector georeferencer
		Riepiloga le coppie di punti origine/destinazione
	"""

	def __init__(self,lList,orig,dest):
		"""
			Inizializza la maschera
			orig e dest sono liste di liste
		"""
		QDialog.__init__(self)
		# impostazione interfaccia utente
		self.setWindowTitle("Vector georeferencer")
		num = len(orig)
		self.resize(600,80+30*num)

		# contenitore generale
		bigBox = QVBoxLayout(self)

		# spazio per il layer
		bBox = QHBoxLayout(self)
		label = QLabel(self)
		bBox.addWidget(label)
		label.setText('layer')
		self.eLay = QComboBox()
		bBox.addWidget(self.eLay)
		for i in lList:
			self.eLay.addItem(i.name())
		bigBox.addLayout(bBox)

		# spazio per le coordinate
		"""
			dispone il numero max di caselle;
			dove mancano le coordinate pone a zero
		"""
		entryList = []	# lista di liste
		num = max(len(orig),len(dest))
		for i in range(num):
			row = []	# lista
			bBox1 = QHBoxLayout(self)
			bBox1.setGeometry(QRect(10,30+30*i,550,20))
			label = QLabel(self)
			label.setText(str(i))
			bBox1.addWidget(label)
			# coordinate origini
			entry1 = QLineEdit(self)
			entry2 = QLineEdit(self)
			if i <len(orig):
				entry1.setText(str(orig[i][0]))
				entry2.setText(str(orig[i][1]))
			else:
				entry1.setText('')
				entry2.setText('')
			bBox1.addWidget(entry1)
			bBox1.addWidget(entry2)
			row.append(entry1)
			row.append(entry2)
			# coordinate destinazioni
			entry1 = QLineEdit(self)
			entry2 = QLineEdit(self)
			if i <len(dest):
				entry1.setText(str(dest[i][0]))
				entry2.setText(str(dest[i][1]))
			else:
				entry1.setText('')
				entry2.setText('')
			bBox1.addWidget(entry1)
			bBox1.addWidget(entry2)
			row.append(entry1)
			row.append(entry2)
			# salva la riga
			entryList.append(row)
			bigBox.addLayout(bBox1)

		# spazio per i bottoni
		bBox2 = QHBoxLayout(self)
		bBox2.setGeometry(QRect(120,50+30*num,550,30))
		btn = QPushButton("Cancel")
		QObject.connect(btn,SIGNAL("clicked()"),self.cancel)
		bBox2.addWidget(btn)
		btn = QPushButton("More")
		QObject.connect(btn,SIGNAL("clicked()"),self.more)
		bBox2.addWidget(btn)
		btn = QPushButton("Done")
		QObject.connect(btn,SIGNAL("clicked()"),self.apply)
		bBox2.addWidget(btn)
		bigBox.addLayout(bBox2)

	def cancel(self):
		self.returnVal = -1
		self.close()
		return

	def more(self):
		self.returnVal = 0
		self.close()
		return

	def apply(self):
		self.returnVal = 1
		self.close()
		return

	def getRes(self):
		return self.returnVal

	def getLayer(self):
		layName = self.eLay.currentText()
		return layName










