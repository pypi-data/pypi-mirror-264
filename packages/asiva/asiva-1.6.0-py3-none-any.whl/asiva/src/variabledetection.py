#importing all the required modules
import sys
import os, subprocess
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QFileDialog, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel, QApplication, QMessageBox, QProgressBar, QComboBox
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import mplcursors
import datetime
import time
from asiva.src.home import *
import qtawesome as qta
sns.set()
plt.style.use('seaborn-ticks')
import matplotlib.patches as mpatches


class VariableDetection(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Variable Detection')

#creation of user interface design
        horizontalLayout = QHBoxLayout()

        verticallayout = QVBoxLayout()

        search_icon = qta.icon('fa5s.search',
                        color='white')
        
        graph_icon = qta.icon('fa5s.chart-area',
                        color='white')

        delete_icon = qta.icon('fa5s.trash-alt',
                        color='white')

        save_icon = qta.icon('fa5s.save',
                        color='white')

        corr_icon = qta.icon('fa5s.link',
                        color='white')

        folder_icon = qta.icon('fa5s.folder-open',
                        color='white')

        files_icon = qta.icon('fa5s.eye',
                        color='#2196f3')

        view_plot_icon = qta.icon("mdi.chart-scatter-plot-hexbin",
                        color="white")

        tips_icon = qta.icon('fa5s.lightbulb',
                        color='#e8a92c')

        self.openFile = QPushButton("Load Processed Data")
        self.openFile.setToolTip('Load Processed Ensemble.csv from output of Data Processing') 
        self.openFile.setIcon(folder_icon)
        self.openFile.setIconSize(QSize(30, 30))
        self.openFile.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #7ebdbd;\n"
                                    "width:100%;\n"
                                    "min-height:35px;\n"
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
        self.dataName = QLabel()
        self.dataName.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #ff9800;\n"
                                    "}\n"
                                    "")
        self.matrixSize = QLabel()
        self.matrixSize.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #007427;\n"
                                    "}\n"
                                    "")

        self.stdLabel = QLabel("Std Dev Limit")
        self.stdLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-style: italic;\n"
                                    "margin-top:10px;\n"
                                    "}\n"
                                    "")

        self.ciLabel = QLabel("Confidence")
        self.ciLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-style: italic;\n"
                                    "margin-top:10px;\n"
                                    "}\n"
                                    "")

        self.orderLabel = QLabel("Order")
        self.orderLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-style: italic;\n"
                                    "margin-top:10px;\n"
                                    "}\n"
                                    "")

        self.stdValue = QLineEdit("0.04")
        self.stdValue.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:30%;\n"
                                    "height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.ciValue = QLineEdit("0.2")
        self.ciValue.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:30%;\n"
                                    "height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.orderValue = QComboBox()
        self.orderValue.setStyleSheet(u"QComboBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:90%;\n"
                                    "min-height:30px;\n"
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
        self.orderValue.addItem("2")
        self.orderValue.addItem("3")
        self.orderValue.addItem("4")
        self.orderValue.addItem("5")
        self.orderValue.setCurrentText("2")

        self.processButton = QPushButton("Detect Variables")
        self.processButton.setIcon(search_icon)
        self.processButton.setIconSize(QSize(30, 30))
        self.processButton.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "width:170%;\n"
                                    "height:35px;\n"
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

        self.dumpLabel1 = QLabel("Delete Star")
        self.dumpLabel1.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "")

        self.dumpIndex1 = QLineEdit()
        self.dumpIndex1.setPlaceholderText("Enter Star ID")
        self.dumpIndex1.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:100%;\n"
                                    "height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.dumpButton1 = QPushButton("Delete")
        self.dumpButton1.setIcon(delete_icon)
        self.dumpButton1.setIconSize(QSize(30, 30))
        self.dumpButton1.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #f44336;\n"
                                    "width:150%;\n"
                                    "height:35px;\n"
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

        self.dumpLabel = QLabel("Generate Light Curve using Star ID")
        self.dumpLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "margin-top:5px;\n"
                                    "}\n"
                                    "")

        self.dumpIndex = QLineEdit()
        self.dumpIndex.setPlaceholderText("Enter Star ID")
        self.dumpIndex.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:110%;\n"
                                    "height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.dumpButton = QPushButton("Save")
        self.dumpButton.setIcon(save_icon)
        self.dumpButton.setIconSize(QSize(30, 30))
        self.dumpButton.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #4caf50;\n"
                                    "width:150%;\n"
                                    "height:35px;\n"
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
        
        self.corelation = QLabel("Correlation & Differential")
        self.corelation.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "margin-top:5px;\n"
                                    "}\n"
                                    "")

        self.starID1 = QLineEdit()
        self.starID1.setPlaceholderText("Enter Star ID")
        self.starID1.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:100%;\n"
                                    "height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.starID2 = QLineEdit()
        self.starID2.setPlaceholderText("Enter Star ID")
        self.starID2.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:100%;\n"
                                    "height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.checkcor = QPushButton("Correlation Coeff")
        self.checkcor.setIcon(corr_icon)
        self.checkcor.setIconSize(QSize(30, 30))
        self.checkcor.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "width:100%;\n"
                                    "height:35px;\n"
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

        self.diffLC = QPushButton("Differential LC")
        self.diffLC.setIcon(graph_icon)
        self.diffLC.setIconSize(QSize(30, 30))
        self.diffLC.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #f44336;\n"
                                    "width:100%;\n"
                                    "height:35px;\n"
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

        self.pear = QLabel()
        self.pear.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #007427;\n"
                                    "}\n"
                                    "")       
        self.spear = QLabel()
        self.spear.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #007427;\n"
                                    "}\n"
                                    "")       

        self.diffInfo = QLabel()
        self.diffInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#007427;"
                                    "}\n"
                                    "")

        self.busyLabel = QLabel()
        self.busyLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #00bcd4;\n"
                                    "}\n"
                                    "")       

        self.starInfo = QLabel()
        self.starInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:red;\n"
                                    "}\n"
                                    "")
        
        self.dumpInfo = QLabel()
        self.dumpInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#007427;"
                                    "}\n"
                                    "")

        self.viewfile = QPushButton("View Files")
        self.viewfile.setIcon(files_icon)
        self.viewfile.setIconSize(QSize(30, 30))
        self.viewfile.setStyleSheet(u"QPushButton{\n"
                                    "width:100%;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border:2px solid #2196f3;\n"
                                    "border-radius: 5px;\n"
                                    "color:#2196f3;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#8ad1d1;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        horizontalLayout6 = QHBoxLayout()
        horizontalLayout6.addWidget(self.stdLabel)
        horizontalLayout6.addWidget(self.ciLabel)
        horizontalLayout6.addWidget(self.orderLabel)

        horizontalLayout2 = QHBoxLayout()
        horizontalLayout2.addWidget(self.stdValue)
        horizontalLayout2.addWidget(self.ciValue)
        horizontalLayout2.addWidget(self.orderValue)

        horizontalLayout3 = QHBoxLayout()
        horizontalLayout3.addWidget(self.dumpIndex1)
        horizontalLayout3.addWidget(self.dumpButton1) 

        horizontalLayout5 = QHBoxLayout()
        horizontalLayout5.addWidget(self.starID1)
        horizontalLayout5.addWidget(self.starID2) 

        horizontalLayout4 = QHBoxLayout()
        horizontalLayout4.addWidget(self.checkcor)
        horizontalLayout4.addWidget(self.diffLC)

        horizontalLayout8 = QHBoxLayout()
        horizontalLayout8.addWidget(self.pear)
        horizontalLayout8.addWidget(self.spear)

        horizontalLayout1 = QHBoxLayout()
        horizontalLayout1.addWidget(self.dumpIndex)
        horizontalLayout1.addWidget(self.dumpButton) 

        horizontalLayout10 = QHBoxLayout()
        horizontalLayout10.setAlignment(Qt.AlignBottom)

        self.view_Label = QLabel("View Light Curve using Star ID")
        self.view_Label.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "margin-top:5px;\n"
                                    "}\n"
                                    "")

        self.view_Value = QLineEdit()
        self.view_Value.setPlaceholderText("Enter Star ID")
        self.view_Value.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:30%;\n"
                                    "height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.view_Plot = QPushButton("View Plot")
        self.view_Plot.setIcon(view_plot_icon)
        self.view_Plot.setIconSize(QSize(30, 30))
        self.view_Plot.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "width:150%;\n"
                                    "height:35px;\n"
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

        self.dumpAllButton = QPushButton("Dump All Stars")
        self.dumpAllButton.setIcon(save_icon)
        self.dumpAllButton.setIconSize(QSize(30, 30))
        self.dumpAllButton.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "width:170%;\n"
                                    "height:35px;\n"
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

        self.viewInfo = QLabel()
        self.viewInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#007427;"
                                    "}\n"
                                    "")

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
                                    "QPushButton:disabled {\n"
                                    "background-color:#8ad1d1;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        horizontalLayout7 = QHBoxLayout()
        horizontalLayout7.addWidget(self.view_Value)
        horizontalLayout7.addWidget(self.view_Plot)


        horizontalLayout10.addWidget(self.tips)

        horizontalLayout9 = QHBoxLayout()
        horizontalLayout9.setAlignment(Qt.AlignBottom)
        self.reset = QPushButton('Reset Workspace')
        self.reset.setStyleSheet(u"QPushButton{\n"
                                    "border: none;\n"
                                    "color:red;\n"
                                    "font:18px;\n"
                                    "max-height:20px;\n"
                                    "width:100%;\n"
                                    "font-weight:bold;\n"
                                    "text-align:left;\n"
                                    "max-height:35px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "color:#7ebdbd;\n"
                                    "}\n"
                                    "")
        horizontalLayout9.addWidget(self.reset)

        verticallayout.addWidget(self.openFile)
        verticallayout.addWidget(self.dataName)
        verticallayout.addWidget(self.matrixSize)       
        verticallayout.addLayout(horizontalLayout6)
        verticallayout.addLayout(horizontalLayout2)
        verticallayout.addWidget(self.processButton)
        verticallayout.addWidget(self.progress)
        verticallayout.addWidget(self.busyLabel)
        verticallayout.addWidget(self.dumpLabel1)
        verticallayout.addLayout(horizontalLayout3)
        verticallayout.addWidget(self.starInfo)
        verticallayout.addWidget(self.corelation)
        verticallayout.addLayout(horizontalLayout5)
        verticallayout.addLayout(horizontalLayout4)
        verticallayout.addLayout(horizontalLayout8)
        verticallayout.addWidget(self.diffInfo)
        verticallayout.addWidget(self.view_Label)
        verticallayout.addLayout(horizontalLayout7)
        verticallayout.addWidget(self.viewInfo)
        verticallayout.addWidget(self.dumpLabel)
        verticallayout.addLayout(horizontalLayout1)
        verticallayout.addWidget(self.dumpAllButton)
        verticallayout.addWidget(self.progress1)
        verticallayout.addWidget(self.dumpInfo)
        verticallayout.addWidget(self.viewfile)
        verticallayout.addStretch()
        verticallayout.addLayout(horizontalLayout10)
        verticallayout.addLayout(horizontalLayout9)

        verticallayout1 = QVBoxLayout()
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        verticallayout1.addWidget(self.canvas)
        verticallayout1.addWidget(self.toolbar)

        horizontalLayout.addLayout(verticallayout,1)
        horizontalLayout.addLayout(verticallayout1,4)

        self.setLayout(horizontalLayout)


