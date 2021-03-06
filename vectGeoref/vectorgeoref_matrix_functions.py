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
"""
class Matrix_functions:
	# ------------ matrix functions ------------

	def printMatrix(self, mat):
		nr = len(mat)
		nc = len(mat[0])
		print ' ',
		for c in range(nc):
			print '%5s ' % (c+1),
		print
		print "------" * (nc+2)
		for r in range(nr):
			print r+1, "|",
			for c in range(nc):
				print '%5.2f ' % mat[r][c],
			print
		print "------" * (nc+2)

	def nullMatrix(self, nr,nc):
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

	def adjoint(self, mat1,nr,mat2):
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

	def matrixTranspose(self, mat):
		"""
			esegue la trasposta di una matrice
		"""
		nr = len(mat)
		nc = len(mat[0])
		matT = self.nullMatrix(nc,nr)
		for r in range(nr):
			for c in range(nc):
				matT[c][r] = mat[r][c]
		return matT

	def matrixMultiplication(self, mat1,mat2):
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

	def EchelonNF(self, mat):
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

	def prelievoColonne(self, mat,list):
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

	def lsm2(self, old,new):
		"""
			l(est) s(quare) m(ethod)
			in questa seconda versione anzichè calcolare l'inversa troviamo la soluzione
			dalla echelon form della matrice aggiunta, previa normalizzazione degli elementi
			diagonali;
			#ATTENZIONE: poichè noi accettiamo in generale anche una disposizione dei pivot
			non diagonale, la routine potrebbe dare dei problemi; in caso modificare
		"""
		print "devo far coincidere i punti"
		self.printMatrix(old)
		print "con i punti"
		self.printMatrix(new)
		print "matrice trasposta"
		oldT = self.matrixTranspose(old)
		self.printMatrix(oldT)
		print "matrice normale"
		mat = self.matrixMultiplication(oldT,old)
		self.printMatrix(mat)
		print "Termine noto"
		tn = self.matrixMultiplication(oldT,new)
		self.printMatrix(tn)
		print "matrice aggiunta"
		nr = len(mat)
		mat = self.adjoint(mat,nr,tn)
		self.printMatrix(mat)
		print "Echelon form"
		self.EchelonNF(mat)
		self.printMatrix(mat)
		print "(Experimental) normalization"
		for i in range(nr):
			if abs(mat[i][i] - 1.00) > 0.005:	#ATTENZIONE: noi accettiamo anche una forma con pivot disposti diversamente!
				alfa = 1/mat[i][i]
				print "normalization of row",i,"by factor",alfa
				for k in range(len(mat[i])):
					print "element",k,mat[i][k],
					mat[i][k] = mat[i][k] * alfa
					print "become",mat[i][k]
		self.printMatrix(mat)
		# soluzione
		sol = []
		for i in range(len(tn[0])):	# per ogni colonna del termine noto 
		# ma myList non esiste giò?
			myList = [[0,nr+i]]	# questa strana forma Ã¨ dovuta a precedenti (vedi rank())
			tmp = self.prelievoColonne(mat,myList)
			tmp = self.matrixTranspose(tmp)
			print tmp
			sol.append(tmp[0])	# questa operazione Ã¨ empirica, serve ad eliminare un livello di parentesi, controllare
		self.printMatrix(sol)
		return sol


