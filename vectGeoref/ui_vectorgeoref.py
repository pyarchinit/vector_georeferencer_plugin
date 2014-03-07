# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vectorgeoref.ui'
#
# Created: Wed Feb 12 21:46:13 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_VectorGeoref(object):
    def setupUi(self, VectorGeoref):
        VectorGeoref.setObjectName(_fromUtf8("VectorGeoref"))
        VectorGeoref.resize(700, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/vectorgeoref/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        VectorGeoref.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(VectorGeoref)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget = QtGui.QTableWidget(VectorGeoref)
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 161))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(5)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.gridLayout.addWidget(self.tableWidget, 5, 0, 1, 7)
        self.tabWidget = QtGui.QTabWidget(VectorGeoref)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(QtCore.QSize(300, 400))
        self.tabWidget.setMaximumSize(QtCore.QSize(600, 600))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.gridLayout.addWidget(self.tabWidget, 0, 2, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton_load_layer = QtGui.QPushButton(VectorGeoref)
        self.pushButton_load_layer.setObjectName(_fromUtf8("pushButton_load_layer"))
        self.verticalLayout.addWidget(self.pushButton_load_layer)
        self.pushButtonCP_Selection = QtGui.QPushButton(VectorGeoref)
        self.pushButtonCP_Selection.setToolTip(_fromUtf8(""))
        self.pushButtonCP_Selection.setIcon(icon)
        self.pushButtonCP_Selection.setCheckable(True)
        self.pushButtonCP_Selection.setChecked(False)
        self.pushButtonCP_Selection.setObjectName(_fromUtf8("pushButtonCP_Selection"))
        self.verticalLayout.addWidget(self.pushButtonCP_Selection)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_save_CPT = QtGui.QPushButton(VectorGeoref)
        self.pushButton_save_CPT.setObjectName(_fromUtf8("pushButton_save_CPT"))
        self.verticalLayout.addWidget(self.pushButton_save_CPT)
        self.pushButton_read_CPT = QtGui.QPushButton(VectorGeoref)
        self.pushButton_read_CPT.setObjectName(_fromUtf8("pushButton_read_CPT"))
        self.verticalLayout.addWidget(self.pushButton_read_CPT)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.pushButton_clear = QtGui.QPushButton(VectorGeoref)
        self.pushButton_clear.setObjectName(_fromUtf8("pushButton_clear"))
        self.verticalLayout.addWidget(self.pushButton_clear)
        self.pushButton_run = QtGui.QPushButton(VectorGeoref)
        self.pushButton_run.setObjectName(_fromUtf8("pushButton_run"))
        self.verticalLayout.addWidget(self.pushButton_run)
        self.pushButton_quit = QtGui.QPushButton(VectorGeoref)
        self.pushButton_quit.setObjectName(_fromUtf8("pushButton_quit"))
        self.verticalLayout.addWidget(self.pushButton_quit)
        self.gridLayout.addLayout(self.verticalLayout, 0, 4, 1, 1)

        self.retranslateUi(VectorGeoref)
        QtCore.QMetaObject.connectSlotsByName(VectorGeoref)

    def retranslateUi(self, VectorGeoref):
        VectorGeoref.setWindowTitle(QtGui.QApplication.translate("VectorGeoref", "VectorGeoref", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("VectorGeoref", "selected", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("VectorGeoref", "x  origine", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("VectorGeoref", "y  origine", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(QtGui.QApplication.translate("VectorGeoref", "x destinazione", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(QtGui.QApplication.translate("VectorGeoref", "y destinazione", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_load_layer.setText(QtGui.QApplication.translate("VectorGeoref", "Load Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCP_Selection.setText(QtGui.QApplication.translate("VectorGeoref", "add CP", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCP_Selection.setShortcut(QtGui.QApplication.translate("VectorGeoref", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_save_CPT.setText(QtGui.QApplication.translate("VectorGeoref", "CP save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_read_CPT.setText(QtGui.QApplication.translate("VectorGeoref", "CP read", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_clear.setText(QtGui.QApplication.translate("VectorGeoref", "clear", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_run.setText(QtGui.QApplication.translate("VectorGeoref", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_quit.setText(QtGui.QApplication.translate("VectorGeoref", "Quit", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