#signals and slots: connecting the buttons with their desired action
        self.openFile.clicked.connect(self.file)
        self.processButton.clicked.connect(self.preprocess)
        self.dumpButton.clicked.connect(self.dumpStar)
        self.dumpAllButton.clicked.connect(self.dumpAllStar)
        self.checkcor.clicked.connect(self.checkcorltn)
        self.diffLC.clicked.connect(self.calcdiffLC)
        self.dumpButton1.clicked.connect(self.deletestar)
        self.viewfile.clicked.connect(self.finalfile)
        self.reset.clicked.connect(self.resetWorkspace)
        self.view_Plot.clicked.connect(self.plot)
        self.tips.clicked.connect(self.tipsAndTricks)

#default visibility of widgets
        self.viewfile.setVisible(False)
        self.openFile.setEnabled(True)
        self.stdValue.setEnabled(False)
        self.ciValue.setEnabled(False)
        self.orderValue.setEnabled(False)
        self.dumpIndex.setEnabled(False)
        self.dumpIndex1.setEnabled(False)
        self.checkcor.setEnabled(False)
        self.diffLC.setEnabled(False)
        self.progress.setVisible(False)
        self.progress1.setVisible(False)
        self.processButton.setEnabled(False)
        self.view_Value.setEnabled(False)
        self.view_Plot.setEnabled(False)
        self.dumpButton.setEnabled(False)
        self.dumpButton1.setEnabled(False)
        self.dumpAllButton.setEnabled(False)
        self.starID1.setEnabled(False)
        self.starID2.setEnabled(False)

