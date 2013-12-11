# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VectorGeorefDialog
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

from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.QtGui

from qgis.core import *
from qgis.gui import *

from ui_vectorgeoref import Ui_VectorGeoref
# create the dialog for zoom to point

# ------------ matrix functions ------------

def printMatrix(mat):
	pass
##	nr = len(mat)
##	nc = len(mat[0])
##	print ' ',
##	for c in range(nc):
##		print '%5s ' % (c+1),
##	print
##	print "------" * (nc+2)
##	for r in range(nr):
##		print r+1, "|",
##		for c in range(nc):
##			pass
##			#print '%5.2f ' % mat[r][c],
##		print
##	print "------" * (nc+2)

def nullMatrix(nr,nc):
	"""
		resituisce la matrice nulla di nr x nc
	"""
	mat = []
	for i in range(nr):
		tmp = []
		for j in range(nc):
			tmp.append(0.0)
		mat.append(tmp)
	return mat

def adjoint(mat1,nr,mat2):
	"""
		Costruisce la matrice aggiunta composta dalle due matrici in input
		(presume le matrice di nr numero di righe)
	"""
	nc2 = len(mat2[1])
	adj = []
	for i in range(nr):
		tmp = mat1[i][:]
		for j in mat2[i]:
			tmp.append(j)
		adj.append(tmp)
	return adj

def matrixTranspose(mat):
	"""
		esegue la trasposta di una matrice
	"""
	nr = len(mat)
	nc = len(mat[0])
	matT = nullMatrix(nc,nr)
	for r in range(nr):
		for c in range(nc):
			matT[c][r] = mat[r][c]
	return matT

def matrixMultiplication(mat1,mat2):
	"""
		Calcola il prodotto delle matrici mat1*mat2
	"""
#	print "matrice 1:"
#	self.printMatrix(mat1)
#	print "matrice 2:"
#	self.printMatrix(mat2)
	nr1 = len(mat1)
	nc1 = len(mat1[0])
	nr2 = len(mat2)
	nc2 = len(mat2[0])
	mat = []
	if nc1 == nr2:
		for i in range(nr1):
			tmp = []
			for j in range (nc2):
				val = 0
				for k in range (nc1):
			  		val += mat1[i][k] * mat2[k][j]
				tmp.append(val)
			mat.append(tmp)
		return mat
	else:
		print "matrici non congruenti per la moltiplicazione"
		return -1

def EchelonNF(mat):
	"""
		2013-02-12
		calcola la Echelon Normal Form
		NB: gestisce matrici rettangolari
	"""
	nr = len(mat)
	nc = len(mat[0])
	# print "discesa"
	for i in range(nr):
		# print "riga",i
		# determina il pivot
		# dovrebbe essere da i in avanti perchÃ¨ dietro dovrebbero essere nulli
		# perÃ², poichÃ¨ non facciamo lo swap delle righe, ripartiamo dall'inizio
		for j in range(nc):
			if abs(mat[i][j]) > 1E-10:
				# print "controllo",i,j
				cp = j
				piv = mat[i][cp]
				# print "trovato pivot riga",i,"in colonna",cp,"e vale",piv,"normalizzo la riga"
				for l in range(nc):	# forse si puÃ² partire da cp che Ã¨ la prima colonna nonnulla
					mat[i][l] = mat[i][l]/piv
				# elimina dalla colonna pivot in avanti
				for j in range(i+1,nr):
					# print "elimino all'ingiu riga",j
					k = mat[j][cp]
					for l in range(cp,nc):
						mat[j][l] = mat[j][l]-k*mat[i][l]
				break
		# printMatrix(mat)
	# print "salita"
	for i in reversed(range(nr)):
		#print "riga",i
		# determina il pivot (vedi sopra a proposito della ricerca del pivot)
		for j in range(nc):
			if abs(mat[i][j]) > 1E-10:
				cp = j
				piv = mat[i][j]
				#print "trovato pivot riga",i,"in colonna",cp,"e vale",piv
				for j in range(i):
					#print "elimino riga",j
					k = mat[j][cp]/piv
					for l in range(cp,nc):
						mat[j][l] = mat[j][l]-k*mat[i][l]
				break
		#printMatrix(mat,nr,nc)
	return mat

