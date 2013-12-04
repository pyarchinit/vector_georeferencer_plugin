# -*- coding: utf-8 -*-

"""
/***************************************************************************
point4qgis		A QGIS plugin Tools for managing OGR point vector layers

                             -------------------
        begin                : 2013-11-09
        copyright            : (C) 2013 by giuliano curti
        email                : giulianc51 at gmail dot com
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

# Import standard libraries
import math

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

# none Qt resources to initialize

# Import custom libraries
from genericDlg import genericDlg
from geoReferDlg import geoReferDlg

# ------------general functions ------------

def about(mw,parent):
	"""
		Visualizza info sulla procedura
		presume che parent abbia le variabili: vers,build_date,author,mail,copyright,license
	"""
	QMessageBox.about(
		mw,
		'About',
		"Georeferencer of vector layer for QGIS"
+ "\n----------------------------"
+ "\nversion:      %s" % (parent.vers)
+ "\nbuild_date:   %s" % (parent.build_date)
+ "\nauthor:       %s" % (parent.author)
+ "\ncontributor:  %s" % (parent.contributor)
+ "\ncopyright:    %s" % (parent.copyright)
+ "\nlicense:      %s" % (parent.license)
	)

def info(mw,vers,mail):
	"""
		First advice to users
	"""
	msg = """

	"""

	QMessageBox.about(
		mw,
		'Info',
		"Georeferencer of vector layer for QGIS ("
+ vers
+ ")"
+ "\n-----------------------------------------------"
+ "\nThe procedure allows georeferencing vector"
+ "\nlayer by 1, 2, 3 or more points."
+ "\nThe modified layer is displayed on QGIS canvas"
+ "\nas a new layer allowing the user to control"
+ "\nand retain the new result or reject it if"
+ "\nanything went wrong."
+ "\n"
+ "\nBy opening the python console, You can enjoy"
+ "\nsome useful info from the system."
+ "\n" 
+ "\nThis procedure is EXPERIMENTAL; it might"
+ "\ncontains many bugs, few duplications and some"
+ "\nmistakes, only in part known to the author;"
+ "\n"
+ "\nplease let us know about any encountered"
+ "\nproblems"
+ "\n [" + mail + "]"
	)
	
# ---------- graphics functions ------------

def annotationText(canvas,text,pos):
	"""
		disegna una didascalia a video (purtroppo c'è uno spostamento incomprensibile)
		- canvas	area di disegno
		- text	testo da visualizzare
		- pos		posizione (QgsPoint)
	"""
	myDoc = QTextDocument(text)
	myTxt = QgsTextAnnotationItem(canvas)
	myTxt.setDocument(myDoc)
	myTxt.setMapPosition(pos) 
	canvas.refresh()
	return myTxt

# ------------ matrix functions ------------

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

def identity(n):
	"""
		Restituisce la matrice identitÃ 
		di dimensione n
	"""
	mat = nullMatrix(n,n)
	for i in range (0,n):
		mat[i][i] = 1.0
	return mat

def matTranslation2D(dx,dy):
	"""
		Calcola la matrice di traslazione;
	"""
	return [
		[1.,0.,dx],
		[0.,1.,dy],
		[0.,0.,1.]
	]

def matRotation2D(a):
	"""
		rotazione dell'angolo a [radians]
	"""
	c= math.cos(a)
	s = math.sin(a)
	return [
		[c,-s,0.],
		[s, c,0.],
		[0.,0.,1.]
	]

def adjoint(mat1,nr,mat2):
	"""
		Costruisce la matrice aggiunta composta dalle due matrici in input
		(presume le matrice di pri numero di righe)
	"""
	nc2 = len(mat2[1])
	adj = []
	for i in range(nr):
		tmp = mat1[i][:]
		for j in mat2[i]:
			tmp.append(j)
		adj.append(tmp)
	return adj

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

def matRotoTrasla2D(s1,s2,d1,d2):
	"""
		matrice di collimazione a 2 punti
		s1	vecchio centro
		s2	vecchio punto di allineamento
		d1	nuovo centro
		d2	nuovo punto di allineamento
		rototrasla in XY e trasla in Z
	"""
	s1x,s1y = s1
	s2x,s2y = s2
	d1x,d1y = d1
	d2x,d2y = d2
	# calcola matrice di trasformazione
#	print "trasla s1 nell'origine",-s1x,-s1y
	mat = matTranslation2D(-s1x,-s1y)
	# ruota la linea s1-s2 sull'orizzontale
	a1 = math.atan2(s2y-s1y,s2x-s1x)
	# ruota per allinearla a d1-d2
	a2 = math.atan2(d2y-d1y,d2x-d1x)
#	print "ruota di",a2-a1
	mat1 = matRotation2D(a2-a1)
	mat = matrixMultiplication(mat1,mat)
#	print "trasla nel punto d1",d1x,d1y,d1z
	mat1 = matTranslation2D(d1x,d1y)
	mat = matrixMultiplication(mat1,mat)
	return mat

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

def matrixInvert(mat):
	"""
		calcola l'inversa della matrice

		codici di errore:
			-1	matrice non quadrata
			-2	matrice singolare
	"""
	nr = len(mat)
	nc = len(mat[0])
	if nr == nc:
		if nr == 1:
			mat[0][0] = 1/mat[0][0]
			return mat
		else:
			# crea la matrice aggiunta
			matId = identity(nr)
			mat = adjoint(mat,nr,matId)
			# printMatrix(mat)
			# genera la echelon form
			mat = EchelonNF(mat)
			# printMatrix(mat)
			# calcola il rank (nelle prime nc colonne!)
			rng = rank(mat)
			rk = len(rng)
			# print "Rank =",rk,"colonne del range",rng
			if rk == nr:
				# preleva la parte destra della matrice ridotta
				list = []
				for i in range(nr):
					list.append([i,nr+i])
				# print "lista Ã¨",list
				# deve prelevare la inversa
				mat = prelievoColonne(mat,list)
				return mat
			else:
				# print "la matrice non Ã¨ invertibile"
				return -2
	else:
		# print "matrice non quadrata: non esiste l'inversa!"
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

def rank(mat):
	"""
		calcola i vettori colonna linearmente indipendenti
		e registra la riga e colonna del pivot;
		a rigore non sarebbe necessario registrare la riga, perÃ² voglio sperimentare
		la possibilitÃ  di operare senza swappare le righe pertanto le registro
	"""
	nr = len(mat)
	nc = len(mat[0])
	rng = []
	for i in range(nr):
		# print "riga",i
		for j in range(nc):
			# print "colonna",j
			if mat[i][j] > 1E-10:
				# print "      ",mat[i][j],"Ã¨ un pivot"
				rng.append([i,j])
				break
	return rng

def lsm(old,new):
	"""
		l(est) s(quare) m(ethod)
	"""
#	printMatrix(old)
#	printMatrix(new)
	# calcolo la trasposta
	oldT = matrixTranspose(old)
	mat = matrixMultiplication(oldT,old)
#	printMatrix(mat)
#	print "Termine noto"
	tn = matrixMultiplication(oldT,new)
#	print tn
	#	print "matrice inversa"
	iMat = matrixInvert(mat)
#	printMatrix(iMat)
	sol = []
	for i in range(len(tn)):	# per ogni colonna del termine noto
#		print "---------- calcolo ----------",i
		myList = [[0,i]]	# questa strana forma Ã¨ dovuta a precedenti (vedi rank())
		tmp = prelievoColonne(tn,myList)
#		print "termine noto"
#		printMatrix(tmp)
		solTmp = matrixMultiplication(iMat,tmp)
#		print "soluzione",solTmp
		tmp = matrixTranspose(solTmp)
#		print tmp
		sol.append(tmp[0])	# questa operazione Ã¨ empirica, serve ad eliminare un livello di parentesi, controllare
#	printMatrix(sol)
	return sol

# --------------- classe principale ----------------------

class vectGeoref:

	vers = '0.00'
	build_date = '2013-11-09'
	author = 'giuliano curti (giulianc51 at gmail dot com)'
	contributor = 'giuseppe patti (gpatt at tiscali dot it)'
	copyright = '2013-2014 giuliano curti'
	license = 'GPL v2 (http://www.gnu.org/licenses/gpl-2.0.html)'

	attrList = [QgsField("indice",QVariant.Int)]	#ttributi (semplificati) dei nuovi layer

	markerList = []	# lista dei marcatori (features)
	anTxtList = []		# lista delle annotazioni
	isClickToolActivated = False

	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		# reference to map canvas
		self.canvas = self.iface.mapCanvas()
		# il rubber band deve essere sempre attivo
		self.rubBnd = QgsRubberBand(self.canvas)
		# create our GUI dialog
		self.dlg = QDialog()

	def initGui(self):
		# Create action that will start plugin configuration
		self.action = QAction(QIcon("Icons/vectGeoref.png"),"vectGeoref",self.iface.mainWindow())
		# connect the action to the run method
		QObject.connect(self.action, SIGNAL("triggered()"), self.run)
		# Add toolbar button and menu item
		self.iface.addToolBarIcon(self.action)
		self.iface.addPluginToMenu("vectGeoref", self.action)
#		-------- file menu -----
		mb = QMenuBar(self.dlg)
		mb.setGeometry(0,0,200,30)
#		-------- referencer menu -----
		myMenu = mb.addMenu('Vector georeferencer')
		tmp = QAction(QIcon(''),u'Modalità 1',self.dlg)        
		tmp.triggered.connect(self.vecLayGeorefTool_1) #1
		myMenu.addAction(tmp)
		tmp = QAction(QIcon(''),u'Modalità 2',self.dlg)        
		tmp.triggered.connect(self.vecLayGeorefTool_2)
		myMenu.addAction(tmp)
		# ----------- help menu ----------------
		mHelp = mb.addMenu('Help')
		tmp = QAction(QIcon(''),'About',self.dlg)        
		tmp.triggered.connect(self.about)
		mHelp.addAction(tmp)
		tmp = QAction(QIcon(''),'Info',self.dlg)        
		tmp.triggered.connect(self.info)
		mHelp.addAction(tmp)

	# run method that performs all the real work
	def run(self):
		# display user info
		self.info()
		# connect the layer changed handler to a signal that the TOC layer has changed
		QObject.connect(self.iface,SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.myHandleLayerChange)
		# inizializza i dati sul layer
		self.myHandleLayerChange()
		# out click tool will emit a QgsPoint on every click
		self.clickTool = QgsMapToolEmitPoint(self.canvas)
		# make our clickTool the tool that we'll use for now
		self.canvas.setMapTool(self.clickTool)
		# show the dialog
		self.dlg.show()
		result = self.dlg.exec_()

	def unload(self):
		# rimuove ogni selezione
		if self.cLayer:	# potrebbero non esserci layer attivi
			self.cLayer.removeSelection()
			self.cleanSelection()
			# disconnect the layer changed handler
			self.iface.currentLayerChanged.disconnect()
			# try to disconnect all signals
			if self.isClickToolActivated:
				self.clickTool.canvasClicked.disconnect()
				self.isClickToolActivated = False
		# Remove the plugin menu item and icon
		self.iface.removePluginMenu("vectGeoref",self.action)
		self.iface.removeToolBarIcon(self.action)

	def about(self):
		about(self.iface.mainWindow(),self)

	def info(self):
		info(self.iface.mainWindow(),self.vers,self.author)

	def myHandleLayerChange(self):
		"""
			è un wrapper alla funzione omologa funzione del core
		"""
		if self.iface.activeLayer():
			# registra il layer corrente
			self.cLayer = self.iface.activeLayer()
			# registra il provider
			self.provider = self.cLayer.dataProvider()
			# al cambio del layer stabilisce la tolleranza di ricerca
			self.eps = self.canvas.mapUnitsPerPixel() * 5
		else:
			self.cLayer = ''
			self.provider = ''
			self.eps = 1.0

	def pntHighligth(self,x,y,color=QColor(250,150,0),size=25):
		"""
			attiva il marcatore del punto
			NB: riceve una feature
		"""
		marker = QgsVertexMarker(self.canvas)
		marker.setIconType(QgsVertexMarker.ICON_CROSS)
		marker.setColor(color)
		marker.setIconSize(size)
		marker.setCenter(QgsPoint(x,y))
		marker.show()
		return marker

	def searchFeat(self,point):
		"""
			Seleziona le features individuate con il mouse;
		"""
		# setup the provider select to filter results based on a rectangle
		pntGeom = QgsGeometry.fromPoint(point)
		# scale-dependent buffer of 5 pixels-worth of map units	
		pntBuff = pntGeom.buffer(self.eps,0) 
		rect = pntBuff.boundingBox()
		# create the select statement
#		print"interrogo il layer",self.cLayer.name()
		self.cLayer.select(rect,True)	# prende quelli che intersecano

	def pointCds(self,feat):
		"""
			Restituisce id e coordinate di una feature PUNTO;
			in caso di fallimento restituisce un id = -1.
		"""
		id = feat.id()
		geom = feat.geometry()
		typ = geom.type()	
		if typ == QGis.Point:
			pnt = geom.asPoint()
			x,y = pnt.x(),pnt.y()
		else:
			id,x,y = -1,0.0,0.0
		return int(id),x,y

	def cleanSelection(self):
		"""
			Pulisce lo stack dei selezionati e toglie i marker;
		"""
		# pulisce qualsiasi eventuale selezione
		self.cLayer.removeSelection()
		# elimina i marcatori
		for m in self.markerList:
			self.canvas.scene().removeItem(m)
		self.markerList = []
		# elimina gli annotationText
		for i in self.anTxtList:
			self.canvas.scene().removeItem(i)
		# resetta la rubber band
#		self.rubBnd.reset()
		# rinfresca il video
		self.canvas.refresh()

	def newLayer(self,layType,layName):
		# create Point layer
		self.cLayer = QgsVectorLayer(layType,layName,"memory")
		self.provider = self.cLayer.dataProvider()
		# add fields
		self.provider.addAttributes(self.attrList)
		# aggiunge al registry
		QgsMapLayerRegistry.instance().addMapLayer(self.cLayer)

	def getLayerByName(self,layName):
		for l in self.canvas.layers():
			if l.name() == layName:
				return l
		return -1

# ----------------- functions ------------------------

	def vecLayGeorefTool_1(self):
		"""
			georeferenzazione di layer vettoriali
			il layer affetto dalle operazioni è quello attivo al momento dell'avvio del plugin
			il layer modificato è consegnato in un nuovo layer;
			è compito dell'utente gestire salvataggio e sostituzione
		"""
		dlg = genericDlg('Vector layer georeferentiation',['# control points'])
		dlg.setValues([3])
		dlg.show()
		result = dlg.exec_()
		if result:
			tmp = dlg.getValues()
			self.ctp = int(tmp.pop())
			if self.ctp > 0:
				# try to disconnect all signals
				if self.isClickToolActivated:
					self.clickTool.canvasClicked.disconnect()
					self.isClickToolActivated = False
				# connect to click signal
				QObject.connect(
					self.clickTool,
					SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"),
					self.vecLayGeoref_1
				)
				# inizializza le variabili
				self.sLayer = self.cLayer
				self.sLayerCtp = []
				self.tLayerCtp = []
				self.cleanSelection()
				QMessageBox.information(
					self.iface.mainWindow(),
					'vecLayGeoref',
					"dammi i punti liberamente; quando hai completato il numero di coppie predefinito, eseguo il calcolo"
				)
			else:
				self.iface.messageBar().pushMessage(
					"vecLayGeoref",
					"Devi darmi almeno un punto",
					level=QgsMessageBar.WARNING,
					duration=3
				)

	def vecLayGeoref_1(self,point):
		"""
		esegue la selezione dei ctp
		NB: controllare che i punti non coincidano
		"""
		self.searchFeat(point)
		# è stato selezionato qualche punto?
		if self.cLayer.selectedFeatureCount():
			# se sì lo salvo
			pnts = self.cLayer.selectedFeatures()
			self.cLayer.removeSelection()
			id,x,y = self.pointCds(pnts[0])	# prende solo il primo punto
#			print "feat",id,"of layer",self.cLayer.name()
			# è il layer sorgente?
			if self.cLayer.name() == self.sLayer.name():
				if len(self.sLayerCtp) < self.ctp:
					self.sLayerCtp.append([x,y])
					self.markerList.append(self.pntHighligth(x,y))
					#applica l'annotazione
					msg = 's%d' % (len(self.sLayerCtp))
					tmp = annotationText(self.canvas,msg,QgsPoint(x,y))
					self.anTxtList.append(tmp)
					self.vecLayGeorefExecute_1()
				else:
					QMessageBox.information(
						self.iface.mainWindow(),
						'vecLayGeoref',
						"ok, the source ctp are yet ready"
					)
					self.vecLayGeorefExecute_1()
			# è il layer sorgente?
			else:
				if len(self.tLayerCtp) < self.ctp:
					self.tLayerCtp.append([x,y])
					self.markerList.append(self.pntHighligth(x,y))
					#applica l'annotazione
					msg = 't%d' % (len(self.tLayerCtp))
					tmp = annotationText(self.canvas,msg,QgsPoint(x,y))
					self.anTxtList.append(tmp)
					self.vecLayGeorefExecute_1()
				else:
					QMessageBox.information(
						self.iface.mainWindow(),
						'vecLayGeoref',
						"ok, the target ctp are yet ready"
					)
					self.vecLayGeorefExecute_1()

	def vecLayGeorefExecute_1(self):
		"""
			esegue la trasformazione
		"""
		# controlla se ci sono tutti i punti
		if len(self.sLayerCtp) >= self.ctp and len(self.tLayerCtp) >= self.ctp:
			msg = "Control terrain points report"
			msg= msg + "\nn               source                               target"
			msg= msg + "\n                X                  Y                 X                 Y"
			msg= msg + "\n----------------------------------------------------------"
			for i in range(self.ctp):
				tmpS = self.sLayerCtp[i]
				tmpT = self.tLayerCtp[i]
				msg = msg + "\n%d %12.3f %12.3f %12.3f %12.3f"% (i,tmpS[0],tmpS[1],tmpT[0],tmpT[1])
			QMessageBox.information(
				self.iface.mainWindow(),
				'vecLayGeoref',
				msg
			)
			# esegue l'operazione
			if self.ctp == 1:
				# calcolo i parametri
				s1x,s1y = self.sLayerCtp[0]
				d1x,d1y = self.tLayerCtp[0]
				mat = matTranslation2D(d1x-s1x,d1y-s1y)
				title = self.sLayer.name()+'_1'
			elif self.ctp == 2:
				# calcolo i parametri
				s1 = self.sLayerCtp[0]
				s2 = self.sLayerCtp[1]
				d1 = self.tLayerCtp[0]
				d2 = self.tLayerCtp[1]
				mat = matRotoTrasla2D(s1,s2,d1,d2)
				title = self.sLayer.name()+'_2ss'
			else:
				for i in self.sLayerCtp:
					i.append(1.0)	#aggiunge la coordinata omogenea
				for i in self.tLayerCtp:
					i.append(1.0)	#aggiunge la coordinata omogenea
				mat = lsm(self.sLayerCtp,self.tLayerCtp)
				print mat
				title = self.sLayer.name()+'_3'
			# crea nuovo layer
			self.newLayer('Point',title)
			# e lo mette in editing mode
			self.cLayer.startEditing()	# il nuovo layer è adesso registrato in self.cLayer
			# duplica il layer sorgente nel nuovo
			for feat in self.sLayer.getFeatures():
				self.cLayer.addFeatures([feat])
			# modifica la geometria del nuovo
			for feat in self.cLayer.getFeatures():
				# legge la geometria
				id,x,y = self.pointCds(feat)
				# trasforma la geometria
				tmp = matrixMultiplication(mat,[[x],[y],[1.0]])	# NB. forzato a vettore colonna
				print"feature",id,tmp
				geom = QgsGeometry.fromPoint(QgsPoint(tmp[0][0],tmp[1][0]))
				self.cLayer.changeGeometry(id,geom)
			# Commit changes
			self.cLayer.commitChanges()
			# canvas refresh
			self.canvas.refresh()
			# pulisce i markers
			self.cleanSelection()
			# try to disconnect all signals
			if self.isClickToolActivated:
				self.clickTool.canvasClicked.disconnect()
				self.isClickToolActivated = False

	def vecLayGeorefTool_2(self):
		"""
			georeferenzazione di layer vettoriali
		"""
		# try to disconnect all signals
		if self.isClickToolActivated:
			self.clickTool.canvasClicked.disconnect()
			self.isClickToolActivated = False
		# connect to click signal
		QObject.connect(
			self.clickTool,
			SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"),
			self.vecLayGeoref_2
		)
		# inizializza le variabili
		self.sLayer = self.cLayer
		self.sLayerCtp = []
		self.tLayerCtp = []
		self.cleanSelection()
		self.isFirst = True
		QMessageBox.information(
			self.iface.mainWindow(),
			'vecLayGeoref',
			"dammi le coppie di punti; quando hai finito premi Done."
			+ u"\n(NB: la correzione da tastiera non è ancora attiva)"
		)

	def vecLayGeoref_2(self,point):
		"""
		esegue la selezione dei ctp
		quì il primo punto è origine, il secondo destinazione

		NB: controllare che i punti non coincidano
		"""
		self.searchFeat(point)
		# è stato selezionato qualche punto?
		if self.cLayer.selectedFeatureCount():
			# se sì lo salvo
			pnts = self.cLayer.selectedFeatures()
			self.cLayer.removeSelection()
			id,x,y = self.pointCds(pnts[0])	# prende solo il primo punto
			self.markerList.append(self.pntHighligth(x,y))
#			print "feat",id,"of layer",self.cLayer.name()
			# lo mette nella lista giusta
			if self.isFirst:
				self.isFirst =  False
				self.sLayerCtp.append([x,y])
				# applica l'annotazione
				msg = 's%d' % (len(self.sLayerCtp))
				tmp = annotationText(self.canvas,msg,QgsPoint(x,y))
				self.anTxtList.append(tmp)
			else:
				self.isFirst =  True
				self.tLayerCtp.append([x,y])
				# applica l'annotazione
				msg = 't%d' % (len(self.tLayerCtp))
				tmp = annotationText(self.canvas,msg,QgsPoint(x,y))
				self.anTxtList.append(tmp)
				# dialogo
				dlg = geoReferDlg(self.iface.mapCanvas().layers(),self.sLayerCtp,self.tLayerCtp)
				dlg.show()
				dlg.exec_()
				res = dlg.getRes()
				if res == -1:
					print "---- cancel -----"
					# pulisce i markers
					self.cleanSelection()
					# try to disconnect all signals
					if self.isClickToolActivated:
						self.clickTool.canvasClicked.disconnect()
						self.isClickToolActivated = False
				elif res == 1:
					layer = dlg.getLayer()
					self.sLayer = self.getLayerByName(layer)
					if self.sLayer != -1:
						# prelevare self.sLayerCtp,self.tLayerCtp per intercettare
						# eventuali modifiche da tastiera
						print "eseguo il calcolo sul layer:",self.sLayer
						self.vecLayGeorefExecute_2()
					else:
						self.iface.messageBar().pushMessage(
							"openEDM",
							"il layer"+layer+"non esiste",
							level=QgsMessageBar.CRITICAL,
							duration=3
						)
				else:
					print "aspetto altri punti"

	def vecLayGeorefExecute_2(self):
		"""
			esegue la trasformazione
		"""
		# esegue l'operazione
		if len(self.sLayerCtp) == 1:
			# calcolo i parametri
			s1x,s1y = self.sLayerCtp[0]
			d1x,d1y = self.tLayerCtp[0]
			mat = matTranslation2D(d1x-s1x,d1y-s1y)
			title = self.sLayer.name()+'_1'
		elif len(self.sLayerCtp) == 2:
			# calcolo i parametri
			s1 = self.sLayerCtp[0]
			s2 = self.sLayerCtp[1]
			d1 = self.tLayerCtp[0]
			d2 = self.tLayerCtp[1]
			mat = matRotoTrasla2D(s1,s2,d1,d2)
			title = self.sLayer.name()+'_2ss'
		else:
			for i in self.sLayerCtp:
				i.append(1.0)	#aggiunge la coordinata omogenea
			for i in self.tLayerCtp:
				i.append(1.0)	#aggiunge la coordinata omogenea
			mat = lsm(self.sLayerCtp,self.tLayerCtp)
			print mat
			title = self.sLayer.name()+'_3'
		# crea nuovo layer
		self.newLayer('Point',title)
		# e lo mette in editing mode
		self.cLayer.startEditing()	# il nuovo layer è adesso registrato in self.cLayer
		# duplica il layer sorgente nel nuovo
		for feat in self.sLayer.getFeatures():
			self.cLayer.addFeatures([feat])
		# modifica la geometria del nuovo
		for feat in self.cLayer.getFeatures():
			# legge la geometria
			id,x,y = self.pointCds(feat)
			# trasforma la geometria
			tmp = matrixMultiplication(mat,[[x],[y],[1.0]])	# NB. forzato a vettore colonna
			print"feature",id,tmp
			geom = QgsGeometry.fromPoint(QgsPoint(tmp[0][0],tmp[1][0]))
			self.cLayer.changeGeometry(id,geom)
		# Commit changes
		self.cLayer.commitChanges()
		# canvas refresh
		self.canvas.refresh()
		# pulisce i markers
		self.cleanSelection()
		# try to disconnect all signals
		if self.isClickToolActivated:
			self.clickTool.canvasClicked.disconnect()
			self.isClickToolActivated = False