#function to reset UI
    def resetWorkspace(self):
        self.dataName.clear()
        self.matrixSize.clear()
        self.stdValue.setEnabled(False)
        self.ciValue.setEnabled(False)
        self.orderValue.setEnabled(False)
        self.processButton.setEnabled(False)
        self.stdValue.setText("0.04")
        self.ciValue.setText("0.2")
        self.orderValue.setCurrentText("2")
        self.dumpIndex1.clear()
        self.dumpIndex1.setEnabled(False)
        self.dumpButton1.setEnabled(False)
        self.dumpIndex.clear()
        self.dumpIndex.setEnabled(False)
        self.view_Value.clear()  
        self.view_Value.setEnabled(False)  
        self.view_Plot.setEnabled(False)
        self.dumpButton.setEnabled(False)
        self.dumpAllButton.setEnabled(False)
        self.starID1.clear()
        self.starID1.setEnabled(False)
        self.starID2.clear()
        self.starID2.setEnabled(False)
        self.checkcor.setEnabled(False)
        self.diffLC.setEnabled(False)
        self.pear.clear()
        self.spear.clear()
        self.diffInfo.clear()
        self.busyLabel.clear()
        self.starInfo.clear()
        self.dumpInfo.clear()
        self.viewInfo.clear()
        self.viewfile.setVisible(False)
        self.figure.clear()
        self.canvas.draw()

    def plot(self):
#displaying an error message if the Star ID field is left empty
        if self.view_Value.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter a star ID")
            msg.setWindowTitle("Warning")
            msg.exec_()
            self.view_Value.clear()
