# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VectorGeorefDialog
                                 A QGIS plugin
 A visual tool to georeferencing vector layers
                             -------------------
        begin                : 2013-11-11
        updated              : 2014-02-10 (027)
        copyright            : (C) 2013 by Giuliano Curti
        email                : giulianc51@gmail.com
 ***************************************************************************/

usare lo stesso formato dei CTP del georef raster
usare anche ON/OFF per la checkbox dei CP
eliminare il layer dall'elenco degli snap quando lo si elimina dal canvas2
attivare/eliminare tasto QUIT dalla dialog form

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
027	2014-02-10
	settaggio del CRS corretto del nuovo layer (CRS corrente)
	uso dello snapper nativo

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

from vectorgeoref_matrix_functions import Matrix_functions
# ================= classe principale ================

class VectorGeorefDialog(QtGui.QDialog, Matrix_functions):
	vLayer = ""
	mapPreview = ""
	markerList1 = []	# lista dei marcatori del canvas1
	markerList2 = []	# lista dei marcatori del canvas2
	anTxtList = []		# lista delle annotazioni

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
			# azzera la tabella dei CP
			self.on_pushButton_clear_pressed()

	def on_pushButton_run_pressed(self):
		# legge i dati della tabella...
		tmp = self.getValues()
		#  .. e li deposita nelle due liste
		srcPntList = []
		dstPntList = []
		for [check,oX,oY,dX,dY] in tmp:
			if check == 'ok':
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
					newLayer = self.cloneLayer(self.vLayer,vtype[gT],lN)
					# calcola la matrice ai minimi quadrati
					mat = self.lsm2(srcPntList,dstPntList)
#					self.printMatrix(mat)
					if gT == 0:
#						print "layer puntuale"
						self.pointTransform(newLayer,mat)
					elif gT == 1:
#						print "layer lineare"
						self.lineTransform(newLayer,mat)
					elif gT == 2:
#						print "layer poligonale"
						self.polygTransform(newLayer,mat)
					# Commit changes
					newLayer.commitChanges()
					# set CRS
					render = self.canvas.mapRenderer()
					curCrs = render.destinationCrs()
					newLayer.setCoordinateSystem(curCrs)
					# update layer's extent
					newLayer.updateExtents()
					# user warning
					self.iface.messageBar().pushMessage(
						"on_pushButton_run_pressed",
						"Layer in memory, save it!",
						level=QgsMessageBar.INFO,
						duration=4
					)
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

	def on_pushButton_save_CPT_pressed(self):
		"""
			salva i CTP su file
		"""
		if self.vLayer:
			# legge i dati della tabella...
			tmp = self.getValues()
			# crea il file di output
			fname = self.vLayer.name() + '.ctp'
			f = open(fname,'w')
			if f:
				# salva i CRS (source & dest) coinvolti
				srcCrs = self.vLayer.crs().authid()
				curCrs = self.canvas.mapRenderer().destinationCrs().authid()
				f.write("%s %s\n" %(srcCrs,curCrs))
				#  .. e salva i punti
				for [check,oX,oY,dX,dY] in tmp:
					f.write("%s %s %s %s %s\n" % (check,oX,oY,dX,dY))
				f.close()
				self.iface.messageBar().pushMessage(
					"on_pushButton_save_pressed",
					"C(ontrol) T(errain) Points salvati su "+fname,
					level=QgsMessageBar.INFO,
					duration=3
				)
			else:
				self.iface.messageBar().pushMessage(
					"on_pushButton_save_pressed",
					"errore: impossibile aprire il file"+fname,
					level=QgsMessageBar.CRITICAL,
					duration=3
				)
		else:
			self.iface.messageBar().pushMessage(
				"on_pushButton_save_pressed",
				"errore: devi prima aprire il layer e definire i punti di controllo",
				level=QgsMessageBar.CRITICAL,
				duration=3
			)

	def on_pushButton_read_CPT_pressed(self):
		"""
			legge i CTP salvati su file
		"""
		if self.vLayer:
			# pulisce la maschera
			self.on_pushButton_clear_pressed()
			# legge il file di input
			fname = QFileDialog.getOpenFileName(self.iface.mainWindow(),'Open file','/home/giuliano','*.ctp')
			if fname:
				f = open(fname,'r')
				if f:
					tmp = f.readline()
					srcCrs,curCrs = tmp.split(' ')
					srcCrs = srcCrs.rstrip()
					curCrs = curCrs.rstrip()
					if srcCrs != self.vLayer.crs().authid():
						self.iface.messageBar().pushMessage(
							"on_pushButton_read_pressed",
							"errore: il CRS di provenienza non coincide con quello del layer da trasformare",
							level=QgsMessageBar.CRITICAL,
							duration=3
						)
					elif curCrs != self.canvas.mapRenderer().destinationCrs().authid():
						self.iface.messageBar().pushMessage(
							"on_pushButton_read_pressed",
							"errore: il CRS di destinazione non coincide con quello quello corrente",
							level=QgsMessageBar.CRITICAL,
							duration=3
						)
					else:
						for tmp in f:
							check,origX,origY,destX,destY = tmp.split()
							self.insertNewRow([check,origX,origY,destX,destY])
							vertex = QgsPoint(float(origX),float(origY))
							self.markerList2.append(self.pntHighligth(self.mapPreview,vertex,color=QColor(250,150,0),size=25))
							vertex = QgsPoint(float(destX),float(destY))
							self.markerList1.append(self.pntHighligth(self.canvas,vertex,color=QColor(250,150,0),size=25))
				else:
					self.iface.messageBar().pushMessage(
						"on_pushButton_read_pressed",
						"errore: impossibile aprire il file"+fname,
						level=QgsMessageBar.CRITICAL,
						duration=3
					)
			else:
				self.iface.messageBar().pushMessage(
					"on_pushButton_read_pressed",
					"errore: dammi un file valido",
					level=QgsMessageBar.CRITICAL,
					duration=3
				)	
		else:
			self.iface.messageBar().pushMessage(
				"on_pushButton_save_pressed",
				"errore: devi prima aprire il layer e definire i punti di controllo",
				level=QgsMessageBar.CRITICAL,
				duration=3
			)

