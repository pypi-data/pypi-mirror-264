#importing required modules
import sys
import glob
import os, subprocess
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QWidget, QMessageBox, QFileDialog, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QApplication, QProgressBar, QTableWidget,
                            QTableWidgetItem, QComboBox, QPlainTextEdit, QStatusBar, QToolBar)

import pandas as pd
from asiva.src.features import allFeatures
from asiva.src.features import modelFeatures
from asiva.src.features import customFeatures
from asiva.src.features.allFeatures import *
from asiva.src.features.modelFeatures import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import qtawesome as qta
import seaborn as sns
from asiva.src.home import *
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#creating a subclass of QWidget
class Feature(QWidget):
    def __init__(self):
        
        super(Feature, self).__init__() 
        self.setWindowTitle('Feature Extraction')

#Creating GUI --- Setting up Layouts        
        horizontalLayout = QHBoxLayout()
        verticalLayout = QVBoxLayout()

        clean_icon = qta.icon('fa5s.broom',
                        color='white')

        extract_icon = qta.icon('fa5s.download',
                        color='white')

        save_icon = qta.icon('fa5s.save',
                        color='white')

        folder_icon = qta.icon('fa5s.folder-open',
                        color='white')

        files_icon = qta.icon('fa5s.eye',
                        color='#2196f3')

        edit_icon = qta.icon('fa5s.pen',
                        color='#7ebdbd')

        update_icon = qta.icon('fa5s.redo',
                        color='#7ebdbd')

        info_icon = qta.icon('fa5s.info-circle',
                        color='#7ebdbd')

        tips_icon = qta.icon('fa5s.lightbulb',
                        color='#e8a92c')

        self.directory1 = QPushButton('Select Light Curve Directory')
        self.directory1.setIcon(folder_icon)
        self.directory1.setIconSize(QSize(30, 30))
        self.directory1.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #7ebdbd;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
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

        self.directoryInfo = QLabel()
        self.directoryInfo.setWordWrap(True)
        self.directoryInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "width:100%;\n"
                                    "color: #ff9800;\n"
                                    "}\n"
                                    "")

        self.dataHeader = QLabel("Data Source")
        self.dataHeader.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
                                    "}\n"
                                    "")

        self.selectData = QComboBox()
        self.selectData.setStyleSheet(u"QComboBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
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
                                    "border:none;\n"
                                    "}\n"
                                    "")
        self.selectData.addItem('--Select--')
        self.selectData.addItem('Standard (CSV)')
        self.selectData.addItem('ASAS (RAW)')

        self.directoryInfo1 = QLabel()
        self.directoryInfo1.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
                                    "color: #007427;\n"
                                    "margin-bottom:10px;\n"
                                    "}\n"
                                    "")

        self.clean = QPushButton('Clean Data')
        self.clean.setIcon(clean_icon)
        self.clean.setIconSize(QSize(30, 30))
        self.clean.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #2196f3;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
                                    "margin-top:5px;\n"
                                    "margin-bottom:10px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#7ac0f8;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")
        self.cleanInfo = QLabel()
        self.cleanInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
                                    "color: #2196f3;\n"
                                    "}\n"
                                    "")

        self.cleansave = QPushButton('Save Data')
        self.cleansave.setIcon(save_icon)
        self.cleansave.setIconSize(QSize(30, 30))
        self.cleansave.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #4caf50;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
                                    "margin-top:5px;\n"
                                    "margin-bottom:10px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#88bb8a;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")
        self.saveInfo = QLabel()
        self.saveInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
                                    "color: #4caf50;\n"
                                    "}\n"
                                    "")
        self.featureHeader = QLabel("Select Feature")
        self.featureHeader.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
                                    "}\n"
                                    "")

        self.selectFeature = QComboBox()
        self.selectFeature.setStyleSheet(u"QComboBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
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
        self.selectFeature.addItem('--Select--')
        self.selectFeature.addItem('Model Features')
        self.selectFeature.addItem('Only Period')
        #self.selectFeature.addItem('Fractal Features')     
        self.selectFeature.addItem('All Features')
        self.selectFeature.addItem('Custom Features')     

        self.extractButton = QPushButton('Extract features')
        self.extractButton.setIcon(extract_icon)
        self.extractButton.setIconSize(QSize(30, 30))
        self.extractButton.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
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
        self.extractInfo = QLabel()
        self.extractInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
                                    "color: #00bcd4;\n"
                                    "}\n"
                                    "")

        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)
        self.progress.setStyleSheet(u"QProgressBar\n"
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


        self.viewfile = QPushButton("View Files")
        self.viewfile.setIcon(files_icon)
        self.viewfile.setIconSize(QSize(30, 30))
        self.viewfile.setStyleSheet(u"QPushButton{\n"
                                    "width:100%;\n"
                                    "margin-top:10px;\n"
                                    "height:40px;\n"
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

        horizontalLayout2 = QHBoxLayout()
        horizontalLayout2.setAlignment(Qt.AlignBottom)

        self.customFeatures = QPushButton('Build Custom Features')
        self.customFeatures.setStyleSheet(u"QPushButton{\n"
                                    "background-color:#4682B4;"
                                    "color:white;\n"
                                    "font:18px;\n"
                                    "width:100%;\n"
                                    "height:50px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius: 5px;\n"
                                    "text-align:center;\n"
                                    "padding-left:10px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "color:#4682B4;\n"
                                    "background-color:white;\n"
                                    "border:2px solid #4682B4;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "color:#cccccc;\n"
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
                                    "margin-top:10px;\n"
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
                                    "font-weight:bold;\n"
                                    "text-align:left;\n"
                                    "max-height:35px;\n"
                                    "margin-top:10px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "color:#7ebdbd;\n"
                                    "}\n"
                                    "")
        
        horizontalLayout2.addWidget(self.customFeatures)
        horizontalLayout9.addWidget(self.reset)

        verticalLayout.addWidget(self.directory1)
        verticalLayout.addWidget(self.directoryInfo)
        verticalLayout.addWidget(self.dataHeader)
        verticalLayout.addWidget(self.selectData)
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
        verticalLayout.addWidget(self.progress1)
        verticalLayout.addWidget(self.directoryInfo1)

        horizontalLayout4 = QHBoxLayout()
        horizontalLayout4.addWidget(self.clean)
        horizontalLayout4.addWidget(self.cleansave)
        verticalLayout.addLayout(horizontalLayout4)

        horizontalLayout5 = QHBoxLayout()
        horizontalLayout5.addWidget(self.cleanInfo)
        horizontalLayout5.addWidget(self.saveInfo)
        verticalLayout.addLayout(horizontalLayout5)

        verticalLayout.addWidget(self.featureHeader)
        verticalLayout.addWidget(self.selectFeature)
        verticalLayout.addWidget(self.extractButton)
        verticalLayout.addWidget(self.extractInfo)
        verticalLayout.addWidget(self.progress)
        verticalLayout.addWidget(self.viewfile)
        verticalLayout.addStretch()
        verticalLayout.addLayout(horizontalLayout2)
        verticalLayout.addLayout(horizontalLayout10)
        verticalLayout.addLayout(horizontalLayout9)

        verticalLayout1 = QVBoxLayout()
##
        self.info = QPushButton()
        self.info.setToolTip('View Instructions')
        self.info.setIconSize(QSize(30, 30))
        self.info.setIcon(info_icon)
        self.info.setStyleSheet(u"QPushButton{\n"
                                    "border: none;\n"
                                    "color:#7ebdbd;\n"
                                    "font:16px;\n"
                                    "min-width:100px;\n"
                                    "max-width:100px;\n"
                                    "font-weight:bold;\n"
                                    "text-align:right;\n"
                                    "max-height:35px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "color:#4caf50;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "color:#cccccc;\n"
                                    "}\n"
                                    "")
##
        self.updateCF = QPushButton('Update')
        self.updateCF.setToolTip('Update Features file')
        self.updateCF.setIcon(update_icon)
        self.updateCF.setIconSize(QSize(30, 30))
        self.updateCF.setStyleSheet(u"QPushButton{\n"
                                    "border: none;\n"
                                    "color:#7ebdbd;\n"
                                    "font:16px;\n"
                                    "min-width:100px;\n"
                                    "max-width:100px;\n"
                                    "font-weight:bold;\n"
                                    "text-align:right;\n"
                                    "max-height:35px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "color:#4caf50;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "color:#cccccc;\n"
                                    "}\n"
                                    "")

        self.editoropen = QPushButton('Edit')
        self.editoropen.setIcon(edit_icon)
        self.editoropen.setIconSize(QSize(30, 30))
        self.editoropen.setStyleSheet(u"QPushButton{\n"
                                    "border: none;\n"
                                    "color:#7ebdbd;\n"
                                    "font:16px;\n"
                                    "min-width:80px;\n"
                                    "max-width:80px;\n"
                                    "font-weight:bold;\n"
                                    "text-align:right;\n"
                                    "max-height:35px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "color:#4caf50;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "color:#cccccc;\n"
                                    "}\n"
                                    "")

        self.textedit = QPlainTextEdit()
        self.textedit.setReadOnly(True)
        self.textedit.setStyleSheet(u"QPlainTextEdit{\n"
                                    "width:100%;\n"
                                    "font:13px;\n"
                                    "}\n"
                                    "")

        self.extractmet = QLabel()
        self.extractmet.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "text-decoration: underline;\n"
                                    "margin-left:10px;\n"
                                    "color:red;\n"
                                    "}\n"
                                    "")

        self.featureTable = QTableWidget()
        self.featureTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.featureTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.featureTable.horizontalHeader().setStyleSheet("QHeaderView { font-weight: bold; }")
        self.featureTable.setColumnCount(0)
        self.featureTable.setRowCount(0)
        self.featureTable.setStyleSheet(u"QTableWidget{\n"
                                    "background-color: white;\n"
                                    "width:100%;\n"
                                    "margin-top:20px;\n"
                                    "margin-left:10px;\n"
                                    "font:13px;\n"
                                    "}\n"
                                    "")
        self.figure4 = plt.Figure()
        self.canvas4 = FigureCanvas(self.figure4)

        horizontalLayout1 = QHBoxLayout()
        horizontalLayout1.addWidget(self.extractmet)

        horizontalLayout3 = QHBoxLayout()
        horizontalLayout3.setAlignment(Qt.AlignRight)
##
        horizontalLayout3.addWidget(self.info)
##
        horizontalLayout3.addWidget(self.updateCF)
        horizontalLayout3.addWidget(self.editoropen)

        verticalLayout1.addLayout(horizontalLayout1)
        verticalLayout1.addLayout(horizontalLayout3)
        verticalLayout1.addWidget(self.textedit)
        verticalLayout1.addWidget(self.featureTable)
        verticalLayout1.addWidget(self.canvas4)
        
        horizontalLayout.addLayout(verticalLayout,1)
        horizontalLayout.addLayout(verticalLayout1,4)

        self.setLayout(horizontalLayout)

        self.directory1.clicked.connect(self.loadfolder)
        self.extractButton.clicked.connect(self.extract)
        self.selectData.activated[str].connect(self.dsource)
        self.clean.clicked.connect(self.cleaning)
        self.cleansave.clicked.connect(self.cleanedsave)
        self.viewfile.clicked.connect(self.finalfile)
        self.selectFeature.activated[str].connect(self.checkext)
        self.reset.clicked.connect(self.resetWorkspace)
        self.customFeatures.clicked.connect(self.custom)
        self.editoropen.clicked.connect(self.editor)
        self.updateCF.clicked.connect(self.updateCustom)
        self.tips.clicked.connect(self.tipsAndTricks)
        self.info.clicked.connect(self.custom)
        self.directory1.setEnabled(True)
        self.selectFeature.setEnabled(False) 
        self.progress.setVisible(False)
        self.progress1.setVisible(False)
        self.extractButton.setEnabled(False)
        self.selectData.setEnabled(False)
        self.clean.setEnabled(False)
        self.cleansave.setEnabled(False)
        self.clean.setVisible(False)
        self.cleansave.setVisible(False)
        self.viewfile.setVisible(False)
        self.featureTable.setVisible(False)
        self.canvas4.setVisible(False)
        self.editoropen.setVisible(False)
        self.textedit.setVisible(False)
        self.updateCF.setVisible(False)
        self.info.setVisible(False)

#function to reset UI
    def resetWorkspace(self):
        self.directoryInfo.clear()
        self.directoryInfo1.clear()
        self.selectData.setEnabled(False)
        self.figure4.clear()
        self.canvas4.draw()
        self.featureTable.setRowCount(0)
        self.featureTable.setColumnCount(0)
        self.featureTable.setVisible(False)
        self.extractmet.clear()
        self.extractInfo.clear()
        self.viewfile.setVisible(False)
        self.cleanInfo.clear()
        self.saveInfo.clear()
        self.selectFeature.setCurrentText("--Select--")
        self.selectData.setCurrentText("--Select--")
        self.clean.setEnabled(False)
        self.cleansave.setEnabled(False)
        self.clean.setVisible(False)
        self.cleansave.setVisible(False)
        self.extractButton.setEnabled(False)
        self.selectFeature.setEnabled(False)
        self.updateCF.setVisible(False)
        self.editoropen.setVisible(False)
        self.textedit.setVisible(False)
        self.updateCF.setVisible(False)
##
        self.info.setVisible(False)
##

    def tipsAndTricks(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("COMING SOON")
        msg.setWindowTitle("Information")
        msg.exec_()

#function to view output
    def finalfile(self):
        path = self.dir+'/05Feature_Extraction'
        path = os.path.realpath(path)
        if sys.platform == "win32":
            os.startfile(path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])

    def custom(self):
        self.dir = self.dir=Home.setupdir(self)
        path = self.dir+'/config'
        if not os.path.exists(path):
            if sys.platform == "win32":
                os.mkdir(path)
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ret = ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)    
            else:
                os.mkdir(path)

        filepath = os.path.dirname(os.path.realpath(__file__))
        sourcefile = filepath+'/features/customFeatures.py'
        destfile = self.dir+'/config/customFeatures.py'

        if os.path.exists(destfile):
            pass
        else:
            with open(sourcefile, 'rb') as f, open(destfile, 'wb') as g:
                while True:
                    block = f.read(16*1024*1024)
                    if not block: 
                        break
                    g.write(block)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("*****IMPORTANT INSTRUCTIONS BEFORE PROCEEDING*****\n\n1. Use your default editor to write the functions. A commented line is given above every block for better understanding.\n\n2. Do not modify any function name, imported modules and variable names.\n\n3. Maximum of 10 features can be included in Custom Features.\n\n4. A default feature name is given for all 10 features. A user can change them accordingly.\n\n5. A sample function is included in the file. Do not edit this function.\n\n6. DO NOT FORGET TO SAVE YOUR WORK IN THE EDITOR. Once done click on update to check for errors.")
        msg.setWindowTitle("Message")
        msg.exec_()

        self.directoryInfo.clear()
        self.directoryInfo1.clear()
        self.selectData.setEnabled(False)
        self.figure4.clear()
        self.canvas4.draw()
        self.featureTable.setRowCount(0)
        self.featureTable.setColumnCount(0)
        self.featureTable.setVisible(False)
        self.extractmet.setVisible(False)
        self.extractmet.clear()
        self.extractInfo.clear()
        self.viewfile.setVisible(False)
        self.cleanInfo.clear()
        self.saveInfo.clear()
        self.selectFeature.setCurrentText("--Select--")
        self.selectData.setCurrentText("--Select--")
        self.clean.setEnabled(False)
        self.cleansave.setEnabled(False)
        self.clean.setVisible(False)
        self.cleansave.setVisible(False)
        self.extractButton.setEnabled(False)
        self.selectFeature.setEnabled(False)

        self.textedit.setVisible(True)
        self.dir=Home.setupdir(self)
        os.chdir(self.dir)
        self.cfpath = self.dir+'/config/customFeatures.py'
        text=open(self.cfpath).read()
        self.textedit.setPlainText(text)

        self.editoropen.setVisible(True)