#displaying an error message if some out of index Star ID is entered    
        elif (self.view_Value.text()) not in self.newdf.columns:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Enter valid Star ID")
            msg.setWindowTitle("Warning")
            msg.exec_()
            self.view_Value.clear()
        else:
            try:
                self.view_Plot_instance = plottingVariables(self.datecol, self.df, self.mat, self.view_Value.text())
                self.view_Plot_instance.show()
                self.viewInfo.setText(f"Light Curve of Star ID {int(self.view_Value.text())} plotted!")
                self.view_Value.clear()

            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Error plotting the Light Curve!")
                msg.setWindowTitle("Warning")
                msg.exec_() 

    def tipsAndTricks(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("COMING SOON")
        msg.setWindowTitle("Information")
        msg.exec_()

    def finalfile(self):
        path = self.dir+'/02Variable_Detection'
        path = os.path.realpath(path)
        if sys.platform == "win32":
            os.startfile(path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])

#function for fetching the star data file and displaying it's details like no. of frames & no. of stars
    def file(self):
        self.dir=Home.setupdir(self)
        os.chdir(self.dir)
        if "02Variable_Detection" not in os.listdir(self.dir):
            os.mkdir("02Variable_Detection")
        if "output" not in os.listdir("./02Variable_Detection/"):
            os.mkdir("02Variable_Detection/output")
        if "extras" not in os.listdir("./02Variable_Detection/"):
            os.mkdir("02Variable_Detection/extras")
        if "allLCs" not in os.listdir("./02Variable_Detection/output/"):
            os.mkdir("02Variable_Detection/output/allLCs")
            os.mkdir("02Variable_Detection/output/allLCs/diffLCs")
            os.mkdir("02Variable_Detection/output/allLCs/rawLCs")
        if "rawLCs" not in os.listdir("./02Variable_Detection/output/"):
            os.mkdir("02Variable_Detection/output/rawLCs")
        if "diffLCs" not in os.listdir("./02Variable_Detection/output/"):
            os.mkdir("02Variable_Detection/output/diffLCs")
        if "plots" not in os.listdir("./02Variable_Detection/"):
            os.mkdir("02Variable_Detection/plots")
        if "logs" not in os.listdir("./02Variable_Detection/"):
            os.mkdir("02Variable_Detection/logs")

        self.logtime = time.time()
        with open(f"02Variable_Detection/logs/VD_{self.logtime}.txt", "w") as file:
            file.write(f"Login Date and Time: {datetime.datetime.now()}")

        self.filename,_filter = QFileDialog.getOpenFileName(None, "Window name", self.dir, "CSV files (*.csv)")
        if self.filename == "":
            if self.dataName.text() == "":
                self.dataName.setText("No file selected")
            else:
                self.dataName.setText(self.dataName.text())
        else:
            self.openFile.setText("Load New Processed Data")
            self.std = self.stdValue.text()
            self.ci = self.ciValue.text()
            self.order = self.orderValue.currentText()
            self.dataName.setText(f"File: {self.filename.split('/')[-1]}")
            self.dataName.setWordWrap(True)
            self.df = pd.read_csv(self.filename)

            str_values=0
            for rowIndex, row in self.df.iterrows():
                for columnIndex, value in row.items():
                    if type(value) == int or type(value) ==float:
                        pass
                    else:
                        str_values = str_values+1
            if str_values > 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("String data not allowed. Please remove header or non numerical data before loading the file")
                msg.setWindowTitle("Warning")
                msg.exec_()
            else: 
                self.datecol = self.df.iloc[: , 0]
                self.df.drop(self.df.columns[[0]], axis = 1, inplace = True)
                self.newdf = pd.DataFrame(self.df)
                self.matrixSize.setText(f"Details: {self.df.shape[0]} frames & {self.df.shape[1]} stars")

                self.date = pd.DataFrame(self.datecol)
                self.stdValue.setEnabled(True)
                self.ciValue.setEnabled(True)
                self.orderValue.setEnabled(True)
                self.processButton.setEnabled(True)

        self.stdValue.setText("0.04")
        self.ciValue.setText("0.2")
        self.orderValue.setCurrentText("2")
        self.dumpIndex1.clear()
        self.dumpIndex1.setEnabled(False)
        self.dumpButton1.setEnabled(False)
        self.dumpIndex.clear()
        self.dumpIndex.setEnabled(False)
        self.view_Value.clear()
        self.view_Value.setEnabled(False)
        self.view_Plot.setEnabled(False)
        self.dumpButton.setEnabled(False)
        self.dumpAllButton.setEnabled(False)
        self.starID1.clear()
        self.starID1.setEnabled(False)
        self.starID2.clear()
        self.starID2.setEnabled(False)
        self.checkcor.setEnabled(False)
        self.diffLC.setEnabled(False)
        self.pear.clear()
        self.spear.clear()
        self.diffInfo.clear()
        self.busyLabel.clear()
        self.starInfo.clear()
        self.dumpInfo.clear()
        self.viewInfo.clear()
        self.viewfile.setVisible(False)
        self.figure.clear()
        self.canvas.draw()