def prelievoColonne(mat,list):
	"""
		preleva le colonne indicate in list dalla matrice mat
		e le restituisce in newMat;
		presume che list sia corretta, cioÃ¨ non contenga riferimenti a colonne inesistenti;

		Ã¨ tagliata sul columnSpace per il quale arriva la lista rng i cui items sono duple
		riga,colonna del pivot;
	"""
	nr = len(mat)
	newMat = []
	for r in range(nr):
		tmp = []
		for k,c in list:
			tmp.append(mat[r][c])
		newMat.append(tmp)
	return newMat

def lsm2(old,new):
	"""
		l(est) s(quare) m(ethod)
		in questa seconda versione anzichè calcolare l'inversa troviamo la soluzione
		dalla echelon form della matrice aggiunta, previa normalizzazione degli elementi
		diagonali;
		#ATTENZIONE: poichè noi accettiamo in generale anche una disposizione dei pivot
		non diagonale, la routine potrebbe dare dei problemi; in caso modificare
	"""
	print "devo far coincidere i punti"
	printMatrix(old)
	print "con i punti"
	printMatrix(new)
	print "matrice trasposta"
	oldT = matrixTranspose(old)
	printMatrix(oldT)
	print "matrice normale"
	mat = matrixMultiplication(oldT,old)
	printMatrix(mat)
	print "Termine noto"
	tn = matrixMultiplication(oldT,new)
	printMatrix(tn)
	print "matrice aggiunta"
	nr = len(mat)
#	for i in range(len(tn[0])):	# per ogni colonna del termine noto 
#		myList = [[0,i]]	# questa strana forma Ã¨ dovuta a precedenti (vedi rank())	
#		tmp = prelievoColonne(tn,myList)
#		mat = adjoint(mat,nr,tmp)
	mat = adjoint(mat,nr,tn)
	printMatrix(mat)
	print "Echelon form"
	EchelonNF(mat)
	printMatrix(mat)
	print "(Experimental) normalization"
	for i in range(nr):
		if abs(mat[i][i] - 1.00) > 0.005:	#ATTENZIONE: noi accettiamo anche una forma con pivot disposti diversamente!
			alfa = 1/mat[i][i]
			print "normalization of row",i,"by factor",alfa
			for k in range(len(mat[i])):
				print "element",k,mat[i][k],
				mat[i][k] = mat[i][k] * alfa
				print "become",mat[i][k]
	printMatrix(mat)
	# soluzione
	sol = []
	for i in range(len(tn[0])):	# per ogni colonna del termine noto 
	# ma myList non esiste giò?
		myList = [[0,nr+i]]	# questa strana forma Ã¨ dovuta a precedenti (vedi rank())
		tmp = prelievoColonne(mat,myList)
		tmp = matrixTranspose(tmp)
		print tmp
		sol.append(tmp[0])	# questa operazione Ã¨ empirica, serve ad eliminare un livello di parentesi, controllare
	printMatrix(sol)
	return sol

# -------- retrieving functions -------

def snapPoint(layer,point,eps):
	"""
		Seleziona il vertice di una feature più vicino al mouse;
	"""
	print "interrogo il layer",layer.name(),"con tolleranza",eps

	# setup the provider select to filter results based on a rectangle
	pntGeom = QgsGeometry.fromPoint(point)  
	# scale-dependent buffer of 5 pixels-worth of map units
	pntBuff = pntGeom.buffer(eps,0) 
	rect = pntBuff.boundingBox()
	# create the select statement
#	print "interrogo il layer",layer.name()
	layer.select(rect,True)	# prende quelli che intersecano	
	# ha trovato qualcosa?

	print "trovate",layer.selectedFeatureCount(),"features"

	if layer.selectedFeatureCount():
		# legge le features e pulisce
		feat = layer.selectedFeatures().pop()
		layer.removeSelection()
		# legge la geometria
		geom = feat.geometry()
		gT = layer.geometryType()
		print "geometria tipo",gT
		if gT == 0:
			p = geom.asPoint()
			print "trovata",feat.id()
			return p
		elif gT == 1:
			line = geom.asPolyline()
			# scandisce i vertici
			for p in line:
				if abs(point.x()-p.x()) <= eps and abs(point.y()-p.y()) <= eps:
					print "trovata",feat.id()
					return p
		elif gT == 2:
			print "layer di poligoni"
			plines = geom.asPolygon()
			# cerca il vertice
			for line in plines:
				for p in line:
					print "confronto punto",point.x(),point.y(),"con punto",p.x(),p.y()
					if abs(point.x()-p.x()) <= eps and abs(point.y()-p.y()) <= eps:
						print "trovata",feat.id()
						return p
	return []

# -------- layer functions -------

