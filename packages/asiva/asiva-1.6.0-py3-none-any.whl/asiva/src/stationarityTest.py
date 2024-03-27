#IMPORTING REQUIRED MODULES
import sys
import glob
import os, subprocess
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QFileDialog, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QApplication, QMessageBox, QProgressBar, QTableWidget, 
                            QTableWidgetItem, QComboBox)                           
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.signal import detrend
from scipy import signal
import numpy as np
from statsmodels.tsa.stattools import adfuller
from sklearn.impute import SimpleImputer
from pyts.preprocessing import InterpolationImputer
import datetime
import time
import qtawesome as qta
from asiva.src.home import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
sns.set()
plt.style.use('seaborn-ticks')

#CREATING SUBCLASS OF QWIDGET
class Stationarity(QWidget):
    def __init__(self):
        super(Stationarity, self).__init__()
        self.setWindowTitle('Stationarity Test')
        
#ADDING QWIDGETS IN GUI-- SETTING THE LAYOUT
        horizontalLayout = QHBoxLayout()
        
        verticalLayout = QVBoxLayout()

        search_icon = qta.icon('fa5s.search',
                        color='white')

        erase_icon = qta.icon('fa5s.eraser',
                        color='white')

        handle_icon = qta.icon('fa5s.check',
                        color='white')

        detrend_icon = qta.icon('fa5s.location-arrow',
                        color='white')

        folder_icon = qta.icon('fa5s.folder-open',
                        color='white')

        files_icon = qta.icon('fa5s.eye',
                        color='#2196f3')

        tips_icon = qta.icon('fa5s.lightbulb',
                        color='#e8a92c')
        
        self.loadDirectory = QPushButton("Select Light Curve Directory")
        self.loadDirectory.setIcon(folder_icon)
        self.loadDirectory.setIconSize(QSize(30, 30))
        self.loadDirectory.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #7ebdbd;\n"
                                    "width:100%;\n"
                                    "min-height:40px;\n"
                                    "margin-top:10px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #568585;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "")

        self.directoryLabel = QLabel()
        self.directoryLabel.setWordWrap(True)
        self.directoryLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #ff9800;\n"
                                    "width:100%;\n"
                                    "margin-top:5px;\n"
                                    "}\n"
                                    "")

        self.shapeLabel = QLabel()
        self.shapeLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #007427;\n"
                                    "}\n"
                                    "")

        self.checkm = QPushButton("Check Missing Values")
        self.checkm.setIcon(search_icon)
        self.checkm.setIconSize(QSize(30, 30))
        self.checkm.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "width:100%;\n"
                                    "margin-top:10px;\n"
                                    "min-height:40px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius: 5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#66d7e5;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        self.missInfo = QLabel()
        self.missInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#00bcd4;"
                                    "}\n"
                                    "")

        self.immet = QLabel('Impute Strategy')
        self.immet.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "margin-bottom:5px;\n"
                                    "}\n"
                                    "")

        self.strategy = QComboBox()
        self.strategy.setStyleSheet(u"QComboBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:100%;\n"
                                    "min-height:40px;\n"
                                    "padding-left:5px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QComboBox:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "QComboBox:disabled {\n"
                                    "background-color:#cccccc;\n"
                                    "color:gray;\n"
                                    "border:none;\n"
                                    "}\n"
                                    "")

        self.strategy.addItem("--Select--")
        self.strategy.addItem("Mean")
        self.strategy.addItem("Median")
        self.strategy.addItem("Backward Fill")
        self.strategy.addItem("Forward Fill")
        self.strategy.addItem("Most Frequent")
        self.strategy.addItem("Linear Interpolate")
        self.strategy.addItem("Quadratic Interpolate")
        self.strategy.addItem("Cubic Interpolate")

        self.handlem = QPushButton("Handle Missing Values")
        self.handlem.setIcon(handle_icon)
        self.handlem.setIconSize(QSize(30, 30))
        self.handlem.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #4caf50;\n"
                                    "width:100%;\n"
                                    "min-height:40px;\n"
                                    "margin-top:5px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius: 5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #398714;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#88bb8a;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        self.handlelabel = QLabel()
        self.handlelabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#4caf50;\n"
                                    "}\n"
                                    "")

        self.coutliers = QPushButton("Check Outliers")
        self.coutliers.setIcon(search_icon)
        self.coutliers.setIconSize(QSize(30, 30))
        self.coutliers.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "width:100%;\n"
                                    "margin-top:10px;\n"
                                    "min-height:40px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius: 5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#66d7e5;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        self.outlabel = QLabel()
        self.outlabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#00bcd4;\n"
                                    "}\n"
                                    "")
        
        self.handleo = QPushButton("Remove Outliers")
        self.handleo.setIcon(erase_icon)
        self.handleo.setIconSize(QSize(30, 30))
        self.handleo.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #f44336;\n"
                                    "width:100%;\n"
                                    "min-height:40px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius: 5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #cc4f41;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#f88e86;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        self.progress1 = QProgressBar()
        self.progress1.setMinimum(0)
        self.progress1.setMaximum(0)
        self.progress1.setStyleSheet(u"QProgressBar\n"
                                    "{\n"
                                    "   border: 2px solid  rgb(55, 65, 73);\n"
                                    "   color:rgb(84, 84, 84);\n"
                                    "width:100%;\n"
                                    "text-align:center;\n"
                                    "    border-radius: 5px;\n"
                                    "    background-color: #FAFAFA;\n"
                                    "}\n"
                                    "QProgressBar::chunk \n"
                                    "{\n"
                                    "    background-color: #80CBC4;\n"
                                    "    width: 7px; \n"
                                    "    margin: 0.5px;\n"
                                    "} ")

        self.handleolabel = QLabel()
        self.handleolabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#f44336;\n"
                                    "}\n"
                                    "")

        self.progress2 = QProgressBar()
        self.progress2.setMinimum(0)
        self.progress2.setMaximum(0)
        self.progress2.setStyleSheet(u"QProgressBar\n"
                                    "{\n"
                                    "   border: 2px solid  rgb(55, 65, 73);\n"
                                    "   color:rgb(84, 84, 84);\n"
                                    "width:100%;\n"
                                    "text-align:center;\n"
                                    "    border-radius: 5px;\n"
                                    "    background-color: #FAFAFA;\n"
                                    "}\n"
                                    "QProgressBar::chunk \n"
                                    "{\n"
                                    "    background-color: #80CBC4;\n"
                                    "    width: 7px; \n"
                                    "    margin: 0.5px;\n"
                                    "} ")

        self.checkst = QPushButton("Check Stationarity")
        self.checkst.setIcon(search_icon)
        self.checkst.setIconSize(QSize(30, 30))
        self.checkst.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "width:100%;\n"
                                    "min-height:40px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius: 5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#66d7e5;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        self.stationaritylabel = QLabel()
        self.stationaritylabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#00bcd4;\n"
                                    "}\n"
                                    "")

        self.detrend = QPushButton("Detrend Data")
        self.detrend.setIcon(detrend_icon)
        self.detrend.setIconSize(QSize(30, 30))
        self.detrend.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #4caf50;\n"
                                    "width:100%;\n"
                                    "min-height:40px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius: 5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #398714;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#88bb8a;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        self.handlelabel1 = QLabel()
        self.handlelabel1.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#4caf50;\n"
                                    "}\n"
                                    "")

        self.viewfile = QPushButton("View Files")
        self.viewfile.setIcon(files_icon)
        self.viewfile.setIconSize(QSize(30, 30))
        self.viewfile.setStyleSheet(u"QPushButton{\n"
                                    "width:100%;\n"
                                    "min-height:40px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border:2px solid #2196f3;\n"
                                    "border-radius: 5px;\n"
                                    "color: #2196f3;\n"
                                    "}\n"
                                    "\n"
                                    #"QPushButton:hover{\n"
                                    #"border:2px solid #568585;\n"
                                    #"color:white;\n"
                                    #"}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#8ad1d1;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        horizontalLayout10 = QHBoxLayout()
        horizontalLayout10.setAlignment(Qt.AlignBottom)
        self.tips = QPushButton('Tips!')
        self.tips.setIcon(tips_icon)
        self.tips.setIconSize(QSize(30, 30))
        self.tips.setStyleSheet(u"QPushButton{\n"
                                    "width:100%;\n"
                                    "border:2px solid #e8a92c;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius: 5px;\n"
                                    "color: #e8a92c;\n"
                                    "}\n"
                                    "\n"
                                    #"QPushButton:hover{\n"
                                    #"border:2px solid #2196f3;\n"
                                    #"}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#8ad1d1;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        horizontalLayout10.addWidget(self.tips)

        horizontalLayout9 = QHBoxLayout()
        horizontalLayout9.setAlignment(Qt.AlignBottom)
        self.reset = QPushButton('Reset Workspace')
        self.reset.setStyleSheet(u"QPushButton{\n"
                                    "border: none;\n"
                                    "color:red;\n"
                                    "font:18px;\n"
                                    "width:100%;\n"
                                    "text-align:left;\n"
                                    "font-weight:bold;\n"
                                    "max-height:35px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "color:#7ebdbd;\n"
                                    "}\n"
                                    "")
        
        horizontalLayout9.addWidget(self.reset)

        verticalLayout.addWidget(self.loadDirectory)
        self.progress3 = QProgressBar()
        self.progress3.setMinimum(0)
        self.progress3.setMaximum(0)
        self.progress3.setStyleSheet(u"QProgressBar\n"
                                    "{\n"
                                    "   border: 2px solid  rgb(55, 65, 73);\n"
                                    "   color:rgb(84, 84, 84);\n"
                                    "width:100%;\n"
                                    "text-align:center;\n"
                                    "    border-radius: 5px;\n"
                                    "    background-color: #FAFAFA;\n"
                                    "}\n"
                                    "QProgressBar::chunk \n"
                                    "{\n"
                                    "    background-color: #80CBC4;\n"
                                    "    width: 7px; \n"
                                    "    margin: 0.5px;\n"
                                    "} ")
        verticalLayout.addWidget(self.progress3)
        verticalLayout.addWidget(self.directoryLabel)
        verticalLayout.addWidget(self.shapeLabel)
        verticalLayout.addWidget(self.checkm)
        verticalLayout.addWidget(self.missInfo)
        verticalLayout.addWidget(self.immet)
        verticalLayout.addWidget(self.strategy)
        verticalLayout.addWidget(self.handlem)
        verticalLayout.addWidget(self.handlelabel)
        verticalLayout.addWidget(self.coutliers)
        verticalLayout.addWidget(self.outlabel)
        verticalLayout.addWidget(self.handleo)
        verticalLayout.addWidget(self.handleolabel)
        verticalLayout.addWidget(self.progress1)
        verticalLayout.addWidget(self.checkst)
        verticalLayout.addWidget(self.stationaritylabel)
        verticalLayout.addWidget(self.detrend)
        verticalLayout.addWidget(self.progress2)
        verticalLayout.addWidget(self.handlelabel1)
        verticalLayout.addWidget(self.viewfile)
        verticalLayout.addStretch()

        
        verticalLayout2 = QVBoxLayout()

        self.dataTableLabel = QLabel("Missing Value Data")
        self.dataTableLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "text-decoration:underline;\n"
                                    "}\n"
                                    "")

        self.dataTable = QTableWidget()
        self.dataTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.dataTable.horizontalHeader().setStyleSheet("QHeaderView { font-weight: bold; }")
        self.dataTable.setColumnCount(0)
        self.dataTable.setRowCount(0)
        self.dataTable.setStyleSheet(u"QTableWidget{\n"
                                    "min-width:0px;\n"
                                    "max-width:100%;\n"
                                    "min-height:40%\n"
                                    "font:13px;\n"
                                    "}\n"
                                    "")

        self.dataTableLabel1 = QLabel("Outliers Data")
        self.dataTableLabel1.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "text-decoration:underline;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "")

        self.dataTable2 = QTableWidget()
        self.dataTable2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.dataTable2.horizontalHeader().setStyleSheet("QHeaderView { font-weight: bold; }")
        self.dataTable2.setColumnCount(0)
        self.dataTable2.setRowCount(0)
        self.dataTable2.setStyleSheet(u"QTableWidget{\n"
                                    "min-width:0px;\n"
                                    "max-width:100%;\n"
                                    "min-height:40%\n"
                                    "font:13px;\n"
                                    "}\n"
                                    "")

        verticalLayout2.addWidget(self.dataTableLabel)
        verticalLayout2.addWidget(self.dataTable)
        verticalLayout2.addWidget(self.dataTableLabel1)
        verticalLayout2.addWidget(self.dataTable2)

        verticalLayout1 = QVBoxLayout()

        self.adfinfo = QLabel()
        self.adfinfo.setAlignment(Qt.AlignCenter)
        self.adfinfo.setStyleSheet(u"QLabel{\n"
                                    "text-decoration: underline;\n"
                                    "min-height:40px;\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "")

        self.statinfo = QLabel()
        self.statinfo.setStyleSheet(u"QLabel{\n"
                                    "background-color:red;\n"
                                    "margin-bottom:20px;\n"
                                    "min-height:35px;\n"
                                    "max-width:200px;\n"
                                    "padding-left:12px;\n"
                                    "font:13px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "")
        
        self.dataTable1 = QTableWidget()
        self.dataTable1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.dataTable1.horizontalHeader().setStyleSheet("QHeaderView { font-weight: bold; }")
        self.dataTable1.setColumnCount(0)
        self.dataTable1.setRowCount(0)
        self.dataTable1.setStyleSheet(u"QTableWidget{\n"\
                                    "font:13px;\n"
                                    "width:100%;\n"
                                    "}\n"
                                    "")
        
        verticalLayout1.addWidget(self.adfinfo)
        verticalLayout1.addWidget(self.statinfo)
        verticalLayout1.addWidget(self.dataTable1)
        verticalLayout.addStretch(1)
        
        verticalLayout.addLayout(horizontalLayout10)
        verticalLayout.addLayout(horizontalLayout9)
        horizontalLayout.addLayout(verticalLayout,1)
        horizontalLayout.addLayout(verticalLayout2)
        horizontalLayout.addLayout(verticalLayout1,4)
         
        self.setLayout(horizontalLayout)

#CONNECTING SIGNALS
        self.loadDirectory.clicked.connect(self.loadfolder)
        self.checkm.clicked.connect(self.checkmissing)
        self.handlem.clicked.connect(self.impute)
        self.coutliers.clicked.connect(self.checkol)
        self.handleo.clicked.connect(self.handleol)
        self.checkst.clicked.connect(self.checkstat)
        self.detrend.clicked.connect(self.dtrend)
        self.viewfile.clicked.connect(self.finalfile)
        self.strategy.activated[str].connect(self.checkimp)
        self.reset.clicked.connect(self.resetWorkspace)
        self.tips.clicked.connect(self.tipsAndTricks)
        
#SETTING DEFAULT STATE OF SOME QWIDGETS
        self.progress1.setVisible(False)
        self.progress2.setVisible(False)
        self.progress3.setVisible(False)
        self.loadDirectory.setEnabled(True)
        self.checkm.setEnabled(False)
        self.handlem.setEnabled(False)
        self.handlem.setEnabled(False)
        self.coutliers.setEnabled(False)
        self.handleo.setEnabled(False)
        self.checkst.setEnabled(False)
        self.detrend.setEnabled(False)
        self.viewfile.setVisible(False)
        self.adfinfo.setVisible(False)
        self.statinfo.setVisible(False)
        self.dataTable.setVisible(False)
        self.dataTable1.setVisible(False)
        self.dataTable2.setVisible(False)
        self.strategy.setEnabled(False)
        self.dataTableLabel.setVisible(False)
        self.dataTableLabel1.setVisible(False)

#Function for viewing Tips
    def tipsAndTricks(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("COMING SOON")
        msg.setWindowTitle("Information")
        msg.exec_()

#FUNCTION TO RESET UI
    def resetWorkspace(self):
        self.checkm.setEnabled(False)
        self.directoryLabel.clear()
        self.shapeLabel.clear()
        self.dataTable.setVisible(False)
        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(0)
        self.dataTable1.setVisible(False)
        self.dataTable1.setRowCount(0)
        self.dataTable1.setColumnCount(0)
        self.dataTable2.setVisible(False)
        self.dataTable2.setRowCount(0)
        self.dataTable2.setColumnCount(0)
        self.missInfo.clear()
        self.strategy.setEnabled(False)
        self.strategy.setCurrentText("--Select--")
        self.handlem.setEnabled(False)
        self.handlelabel.clear()
        self.coutliers.setEnabled(False)
        self.handleo.setEnabled(False)
        self.handleolabel.clear()
        self.checkst.setEnabled(False)
        self.detrend.setEnabled(False)
        self.handlelabel1.clear()
        self.viewfile.setVisible(False)
        self.adfinfo.setVisible(False)
        self.statinfo.setVisible(False)
        self.outlabel.clear()
        self.stationaritylabel.clear()
        self.dataTableLabel.setVisible(False)
        self.dataTableLabel1.setVisible(False)

#FUNCTION TO VIEW OUTPUT FOLDER
    def finalfile(self):
        path = self.dir+'/03Stationarity_Test'
        path = os.path.realpath(path)
        if sys.platform == "win32":
            os.startfile(path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])
                    
#FUNCTION TO SELECT THE INPUT FILES                 
    def loadfolder(self):
        self.dir=Home.setupdir(self)
        os.chdir(self.dir)
        self.dialog = QFileDialog()
        self.fpath = self.dialog.getExistingDirectory(None, self.dir,"Select Folder")
        if self.fpath == "":
            if self.directoryLabel.text() == "":
                self.directoryLabel.setText("No Directory selected")
            else:
                self.directoryLabel.setText(self.directoryLabel.text())
                self.directoryLabel.setText("No Directory selected")
        else:
            self.progress3.setVisible(True)
            QApplication.processEvents()
            self.loadDirectory.setText("Select Light Curve Directory")
            QApplication.processEvents()
            self.directoryLabel.setText('Directory:{}'.format(self.fpath))
            QApplication.processEvents()
            if "03Stationarity_Test" not in os.listdir(self.dir):
                QApplication.processEvents()
                os.mkdir("03Stationarity_Test")
                QApplication.processEvents()
            if "output" not in os.listdir("./03Stationarity_Test/"):
                QApplication.processEvents()
                os.mkdir("03Stationarity_Test/output")
                QApplication.processEvents()
            if "extras" not in os.listdir("./03Stationarity_Test/"):
                QApplication.processEvents()
                os.mkdir("03Stationarity_Test/extras")
                QApplication.processEvents()
            if "logs" not in os.listdir("./03Stationarity_Test/"):
                QApplication.processEvents()
                os.mkdir("03Stationarity_Test/logs")
                QApplication.processEvents()
            if "outlierRemovedLCs" not in os.listdir("./03Stationarity_Test/output/"):
                QApplication.processEvents()
                os.mkdir("03Stationarity_Test/output/outlierRemovedLCs")
                QApplication.processEvents()
            if "detrendedLCs" not in os.listdir("./03Stationarity_Test/output/"):
                QApplication.processEvents()
                os.mkdir("03Stationarity_Test/output/detrendedLCs")
                QApplication.processEvents()
            if "plots" not in os.listdir("./03Stationarity_Test/"):
                QApplication.processEvents()
                os.mkdir("03Stationarity_Test/plots")
                QApplication.processEvents()
            # if "handleMissingComparison" not in os.listdir("./03Stationarity_Test/plots/"):
            #     QApplication.processEvents()
            #     os.mkdir("03Stationarity_Test/plots/handleMissingComparison")
            #     QApplication.processEvents()
            if "detrendedComparison" not in os.listdir("./03Stationarity_Test/plots/"):
                QApplication.processEvents()
                os.mkdir("03Stationarity_Test/plots/detrendedComparison")
                QApplication.processEvents()
            if "outlierRemovedComparison" not in os.listdir("./03Stationarity_Test/plots/"):
                QApplication.processEvents()
                os.mkdir("03Stationarity_Test/plots/outlierRemovedComparison")
                QApplication.processEvents()

            self.logtime = time.time()
            QApplication.processEvents()
            with open(f"03Stationarity_Test/logs/ST_{self.logtime}.txt", "a") as file:
                QApplication.processEvents()
                file.write(f"Login Date and Time: {datetime.datetime.now()}")
                QApplication.processEvents()

            os.chdir(self.fpath)
            QApplication.processEvents() 
            self.filelist=glob.glob('*.csv')
            QApplication.processEvents()
            str_values=0
            QApplication.processEvents()
            try:
                for file in self.filelist:  
                    QApplication.processEvents()           
                    self.df = pd.read_csv(file, header = None)
                    QApplication.processEvents()
                    for rowIndex, row in self.df.iterrows():
                        QApplication.processEvents()
                        for columnIndex, value in row.items():
                            QApplication.processEvents()
                            if type(value) == int or type(value) ==float:
                                QApplication.processEvents()
                                pass
                                QApplication.processEvents()
                            else:
                                QApplication.processEvents()
                                str_values = str_values+1
                                QApplication.processEvents()
                self.progress3.hide()
                if str_values > 0:
                    self.resetWorkspace()
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("String data not allowed. Please remove header or non numerical data before loading the file")
                    msg.setWindowTitle("Warning")
                    msg.exec_()
                else:
                    csvcounter = len(glob.glob1(self.fpath,"*.csv"))
                    self.shapeLabel.setText('{} Light Curves Loaded!'.format(csvcounter))
                    if csvcounter == 0:
                        self.checkm.setEnabled(False)
                    else:
                        self.checkm.setEnabled(True)

                    self.dataTable.setVisible(False)
                    self.dataTable.setRowCount(0)
                    self.dataTable.setColumnCount(0)
                    self.dataTable1.setVisible(False)
                    self.dataTable1.setRowCount(0)
                    self.dataTable1.setColumnCount(0)
                    self.dataTable2.setVisible(False)
                    self.dataTable2.setRowCount(0)
                    self.dataTable2.setColumnCount(0)
                    self.missInfo.clear()
                    self.strategy.setEnabled(False)
                    self.strategy.setCurrentText("--Select--")
                    self.handlem.setEnabled(False)
                    self.handlelabel.clear()
                    self.coutliers.setEnabled(False)
                    self.handleo.setEnabled(False)
                    self.handleolabel.clear()
                    self.checkst.setEnabled(False)
                    self.detrend.setEnabled(False)
                    self.handlelabel1.clear()
                    self.viewfile.setVisible(False)
                    self.adfinfo.setVisible(False)
                    self.statinfo.setVisible(False)
                    self.outlabel.clear()
                    self.stationaritylabel.clear()

            except pd.errors.EmptyDataError:
                self.progress3.hide()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("No columns to parse from file")
                msg.setWindowTitle("Warning")
                msg.exec_()
                    
#FUNCTION TO CHECK MISSING VALUES     
    def checkmissing(self):
        os.chdir(self.fpath) 
        self.filelist=glob.glob('*.csv') 
        self.fileIndex = []
        self.missCount = []
        self.newFile = []
        self.newMiss = []
        self.noMiss = []
        for file in self.filelist:             
            self.df = pd.read_csv(file, header = None)
            self.df.columns = range(1, self.df.shape[1] + 1)
            self.df.index = range(1, self.df.shape[0] + 1)
            self.df = self.df.replace([np.inf, -np.inf, "nan "], np.nan)
            
            self.fileIndex.append(file)
            self.missCount.append(self.df.isnull().sum().sum())
        
        for (i,j) in zip(self.fileIndex, self.missCount):
            if j != 0:
                self.newFile.append(i)
                self.newMiss.append(j)
            else:
                self.noMiss.append(i)

        self.missing = pd.DataFrame(list(zip(self.newFile,self.newMiss)))
        
        t=sum(self.missCount)

        if t==0:
            self.strategy.setEnabled(False)
            self.coutliers.setEnabled(True)
            self.missInfo.setText("No missing values...")
        else:
            self.dataTableLabel.setVisible(True)
            self.missInfo.setText("Missing Values Detected!")
            self.dataTable.setVisible(True)
            self.dataTable.setColumnCount(self.missing.shape[1])
            self.dataTable.setRowCount(self.missing.shape[0])
            self.dataTable.setHorizontalHeaderLabels(["Filename", "Missing Values"])
                
            for i in range(len(self.missing.index)): 
                for j in range(len(self.missing.columns)):
                    self.dataTable.setItem(i,j,QTableWidgetItem(str(self.missing.iloc[i, j])))
            self.strategy.setEnabled(True)

            with open(f"{self.dir}/03Stationarity_Test/logs/ST_{self.logtime}.txt", "a") as file:
                file.write(f"\nStar ID and missing values count:")
                for (i,j) in zip(self.newFile, self.newMiss):
                    file.write(f"\n{i,j}")


#FUNCTION TO CALCULATE MEAN OR MEDIAN FOR MISSING VALUES
    def checkimp(self):  
        if self.strategy.currentText() == "--Select--":
            self.handlem.setEnabled(False)
        elif self.strategy.currentText() == "Mean":
            self.handlem.setEnabled(True)
        elif self.strategy.currentText() == "Median":
            self.handlem.setEnabled(True)
        elif self.strategy.currentText() == "Backward Fill":
            self.handlem.setEnabled(True)
        elif self.strategy.currentText() == "Forward Fill":
            self.handlem.setEnabled(True)
        elif self.strategy.currentText() == "Most Frequent":
            self.handlem.setEnabled(True)
        elif self.strategy.currentText() == "Linear Interpolate":
            self.handlem.setEnabled(True)
        elif self.strategy.currentText() == "Quadratic Interpolate":
            self.handlem.setEnabled(True)
        elif self.strategy.currentText() == "Cubic Interpolate":
            self.handlem.setEnabled(True)
        else:
            pass

    def impute(self):
        os.chdir(self.dir)    
        if "handleMissingLCs" not in os.listdir("./03Stationarity_Test/output/"):
                os.mkdir("03Stationarity_Test/output/handleMissingLCs")
        if "handleMissingComparison" not in os.listdir("./03Stationarity_Test/plots/"):
            os.mkdir("03Stationarity_Test/plots/handleMissingComparison")

        os.chdir(self.fpath)
        for i in self.noMiss:
            self.fd=pd.read_csv(i, names=["time", "mag"])
            self.fd.to_csv(self.dir+'/03Stationarity_Test/output/handleMissingLCs/{0}'.format(i), header = None, index = False)
            
        for file in self.newFile: 
            self.df1 = pd.read_csv(file, names=["time", "mag"])
            self.df2 = self.df1
            columns = self.df1.columns
            if self.strategy.currentText() == "Mean":
                imputer = SimpleImputer(strategy="mean")
                imputer.fit(self.df1)
                self.df1 = imputer.transform(self.df1)
                self.df1 = pd.DataFrame(self.df1, columns=columns)
                self.df1 = self.df1.round(3)
                self.df1.to_csv(self.dir+'/03Stationarity_Test/output/handleMissingLCs/{0}'.format(file), header = None, index = False)
            elif self.strategy.currentText() == "Median":
                imputer = SimpleImputer(strategy="median")
                imputer.fit(self.df1)
                self.df1 = imputer.transform(self.df1)
                self.df1 = pd.DataFrame(self.df1, columns=columns)
                self.df1 = self.df1.round(3)
                self.df1.to_csv(self.dir+'/03Stationarity_Test/output/handleMissingLCs/{0}'.format(file), header = None, index = False)
            elif self.strategy.currentText() == "Backward Fill":
                self.df1 = self.df1.bfill(axis = 0).ffill(axis = 0)
                self.df1 = pd.DataFrame(self.df1, columns=columns)
                self.df1 = self.df1.round(3)
                self.df1.to_csv(self.dir+'/03Stationarity_Test/output/handleMissingLCs/{0}'.format(file), header = None, index = False)
            elif self.strategy.currentText() == "Forward Fill":
                self.df1 = self.df1.ffill(axis = 0).bfill(axis = 0)
                self.df1 = pd.DataFrame(self.df1, columns=columns)
                self.df1 = self.df1.round(3)
                self.df1.to_csv(self.dir+'/03Stationarity_Test/output/handleMissingLCs/{0}'.format(file), header = None, index = False)
            elif self.strategy.currentText() == "Most Frequent":
                imputer = SimpleImputer(strategy="most_frequent")
                imputer.fit(self.df1)
                self.df1 = imputer.transform(self.df1)
                self.df1 = pd.DataFrame(self.df1, columns=columns)
                self.df1 = self.df1.round(3)
                self.df1.to_csv(self.dir+'/03Stationarity_Test/output/handleMissingLCs/{0}'.format(file), header = None, index = False)
            elif self.strategy.currentText() == "Linear Interpolate":
                imputer = InterpolationImputer(strategy='linear')
                mag_new = imputer.fit_transform([self.df1.iloc[:, 1]])
                mag_new = mag_new.flatten()
                self.df2 = pd.DataFrame({'time': self.df1.iloc[:,0], 'mag': mag_new}, columns=["time", "mag"])
                self.df2 = self.df2.round(3)
                self.df2.to_csv(self.dir+'/03Stationarity_Test/output/handleMissingLCs/{0}'.format(file), header = None, index = False)
            elif self.strategy.currentText() == "Quadratic Interpolate":
                imputer = InterpolationImputer(strategy='quadratic')
                mag_new = imputer.fit_transform([self.df1.iloc[:, 1]])
                mag_new = mag_new.flatten()
                self.df2 = pd.DataFrame({'time': self.df1.iloc[:,0], 'mag': mag_new}, columns=["time", "mag"])
                self.df2 = self.df2.round(3)
                self.df2.to_csv(self.dir+'/03Stationarity_Test/output/handleMissingLCs/{0}'.format(file), header = None, index = False)
            elif self.strategy.currentText() == "Cubic Interpolate":
                imputer = InterpolationImputer(strategy='cubic')
                mag_new = imputer.fit_transform([self.df1.iloc[:, 1]])
                mag_new = mag_new.flatten()
                self.df2 = pd.DataFrame({'time': self.df1.iloc[:,0], 'mag': mag_new}, columns=["time", "mag"])
                self.df2 = self.df2.round(3)
                self.df2.to_csv(self.dir+'/03Stationarity_Test/output/handleMissingLCs/{0}'.format(file), header = None, index = False)

            plt.plot()
            QApplication.processEvents()
            plt.scatter(self.df2["time"], self.df2["mag"], c='r')
            plt.scatter(self.df1["time"], self.df1["mag"])
            QApplication.processEvents()
            
            plt.title("Missing Imputed")
            plt.xlabel('Date')
            plt.ylabel('Magnitude')
            QApplication.processEvents()

            plt.savefig(f"{self.dir}/03Stationarity_Test/plots/handleMissingComparison/{file.split('.csv')[0]}_comparison.png")
            QApplication.processEvents()
            plt.close()
            QApplication.processEvents()

            self.handlelabel.setText("Missing Data Processed!")
            self.coutliers.setEnabled(True)       

#FUNCTION TO CHECK OUTLIERS    
    def checkol(self):
        self.fileslist=[]
        self.outvalues=[]
        self.adfInput = []
        self.outlierFiles = []
        self.noOutlierFiles = []
        self.checkFileName = []

        if self.newFile != []:
            path = self.dir+"/03Stationarity_Test/output/handleMissingLCs/"
        elif self.newFile == []:
            path = self.fpath
        else:
            pass
    
        loadedFiles = self.newFile + self.noMiss 

        for file in os.listdir(path):
            for i in loadedFiles:
                if file == i:
                    if i.split(".")[-1] == "csv":
                        df = pd.read_csv(path+'//'+i, names=["time", "mag"])
                        oldShape = df.shape[0]
                        q1, q2, q3 = np.quantile(df["mag"], [0.25, 0.5, 0.75])
                        iqr = q3 - q1
                        df = df[(df["mag"] > (q1- 1.5 * iqr))]
                        df = df[(df["mag"] < (q3 + 1.5 * iqr))]
                        newShape = df.shape[0]
                        
                        if oldShape != newShape:
                            self.outlierFiles.append(i)
                            self.outvalues.append(oldShape - newShape)
                        else:
                            self.noOutlierFiles.append(i)

                        self.checkFileName.append(i)

        if self.outlierFiles != []:
            self.dataTableLabel1.setVisible(True)
            self.outfiles = pd.DataFrame(list(zip(self.outlierFiles,self.outvalues)))
            self.outlabel.setText("Outliers Detected!")
            self.dataTable2.setVisible(True)
            self.dataTable2.setColumnCount(self.outfiles.shape[1])
            self.dataTable2.setRowCount(self.outfiles.shape[0])
            self.dataTable2.setHorizontalHeaderLabels(["File", "Outliers"])

            for i in range(len(self.outfiles.index)): 
                for j in range(len(self.outfiles.columns)):
                    self.dataTable2.setItem(i,j,QTableWidgetItem(str(self.outfiles.iloc[i, j])))

            with open(f"{self.dir}/03Stationarity_Test/logs/ST_{self.logtime}.txt", "a") as file:
                file.write(f"\nFiles and outlier count:")
                for (i,j) in zip(self.outlierFiles, self.outvalues):
                    file.write(f"\n{i,j}")
            self.handleo.setEnabled(True)
            self.checkst.setEnabled(True)
        else:
            self.outlabel.setText("No Outliers Detected")
            self.handleo.setEnabled(False)
            self.checkst.setEnabled(True)

#FUNCTION TO HANDLE OUTLIERS AND SAVE THE FILES AND FIGURES
    def handleol(self):
        self.progress1.setVisible(True)
        QApplication.processEvents()
        if self.newFile != []:
            QApplication.processEvents()
            path = self.dir+"/03Stationarity_Test/output/handleMissingLCs/"
            QApplication.processEvents()
        elif self.newFile == []:
            QApplication.processEvents()
            path = self.fpath
        else:
            QApplication.processEvents()
            pass

        for file in os.listdir(path):
            QApplication.processEvents()
            self.adfInput.append(file)
            QApplication.processEvents()
            for i in self.noOutlierFiles:
                QApplication.processEvents()
                if file == i:
                    QApplication.processEvents()
                    if i.split(".")[-1] == "csv":
                        QApplication.processEvents()
                        df = pd.read_csv(path+'//'+i, names=["time", "mag"])
                        QApplication.processEvents()
                        df.to_csv(f"{self.dir}/03Stationarity_Test/output/outlierRemovedLCs/{i}", index=None, header=None)
                        QApplication.processEvents()
                
            for i in self.outlierFiles:
                QApplication.processEvents()
                if file == i:
                    QApplication.processEvents()
                    if i.split(".")[-1] == "csv":
                        QApplication.processEvents()
                        df = pd.read_csv(path+'//'+i, names=["time", "mag"])
                        QApplication.processEvents()

                        plt.subplot(1, 2, 1)
                        QApplication.processEvents()
                        plt.scatter(df["time"], df["mag"])
                        QApplication.processEvents()
                        plt.title("Original LC")
                        QApplication.processEvents()

                        q1, q2, q3 = np.quantile(df["mag"], [0.25, 0.5, 0.75])
                        QApplication.processEvents()
                        iqr = q3 - q1
                        QApplication.processEvents()
                        df = df[(df["mag"] > (q1- 1.5 * iqr))]
                        QApplication.processEvents()
                        df = df[(df["mag"] < (q3 + 1.5 * iqr))]
                        QApplication.processEvents()
                        df.to_csv(f"{self.dir}/03Stationarity_Test/output/outlierRemovedLCs/{i}", index=None, header=None)
                        QApplication.processEvents()

                        plt.subplot(1, 2, 2)
                        QApplication.processEvents()
                        plt.scatter(df["time"], df["mag"])
                        QApplication.processEvents()

                        plt.title("Outliers Removed")
                        QApplication.processEvents()
                        plt.savefig(f"{self.dir}/03Stationarity_Test/plots/outlierRemovedComparison/{i.split('.csv')[0]}_comparison.png")
                        QApplication.processEvents()
                        plt.close()
                        QApplication.processEvents()
        self.progress1.hide()
        self.checkst.setEnabled(True)
        QApplication.processEvents()
        self.handleolabel.setText("Outliers Removed!")
        
#FUNCTION TO CHECK STATIONARITY AND DISPLAY RESULT IN A TABLE
    def checkstat(self):
        if self.adfInput != []:
            path = self.dir+"/03Stationarity_Test/output/outlierRemovedLCs/"
        else:
            if self.newFile != []:
                path = self.dir+"/03Stationarity_Test/output/handleMissingLCs/"
            else:
                path = self.fpath
                        
        allFile = self.outlierFiles + self.noOutlierFiles
        
        self.fileName = []
        self.testStats = []
        self.pValue = []
        self.critical1 = []
        self.critical5 = []
        self.critical10 = []
        self.stationarity = []

        try:
            for file in os.listdir(path):
                for i in allFile:
                    if file == i:
                        series = pd.read_csv(path+'//'+i, names=["time", "mag"])
                        df_sort = series.sort_values(by="time")
                        test = adfuller(df_sort["mag"], autolag="AIC")
                        self.fileName.append(file)
                        self.testStats.append(test[0])
                        self.pValue.append(test[1])
                        self.critical1.append(test[4]["1%"])
                        self.critical5.append(test[4]["5%"])
                        self.critical10.append(test[4]["10%"])
                        if (test[1] < 0.05):
                            self.stationarity.append(1)
                        elif (test[1] > 0.05):
                            if (test[0] < test[4]["1%"]) and (test[0] < test[4]["5%"]) and (test[0] < test[4]["10%"]):
                                self.stationarity.append(1)
                            else:
                                self.stationarity.append(0)
                                self.detrend.setEnabled(True)

            self.stats = pd.DataFrame(list(zip(self.fileName,self.testStats,self.pValue,self.critical1,self.critical5,self.critical10,self.stationarity)))
            self.stats.round(3)
            self.stats.columns=["Filename","ADF score","p-value","Critical 1%","Critical 5%","Critical 10%","Stationarity"]
            self.stats.to_csv(self.dir+'/03Stationarity_Test/extras/adfResult.csv', index = None)
            self.stationaritylabel.setText("Stationarity Checked!")

            self.adfinfo.setVisible(True)
            self.statinfo.setVisible(True)
            self.adfinfo.setText("ADF Statistics")
            self.statinfo.setText("Stationarity [0=False, 1=True]")

            self.dataTable1.setVisible(True)
            self.dataTable1.setColumnCount(self.stats.shape[1])
            self.dataTable1.setRowCount(self.stats.shape[0])
            self.dataTable1.setHorizontalHeaderLabels(["Filename","ADF score","p-value","Critical 1%","Critical 5%","Critical 10%","Stationarity"])
            
            for i in range(len(self.stats.index)): 
                for j in range(len(self.stats.columns)):
                    self.dataTable1.setItem(i,j,QTableWidgetItem(str(self.stats.iloc[i, j])))
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Sample size is too short to use selected regression component")
            msg.setWindowTitle("Warning")
            msg.exec_()
        self.viewfile.setVisible(True)
                
#DETREND FUNCTION AND SAVE FILES AND FIGURES    
    def dtrend(self):
        if self.adfInput != []:
            path = self.dir+"/03Stationarity_Test/output/outlierRemovedLCs/"
        else:
            if self.newFile != []:
                path = self.dir+"/03Stationarity_Test/output/handleMissingLCs/"
            else:
                path = self.fpath

        self.progress2.setVisible(True)
        self.progress2.setMinimum(0)
        self.progress2.setMaximum(0)
        QApplication.sendPostedEvents()
        QApplication.processEvents()
        for i in range(self.stats.shape[0]):

            df = pd.read_csv(path+'//' + self.stats.iloc[i]["Filename"], names=["time", "mag"])
            
            if self.stats.iloc[i]["Stationarity"] == 1:
                df.to_csv(f"{self.dir}/03Stationarity_Test/output/detrendedLCs/{self.stats.iloc[i]['Filename']}", index=None, header=None)
            
            if self.stats.iloc[i]["Stationarity"] == 0:
                x1=df[df.columns[0]]
                y1=df[df.columns[1]]

                fig = plt.figure()           
                ax1= fig.add_subplot(121)
                ax2= fig.add_subplot(122)

                ax1.scatter(x1,y1)
                ax1.set_title('Original LC')
                ax1.set_xlabel('Date')
                ax1.set_ylabel('Magnitude')

                df_sort = df.sort_values(by="time")
                df_sort["dtrended"] = signal.detrend(df_sort["mag"])
                df_sort = df_sort.drop(["mag"], axis=1)

                x2=df_sort[df_sort.columns[0]]
                y2=df_sort[df_sort.columns[1]]
                ax2.scatter(x2,y2)
                ax2.set_title('Detrended LC')
                ax2.set_xlabel('Date')
                ax2.set_ylabel('Magnitude')
                fig.tight_layout(pad=2.0)

                df_sort.to_csv(f"{self.dir}/03Stationarity_Test/output/detrendedLCs/{self.stats.iloc[i]['Filename']}", index=None, header=None)
                plt.savefig(f"{self.dir}/03Stationarity_Test/plots/detrendedComparison/{self.stats.iloc[i]['Filename'].split('.csv')[0]}_comparison.png")
                plt.close()
        self.progress2.hide()
        self.handlelabel1.setText("Light Curves Detrended!")
        self.viewfile.setVisible(True)