#processing of the selected data file
    def preprocess(self):
#displaying a warning dialog box if the standard deviation fields is left empty
        if self.stdValue.text() == '' :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No value given for Standard Deviation")
            msg.setWindowTitle("Warning")
            msg.exec_()
        else: 
            try:
                self.progress.setVisible(True)
                self.progress.setMinimum(0)
                self.progress.setMaximum(0)
                QApplication.sendPostedEvents()
                QApplication.processEvents()
                
                self.std = float(self.stdValue.text())
                QApplication.processEvents()
                self.ci = float(self.ciValue.text())
                QApplication.processEvents()
                self.order = float(self.orderValue.currentText())
                QApplication.processEvents()
                self.df_new = self.newdf
                QApplication.processEvents()
                self.deleted_columns = []
                QApplication.processEvents()
                y = 0
                QApplication.processEvents()
                while True:
                    QApplication.processEvents()
#filtering out the required data from the loaded data file based on the entered value of standard deviation                    
                    y += 1
                    QApplication.processEvents()
                    self.df_row_mean = self.df_new.mean(axis=1)
                    QApplication.processEvents()

                    self.df_col_mean_1 = self.df_new.mean(axis=0)
                    QApplication.processEvents()

                    self.df_row_sub = self.df_new.subtract(self.df_row_mean, axis=0)
                    QApplication.processEvents()

                    self.df_col_mean = self.df_row_sub.mean(axis=0)
                    QApplication.processEvents()

                    self.df_col_sub = self.df_row_sub.subtract(self.df_col_mean, axis=1)
                    QApplication.processEvents()

                    self.df_mean = self.df_col_sub.mean(axis=0)
                    QApplication.processEvents()

                    self.df_std = self.df_col_sub.std(axis=0)
                    QApplication.processEvents()

                    self.sorted_index = []
                    QApplication.processEvents()
                    for i in self.df_new.columns:
                        QApplication.processEvents()
                        if self.df_std[i] > self.std:
                            QApplication.processEvents()
                            self.sorted_index.append(i)
                            QApplication.processEvents()
                    self.df_sorted_index = pd.Series(self.df_std[self.sorted_index])
                    QApplication.processEvents()
                    if self.sorted_index == []:
                        QApplication.processEvents()
                        break
                    QApplication.processEvents()
                    self.df_new = self.df_new.drop([self.df_sorted_index.idxmax()], axis=1)
                    QApplication.processEvents()
                    self.deleted_columns.append(self.df_sorted_index.idxmax())
                    QApplication.processEvents()

                self.df_new = self.df_new.round(3)
                QApplication.processEvents()
                
                self.aftermath = pd.DataFrame({"#Star ID": self.df_new.columns, "Avg Mag": self.df_col_mean_1, "Standard Dev": self.df_std})
                QApplication.processEvents()
                self.aftermath = self.aftermath.round(3)
                QApplication.processEvents()

#saving the filtered out data in separate files
                self.df_new.to_csv(self.dir+'/02Variable_Detection/extras/NonVariables.csv', index=None)
                QApplication.processEvents()
                self.aftermath.to_csv(self.dir+'/02Variable_Detection/extras/NonVariables_info.csv', index=None)
                QApplication.processEvents()

                self.busyLabel.setText(f"Variables Detected! \nNo. of iterations: {y} \nDetails: {self.df_new.shape[0]} frames & {self.df_new.shape[1]} non-variables")
                QApplication.processEvents()

                self.processButton.setEnabled(True)
                QApplication.processEvents()
                self.checkcor.setEnabled(True)
                self.diffLC.setEnabled(True)
                QApplication.processEvents()

                self.variableStar()
                QApplication.processEvents()

                self.progress.hide()
                QApplication.processEvents()
                self.starID1.setEnabled(True)
                self.starID2.setEnabled(True)

#displaying an error message if some text is entered in the standard deviation field
            except ValueError:
                QApplication.processEvents()
                self.progress.setValue(0)
                self.progress.hide()
                self.busyLabel.setText("")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Pass numerical values only")
                msg.setWindowTitle("Warning")
                msg.exec_()