def cloneLayer(oldLayer,type,name):
	"""
		clone the layer in newlayer
	"""
	newLayer = QgsVectorLayer()
	# copia gli attributi
	oProv = oldLayer.dataProvider()
	myAttrList = oProv.fields()
	# copia il CRS
	myCrs = oldLayer.crs()
	# creo il nuovo layer
	newLayer = QgsVectorLayer(type,name,"memory")				
	# Enter editing mode
	newLayer.startEditing()
	# setta il crs
	newLayer.setCrs(myCrs)
	# aggiunge gli attributi
	nProv = newLayer.dataProvider()
	for att in myAttrList:
		nProv.addAttributes([att])
	# duplica le features
	for feat in oldLayer.getFeatures():
		nProv.addFeatures([feat])
	# aggiunge al registry
	QgsMapLayerRegistry.instance().addMapLayer(newLayer)
	return newLayer

def pointTransform(layer,matrix):
	"""
		Esegue la trasformazione di un layer puntuale
		questa forma non mi piace però la gestione degli attributi è
		piuttosto ostica e questa sembra funzionare
	"""
	for feat in layer.getFeatures():
		geom = feat.geometry()
		p = geom.asPoint()
		cds = matrixMultiplication(matrix,[[p.x()],[p.y()],[1]])
#		print cds
		geom = QgsGeometry.fromPoint(QgsPoint(cds[0][0],cds[1][0]))
		layer.changeGeometry(feat.id(),geom)

def lineTransform(layer,matrix):
	"""
		Esegue la trasformazione di un layer lineare
	"""
	for feat in layer.getFeatures():
		geom = feat.geometry()
		line = geom.asPolyline()
		# costruisce la nuova
		newLine = []
		for p in line:
			cds = matrixMultiplication(matrix,[[p.x()],[p.y()],[1]])
#			print cds
			newLine.append(QgsPoint(cds[0][0],cds[1][0]))
		geom = QgsGeometry.fromPolyline(newLine)
		layer.changeGeometry(feat.id(),geom)

def polygTransform(layer,matrix):
	"""
		Esegue la trasformazione di un layer poligonale
	"""
	for feat in layer.getFeatures():
		geom = feat.geometry()
		plgns = geom.asPolygon()
		# nuova geometria
		newPlgns = []
		for line in plgns:
			# costruisce il nuovo poligono
			newLine = []
			for v in line:
				cds = matrixMultiplication(matrix,[[v.x()],[v.y()],[1]])
#				print cds
				newLine.append(QgsPoint(cds[0][0],cds[1][0]))
			# aggiorna la geometria
			newPlgns.append(newLine)
		geom = QgsGeometry.fromPolygon(newPlgns)
		layer.changeGeometry(feat.id(),geom)

# ================= classe principale ================

class VectorGeorefDialog(QtGui.QDialog):
	vLayer = ""
	mapPreview = ""
	markerList1 = []	# lista dei marcatori del canvas1
	markerList2 = []	# lista dei marcatori del canvas2
	anTxtList = []		# lista delle annotazioni
	checked_list = []	# lista delle righe scelte

	def __init__(self, iface):
		QtGui.QDialog.__init__(self)
		# Set up the user interface from Designer.
		self.iface = iface
		self.canvas = iface.mapCanvas()
		self.ui = Ui_VectorGeoref()
		self.ui.setupUi(self)
		self.customize_GUI()

		# connect the layer changed handler to a signal that the TOC layer has changed
		QObject.connect(self.iface,SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.myHandleLayerChange)
		# inizializza i dati sul layer
		self.myHandleLayerChange()
		self.newProj()

	def customize_GUI(self):
		# map prevew system
		self.mapPreview = QgsMapCanvas(self)
		self.mapPreview.setCanvasColor(QColor(225,225,225))
		self.ui.tabWidget.addTab(self.mapPreview, "Map Canvas")

	def newProj(self):
		self.firstPntDone = False	# if true pnt fom canvas2, if false pnt from canvas1
		self.isClickToolActivated = 0	# 0-noactive 1-canvas1 2-canvas2

	def on_pushButtonCP_Selection_pressed(self):
		# out click tool will emit a QgsPoint on every click
		self.clickTool1 = QgsMapToolEmitPoint(self.canvas)
		self.clickTool2 = QgsMapToolEmitPoint(self.mapPreview)
		# make our clickTool the tool that we'll use for now
		self.canvas.setMapTool(self.clickTool1)
		self.mapPreview.setMapTool(self.clickTool2)
		self.firstPntDone = False
		self.vecLayGeorefTool()
		
	def on_pushButton_load_layer_pressed(self):
		# ---------- carica il layer da file -----------
		fname = QFileDialog.getOpenFileName(self.iface.mainWindow(),'Open file','/home/giuliano','*.shp')
		if fname:
			print "aperto layer",fname
			layerToSet = []
			self.vLayer = QgsVectorLayer(fname, "layer_prova", "ogr")
			QgsMapLayerRegistry.instance().addMapLayers([self.vLayer], False)
			layerToSet.append(QgsMapCanvasLayer(self.vLayer, True, False))
			self.mapPreview.setLayerSet(layerToSet)
			self.mapPreview.zoomToFullExtent()
			# stabilisce la tolleranza di ricerca
			self.eps2 = self.mapPreview.mapUnitsPerPixel() * 5
			# azzera la tabella dei CP
			self.on_pushButton_clear_pressed()


	def on_pushButton_run_pressed(self):
		# legge i dati della tabella...
		tmp = self.getValues()
		#  .. e li deposita nelle due liste
		srcPntList = []
		dstPntList = []
		for [chek,oX,oY,dX,dY] in tmp:
			#QMessageBox.about(self,'test',chek)
			if chek == 'ok':
				srcPntList.append([float(oX),float(oY),1.0])	# aggiunge la coordinata omogenea
				dstPntList.append([float(dX),float(dY),1.0])