# ----------- utility functions ----------------

	def myHandleLayerChange(self):
		if self.iface.activeLayer():
			# registra il layer corrente
			self.cLayer = self.iface.activeLayer()

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
			item = QtGui.QTableWidgetItem(unicode(val))
			self.ui.tableWidget.setItem(nRow,i,item)

	def getValues(self):
		"""
			get the table values
		"""
		nRow = self.ui.tableWidget.rowCount()
		nCol = self.ui.tableWidget.columnCount()
		data = []
		for r in range(nRow):
			riga = []
			for c in range(nCol):
				item = self.ui.tableWidget.item(r,c)
				print item.text()
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
			# trasforma in screen coordinates
			newPoint = self.mapPreview.getCoordinateTransform().transform(point)
			# .. e in QPoint
			pnt = QPoint(newPoint.x(),newPoint.y())
			# attiva lo snapper
			mySnapper = QgsMapCanvasSnapper(self.mapPreview)
			(reval, snapped) = mySnapper.snapToBackgroundLayers(pnt)
			if snapped != []:
				vertex = QgsPoint(snapped[0].snappedVertex.x(), snapped[0].snappedVertex.y())
				self.origX,self.origY = vertex.x(),vertex.y()
#				print "punto origine",self.origX,self.origY
				self.markerList2.append(self.pntHighligth(self.mapPreview,vertex,color=QColor(250,150,0),size=25))
				self.firstPntDone = True
				self.vecLayGeorefTool()
			else:
				QMessageBox.information(
					self.iface.mainWindow(),
					'vecLayGeoref',
					"nessun punto individuato"
				)
		else:
			# trasforma in screen coordinates
			newPoint = self.canvas.getCoordinateTransform().transform(point)
			# .. e in QPoint
			pnt = QPoint(newPoint.x(),newPoint.y())
			# attiva lo snapper
			mySnapper = QgsMapCanvasSnapper(self.canvas)
			(reval, snapped) = mySnapper.snapToCurrentLayer(pnt,QgsSnapper.SnapToVertex)
			if snapped != []:
				vertex = QgsPoint(snapped[0].snappedVertex.x(), snapped[0].snappedVertex.y())
				destX,destY = vertex.x(),vertex.y()
#				print "punto destinazione",destX,destY
				self.markerList1.append(self.pntHighligth(self.canvas,vertex,color=QColor(250,150,0),size=25))
				# accoda alla tabella
				self.insertNewRow(['ok',self.origX,self.origY,destX,destY])
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

	# -------- layer functions -------

	def cloneLayer(self, oldLayer,type,name):
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

	def pointTransform(self, layer,matrix):
		"""
			Esegue la trasformazione di un layer puntuale
			questa forma non mi piace però la gestione degli attributi è
			piuttosto ostica e questa sembra funzionare
		"""
		for feat in layer.getFeatures():
			geom = feat.geometry()
			p = geom.asPoint()
			cds = self.matrixMultiplication(matrix,[[p.x()],[p.y()],[1]])
	#		print cds
			geom = QgsGeometry.fromPoint(QgsPoint(cds[0][0],cds[1][0]))
			layer.changeGeometry(feat.id(),geom)

	def lineTransform(self, layer,matrix):
		"""
			Esegue la trasformazione di un layer lineare
		"""
		for feat in layer.getFeatures():
			geom = feat.geometry()
			line = geom.asPolyline()
			# costruisce la nuova
			newLine = []
			for p in line:
				cds = self.matrixMultiplication(matrix,[[p.x()],[p.y()],[1]])
	#			print cds
				newLine.append(QgsPoint(cds[0][0],cds[1][0]))
			geom = QgsGeometry.fromPolyline(newLine)
			layer.changeGeometry(feat.id(),geom)

	def polygTransform(self, layer,matrix):
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
					cds = self.matrixMultiplication(matrix,[[v.x()],[v.y()],[1]])
	#				print cds
					newLine.append(QgsPoint(cds[0][0],cds[1][0]))
				# aggiorna la geometria
				newPlgns.append(newLine)
			geom = QgsGeometry.fromPolygon(newPlgns)
			layer.changeGeometry(feat.id(),geom)