#function for plotting the stars w.r.t. their magnitude and standard deviation
    def variableStar(self):

        df_standard = self.df_new

        df_average = self.newdf.mean(axis=0)

        df_standard = df_standard.mean(axis=1)
        df_standard.to_csv(self.dir+'/02Variable_Detection/extras/standard_row_mean.csv', index=None)

        matc = self.newdf
        mats = df_standard
        Onestd = mats.iloc[1:]

        matd = -1 * matc.subtract(mats, axis=0)
        self.mat=matd
        round(matd, 3).to_csv(self.dir+'/02Variable_Detection/extras/standard_minus_row_mean.csv', index=None)

        x = matd.mean()
        y = matd.std()
        plt.figure(figsize=(20,15))
        plt.scatter(x, y,s=40, c='#d13f3f', marker='*', alpha=0.8)
        plt.title("Differential Ensemble plot")
        plt.xlabel("Mean Magnitude")
        plt.ylabel("Standard Deviation")
        plt.savefig(self.dir+'/02Variable_Detection/plots/diffEnsPlot.png')
        plt.close()

        matc_col_avg = matd.mean(axis=0)
        matc_col_avg.tail()

        matg = matd.subtract(matc_col_avg, axis=1)
        matg.tail()

        matg_sq = np.square(matg)
        matg_sq.tail()

        matv_col_avg = matg_sq.mean(axis=0)
        matv_col_avg.tail()

        sd = np.sqrt(matv_col_avg)
        sd.tail()

        # fitting
        self.ensemble = pd.concat([df_average, sd],axis=1)
        x_ens = self.ensemble[0].values
        x_ens = x_ens.reshape(-1,1)
        y_ens = self.ensemble[1].values

        x_fit = x_ens
        x_conf = x_fit - self.ci*x_fit.std()

        fit_polyReg = PolynomialFeatures(degree=int(self.order))
        fit_x_poly = fit_polyReg.fit_transform(x_fit)
        fit_reg = LinearRegression()
        fit_reg.fit(fit_x_poly,y_ens)
        fit_pred_y = fit_reg.predict(fit_polyReg.transform(x_ens))

        conf_polyReg = PolynomialFeatures(degree=int(self.order))
        conf_x_poly = conf_polyReg.fit_transform(x_conf)
        conf_reg = LinearRegression()
        conf_reg.fit(conf_x_poly,y_ens)
        conf_pred_y = conf_reg.predict(conf_polyReg.transform(x_ens))

        # automating variable detection
        variable = []
        for avg,std in zip(self.ensemble[0], self.ensemble[1]):
            if std > conf_reg.predict(conf_polyReg.transform([[avg]])):
                variable.append(1)
            else:
                variable.append(0)
        
        self.ensemble["variable"] = variable

        colour = ["b" if i == 0 else "r" for i in variable]
        leg = ["variable" if i == 0 else "r" for i in variable]

        red_patch = mpatches.Patch(color='r', label='Variable')
        blue_patch = mpatches.Patch(color='b', label='Non-Variable')

        self.canvas.show()
        self.figure.clear()
        self.ax = self.figure.add_subplot()

        #plot the fit
        self.ax.scatter(x=df_average, y=conf_pred_y, s=20, c='y', marker='.', alpha=0.8)

        self.ax.scatter(x=df_average, y=sd, s=40, c=colour, marker='*', alpha=0.8)
        self.ax.set_xlabel("Star Mean Magnitude")
        self.ax.set_ylabel("Standard Deviation")
        self.ax.set_title("Star Ensemble plot (Hover for Details)")
        self.ax.legend(handles=[red_patch,blue_patch])

        mplcursors.cursor(self.canvas.figure.axes, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(df_average.index[sel.target.index]))
        self.canvas.figure.savefig(self.dir+'/02Variable_Detection/plots/StarEnsemblePlot2.png')
        self.figure.tight_layout(pad=1.0)
        self.canvas.draw()
        self.dumpIndex1.setEnabled(True)
        self.dumpButton1.setEnabled(True)
        self.dumpIndex.setEnabled(True)
        self.view_Value.setEnabled(True)
        self.view_Plot.setEnabled(True)
        self.dumpButton.setEnabled(True)
        self.dumpAllButton.setEnabled(True)

        self.ensemble.to_csv(self.dir+'/02Variable_Detection/extras/PlotEnsemble.csv', index=None, header=None)


#function to delete a star using the star ID
    def deletestar(self):
        self.starInfo.setVisible(True)
        self.starInfo.clear()
        self.deletedstars=[]
        if self.dumpIndex1.text() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please input a star id to delete")
            msg.setWindowTitle("Warning")
            msg.exec_()
        else:
            try:
                x = self.dumpIndex1.text()
                x = x.split(",")
                column = x
                self.newdf = self.newdf.drop(column, axis=1)
                self.starInfo.setText(f"Star ID {column} removed, Updating Plot...")
                self.deletedstars.append(column)
                self.preprocess()
                self.variableStar()
                self.starInfo.clear()
                self.dumpIndex1.clear()
                self.starInfo.setText("Plot Updated!")
                self.newdfs = pd.concat([self.date, self.newdf],axis=1)
                self.newdfs.to_csv(self.dir+'/02Variable_Detection/extras/UpdatedEnsemble.csv', index=None)
                with open(f"02Variable_Detection/logs/VD_{self.logtime}.txt", "a") as file:
                    file.write(f"\nDeleted stars: {self.deletedstars}")

            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Invalid Star ID")
                msg.setWindowTitle("Warning")
                msg.exec_()
                self.dumpIndex1.clear()
                
#function for saving the Light Curve data of a star based on it's Star ID
    def dumpStar(self):