#				print "il punto (%s %s) va in (%s %s)" % (oX,oY,dX,dY)
		# ------- trasformazione dei layer ------
		# numero di coppie
		nP = len(srcPntList)
		if nP >= 2:
			vtype = ['Point','Linestring','Polygon']
			if self.vLayer:
				gT = self.vLayer.geometryType()
				if gT in (0,1,2):
					lN = self.vLayer.name()+'-modificato'
					newLayer = cloneLayer(self.vLayer,vtype[gT],lN)
					# calcola la matrice ai minimi quadrati
					mat = lsm2(srcPntList,dstPntList)
#					printMatrix(mat)
					if gT == 0:
#						print "layer puntuale"
						pointTransform(newLayer,mat)
					elif gT == 1:
#						print "layer lineare"
						lineTransform(newLayer,mat)
					elif gT == 2:
#						print "layer poligonale"
						polygTransform(newLayer,mat)
					# Commit changes
					newLayer.commitChanges()
					# update layer's extent
					newLayer.updateExtents()
				else:
					self.iface.messageBar().pushMessage(
						"on_pushButton_run_pressed",
						"Layer sconosciuto",
						level=QgsMessageBar.CRITICAL,
						duration=4
					)
		else:
			self.iface.messageBar().pushMessage(
				"on_pushButton_run_pressed",
				"Numero di punti insufficiente",
				level=QgsMessageBar.CRITICAL,
				duration=3
			)

	def on_pushButton_clear_pressed(self):
		"""
			Clear the table
		"""
		self.ui.tableWidget.clear()
		self.ui.tableWidget.setRowCount(0)
		# pulisce lo schermo
		self.cleanSelection()
		
	def on_actionPan_toggled(self):
		self.toolPan = QgsMapToolPan(self.mapPreview)
		self.mapPreview.setMapTool(self.toolPan)

# ----------- utility functions ----------------

	def myHandleLayerChange(self):
		if self.iface.activeLayer():
			# registra il layer corrente
			self.cLayer = self.iface.activeLayer()
			# al cambio del layer stabilisce la tolleranza di ricerca
			self.eps = self.canvas.mapUnitsPerPixel() * 5

	def pntHighligth(self,canvas,pnt,color=QColor(250,150,0),size=25):
		"""
			attiva il marcatore del punto
			NB: riceve una feature
		"""
		x,y = pnt.x(),pnt.y()
		marker = QgsVertexMarker(canvas)