##
        self.info.setVisible(True)
##
    def updateCustom(self):
        try:
            self.cfsPath = self.dir+'/config'
            os.chdir(self.cfsPath)
            with open("customFeatures.py", "a") as file:
                lines1 = "\n\ndf = pd.DataFrame(np.random.randint(0,100,size=(10, 2)), columns=('0','1'))\nfeature1 = function1(df[df.columns[0]], df[df.columns[1]])\nfeature2 = function2(df[df.columns[0]], df[df.columns[1]])\nfeature3 = function3(df[df.columns[0]], df[df.columns[1]])\nfeature4 = function4(df[df.columns[0]], df[df.columns[1]])\nfeature5 = function5(df[df.columns[0]], df[df.columns[1]])\nfeature6 = function6(df[df.columns[0]], df[df.columns[1]])\nfeature7 = function7(df[df.columns[0]], df[df.columns[1]])\nfeature8 = function8(df[df.columns[0]], df[df.columns[1]])\nfeature9 = function9(df[df.columns[0]], df[df.columns[1]])\nfeature10 = function10(df[df.columns[0]], df[df.columns[1]])\n"
                file.writelines(lines1)

            sys.path.append(self.dir)
            from config import customFeatures
            import importlib
            importlib.reload(customFeatures)
            
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "df = pd.DataFrame(np.random.randint(0,100,size=(10, 2)), columns=('0','1'))":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature1 = function1(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature2 = function2(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature3 = function3(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature4 = function4(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature5 = function5(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature6 = function6(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature7 = function7(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature8 = function8(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature9 = function9(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature10 = function10(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)

            text=open(self.cfpath).read()
            self.textedit.setPlainText(text)
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Code Updated Successfully.")
            msg.setWindowTitle("Information")
            msg.exec_()
        except:
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "df = pd.DataFrame(np.random.randint(0,100,size=(10, 2)), columns=('0','1'))":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature1 = function1(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature2 = function2(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature3 = function3(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature4 = function4(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature5 = function5(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature6 = function6(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature7 = function7(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature8 = function8(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature9 = function9(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)
            with open("customFeatures.py", "r") as f:
                lines = f.readlines()
            with open("customFeatures.py", "w") as f:
                for line in lines:
                    if line.strip("\n") != "feature10 = function10(df[df.columns[0]], df[df.columns[1]])":
                        f.write(line)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please check your Custom Features code for indentation errors or undefined variables.\nAlso read the Instructions given there properly.")
            msg.setWindowTitle("Warning")
            msg.exec_()

    def editor(self):
        try:
            if sys.platform == "win32":
                os.startfile(self.cfpath)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, self.cfpath])
            self.updateCF.setVisible(True)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("ERROR. No editor found in the system. Please install an editor before proceeding further.")
            msg.setWindowTitle("Warning")
            msg.exec_()
 
    def loadfolder(self):
        self.dir=Home.setupdir(self)
        os.chdir(self.dir)
        self.dialog = QFileDialog()
        self.fpath = self.dialog.getExistingDirectory(None, self.dir,"Select Folder")
        self.csvcounter = len(glob.glob1(self.fpath,"*.csv"))
        self.txtcounter = len(glob.glob1(self.fpath,"*.txt"))
        if self.fpath == "":
            if self.directoryInfo1.text() == "":
                self.directoryInfo.setText("No Directory selected")
                self.selectData.setEnabled(False)                
            else:
                self.directoryInfo.setText('Directory:{}'.format(self.fpath))
                self.directoryInfo1.setText(self.directoryInfo1.text())
        else:
            self.directory1.setText("Select Light Curve Directory")
            os.chdir(self.dir)
            if "05Feature_Extraction" not in os.listdir(self.dir):
                os.mkdir("05Feature_Extraction")
            if "output" not in os.listdir("./05Feature_Extraction/"):
                os.mkdir("05Feature_Extraction/output")
            if "plots" not in os.listdir("./05Feature_Extraction/"):
                os.mkdir("05Feature_Extraction/plots")
            if "phaseplots" not in os.listdir("./05Feature_Extraction/plots/"):
                os.mkdir("05Feature_Extraction/plots/phaseplots")
            if "phasedata" not in os.listdir("./05Feature_Extraction/plots/"):
                os.mkdir("05Feature_Extraction/plots/phasedata")
            if "original_period" not in os.listdir("./05Feature_Extraction/plots/phaseplots/"):
                os.mkdir("05Feature_Extraction/plots/phaseplots/original_period")
            if "double_period" not in os.listdir("./05Feature_Extraction/plots/phaseplots/"):
                os.mkdir("05Feature_Extraction/plots/phaseplots/double_period")
            if "half_period" not in os.listdir("./05Feature_Extraction/plots/phaseplots/"):
                os.mkdir("05Feature_Extraction/plots/phaseplots/half_period")
            if "original_period_lc" not in os.listdir("./05Feature_Extraction/plots/phasedata/"):
                os.mkdir("05Feature_Extraction/plots/phasedata/original_period_lc")
            if "double_period_lc" not in os.listdir("./05Feature_Extraction/plots/phasedata/"):
                os.mkdir("05Feature_Extraction/plots/phasedata/double_period_lc")
            if "half_period_lc" not in os.listdir("./05Feature_Extraction/plots/phasedata/"):
                os.mkdir("05Feature_Extraction/plots/phasedata/half_period_lc")
            self.directoryInfo.setText('Directory:{}'.format(self.fpath))
            self.directoryInfo1.clear()
            self.selectData.setEnabled(True)
            self.figure4.clear()
            self.featureTable.setRowCount(0)
            self.featureTable.setColumnCount(0)
            self.featureTable.setVisible(False)
            self.extractmet.clear()
            self.extractInfo.clear()
            self.viewfile.setVisible(False)
            self.cleanInfo.clear()
            self.saveInfo.clear()
            self.selectFeature.setCurrentText("--Select--")
            self.selectData.setCurrentText("--Select--")
            self.clean.setEnabled(False)
            self.cleansave.setEnabled(False)
            self.clean.setVisible(False)
            self.cleansave.setVisible(False)
            self.extractButton.setEnabled(False)
            self.selectFeature.setEnabled(False)
                
            os.chdir(self.dir)

    def dsource(self):

        if self.selectData.currentText() == "--Select--":
            self.selectFeature.setEnabled(False)     
            self.extractButton.setEnabled(False)
            self.clean.setEnabled(False)
            self.cleansave.setEnabled(False)
            self.clean.setVisible(False)
            self.cleansave.setVisible(False)

        if self.csvcounter == 0:
            if self.selectData.currentText() == "Standard (CSV)":
                self.selectFeature.setEnabled(False)     
                self.extractButton.setEnabled(False) 
                self.clean.setEnabled(False) 
                self.cleansave.setEnabled(False)
                self.clean.setVisible(False)
                self.cleansave.setVisible(False)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please Select ASAS for RAW files")
                msg.setWindowTitle("Message")
                msg.exec_()
                self.directoryInfo1.clear()

            if self.selectData.currentText() == "ASAS (RAW)":
                self.directoryInfo1.setText('{} Light Curves Loaded!'.format(self.txtcounter))
                self.selectFeature.setEnabled(False)     
                self.extractButton.setEnabled(False)
                self.clean.setEnabled(True)
                self.clean.setVisible(True)
                self.cleansave.setVisible(True) 

        else:

            if self.selectData.currentText() == "Standard (CSV)":
                try:
                    self.progress1.setVisible(True)
                    str_values=0
                    QApplication.processEvents()
                    for i in os.listdir(self.fpath):
                        QApplication.processEvents()
                        if i.split(".")[-1] == "csv":
                            QApplication.processEvents()
                            with open(self.fpath+"/"+i, 'r') as myfile:
                                QApplication.processEvents()
                                checkdf = pd.read_csv(myfile, header=None)  
                                QApplication.processEvents()                          
                                for rowIndex, row in checkdf.iterrows():
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
                    self.progress1.hide()
                    if str_values > 0:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("String data not allowed. Please remove header or non numerical data before loading the file")
                        msg.setWindowTitle("Warning")
                        msg.exec_()
                    else:
                        self.directoryInfo1.clear()
                        self.directoryInfo1.setText('{} Light Curves Loaded!'.format(self.csvcounter))
                        self.selectFeature.setEnabled(True)
                        self.clean.setEnabled(False) 
                        self.cleansave.setEnabled(False)

                except pd.errors.EmptyDataError:
                    self.progress1.hide()
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("No columns to parse from file")
                    msg.setWindowTitle("Warning")
                    msg.exec_()
                    self.selectData.setEnabled(False)
                     
            elif self.selectData.currentText() == "ASAS (RAW)":
                self.selectFeature.setEnabled(False)     
                self.extractButton.setEnabled(False) 
                self.clean.setEnabled(False) 
                self.cleansave.setEnabled(False)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Please Select Standard for csv files")
                msg.setWindowTitle("Message")
                msg.exec_()
                self.directoryInfo1.clear()

    def cleandata(self,x):
        for f in os.listdir():
            list1=[]
            list2=[]
            list3=[]
            list4=[]
            for line in x:
                li=line.strip()
                if not li.startswith("#"):
                    l=line.rstrip()
                    a=l.split()
                    b=a[0]
                    list1.append(b)
                    c=a[1]
                    list2.append(c)
                    d=a[6]
                    list3.append(d)
                    e=a[-2]
                    list4.append(e)
            df=pd.DataFrame({'TIME':list1,'VALUE':list2,'MER_3':list3,'GRADE':list4})
            df.drop(df.loc[df['GRADE']=='C'].index, inplace=True)
            df.drop(df.loc[df['GRADE']=='D'].index, inplace=True)
            df.drop(['GRADE', 'MER_3'], axis = 1, inplace=True)
            return df

    def cleaning(self):
        self.cleanedData_feature = []
        for i in os.listdir(self.fpath):
            try:
                with open(self.fpath+"//"+i, 'r') as myfile:
                    self.cleanedData_feature.append(self.cleandata(myfile))
                    self.cleansave.setEnabled(True)
            except Exception as e:
                os.chdir(self.dir)
                if "logs" not in os.listdir("./05Feature_Extraction/"):
                    os.mkdir("05Feature_Extraction/logs")
                with open(f"{self.dir}/05Feature_Extraction/logs/cleaningErrorLog.txt", "a") as f:
                    print(f"{i}", file=f)
        self.cleanInfo.setText("Cleaning Completed!")

    def cleanedsave(self):
        os.chdir(self.dir)
        if "cleanedData" not in os.listdir("./05Feature_Extraction/"):
            os.mkdir("05Feature_Extraction/cleanedData")
        for name,data in zip(os.listdir(self.fpath),self.cleanedData_feature):
            data.to_csv(f"{self.dir}/05Feature_Extraction/cleanedData/{name}.csv", index=None, header=None)
        self.saveInfo.setText("Files Saved!")
        self.selectFeature.setEnabled(True)

    def checkext(self):  
        if self.selectFeature.currentText() == "--Select--":
            self.extractButton.setEnabled(False)
        elif self.selectFeature.currentText() == "Model Features":
            self.extractButton.setEnabled(True)
        elif self.selectFeature.currentText() == "Only Period":
            self.extractButton.setEnabled(True)
        elif self.selectFeature.currentText() == "All Features":
            self.extractButton.setEnabled(True)
        elif self.selectFeature.currentText() == "Custom Features":
            self.extractButton.setEnabled(True)
        else:
            pass

    def featureext(self, df):
        QApplication.processEvents()
        if self.selectFeature.currentText() == "Model Features":
            self.editoropen.setVisible(False)
            self.textedit.setVisible(False)
            QApplication.processEvents()
            self.features = []
            QApplication.processEvents()
            maxRange = 1000
            QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 1000:
                QApplication.processEvents()
                maxRange = 800
                QApplication.processEvents()
            if (max(df[df.columns[df.columns[0]]]) - min(df[df.columns[0]])) < 800:
                QApplication.processEvents()
                maxRange = 600
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 600:
                QApplication.processEvents()
                maxRange = 400
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 400:
                QApplication.processEvents()
                maxRange = 200
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 200:
                QApplication.processEvents()
                maxRange = 100
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 100:
                QApplication.processEvents()
                maxRange = 10
                QApplication.processEvents()

            gatspy_period = LombScargleFast()
            QApplication.processEvents()
            gatspy_period.fit(df[df.columns[0]], df[df.columns[1]], 0.01)
            QApplication.processEvents()
            gatspy_period.optimizer.period_range=(0.1, maxRange)
            QApplication.processEvents()
            originalPeriod = gatspy_period.best_period
            QApplication.processEvents()

            ecdf = modelFeatures.ecdf(df[df.columns[1]], d=1)[0]
            QApplication.processEvents()

            entropy = modelFeatures.entropy(df[df.columns[1]], prob='standard')
            QApplication.processEvents()

            fap = modelFeatures.falseProbAlarm(df[df.columns[0]].values, df[df.columns[1]].values)
            QApplication.processEvents()

            rcsCalculate = modelFeatures.rcs(df[df.columns[1]].values)
            QApplication.processEvents()

            stetsonKCalculate = modelFeatures.stetsonK(df[df.columns[1]].values)
            QApplication.processEvents()

            kurtosis = modelFeatures.kurtosis(df[df.columns[1]])
            QApplication.processEvents()

            skewness = modelFeatures.skewness(df[df.columns[1]])
            QApplication.processEvents()

            calc_mean = modelFeatures.calc_mean(df[df.columns[1]])
            QApplication.processEvents()

            calc_std = modelFeatures.calc_std(df[df.columns[1]])
            QApplication.processEvents()

            psi_CS_value = psi_CS(df[df.columns[0]].values, df[df.columns[1]].values)
            QApplication.processEvents()

            self.features = [originalPeriod, ecdf, entropy, fap, rcsCalculate, stetsonKCalculate, kurtosis, 
                                skewness, calc_mean, calc_std, psi_CS_value]

            return self.features
            QApplication.processEvents()
            
        if self.selectFeature.currentText() == "Only Period":
            self.editoropen.setVisible(False)
            self.textedit.setVisible(False)
            QApplication.processEvents()
            self.features = []
            QApplication.processEvents()
            maxRange = 1000
            QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 1000:
                QApplication.processEvents()
                maxRange = 800
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 800:
                QApplication.processEvents()
                maxRange = 600
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 600:
                QApplication.processEvents()
                maxRange = 400
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 400:
                QApplication.processEvents()
                maxRange = 200
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 200:
                QApplication.processEvents()
                maxRange = 100
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 100:
                QApplication.processEvents()
                maxRange = 10
                QApplication.processEvents()
            gatspy_period = LombScargleFast()
            QApplication.processEvents()
            gatspy_period.fit(df[df.columns[0]], df[df.columns[1]], 0.1)
            QApplication.processEvents()
            gatspy_period.optimizer.period_range=(0.1, maxRange)
            QApplication.processEvents()
            originalPeriod = gatspy_period.best_period
            QApplication.processEvents()
            doublePeriod = 2*(gatspy_period.best_period)
            QApplication.processEvents()
            halfPeriod = 0.5*(gatspy_period.best_period)
            QApplication.processEvents()
            calc_mean = allFeatures.calc_mean(df[df.columns[1]])
            QApplication.processEvents()
            fap = allFeatures.falseProbAlarm(df[df.columns[0]].values, df[df.columns[1]].values)
            QApplication.processEvents()
            self.features = [originalPeriod, doublePeriod, halfPeriod, calc_mean, fap]
            QApplication.processEvents()
            return self.features
            QApplication.processEvents()

        if self.selectFeature.currentText() == "All Features":
            self.editoropen.setVisible(False)
            self.textedit.setVisible(False)
            QApplication.processEvents()
            autocorr = allFeatures.autocorr(df[df.columns[1]])
            QApplication.processEvents()
            mean_abs_diff = allFeatures.mean_abs_diff(df[df.columns[1]])
            QApplication.processEvents()
            mean_diff = allFeatures.mean_diff(df[df.columns[1]])
            QApplication.processEvents()
            median_abs_diff = allFeatures.median_abs_diff(df[df.columns[1]])
            QApplication.processEvents()
            median_diff = allFeatures.median_diff(df[df.columns[1]])
            QApplication.processEvents()
            distance = allFeatures.distance(df[df.columns[1]])
            QApplication.processEvents()
            sum_abs_diff = allFeatures.sum_abs_diff(df[df.columns[1]])
            QApplication.processEvents()
            slope = allFeatures.slope(df[df.columns[1]])
            QApplication.processEvents()
            pk_pk_distance = allFeatures.pk_pk_distance(df[df.columns[1]])
            QApplication.processEvents()
            entropy = allFeatures.entropy(df[df.columns[1]], prob='standard')
            QApplication.processEvents()
            neighbourhood_peaks = allFeatures.neighbourhood_peaks(df[df.columns[1]], n=10)
            QApplication.processEvents()
            interq_range = allFeatures.interq_range(df[df.columns[1]])
            QApplication.processEvents()
            kurtosis = allFeatures.kurtosis(df[df.columns[1]])
            QApplication.processEvents()
            skewness = allFeatures.skewness(df[df.columns[1]])
            QApplication.processEvents()
            calc_max = allFeatures.calc_max(df[df.columns[1]])
            QApplication.processEvents()
            calc_min = allFeatures.calc_min(df[df.columns[1]])
            QApplication.processEvents()
            calc_mean = allFeatures.calc_mean(df[df.columns[1]])
            QApplication.processEvents()
            calc_median = allFeatures.calc_median(df[df.columns[1]])
            QApplication.processEvents()
            mean_abs_deviation = allFeatures.mean_abs_deviation(df[df.columns[1]])
            QApplication.processEvents()
            median_abs_deviation = allFeatures.median_abs_deviation(df[df.columns[1]])
            QApplication.processEvents()
            rms = allFeatures.rms(df[df.columns[1]])
            QApplication.processEvents()
            calc_std = allFeatures.calc_std(df[df.columns[1]])
            QApplication.processEvents()
            calc_var = allFeatures.calc_var(df[df.columns[1]])
            QApplication.processEvents()
            ecdf = allFeatures.ecdf(df[df.columns[1]], d=1)[0]
            QApplication.processEvents()
            maxRange = 1000
            QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 1000:
                QApplication.processEvents()
                maxRange = 800
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 800:
                QApplication.processEvents()
                maxRange = 600
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 600:
                QApplication.processEvents()
                maxRange = 400
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 400:
                QApplication.processEvents()
                maxRange = 200
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 200:
                QApplication.processEvents()
                maxRange = 100
                QApplication.processEvents()
            if (max(df[df.columns[0]]) - min(df[df.columns[0]])) < 100:
                QApplication.processEvents()
                maxRange = 10
                QApplication.processEvents()
            gatspy_period = LombScargleFast()
            QApplication.processEvents()
            gatspy_period.fit(df[df.columns[0]], df[df.columns[1]], 0.1)
            QApplication.processEvents()
            gatspy_period.optimizer.period_range=(0.1, maxRange)
            QApplication.processEvents()
            originalPeriod = gatspy_period.best_period
            QApplication.processEvents()
            fap = allFeatures.falseProbAlarm(df[df.columns[0]].values, df[df.columns[1]].values)
            QApplication.processEvents()
            rcsCalculate = allFeatures.rcs(df[df.columns[1]].values)
            QApplication.processEvents()
            stetsonKCalculate = allFeatures.stetsonK(df[df.columns[1]].values)
            QApplication.processEvents()
            hurst = allFeatures.hurst(df[df.columns[1]].values)
            QApplication.processEvents()
            fractal_dim = allFeatures.fractal_dimension(data=df.values,data_file_name="",dim=1,l_range=[], file_index=0)
            QApplication.processEvents()
            lyapunov = allFeatures.lyapunov(df[df.columns[1]].values)
            QApplication.processEvents()
            sample_entropy = allFeatures.sample_entropy(df[df.columns[1]].values)
            QApplication.processEvents()
            corr_dimension = allFeatures.corr_dimension(df[df.columns[1]].values, emb_dim=2)
            QApplication.processEvents()
            detrended_fluctuation = allFeatures.detrended_fluctuation(df[df.columns[1]].values)
            QApplication.processEvents()
            amplitude_value = amplitude(df[df.columns[1]])
            QApplication.processEvents()
            psi_CS_value = psi_CS(df[df.columns[0]].values, df[df.columns[1]].values)
            QApplication.processEvents()

            self.features = [amplitude_value, autocorr, corr_dimension, detrended_fluctuation, distance, ecdf, entropy, fap, 
                            fractal_dim, hurst, interq_range, kurtosis, lyapunov, calc_max, calc_mean, mean_abs_deviation, 
                            mean_abs_diff, mean_diff, calc_median, median_abs_deviation, median_abs_diff, median_diff,
                            calc_min, neighbourhood_peaks, originalPeriod, pk_pk_distance, psi_CS_value, 
                            rcsCalculate, rms, sample_entropy, skewness, slope, calc_std, 
                            stetsonKCalculate, sum_abs_diff, calc_var]
                            
            QApplication.processEvents()
            return self.features

        if self.selectFeature.currentText() == "Custom Features":
            self.editoropen.setVisible(False)
            self.textedit.setVisible(False)
            self.updateCF.setVisible(False)

            sys.path.append(self.dir)
            from config import customFeatures

            feature1 = customFeatures.function1(df[df.columns[0]], df[df.columns[1]])
            feature2 = customFeatures.function2(df[df.columns[0]], df[df.columns[1]])
            feature3 = customFeatures.function3(df[df.columns[0]], df[df.columns[1]])
            feature4 = customFeatures.function4(df[df.columns[0]], df[df.columns[1]])
            feature5 = customFeatures.function5(df[df.columns[0]], df[df.columns[1]])
            feature6 = customFeatures.function6(df[df.columns[0]], df[df.columns[1]])
            feature7 = customFeatures.function7(df[df.columns[0]], df[df.columns[1]])
            feature8 = customFeatures.function8(df[df.columns[0]], df[df.columns[1]])
            feature9 = customFeatures.function9(df[df.columns[0]], df[df.columns[1]])
            feature10 = customFeatures.function10(df[df.columns[0]], df[df.columns[1]])

            self.features = [feature1, feature2,feature3, feature4, feature5, feature6, feature7, feature8 ,feature9, feature10]
            self.featureNames = customFeatures.function_Names()
            
            return self.features, self.featureNames

    def extract(self):
        self.info.setVisible(False)
        self.updateCF.setVisible(False)
        if self.selectFeature.currentText() == "Model Features":
            self.extractInfo.clear()
            self.extractedFeatures = []
            QApplication.processEvents()
            self.fileName = []
            QApplication.processEvents()

            if self.selectData.currentText() == "ASAS (RAW)":
                QApplication.processEvents()
                for i in os.listdir(self.dir+"/05Feature_Extraction/cleanedData"):
                    QApplication.processEvents()
                    with open(self.dir+"/05Feature_Extraction/cleanedData/"+ i, 'r') as myfile:
                        QApplication.processEvents()
                        checkdf = pd.read_csv(myfile, header=None)
                        QApplication.processEvents()
                        if checkdf.shape[0] > 100:
                            QApplication.processEvents()
                            newdata = pd.DataFrame(checkdf)
                            QApplication.processEvents()
                            x = self.featureext(newdata)
                            QApplication.processEvents()
                            self.extractedFeatures.append(x)
                            QApplication.processEvents()
                            self.fileName.append(i)
                            QApplication.processEvents()

            if self.selectData.currentText() == "Standard (CSV)":
                QApplication.processEvents()
                for i in os.listdir(self.fpath):
                    QApplication.processEvents()
                    if i.split(".")[-1] == "csv":
                        QApplication.processEvents()
                        with open(self.fpath+"/"+i, 'r') as myfile:
                            QApplication.processEvents()
                            checkdf = pd.read_csv(myfile, header=None)
                            QApplication.processEvents()
                            if checkdf.shape[0] > 100:
                                QApplication.processEvents()
                                newdata = pd.DataFrame(checkdf)
                                QApplication.processEvents()
                                x = self.featureext(newdata)
                                QApplication.processEvents()
                                self.extractedFeatures.append(x)
                                QApplication.processEvents()
                                self.fileName.append(i)
                                QApplication.processEvents()

            self.featureTable.setVisible(True)
            QApplication.processEvents()
            self.progress.setVisible(True)
            QApplication.processEvents()
            try:
                QApplication.processEvents()
                #self.viewplot.setVisible(False)

                QApplication.processEvents()
                ef = pd.DataFrame(self.extractedFeatures, columns = ["Period", "ECDF", "Entropy", "FAP", "RCS", "StetsonK", "Kurtosis",
                                                                    "Skewness", "Mean", "StdDev", "psiCS"])
                QApplication.processEvents()
                ef.insert(0, "filename", self.fileName)
                QApplication.processEvents()
                ef.to_csv(self.dir+"/05Feature_Extraction/output/modelFeatures.csv", index=None)

                QApplication.processEvents()
                #model_df = pd.read_csv("05Feature_Extraction/output/modelFeatures.csv")

                QApplication.processEvents()
                #model_df=model_df.drop(['filename'], axis=1)
                
                QApplication.processEvents()
                #plt.figure(figsize=(50,50))
                
                QApplication.processEvents()
                #sns.pairplot(model_df, diag_kind='kde')
                
                QApplication.processEvents()
                #plt.savefig(self.dir+'/05Feature_Extraction/output/modelFeatures.png')
                
                QApplication.processEvents()
                self.featureTable.setColumnCount(ef.shape[1])
                QApplication.processEvents()
                self.featureTable.setRowCount(ef.shape[0])
                QApplication.processEvents()
                self.featureTable.setHorizontalHeaderLabels(["FileName", "Period", "ECDF", "Entropy", "FAP", "RCS", "StetsonK", "Kurtosis",
                                                            "Skewness", "Mean", "StdDev", "psiCS"])
                QApplication.processEvents()
                for i in range(len(ef.index)): 
                    QApplication.processEvents()
                    for j in range(len(ef.columns)):
                        QApplication.processEvents()
                        self.featureTable.setItem(i,j,QTableWidgetItem(str(ef.iloc[i, j])))
                        QApplication.processEvents()
                
                self.extractmet.setVisible(True)
                self.extractmet.setText(self.selectFeature.currentText())
                QApplication.processEvents()
                
                self.canvas4.setVisible(False)
                QApplication.processEvents()
                
                self.progress.hide()
                QApplication.processEvents()
                
                #self.viewplot.setVisible(True)
                QApplication.processEvents()
                
                self.extractInfo.setText("Extraction Complete!")
                
                QApplication.processEvents()
                self.viewfile.setVisible(True)
                QApplication.processEvents()

            except IOError:
                self.progress.hide()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Plot open in another window. Close the plot and try again.")
                msg.setWindowTitle("Message")
                msg.exec_()

        if self.selectFeature.currentText() == "Only Period":
            self.extractedFeatures = []
            QApplication.processEvents()
            self.fileName = []
            QApplication.processEvents()
            if self.selectData.currentText() == "ASAS (RAW)":
                QApplication.processEvents()
                for i in os.listdir(self.dir+"/05Feature_Extraction/cleanedData"):
                    QApplication.processEvents()
                    self.extractedFeatures.append(self.featureext(pd.read_csv(self.dir+"/05Feature_Extraction/cleanedData/"+i,header=None)))
                    QApplication.processEvents()
                    self.fileName.append(i)
                    QApplication.processEvents()
            if self.selectData.currentText() == "Standard (CSV)":
                QApplication.processEvents()
                for i in os.listdir(self.fpath):
                    QApplication.processEvents()
                    if i.split(".")[-1] == "csv":
                        QApplication.processEvents()
                        self.extractedFeatures.append(self.featureext(pd.read_csv(self.fpath+"/"+i, header=None)))
                        QApplication.processEvents()
                        self.fileName.append(i)
                        QApplication.processEvents()
            self.extractInfo.clear()
            QApplication.processEvents()
            self.progress.setVisible(True)
            QApplication.processEvents()
            ef = pd.DataFrame(self.extractedFeatures, columns = ["period", "doublePeriod", "halfPeriod", "avg_mag", "fap"])
            QApplication.processEvents()
            ef.insert(0, "filename", self.fileName)
            QApplication.processEvents()
            ef.to_csv(self.dir+"/05Feature_Extraction/output/onlyPeriod.csv", index=None)
            QApplication.processEvents()

            self.canvas4.setVisible(True)
            QApplication.processEvents()
            self.figure4.clear()
            QApplication.processEvents()

            df = pd.read_csv("05Feature_Extraction/output/onlyPeriod.csv")
            QApplication.processEvents()
            df1 = df.sort_values(by='avg_mag')
            QApplication.processEvents()

            self.ax = self.figure4.add_subplot(1,1,1)
            QApplication.processEvents()
            self.ax1 = self.ax.twinx()
            QApplication.processEvents()
            self.ax.bar(df1.filename, df1.period, color = '#6090C0')
            QApplication.processEvents()
            self.ax.yaxis.grid(linestyle = '-', linewidth=0.5)
            QApplication.processEvents()
            self.ax.set_axisbelow(True)
            QApplication.processEvents()

            self.ax1.plot(df1.filename, df1.fap, 'o-', color = '#cf6a63', linewidth=3)
            QApplication.processEvents()
            self.ax.set_xlabel('\nLight Curves')
            QApplication.processEvents()
            self.ax.set_ylabel('Period (days)')
            QApplication.processEvents()
            self.ax1.set_ylabel('FAP')
            QApplication.processEvents()

            x=[]
            for i in df1.filename:
                x.append(i)
                
            y=[]
            for i in df1.period:
                y.append(i)
                
            txt=[]
            for i in df1.avg_mag.round(2):
                txt.append(i)
                
            for i in range(len(y)):
                self.ax.text(x[i],y[i],txt[i], ha = 'center')
                QApplication.processEvents()
                
            self.ax.legend([df1.columns[1],df1.columns[5]])
            QApplication.processEvents()
            self.canvas4.draw()
            QApplication.processEvents()
            self.figure4.tight_layout(pad=1.0)
            QApplication.processEvents()
            self.figure4.savefig(self.dir+'/05Feature_Extraction/plots/onlyPeriod.png')
            QApplication.processEvents()

            self.featureTable.setVisible(True)
            QApplication.processEvents()
            self.featureTable.setColumnCount(ef.shape[1])
            QApplication.processEvents()
            self.featureTable.setRowCount(ef.shape[0])
            QApplication.processEvents()
            self.featureTable.setHorizontalHeaderLabels(["FileName", "Period", "Double Period", "Half Period", "Avg Mag", "FAP"])
            QApplication.processEvents()
            for i in range(len(ef.index)): 
                QApplication.processEvents()
                for j in range(len(ef.columns)):
                    QApplication.processEvents()
                    self.featureTable.setItem(i,j,QTableWidgetItem(str(ef.iloc[i, j])))
                    QApplication.processEvents()

            self.extractmet.setVisible(True)
            self.extractmet.setText(self.selectFeature.currentText())
            QApplication.processEvents()
            self.progress.hide()
            QApplication.processEvents()
            
            LightCurve = []
            QApplication.processEvents()
            OriginalPeriod = []
            QApplication.processEvents()
            DoublePeriod = []
            QApplication.processEvents()
            HalfPeriod = []
            QApplication.processEvents()

            for i in df1.filename:
                QApplication.processEvents()
                LightCurve.append(i)

            for i in df1.period:
                QApplication.processEvents()
                OriginalPeriod.append(i)

            for i in df1.doublePeriod:
                QApplication.processEvents()
                DoublePeriod.append(i)

            for i in df1.halfPeriod:
                QApplication.processEvents()
                HalfPeriod.append(i)

            for (a,b,c,d) in zip(LightCurve, OriginalPeriod, DoublePeriod, HalfPeriod):
                QApplication.processEvents()
                self.LC = pd.read_csv(self.dir+"/05Feature_Extraction/cleanedData"+"/"+a, header=None)
                QApplication.processEvents()
                a = a.replace(".csv", "")
                QApplication.processEvents()
                for i,j in zip(self.LC[self.LC.columns[0]],self.LC[self.LC.columns[1]]):
                    QApplication.processEvents()
                    if j == max(self.LC[self.LC.columns[1]]):
                        QApplication.processEvents()
                        t0 = i

                self.phaseDf = self.LC.values
                QApplication.processEvents()
                self.t0 = t0
                QApplication.processEvents()

                m = []
                QApplication.processEvents()
                n = []
                QApplication.processEvents()
                o = []
                QApplication.processEvents()
                for i in self.phaseDf[:, 0]:
                    QApplication.processEvents()  
                    x = i - self.t0
                    QApplication.processEvents()
                    m.append((x / b) - math.floor(x / b))
                    QApplication.processEvents()
                    n.append((x / d) - math.floor(x / d))
                    QApplication.processEvents()
                    o.append((x / c) - math.floor(x / c))
                    QApplication.processEvents()

                self.phaseDf1 = pd.DataFrame({"Phase": m, "Mag": self.phaseDf[:, 1]})
                QApplication.processEvents()
                self.phaseDf1 = self.phaseDf1.round(3)
                QApplication.processEvents()
                
                plt.figure(figsize=(15,15))
                QApplication.processEvents()
                plt.scatter(self.phaseDf1[self.phaseDf1.columns[0]], self.phaseDf1[self.phaseDf1.columns[1]], s=20, alpha=0.8)
                QApplication.processEvents()
                plt.title("Phased Light Curve")
                QApplication.processEvents()
                plt.xlabel("Phase")
                QApplication.processEvents()
                plt.ylabel("Magnitude")
                QApplication.processEvents()
                self.phaseDf1.to_csv(self.dir+f'/05Feature_Extraction/plots/phasedata/original_period_lc/{a}_original_Phased_LC.csv', index = False)
                QApplication.processEvents()
                plt.savefig(self.dir+f'/05Feature_Extraction/plots/phaseplots/original_period/{a}_original_period_Phased_LC.png')
                QApplication.processEvents()
                plt.close()
                QApplication.processEvents()

                self.phaseDf2 = pd.DataFrame({"Phase": n, "Mag": self.phaseDf[:, 1]})
                QApplication.processEvents()
                self.phaseDf2 = self.phaseDf2.round(3)
                QApplication.processEvents()

                plt.figure(figsize=(15,15))
                QApplication.processEvents()
                plt.scatter(self.phaseDf2[self.phaseDf2.columns[0]], self.phaseDf2[self.phaseDf2.columns[1]], s=20, alpha=0.8)
                QApplication.processEvents()
                plt.title("Phased Light Curve")
                QApplication.processEvents()
                plt.xlabel("Phase")
                QApplication.processEvents()
                plt.ylabel("Magnitude")
                QApplication.processEvents()
                self.phaseDf2.to_csv(self.dir+f'/05Feature_Extraction/plots/phasedata/half_period_lc/{a}_half_Phased_LC.csv', index = False)
                QApplication.processEvents()
                plt.savefig(self.dir+f'/05Feature_Extraction/plots/phaseplots/half_period/{a}_half_period_Phased_LC.png')
                QApplication.processEvents()
                plt.close()
                QApplication.processEvents()

                self.phaseDf3 = pd.DataFrame({"Phase": o, "Mag": self.phaseDf[:, 1]})
                QApplication.processEvents()
                self.phaseDf3 = self.phaseDf3.round(3)
                QApplication.processEvents()
                plt.figure(figsize=(15,15))
                QApplication.processEvents()
                plt.scatter(self.phaseDf3[self.phaseDf3.columns[0]], self.phaseDf3[self.phaseDf3.columns[1]], s=20, alpha=0.8)
                QApplication.processEvents()
                plt.title("Phased Light Curve")
                QApplication.processEvents()
                plt.xlabel("Phase")
                QApplication.processEvents()
                plt.ylabel("Magnitude")
                QApplication.processEvents()
                self.phaseDf3.to_csv(self.dir+f'/05Feature_Extraction/plots/phasedata/double_period_lc/{a}_double_Phased_LC.csv', index = False)
                QApplication.processEvents()
                plt.savefig(self.dir+f'/05Feature_Extraction/plots/phaseplots/double_period/{a}_double_period_Phased_LC.png')
                QApplication.processEvents()
                plt.close()
                QApplication.processEvents()

            self.extractInfo.setText("Extraction Complete!")

            QApplication.processEvents()
            self.viewfile.setVisible(True)

        if self.selectFeature.currentText() == "All Features":
            self.extractInfo.clear()
            self.extractedFeatures = []
            QApplication.processEvents()
            self.fileName = []
            QApplication.processEvents()

            if self.selectData.currentText() == "ASAS (RAW)":
                QApplication.processEvents()
                for i in os.listdir(self.dir+"/05Feature_Extraction/cleanedData"):
                    QApplication.processEvents()
                    with open(self.dir+"/05Feature_Extraction/cleanedData/"+ i, 'r') as myfile:
                        QApplication.processEvents()
                        checkdf = pd.read_csv(myfile, header=None)
                        QApplication.processEvents()
                        if checkdf.shape[0] > 100:
                            QApplication.processEvents()
                            newdata = pd.DataFrame(checkdf)
                            QApplication.processEvents()
                            x = self.featureext(newdata)
                            QApplication.processEvents()
                            self.extractedFeatures.append(x)
                            QApplication.processEvents()
                            self.fileName.append(i)
                            QApplication.processEvents()

            if self.selectData.currentText() == "Standard (CSV)":
                QApplication.processEvents()
                for i in os.listdir(self.fpath):
                    QApplication.processEvents()
                    if i.split(".")[-1] == "csv":
                        QApplication.processEvents()
                        with open(self.fpath+"/"+i, 'r') as myfile:
                            QApplication.processEvents()
                            checkdf = pd.read_csv(myfile, header=None)
                            QApplication.processEvents()
                            if checkdf.shape[0] > 100:
                                QApplication.processEvents()
                                newdata = pd.DataFrame(checkdf)
                                QApplication.processEvents()
                                x = self.featureext(newdata)
                                QApplication.processEvents()
                                self.extractedFeatures.append(x)
                                QApplication.processEvents()
                                self.fileName.append(i)
                                QApplication.processEvents()

            self.featureTable.setVisible(True)
            QApplication.processEvents()
            self.progress.setVisible(True)
            QApplication.processEvents()
            self.extractInfo.clear()
            QApplication.processEvents()
            self.progress.setVisible(True)
            try:
                QApplication.processEvents()
                #self.viewplot.setVisible(False)
                QApplication.processEvents()
                ef = pd.DataFrame(self.extractedFeatures, columns = ["Amplitude", "AutoCorr", "CorrDim[2]", "DetrendedFluc", "Distance", "ECDF", "Entropy", "FAP", 
                                                                    "FractalDim", "HurstExp", "InterQ", "Kurtosis", "LyapunovExp", "Max", "Mean", "MeanAbsDev", 
                                                                    "MeanAbsDiff", "MeanDiff", "Median", "MedianAbsDev", "MedianAbsDiff", "MedianDiff", 
                                                                    "Min", "NhoodPeaks", "Period", "PkPkDist", "psiCS", "RCS", "RMS", "SampleEntropy", 
                                                                    "Skewness", "Slope", "StdDev", "StetsonK", "SumAbsDiff", "Var"])

                QApplication.processEvents()
                ef.insert(0, "filename", self.fileName)
                QApplication.processEvents()
                ef.to_csv(self.dir+"/05Feature_Extraction/output/allFeatures.csv", index=None)
                QApplication.processEvents()
                self.canvas4.setVisible(False)
                QApplication.processEvents()
                self.extractmet.setVisible(True)
                self.extractmet.setText(self.selectFeature.currentText())
                QApplication.processEvents()
                
                QApplication.processEvents()
                self.featureTable.setColumnCount(ef.shape[1])
                QApplication.processEvents()
                self.featureTable.setRowCount(ef.shape[0])
                QApplication.processEvents()

                self.featureTable.setHorizontalHeaderLabels(["FileName", "Amplitude", "AutoCorr", "CorrDim[2]", "DetrendedFluc", "Distance", "ECDF", "Entropy", "FAP", 
                                                                    "FractalDim", "HurstExp", "InterQ", "Kurtosis", "LyapunovExp", "Max", "Mean", "MeanAbsDev", 
                                                                    "MeanAbsDiff", "MeanDiff", "Median", "MedianAbsDev", "MedianAbsDiff", "MedianDiff", 
                                                                    "Min", "NhoodPeaks", "Period", "PkPkDist", "psiCS", "RCS", "RMS", "SampleEntropy", 
                                                                    "Skewness", "Slope", "StdDev", "StetsonK", "SumAbsDiff", "Var"])

                QApplication.processEvents()
                for i in range(len(ef.index)):
                    QApplication.processEvents() 
                    for j in range(len(ef.columns)):
                        QApplication.processEvents()
                        self.featureTable.setItem(i,j,QTableWidgetItem(str(ef.iloc[i, j])))
                        QApplication.processEvents()

                self.progress.hide()
                QApplication.processEvents()
                #self.viewplot.setVisible(True)
                QApplication.processEvents()
                
                self.extractInfo.setText("Extraction Complete!")

                QApplication.processEvents()
                self.viewfile.setVisible(True)

            except IOError:
                self.progress.hide()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Plot open in another window. Close the plot and try again.")
                msg.setWindowTitle("Message")
                msg.exec_()


        if self.selectFeature.currentText() == "Custom Features":
            try:
                self.extractInfo.clear()
                self.extractedFeatures = []
                QApplication.processEvents()
                self.fileName = []
                QApplication.processEvents()

                if self.selectData.currentText() == "ASAS (RAW)":
                    QApplication.processEvents()
                    for i in os.listdir(self.dir+"/05Feature_Extraction/cleanedData"):
                        QApplication.processEvents()
                        with open(self.dir+"/05Feature_Extraction/cleanedData/"+ i, 'r') as myfile:
                            QApplication.processEvents()
                            checkdf = pd.read_csv(myfile, header=None)
                            QApplication.processEvents()
                            if checkdf.shape[0] > 100:
                                QApplication.processEvents()
                                newdata = pd.DataFrame(checkdf)
                                QApplication.processEvents()
                                x = self.featureext(newdata)
                                QApplication.processEvents()
                                self.extractedFeatures.append(x)
                                QApplication.processEvents()
                                self.fileName.append(i)
                                QApplication.processEvents()

                if self.selectData.currentText() == "Standard (CSV)":
                    QApplication.processEvents()
                    for i in os.listdir(self.fpath):
                        QApplication.processEvents()
                        if i.split(".")[-1] == "csv":
                            QApplication.processEvents()
                            with open(self.fpath+"/"+i, 'r') as myfile:
                                QApplication.processEvents()
                                checkdf = pd.read_csv(myfile, header=None)
                                QApplication.processEvents()
                                if checkdf.shape[0] > 100:
                                    QApplication.processEvents()
                                    newdata = pd.DataFrame(checkdf)
                                    QApplication.processEvents()
                                    x = self.featureext(newdata)
                                    QApplication.processEvents()
                                    self.extractedFeatures.append(x[0])
                                    QApplication.processEvents()
                                    self.fileName.append(i)
                                    QApplication.processEvents()

                self.featureTable.setVisible(True)
                QApplication.processEvents()
                self.progress.setVisible(True)
                QApplication.processEvents()
                self.extractInfo.clear()
                QApplication.processEvents()
                self.progress.setVisible(True)
                try:
                    QApplication.processEvents()
                    #self.viewplot.setVisible(False)
                    QApplication.processEvents()
                    ef = pd.DataFrame(self.extractedFeatures, columns = x[1])
                    QApplication.processEvents()
                    ef.dropna(how='all', axis=1, inplace=True)
                    if ef.empty:
                        self.extractInfo.setStyleSheet(u"QLabel{\n"
                                                    "font:13px;\n"
                                                    "font-weight:bold;\n"
                                                    "width:100%;\n"
                                                    "height:40px;\n"
                                                    "color: red;\n"
                                                    "}\n"
                                                    "")
                        self.extractInfo.setText("Empty Custom Features")
                        self.progress.hide()
                    else:
                        ef.insert(0, "filename", self.fileName)
                        QApplication.processEvents()
                        ef.to_csv(self.dir+"/05Feature_Extraction/output/customFeatures.csv", index=None)
                        QApplication.processEvents()
                        self.canvas4.setVisible(False)
                        QApplication.processEvents()
                        self.extractmet.setVisible(True)
                        self.extractmet.setText(self.selectFeature.currentText())
                        QApplication.processEvents()
                        self.featureTable.setColumnCount(ef.shape[1])
                        QApplication.processEvents()
                        self.featureTable.setRowCount(ef.shape[0])
                        QApplication.processEvents()
                        
                        file = ['filename']
                        self.headers = file + x[1]
                        self.featureTable.setHorizontalHeaderLabels(self.headers)
                        QApplication.processEvents()
                        for i in range(len(ef.index)):
                            QApplication.processEvents() 
                            for j in range(len(ef.columns)):
                                QApplication.processEvents()
                                self.featureTable.setItem(i,j,QTableWidgetItem(str(ef.iloc[i, j])))
                                QApplication.processEvents()

                        self.progress.hide()
                        QApplication.processEvents()
                        #self.viewplot.setVisible(True)
                        QApplication.processEvents()
                        
                        self.extractInfo.setText("Extraction Complete!")

                        QApplication.processEvents()
                    self.viewfile.setVisible(True)

                except IOError:
                    self.progress.hide()
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Plot open in another window. Close the plot and try again.")
                    msg.setWindowTitle("Message")
                    msg.exec_()

            except:
                self.progress.hide()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Error in custom Functions")
                msg.setWindowTitle("Message")
                msg.exec_()