#displaying an error message if the Star ID field is left empty        
        if self.dumpIndex.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter a star ID")
            msg.setWindowTitle("Warning")
            msg.exec_()
#displaying an error message if some out of index Star ID is entered    
        elif (self.dumpIndex.text()) not in self.newdf.columns:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Enter valid Star ID")
            msg.setWindowTitle("Warning")
            msg.exec_()
            self.dumpIndex.clear()
        else:
#saving the light curve of the specified star
            try:
                self.savedstars=[]
                dstar = pd.concat([self.date, self.newdf[(self.dumpIndex.text())]],axis=1)
                dstar = dstar.round(3)
                dstar.to_csv(self.dir+'/02Variable_Detection/output/rawLCs/lc_'f"{int(self.dumpIndex.text())}.csv", header=None, index=None)
                dpstar = pd.concat([self.date, self.mat[(self.dumpIndex.text())]],axis=1)
                dpstar = dpstar.round(3)
                dpstar.to_csv(self.dir+'/02Variable_Detection/output/diffLCs/lc_'f"{int(self.dumpIndex.text())}.csv", header=None, index=None)
                self.savedstars.append(self.dumpIndex.text())
                self.starInfo.clear()
                self.starInfo.setVisible(False)
                self.viewInfo.clear()
                self.dumpInfo.setText(f"Light Curve of Star ID {int(self.dumpIndex.text())} saved!")
                self.viewfile.setVisible(True)
                self.dumpIndex.clear()

                with open(f"02Variable_Detection/logs/VD_{self.logtime}.txt", "a") as file:
                    file.write(f"\nSaved stars: {self.savedstars}")
#displaying a warning message during the saving of light curve data of a star if the date data is not loaded
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Error Saving / File already exists")
                msg.setWindowTitle("Warning")
                msg.exec_()       

#function for saving the Light Curve data of all star
    def dumpAllStar(self):
#saving the light curve of the specified star
        try:
            self.progress1.setVisible(True)
            self.progress1.setMinimum(0)
            self.progress1.setMaximum(0)
            QApplication.sendPostedEvents()
            QApplication.processEvents()
            
            for i in self.newdf.columns:
                dstar = pd.concat([self.date, self.newdf[i]],axis=1)
                dstar = dstar.round(3)
                dstar.to_csv(self.dir+'/02Variable_Detection/output/allLCs/rawLCs/lc_'f"{i}.csv", header=None, index=None)
                dpstar = pd.concat([self.date, self.mat[i]],axis=1)
                dpstar = dpstar.round(3)
                dpstar.to_csv(self.dir+'/02Variable_Detection/output/allLCs/diffLCs/lc_'f"{i}.csv", header=None, index=None)

            self.progress1.hide()
            QApplication.processEvents

            self.starInfo.clear()
            self.starInfo.setVisible(False)
            self.viewInfo.clear()
            self.dumpInfo.setText("Light Curve of all Stars saved!")
            self.viewfile.setVisible(True)

    #displaying a warning message during the saving of light curve data of a star if the date data is not loaded
        except:
            QApplication.processEvents()
            self.progress1.setValue(0)
            self.progress1.hide()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Error Saving / File already exists")
            msg.setWindowTitle("Warning")
            msg.exec_()

    def checkcorltn(self):

        if self.starID1.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter star ID1")
            msg.setWindowTitle("Warning")
            msg.exec_()

        elif self.starID2.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter star ID2")
            msg.setWindowTitle("Warning")
            msg.exec_()

        elif (((self.starID1.text()) not in self.newdf.columns) and ((self.starID2.text()) not in self.newdf.columns)):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Star ID1 and Star ID2 out of range")
            msg.setWindowTitle("Warning")
            msg.exec_()

        elif (self.starID1.text()) not in self.newdf.columns:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Invalid Star ID1")
            msg.setWindowTitle("Warning")
            msg.exec_()

        elif (self.starID2.text()) not in self.newdf.columns:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Invalid Star ID2")
            msg.setWindowTitle("Warning")
            msg.exec_()

        else:
            x = str(self.starID1.text())
            y = str(self.starID2.text())
            
            star1 = self.newdf[x]
            star2 = self.newdf[y]
            
            pearson = stats.pearsonr(star1, star2)
            spearman = stats.spearmanr(star1, star2)
            
            p=round(pearson[0],4)
            s=round(spearman[0],4)
            with open(f"02Variable_Detection/logs/VD_{self.logtime}.txt", "a") as file:
                        file.write(f"\nStar ID1: {str(self.starID1.text())}, Star ID2: {str(self.starID2.text())}")
                        file.write(f"\nPearson Coefficient: {pearson[0]}\nSpearman Coefficient: {spearman[0]}")

            self.starInfo.clear()
            self.starInfo.setVisible(False)
            self.pear.setText(f"Pearson: {p}")
            self.spear.setText(f"Spearman: {s}")

    def calcdiffLC(self):

        if self.starID1.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter star ID1")
            msg.setWindowTitle("Warning")
            msg.exec_()

        elif self.starID2.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter star ID2")
            msg.setWindowTitle("Warning")
            msg.exec_()

        elif (((self.starID1.text()) not in self.newdf.columns) and ((self.starID2.text()) not in self.newdf.columns)):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Star ID1 and Star ID2 out of range")
            msg.setWindowTitle("Warning")
            msg.exec_()

        elif (self.starID1.text()) not in self.newdf.columns:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Invalid Star ID1")
            msg.setWindowTitle("Warning")
            msg.exec_()

        elif (self.starID2.text()) not in self.newdf.columns:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Invalid Star ID2")
            msg.setWindowTitle("Warning")
            msg.exec_()

        else:
            try:
                x = str(self.starID1.text())
                y = str(self.starID2.text())
                
                self.star1 = self.newdf[x]
                self.star2 = self.newdf[y]
                self.diffMag = self.star1 - self.star2
                self.diffMag = self.diffMag.round(3)

                self.diffLCs = pd.concat([self.date, self.diffMag],axis=1)
                self.diffLCs.to_csv(self.dir+'/02Variable_Detection/output/diffLCs/lc_'f"{int(self.starID1.text())}"'-'f"{int(self.starID2.text())}.csv", header=None, index=None)

                self.starInfo.clear()
                self.starInfo.setVisible(False)
                self.diffInfo.setText(f"Differential Light Curve of Star ID [{int(self.starID1.text())}-{int(self.starID2.text())}] saved!")
                self.viewfile.setVisible(True)

                self.view_diffPlot_instance = plottingDifferential(self.date, self.diffMag)
                self.view_diffPlot_instance.show()

            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Error plotting the Light Curve!")
                msg.setWindowTitle("Warning")
                msg.exec_()