#		marker.setIconType(QgsVertexMarker.ICON_CROSS)
		marker.setColor(color)
		marker.setIconSize(size)
		marker.setCenter(QgsPoint(x,y))
		marker.show()
		return marker

	def cleanSelection(self):
		"""
			Pulisce lo stack dei selezionati e toglie i marker;
		"""
		# elimina i marcatori
		for m in self.markerList1:
			self.canvas.scene().removeItem(m)
		self.markerList1 = []
		for m in self.markerList2:
			self.mapPreview.scene().removeItem(m)
		self.markerList2 = []
		# rinfresca il video
		self.canvas.refresh()
		self.mapPreview.refresh()

	def insertNewRow(self,dataList):
		"""
			Populate the table row
		"""
		nRow = self.ui.tableWidget.rowCount()
		self.ui.tableWidget.insertRow(nRow)
		for i,val in enumerate(dataList):

			if i == 0:
				item = QtGui.QTableWidgetItem()
				item.setFlags(QtCore.Qt.ItemIsUserCheckable |QtCore.Qt.ItemIsEnabled)
				item.setCheckState(QtCore.Qt.Unchecked)
				self.ui.tableWidget.setItem(nRow,i,item)
				self.ui.tableWidget.itemClicked.connect(self.handleItemClicked)
			else:
				item = QtGui.QTableWidgetItem(unicode(val))
				self.ui.tableWidget.setItem(nRow,i,item)

	def handleItemClicked(self, item):
		try:
			if item.checkState() == QtCore.Qt.Checked:
				#QMessageBox.about(self,'test',str(item.row()))
				self.checked_list.append(item.row())
			else:
				self.checked_list.remove(item.row())
		except:
			pass

	def getValues(self):
		"""
			get the table values
		"""
		#QMessageBox.about(self,'chechedlist',str(self.checked_list))
		nRow = self.ui.tableWidget.rowCount()
		nCol = self.ui.tableWidget.columnCount()
		data = []
		for r in range(nRow):
			riga = []
			for c in range(nCol):
				if c == 0:
					if self.checked_list.count(r) != 0:
						#QMessageBox.about(self,'riok',str(r))
						riga.append('ok')
					else:
						riga.append('no')
						#QMessageBox.about(self,'rino',str(r))
				else:
					item = self.ui.tableWidget.item(r,c)

					riga.append(item.text())
			data.append(riga)
		return data

# ------------ georeferencing functions -------------------

	def vecLayGeorefTool(self):
		"""
			attiva/disattiva/switcha il clickTool

			all'inizio (isFirstPnt == False) spegne se necessario il click1 e attiva il click2
			dopo il primo punto spegne il click2 ed attiva il click1
		"""
		if self.firstPntDone:
			# prepara il punto destinazione
			# try to disconnect all signals
			if self.isClickToolActivated == 2:
				self.clickTool2.canvasClicked.disconnect()
			# connect to click signal 1
			QObject.connect(
				self.clickTool1,
				SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"),
				self.vecLayGeoref
			)
			self.isClickToolActivated = 1
			QMessageBox.information(
				self.iface.mainWindow(),
				'vecLayGeoref',
				"ora dammi punto destinazione"
			)
		else:
			# prepara il punto origine
			# try to disconnect all signals
			if self.isClickToolActivated == 1:
				self.clickTool1.canvasClicked.disconnect()
			# connect to click signal 2
			QObject.connect(
				self.clickTool2,
				SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"),
				self.vecLayGeoref
			)
			self.isClickToolActivated = 2
			QMessageBox.information(
				self.iface.mainWindow(),
				'vecLayGeoref',
				"dammi punto origine"
			)

	def vecLayGeoref(self,point):
		"""
		esegue la selezione dei ctp
		quì il primo punto è origine, il secondo destinazione

		NB: controllare che i punti non coincidano
		"""
		if self.isClickToolActivated == 2:
			pnt = snapPoint(self.vLayer,point,self.eps2)
			if pnt:
				self.origX,self.origY = pnt.x(),pnt.y()
#				print "punto origine",self.origX,self.origY
				self.markerList2.append(self.pntHighligth(self.mapPreview,pnt,color=QColor(250,150,0),size=25))
				self.firstPntDone = True
				self.vecLayGeorefTool()
			else:
				QMessageBox.information(
					self.iface.mainWindow(),
					'vecLayGeoref',
					"nessun punto individuato"
				)
		else:
			pnt = snapPoint(self.cLayer,point,self.eps)
			if pnt:
				destX,destY = pnt.x(),pnt.y()
#				print "punto destinazione",destX,destY
				self.markerList1.append(self.pntHighligth(self.canvas,pnt,color=QColor(250,150,0),size=25))
				# accoda alla tabella
				self.insertNewRow(['',self.origX,self.origY,destX,destY])
				# try to disconnect all signals
				if self.isClickToolActivated == 1:
					self.clickTool1.canvasClicked.disconnect()
					self.isClickToolActivated = 0
			else:
				QMessageBox.information(
					self.iface.mainWindow(),
					'vecLayGeoref',
					"nessun punto individuato"
				)