#creating a subclass of QWidget
class plottingVariables(QWidget):
    def __init__(self, date, df, mat, lc):
        super().__init__()
        self.setWindowTitle("Light Curve Viewer")

        starNumber = QLineEdit()

        verticallayout1 = QVBoxLayout()
        self.figure1 = plt.Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.toolbar1 = NavigationToolbar(self.canvas1, self)
        verticallayout1.addWidget(self.canvas1)
        verticallayout1.addWidget(self.toolbar1)

        verticallayout2 = QVBoxLayout()
        self.figure2 = plt.Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        verticallayout2.addWidget(self.canvas2)
        verticallayout2.addWidget(self.toolbar2)

        horizontallayout = QHBoxLayout()
        horizontallayout.addLayout(verticallayout1)
        horizontallayout.addLayout(verticallayout2)
        self.setLayout(horizontallayout)

        self.canvas1.show()
        self.figure1.clear()
        self.ax1 = self.figure1.add_subplot()
        self.ax1.scatter(date, df[lc], s=20, alpha=0.8, label=lc)
        self.ax1.set_xlabel("Julian Date")
        self.ax1.set_ylabel("Magnitude")
        self.ax1.invert_yaxis()
        self.ax1.set_title("Original Light Curve")
        self.ax1.legend(labelcolor = 'Red', fontsize = 'large', loc = 'best')
        self.figure1.tight_layout(pad=1.0)
        self.canvas1.draw()

        self.canvas2.show()
        self.figure2.clear()
        self.ax2 = self.figure2.add_subplot()
        self.ax2.scatter(date, mat[lc], s=20, alpha=0.8, label=lc)
        self.ax2.set_xlabel("Julian Date")
        self.ax2.set_ylabel("Magnitude")
        self.ax2.invert_yaxis()
        self.ax2.set_title("Differential Light Curve")
        self.ax2.legend(labelcolor = 'Red', fontsize = 'large', loc = 'best')
        self.figure2.tight_layout(pad=1.0)
        self.canvas2.draw()

#creating a subclass of QWidget
class plottingDifferential(QWidget):
    def __init__(self, jd, mag):
        super().__init__()
        self.setWindowTitle("Light Curve Viewer")

        starNumber = QLineEdit()

        verticallayout = QVBoxLayout()
        self.diff_figure = plt.Figure()
        self.diff_canvas = FigureCanvas(self.diff_figure)
        self.diff_toolbar = NavigationToolbar(self.diff_canvas, self)
        verticallayout.addWidget(self.diff_canvas)
        verticallayout.addWidget(self.diff_toolbar)

        horizontallayout = QHBoxLayout()
        horizontallayout.addLayout(verticallayout)
        self.setLayout(horizontallayout)

        self.diff_canvas.show()
        self.diff_figure.clear()
        self.diff_ax = self.diff_figure.add_subplot()
        self.diff_ax.scatter(jd, mag, s=20, alpha=0.8)
        self.diff_ax.set_xlabel("Julian Date")
        self.diff_ax.set_ylabel("Magnitude")
        self.diff_ax.invert_yaxis()
        self.diff_ax.set_title("Differential Light Curve")
        self.diff_figure.tight_layout(pad=1.0)
        self.diff_canvas.draw()