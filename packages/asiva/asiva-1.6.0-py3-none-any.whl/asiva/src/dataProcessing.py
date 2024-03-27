#Importing required modules
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QFileDialog, QToolButton, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QLabel,
                            QTableWidget, QComboBox, QMessageBox, QProgressBar, QRadioButton)
from PyQt5.QtCore import *
import numpy as np
import pandas as pd
import os, subprocess
import datetime
import time
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import seaborn as sns
import qtawesome as qta
from collections import Counter
from asiva.src.home import *
plt.style.use('seaborn-ticks')

# creating a subclass of QWidget
class DataProcessing(QWidget):
    
    def __init__(self):
        super(DataProcessing, self).__init__()

#Adding QWidgets in GUI --- Setting the layout

        horizontalLayout = QHBoxLayout()
        verticalLayout = QVBoxLayout()

        impute_icon = qta.icon('fa5s.check',
                        color='white')

        plot_icon = qta.icon('fa5s.chart-pie',
                        color='white')

        save_icon = qta.icon('fa5s.save',
                        color='white')

        stats_icon = qta.icon('fa5s.table',
                        color='white')

        folder_icon = qta.icon('fa5s.folder-open',
                        color='white')

        files_icon = qta.icon('fa5s.eye',
                        color='#2196f3')

        group_icon = qta.icon('fa5s.layer-group',
                        color='white')

        tips_icon = qta.icon('fa5s.lightbulb',
                        color='#e8a92c')

        self.loadData = QPushButton("Load Ensemble Data")
        self.loadData.setIcon(folder_icon)
        self.loadData.setIconSize(QSize(30, 30))
        self.loadData.setStyleSheet(u"QPushButton{\n"
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

        self.fileNameLabel = QLabel()
        self.fileNameLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #ff9800;\n"
                                    "}\n"
                                    "")

        self.dropLabel = QLabel()
        self.dropLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: red;\n"
                                    "}\n"
                                    "")

        self.shapeLabel = QLabel()
        self.shapeLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #007427;\n"
                                    "}\n"
                                    "")

        self.missingLabel = QLabel()
        self.missingLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #007427;\n"
                                    "}\n"
                                    "")

        self.gn = QToolButton(text='Group Nights', checkable=True, checked=False)
        self.gn.setStyleSheet(u"QToolButton{\n"
                                    "background-color: #ebebeb;\n"
                                    "width:265%;\n"
                                    "min-height:30px;\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QToolButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "QToolButton:disabled {\n"
                                    "background-color:#cccccc;\n"
                                    "border:none;\n"
                                    "}\n"
                                    "")
        self.gn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.gn.setArrowType(QtCore.Qt.RightArrow)

        self.groupStrategyLabel = QLabel("Remainder Strategy")
        self.groupStrategyLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "")

        self.groupLabel = QLabel("Grouping Factor (Min. 3, only int)")
        self.groupLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "")

        self.groupBox = QLineEdit("3")
        self.groupBox.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:65%;\n"
                                    "min-height:30px;\n"
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
                                    "QLineEdit:disabled {\n"
                                    "background-color:#cccccc;\n"
                                    "border:none;\n"
                                    "}\n"
                                    "")

        self.groupNights = QPushButton("Group")
        self.groupNights.setIcon(group_icon)
        self.groupNights.setIconSize(QSize(30, 30))
        self.groupNights.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #4caf50;\n"
                                    "width:130%;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:white\n"
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

        self.groupInfos = QLabel()
        self.groupInfos.setWordWrap(True)
        self.groupInfos.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#00bcd4;\n"
                                    "}\n"
                                    "")

        self.groupInfo = QLabel()
        self.groupInfo.setWordWrap(True)
        self.groupInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#4caf50;\n"
                                    "}\n"
                                    "")

        self.groupstrategy =QComboBox()
        self.groupstrategy.setStyleSheet(u"QComboBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:100%;\n"
                                    "min-height:35px;\n"
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

        self.groupstrategy.addItem("--Select--")
        self.groupstrategy.addItem("Drop Remainder")
        self.groupstrategy.addItem("Include Remainder")

        self.removeSaccord = QToolButton(text='Remove Stars', checkable=True, checked=False)
        self.removeSaccord.setStyleSheet(u"QToolButton{\n"
                                    "background-color: #ebebeb;\n"
                                    "width:265%;\n"
                                    "min-height:30px;\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QToolButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "QToolButton:disabled {\n"
                                    "background-color:#cccccc;\n"
                                    "border:none;\n"
                                    "}\n"
                                    "")
        self.removeSaccord.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.removeSaccord.setArrowType(QtCore.Qt.RightArrow)
        
        self.filterLabel = QLabel("Missing Obs (%)")
        self.filterLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "")

        self.filterBox = QLineEdit()
        self.filterBox.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:65%;\n"
                                    "min-height:30px;\n"
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

        self.checkNan = QPushButton("Detect Stars")
        self.checkNan.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #4caf50;\n"
                                    "width:130%;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:white\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #22b33a;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "")

        self.removeOaccord = QToolButton(text='Remove Obs', checkable=True, checked=False)
        self.removeOaccord.setStyleSheet(u"QToolButton{\n"
                                    "background-color: #ebebeb;\n"
                                    "width:265%;\n"
                                    "min-height:30px;\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QToolButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "QToolButton:disabled {\n"
                                    "background-color:#cccccc;\n"
                                    "border:none;\n"
                                    "}\n"
                                    "")
        self.removeOaccord.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.removeOaccord.setArrowType(QtCore.Qt.RightArrow)

        verticalLayout.addWidget(self.loadData)
        verticalLayout.addWidget(self.fileNameLabel)
        verticalLayout.addWidget(self.dropLabel)
        verticalLayout.addWidget(self.shapeLabel)
        verticalLayout.addWidget(self.missingLabel)

        verticalLayout.addWidget(self.removeSaccord)
        verticalLayout.addWidget(self.filterLabel)

        horizontalLayout3 = QHBoxLayout()

        horizontalLayout3.addWidget(self.filterBox)
        horizontalLayout3.addWidget(self.checkNan)

        verticalLayout.addLayout(horizontalLayout3)

        verticalLayout2 = QVBoxLayout()

        self.displayFiltered = QTableWidget()
        self.displayFiltered.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.displayFiltered.horizontalHeader().setStyleSheet("QHeaderView { font-weight: bold; }")
        self.displayFiltered.setColumnCount(0)
        self.displayFiltered.setRowCount(0)
        self.displayFiltered.setStyleSheet(u"QTableWidget{\n"
                                    "min-width:0px;\n"
                                    "max-width:400px;\n"
                                    "font:13px;\n"
                                    "}\n"
                                    "")

        self.rowFiltered = QTableWidget()
        self.rowFiltered.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.rowFiltered.horizontalHeader().setStyleSheet("QHeaderView { font-weight: bold; }")
        self.rowFiltered.setColumnCount(0)
        self.rowFiltered.setRowCount(0)
        self.rowFiltered.setStyleSheet(u"QTableWidget{\n"
                                    "min-width:0px;\n"
                                    "max-width:400px;\n"
                                    "font:13px;\n"
                                    "}\n"
                                    "")

        verticalLayout2.addWidget(self.displayFiltered)
        verticalLayout2.addWidget(self.rowFiltered)

        verticalLayout3 = QVBoxLayout()
        verticalLayout3.setContentsMargins(10,0,0,0)

        # self.starLabel = QLabel()
        # self.starLabel.setStyleSheet(u"QLabel{\n"
        #                            "font:13px;\n"
        #                            "font-weight:bold;\n"
        #                            "text-decoration: underline;\n"
        #                            "color:red;\n"
        #                            "}\n"
        #                            "")

        self.statsTable = QTableWidget()
        self.statsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.statsTable.horizontalHeader().setStyleSheet("QHeaderView { font-weight: bold; }")
        self.statsTable.setColumnCount(0)
        self.statsTable.setRowCount(0)
        self.statsTable.setStyleSheet(u"QTableWidget{\n"
                                    "font:13px;\n"
                                    "}\n"
                                    "")

        horizontallayout2 = QHBoxLayout()

        self.figure1 = plt.Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = plt.Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        
        horizontallayout2.addWidget(self.canvas1,1)
        horizontallayout2.addWidget(self.statsTable,1)

        self.toolbar = NavigationToolbar(self.canvas2, self)
        verticalLayout3.addWidget(self.canvas2)
        verticalLayout3.addWidget(self.toolbar)
        # verticalLayout3.addWidget(self.starLabel)
        verticalLayout3.addLayout(horizontallayout2)

        

        self.removeLabel = QLabel("Enter Star IDs")
        self.removeLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "width:100%;\n"
                                    "font-weight:bold;\n"
                                    "min-height:30px;\n"
                                    "}\n"
                                    "")

        self.removeBox = QLineEdit()
        self.removeBox.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:65%;\n"
                                    "min-height:30px;\n"
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

        self.removeButton = QPushButton("Remove Stars")
        self.removeButton.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #ff9800;\n"
                                    "width:130%;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #fcbe03;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "")

        verticalLayout.addWidget(self.removeLabel)

        horizontalLayout1 = QHBoxLayout()

        self.radiobuttonC1 = QRadioButton("Specific Stars")
        self.radiobuttonC1.setChecked(False)
        horizontalLayout1.addWidget(self.radiobuttonC1, 0)

        self.radiobuttonC2 = QRadioButton("All Stars")
        horizontalLayout1.addWidget(self.radiobuttonC2, 1)

        verticalLayout.addLayout(horizontalLayout1)

        horizontalLayout4 = QHBoxLayout()

        horizontalLayout4.addWidget(self.removeBox)
        horizontalLayout4.addWidget(self.removeButton)

        verticalLayout.addLayout(horizontalLayout4)

        self.removeInfo = QLabel()
        self.removeInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color: red;\n"
                                    "}\n"
                                    "")

        verticalLayout.addWidget(self.removeInfo)
        verticalLayout.addWidget(self.removeOaccord)

        self.rowFilterLabel = QLabel("Missing Obs (%)")
        self.rowFilterLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "width:100%;\n"
                                    "font-weight:bold;\n"
                                    "min-height:30px;\n"
                                    "}\n"
                                    "")

        verticalLayout.addWidget(self.rowFilterLabel)

        self.rowFilterBox = QLineEdit()
        self.rowFilterBox.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:65%;\n"
                                    "min-height:30px;\n"
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

        self.checkRowNan = QPushButton("Detect Obs")
        self.checkRowNan.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #4caf50;\n"
                                    "width:130%;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #22b33a;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "")

        horizontalLayout4 = QHBoxLayout()

        horizontalLayout4.addWidget(self.rowFilterBox)
        horizontalLayout4.addWidget(self.checkRowNan)

        verticalLayout.addLayout(horizontalLayout4)

        self.rowRemoveLabel = QLabel("Enter Obs IDs")
        self.rowRemoveLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "min-height:30px;\n"
                                    "}\n"
                                    "")

        verticalLayout.addWidget(self.rowRemoveLabel)

        self.rowRemoveBox = QLineEdit()
        self.rowRemoveBox.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:65%;\n"
                                    "min-height:35px;\n"
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

        horizontalLayout7 = QHBoxLayout()

        self.radiobuttonR1 = QRadioButton("Specific Obs")
        self.radiobuttonR1.setChecked(False)
        horizontalLayout7.addWidget(self.radiobuttonR1, 0)

        self.radiobuttonR2 = QRadioButton("All Obs")
        horizontalLayout7.addWidget(self.radiobuttonR2, 1)

        verticalLayout.addLayout(horizontalLayout7)

        self.removeObsButton = QPushButton("Remove Obs")
        self.removeObsButton.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #ff9800;\n"
                                    "width:130%;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #fcbe03;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "")

        horizontalLayout5 = QHBoxLayout()

        horizontalLayout5.addWidget(self.rowRemoveBox)
        horizontalLayout5.addWidget(self.removeObsButton)

        verticalLayout.addLayout(horizontalLayout5)


        self.removeObsInfo = QLabel()
        self.removeObsInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color: red;\n"
                                    "}\n"
                                    "")

        verticalLayout.addWidget(self.removeObsInfo)

        self.imputeAccord = QToolButton(text='Handle Missing Values', checkable=True, checked=False)
        self.imputeAccord.setStyleSheet(u"QToolButton{\n"
                                    "background-color: #ebebeb;\n"
                                    "width:265%;\n"
                                    "min-height:30px;\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QToolButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "QToolButton:disabled {\n"
                                    "background-color:#cccccc;\n"
                                    "border:none;\n"
                                    "}\n"
                                    "")
        self.imputeAccord.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.imputeAccord.setArrowType(QtCore.Qt.RightArrow)

        self.imputeLabel = QLabel("Impute Strategy")
        self.imputeLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "")

        self.strategy =QComboBox()
        self.strategy.setStyleSheet(u"QComboBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:100%;\n"
                                    "min-height:35px;\n"
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

        self.strategy.addItem("--Select--")
        self.strategy.addItem("Mean")
        self.strategy.addItem("Median")
        self.strategy.addItem("Backward Fill")
        self.strategy.addItem("Forward Fill")
        self.strategy.addItem("Most Frequent")
        self.strategy.addItem("Custom Value")

        vl = QVBoxLayout()
        hlayout =   QHBoxLayout()
        self.constantLabel = QLabel("Constant")
        self.constantLabel.setFixedSize(70, 15)
        self.constantLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-style: italic;\n"
                                    "}\n"
                                    "")

        self.constantValue = QLineEdit()
        self.constantValue.setStyleSheet(u"QLineEdit{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:100%;\n"
                                    "min-height:30px;\n"
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
                                    "QLineEdit:disabled {\n"
                                    "background-color:#cccccc;\n"
                                    "border:none;\n"
                                    "}\n"
                                    "")

        hlayout.addWidget(self.constantLabel)
        hlayout.addWidget(self.constantValue)

        vl.addLayout(hlayout)

        self.imputeButton = QPushButton("Impute")
        self.imputeButton.setIcon(impute_icon)
        self.imputeButton.setIconSize(QSize(30, 30))
        self.imputeButton.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "width:100%;\n"
                                    "min-height:35px;\n"
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

        self.imputeInfo = QLabel()
        self.imputeInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#00bcd4;"
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

        self.plotButton =QPushButton("Plot Results")
        self.plotButton.setIcon(plot_icon)
        self.plotButton.setIconSize(QSize(30, 30))
        self.plotButton.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #2196f3;\n"
                                    "width:100%;\n"
                                    "min-height:35px;\n"
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

        self.statsInfo = QLabel()
        self.statsInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#00bcd4;"
                                    "}\n"
                                    "")

        self.saveButton = QPushButton("Save Data")
        self.saveButton.setIcon(save_icon)
        self.saveButton.setIconSize(QSize(30, 30))
        self.saveButton.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #4caf50;\n"
                                    "width:100%;\n"
                                    "min-height:35px;\n"
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

        self.saveStatus = QLabel()

        self.viewfile = QPushButton("View Files")
        self.viewfile.setIcon(files_icon)
        self.viewfile.setIconSize(QSize(30, 30))
        self.viewfile.setStyleSheet(u"QPushButton{\n"
                                    "width:100%;\n"
                                    "border:2px solid #2196f3;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius: 5px;\n"
                                    "color: #2196f3;\n"
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

        verticalLayout.addWidget(self.imputeAccord)        
        verticalLayout.addWidget(self.imputeLabel)
        verticalLayout.addWidget(self.strategy)
        verticalLayout.addLayout(vl)
        verticalLayout.addWidget(self.imputeButton)
        verticalLayout.addWidget(self.imputeInfo)

        verticalLayout.addWidget(self.gn)
        verticalLayout.addWidget(self.groupStrategyLabel)
        verticalLayout.addWidget(self.groupstrategy)
        verticalLayout.addWidget(self.groupLabel)

        horizontalLayout6 = QHBoxLayout()
        horizontalLayout6.addWidget(self.groupBox)
        horizontalLayout6.addWidget(self.groupNights)

        verticalLayout.addLayout(horizontalLayout6)
        verticalLayout.addWidget(self.groupInfos)
        verticalLayout.addWidget(self.groupInfo)

        verticalLayout.addWidget(self.progress)

        verticalLayout.addWidget(self.plotButton)
        verticalLayout.addWidget(self.statsInfo)

        verticalLayout.addWidget(self.saveButton)
        verticalLayout.addWidget(self.saveStatus)

        verticalLayout.addWidget(self.viewfile)
        verticalLayout.addStretch()

        verticalLayout.addLayout(horizontalLayout10)
        verticalLayout.addLayout(horizontalLayout9)
        horizontalLayout.addLayout(verticalLayout)
        horizontalLayout.addLayout(verticalLayout2)
        horizontalLayout.addLayout(verticalLayout3, 5)

        horizontalLayout.addStretch()
        self.setLayout(horizontalLayout)

#Connecting Signals
        self.loadData.clicked.connect(self.loadFile)
        self.imputeAccord.pressed.connect(self.impute_accord)
        self.gn.pressed.connect(self.group_nights)
        self.removeSaccord.pressed.connect(self.star)
        self.removeOaccord.pressed.connect(self.obs)
        self.groupNights.clicked.connect(self.groupByFunction)
        self.checkNan.clicked.connect(self.filter)
        self.checkRowNan.clicked.connect(self.row_filter)
        self.radiobuttonC1.toggled.connect(self.onClickedC)
        self.radiobuttonC2.toggled.connect(self.onClickedC)
        self.removeButton.clicked.connect(self.remove)
        self.radiobuttonR1.toggled.connect(self.onClickedR)
        self.radiobuttonR2.toggled.connect(self.onClickedR)
        self.removeObsButton.clicked.connect(self.remove_row)
        self.viewfile.clicked.connect(self.finalfile)
        self.strategy.activated[str].connect(self.impute_strategy)
        self.imputeButton.clicked.connect(self.impute)
        self.groupstrategy.activated[str].connect(self.group_strategy)
        self.plotButton.clicked.connect(self.plots)
        self.saveButton.clicked.connect(self.save)
        self.reset.clicked.connect(self.resetWorkspace)
        self.tips.clicked.connect(self.tipsAndTricks)

#Setting default status of widgets
        self.loadData.setEnabled(True)
        self.groupLabel.setVisible(False)
        self.groupBox.setVisible(False)
        self.groupNights.setVisible(False)
        self.groupInfo.setVisible(False)
        self.groupInfos.setVisible(False)
        self.gn.setEnabled(False)
        self.imputeAccord.setEnabled(False)
        self.removeSaccord.setEnabled(False)
        self.removeOaccord.setEnabled(False)
        self.strategy.setEnabled(False)
        self.groupstrategy.setVisible(False)
        self.groupStrategyLabel.setVisible(False)
        self.constantValue.setEnabled(False)
        self.checkNan.setEnabled(False)
        self.radiobuttonC1.setEnabled(False)
        self.radiobuttonC2.setEnabled(False)
        self.radiobuttonR1.setEnabled(False)
        self.radiobuttonR2.setEnabled(False)
        self.checkRowNan.setEnabled(False)
        self.imputeButton.setEnabled(False)
        self.plotButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.viewfile.setVisible(False)
        self.filterLabel.setVisible(False)
        self.filterBox.setVisible(False)
        self.checkNan.setVisible(False)
        self.radiobuttonC1.setVisible(False)
        self.radiobuttonC2.setVisible(False)
        self.radiobuttonR1.setVisible(False)
        self.radiobuttonR2.setVisible(False)
        self.displayFiltered.setVisible(False)
        self.removeLabel.setVisible(False)
        self.removeBox.setVisible(False)
        self.removeButton.setVisible(False)
        self.removeInfo.setVisible(False)
        self.rowFilterLabel.setVisible(False)
        self.rowFilterBox.setVisible(False)
        self.checkRowNan.setVisible(False)
        self.rowFiltered.setVisible(False)
        self.rowRemoveLabel.setVisible(False)
        self.rowRemoveBox.setVisible(False)
        self.removeObsButton.setVisible(False)
        self.removeObsInfo.setVisible(False)
        self.statsTable.setVisible(False)
        self.progress.setVisible(False)
        self.imputeLabel.setVisible(False)
        self.strategy.setVisible(False)
        self.constantValue.setVisible(False)
        self.constantLabel.setVisible(False)
        self.imputeButton.setVisible(False)
        self.toolbar.setVisible(False)

#function to reset UI
    def resetWorkspace(self):
        self.loadData.setEnabled(True)
        self.fileNameLabel.clear()
        self.dropLabel.clear()
        self.shapeLabel.clear()
        self.missingLabel.clear()
        self.gn.setEnabled(False)
        self.gn.setArrowType(QtCore.Qt.RightArrow)
        self.imputeAccord.setEnabled(False)
        self.imputeAccord.setArrowType(QtCore.Qt.RightArrow)
        self.removeSaccord.setEnabled(False)
        self.removeSaccord.setArrowType(QtCore.Qt.RightArrow)
        self.removeOaccord.setEnabled(False)
        self.removeOaccord.setArrowType(QtCore.Qt.RightArrow)
        self.strategy.setEnabled(False)
        self.checkNan.setEnabled(False)
        self.radiobuttonC1.setEnabled(False)
        self.radiobuttonC2.setEnabled(False)
        self.radiobuttonR1.setEnabled(False)
        self.radiobuttonR2.setEnabled(False)
        self.checkRowNan.setEnabled(False)

        self.checkNan.setVisible(False)
        self.radiobuttonC1.setVisible(False)
        self.radiobuttonC2.setVisible(False)
        self.radiobuttonR1.setVisible(False)
        self.radiobuttonR2.setVisible(False)
        self.checkRowNan.setVisible(False)
        self.filterLabel.setVisible(False)
        self.filterBox.setVisible(False)
        self.removeLabel.setVisible(False)
        self.removeButton.setVisible(False)
        self.removeBox.setVisible(False)
        self.removeInfo.setVisible(False)
        self.rowFilterLabel.setVisible(False)
        self.rowFilterBox.setVisible(False)
        self.checkRowNan.setVisible(False)
        self.rowRemoveLabel.setVisible(False)
        self.rowRemoveBox.setVisible(False)
        self.removeObsButton.setVisible(False)
        self.removeObsInfo.setVisible(False)

        self.plotButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.imputeButton.setEnabled(False)
        self.strategy.setCurrentText("--Select--")
        self.constantValue.clear()
        self.constantValue.setEnabled(False)
        self.imputeInfo.clear()
        self.imputeInfo.clear()
        self.saveStatus.clear()
        self.viewfile.setVisible(False)
        self.filterBox.clear()
        self.rowFilterBox.clear()
        self.removeBox.clear()
        self.rowRemoveBox.clear()
        self.removeInfo.clear()
        self.removeObsInfo.clear()
        self.figure1.clear()
        self.canvas1.draw()
        self.figure2.clear()
        self.canvas2.draw()
        # self.starLabel.clear()
        self.displayFiltered.setVisible(False)
        self.displayFiltered.setRowCount(0)
        self.displayFiltered.setColumnCount(0)
        self.rowFiltered.setVisible(False)
        self.rowFiltered.setRowCount(0)
        self.rowFiltered.setColumnCount(0)
        self.statsTable.setVisible(False)
        self.statsTable.setRowCount(0)
        self.statsTable.setColumnCount(0)
        self.statsInfo.clear()
        self.groupstrategy.setCurrentText("--Select--")
        self.groupstrategy.setVisible(False)
        self.groupStrategyLabel.setVisible(False)
        self.groupInfo.clear()
        self.groupBox.clear()
        self.groupLabel.setVisible(False)
        self.groupBox.setVisible(False)
        self.groupNights.setVisible(False)
        self.groupInfo.setVisible(False)
        self.progress.setVisible(False)
        self.groupBox.setText('3')
        self.loadData.setText("Load Ensemble Data")
        self.groupInfos.setVisible(False)
        self.imputeLabel.setVisible(False)
        self.strategy.setVisible(False)
        self.constantValue.setVisible(False)
        self.constantLabel.setVisible(False)
        self.imputeButton.setVisible(False)
        self.toolbar.setVisible(False)

    def tipsAndTricks(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("COMING SOON")
        msg.setWindowTitle("Information")
        msg.exec_()

    def finalfile(self):
        path = self.dir+'/01Data_Processing'
        path = os.path.realpath(path)
        if sys.platform == "win32":
            os.startfile(path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])

#function to load working directory
    def loadFile(self):
        self.dir=Home.setupdir(self)
        os.chdir(self.dir)
        if "01Data_Processing" not in os.listdir(self.dir):
            os.mkdir("01Data_Processing")
        if "plots" not in os.listdir("./01Data_Processing/"):
            os.mkdir("01Data_Processing/plots")
        if "logs" not in os.listdir("./01Data_Processing/"):
            os.mkdir("01Data_Processing/logs")
        if "output" not in os.listdir("./01Data_Processing/"):
            os.mkdir("01Data_Processing/output")
        if "extras" not in os.listdir("./01Data_Processing/"):
            os.mkdir("01Data_Processing/extras")
        self.fileName,_filter = QFileDialog.getOpenFileName(None, "Window name", self.dir, "CSV files (*.csv)")
        if self.fileName == "":
            if self.fileNameLabel.text() == "":
                self.fileNameLabel.setText("No file selected")
            else:
                self.fileNameLabel.setText(self.fileNameLabel.text())
        else:
            self.removeSaccord.setEnabled(True)
            self.removeOaccord.setEnabled(True)
            self.imputeAccord.setEnabled(True)
            self.groupLabel.setVisible(False)
            self.groupBox.setVisible(False)
            self.groupNights.setVisible(False)
            self.groupNights.setEnabled(False)
            self.groupBox.setEnabled(False)
            self.groupstrategy.setVisible(False)
            self.groupStrategyLabel.setVisible(False)
            self.checkNan.setEnabled(True)
            self.radiobuttonC1.setEnabled(True)
            self.radiobuttonC2.setEnabled(True)
            self.radiobuttonR1.setEnabled(True)
            self.radiobuttonR2.setEnabled(True)
            self.checkRowNan.setEnabled(True)
            self.plotButton.setEnabled(True)
            self.saveButton.setEnabled(False)
            self.imputeButton.setEnabled(False)
            self.strategy.setCurrentText("--Select--")
            self.groupstrategy.setCurrentText("--Select--")
            self.constantValue.clear()
            self.constantValue.setEnabled(False)
            self.imputeInfo.clear()
            self.saveStatus.clear()
            self.viewfile.setVisible(False)
            self.filterBox.clear()
            self.rowFilterBox.clear()
            self.removeBox.clear()
            self.rowRemoveBox.clear()
            self.removeInfo.clear()
            self.removeObsInfo.clear()
            self.figure1.clear()
            self.canvas1.draw()
            self.figure2.clear()
            self.canvas2.draw()
            self.toolbar.setVisible(False)
            # self.starLabel.clear()
            self.displayFiltered.setVisible(False)
            self.displayFiltered.setRowCount(0)
            self.displayFiltered.setColumnCount(0)
            self.rowFiltered.setVisible(False)
            self.rowFiltered.setRowCount(0)
            self.rowFiltered.setColumnCount(0)
            self.statsTable.setVisible(False)
            self.statsTable.setRowCount(0)
            self.statsTable.setColumnCount(0)
            self.statsInfo.clear()
            self.fileNameLabel.setText('')
            self.dropLabel.setText('')
            self.shapeLabel.setText('')
            self.missingLabel.setText('')
            self.grouped_df1 = []

            self.loadData.setText("Load New Ensemble Data")
            self.df = pd.read_csv(self.fileName, header=None)
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
                self.dm = self.df[0].isnull().sum(axis = 0)
                if self.dm == 0:
                    self.df.index = range(1, self.df.shape[0] + 1)
                    self.datecol = self.df.iloc[: , 0]
                    self.df.drop(self.df.columns[[0]], axis = 1, inplace = True)
                    self.df.columns = range(1, self.df.shape[1] + 1)

                    self.fileNameLabel.setText(f"File: {self.fileName.split('/')[-1]}")
                    
                    self.dropColumns = []
                    for i in self.df.columns:
                        if self.df[i].isnull().sum() == len(self.df):
                            self.df = self.df.drop(i,axis=1)
                            self.dropColumns.append(i)
                            self.dropLabel.setText(f"Dropping {self.dropColumns} columns")                           
                    
                    if len(self.dropColumns) != 0:
                        self.plotButton.setEnabled(False)

                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("Dropping entire empty columns!")
                        msg.setWindowTitle("Warning")
                        msg.exec_()

                    self.df = self.df.replace([np.inf, -np.inf, "nan "], np.nan)
                    self.shapeLabel.setText(f"Obs, Stars: ({self.df.shape[0]}, {self.df.shape[1]})")
                    self.missingLabel.setText(f"Missing Obs: {self.df.isnull().sum().sum()}")
                    self.ObsMissCount = self.df.isnull().sum().sum()

                    self.uniqueDates = []
                    for i in self.datecol:
                        self.uniqueDates.append(int(i))
                    y = Counter(self.uniqueDates)
                    self.dateCount = []
                    for i in y:
                        self.dateCount.append(y[i])
                    self.obsCounter = 0
                    for i in self.dateCount:
                        if i < 3:
                            self.obsCounter = self.obsCounter + 1
                        else:
                            pass
                    if self.obsCounter == len(self.dateCount):
                        self.groupBox.setEnabled(False)
                        self.groupNights.setEnabled(False)
                        self.groupstrategy.setEnabled(False)
                        self.groupInfos.setStyleSheet(u"QLabel{\n"
                                        "font:13px;\n"
                                        "font-weight:bold;\n"
                                        "color:red;\n"
                                        "}\n"
                                        "")
                        self.groupInfos.setText(f'Maximum observation per date is {max(self.dateCount)}. The dataset cannot be grouped')
                        self.grouping = False
                    else:
                        self.groupInfos.setText(f"Maximum possible grouping factor: {max(self.dateCount)}")
                        self.grouping = True
                        if self.ObsMissCount == 0:
                            self.groupBox.setEnabled(True)
                            self.groupNights.setEnabled(True)
                            self.groupstrategy.setEnabled(True)
                        else:
                            self.groupBox.setEnabled(False)
                            self.groupNights.setEnabled(False)
                            self.groupstrategy.setEnabled(False)

                    if self.ObsMissCount == 0:
                        self.removeSaccord.setEnabled(False)
                        self.removeOaccord.setEnabled(False)
                        self.imputeAccord.setEnabled(False)
                        self.strategy.setEnabled(False)
                        self.gn.setEnabled(True)
                    else:
                        self.removeSaccord.setEnabled(True)
                        self.removeOaccord.setEnabled(True)
                        self.imputeAccord.setEnabled(True)
                        self.strategy.setEnabled(True)
                        self.gn.setEnabled(False)
                        self.plotButton.setEnabled(False)
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Missing Data in Date Column")
                    msg.setWindowTitle("Warning")
                    msg.exec_()


#function to set accordian view
    def group_nights(self):
        checked = self.gn.isChecked()
        self.gn.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        self.removeSaccord.setArrowType(QtCore.Qt.RightArrow)
        self.removeOaccord.setArrowType(QtCore.Qt.RightArrow)
        self.imputeAccord.setArrowType(QtCore.Qt.RightArrow)

        if checked:
            self.groupLabel.setVisible(False)
            self.groupBox.setVisible(False)
            self.groupNights.setVisible(False)
            self.groupInfo.setVisible(False)
            self.groupInfos.setVisible(False)
            self.groupstrategy.setVisible(False)
            self.groupStrategyLabel.setVisible(False)
            
        else:
            self.groupLabel.setVisible(True)
            self.groupBox.setVisible(True)
            self.groupNights.setVisible(True)
            self.groupInfo.setVisible(True)
            self.groupInfos.setVisible(True)
            self.groupstrategy.setVisible(True)
            self.groupStrategyLabel.setVisible(True)
            self.groupstrategy.setEnabled(True)
            self.groupBox.setEnabled(False)
            self.groupNights.setEnabled(False)


        self.rowFilterLabel.setVisible(False)
        self.rowFilterBox.setVisible(False)
        self.checkRowNan.setVisible(False)
        self.rowFiltered.setVisible(False)
        self.rowRemoveLabel.setVisible(False)
        self.rowRemoveBox.setVisible(False)
        self.removeObsButton.setVisible(False)
        self.removeObsInfo.setVisible(False)
        self.filterLabel.setVisible(False)
        self.filterBox.setVisible(False)
        self.checkNan.setVisible(False)
        self.radiobuttonC1.setVisible(False)
        self.radiobuttonC2.setVisible(False)
        self.radiobuttonR1.setVisible(False)
        self.radiobuttonR2.setVisible(False)
        self.displayFiltered.setVisible(False)
        self.removeLabel.setVisible(False)
        self.removeBox.setVisible(False)
        self.removeButton.setVisible(False)
        self.removeInfo.setVisible(False)
        self.imputeLabel.setVisible(False)
        self.strategy.setVisible(False)
        self.constantValue.setVisible(False)
        self.constantLabel.setVisible(False)
        self.imputeButton.setVisible(False)
        self.imputeInfo.setVisible(False)



    def star(self):
        checked = self.removeSaccord.isChecked()
        self.removeSaccord.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        self.gn.setArrowType(QtCore.Qt.RightArrow)
        self.removeOaccord.setArrowType(QtCore.Qt.RightArrow)
        self.imputeAccord.setArrowType(QtCore.Qt.RightArrow)

        if checked:
            self.filterLabel.setVisible(False)
            self.filterBox.setVisible(False)
            self.checkNan.setVisible(False)
            self.radiobuttonC1.setVisible(False)
            self.radiobuttonC2.setVisible(False)
            self.displayFiltered.setVisible(False)
            self.removeLabel.setVisible(False)
            self.removeBox.setVisible(False)
            self.removeButton.setVisible(False)
            self.removeInfo.setVisible(False)
            
        else:
            self.filterLabel.setVisible(True)
            self.filterBox.setVisible(True)
            self.checkNan.setVisible(True)
            self.radiobuttonC1.setVisible(True)
            self.radiobuttonC2.setVisible(True)
            self.displayFiltered.setVisible(True)
            self.removeLabel.setVisible(True)
            self.removeBox.setVisible(True)
            self.removeButton.setVisible(True)
            self.radiobuttonC1.setEnabled(False)
            self.radiobuttonC2.setEnabled(False)
            self.removeBox.setEnabled(False)
            self.removeButton.setEnabled(False)
            self.removeInfo.setVisible(True)

        self.groupLabel.setVisible(False)
        self.groupBox.setVisible(False)
        self.groupNights.setVisible(False)
        self.groupstrategy.setVisible(False)
        self.groupStrategyLabel.setVisible(False)
        self.rowFilterLabel.setVisible(False)
        self.rowFilterBox.setVisible(False)
        self.radiobuttonR1.setVisible(False)
        self.radiobuttonR2.setVisible(False)
        self.checkRowNan.setVisible(False)
        self.rowFiltered.setVisible(False)
        self.rowRemoveLabel.setVisible(False)
        self.rowRemoveBox.setVisible(False)
        self.removeObsButton.setVisible(False)
        self.removeObsInfo.setVisible(False)
        self.imputeLabel.setVisible(False)
        self.strategy.setVisible(False)
        self.constantValue.setVisible(False)
        self.constantLabel.setVisible(False)
        self.imputeButton.setVisible(False)
        self.imputeInfo.setVisible(False)
        self.groupInfos.setVisible(False)
        self.groupInfo.setVisible(False)


#function to set accordian view
    def obs(self):
        checked = self.removeOaccord.isChecked()
        self.removeOaccord.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        self.gn.setArrowType(QtCore.Qt.RightArrow)
        self.removeSaccord.setArrowType(QtCore.Qt.RightArrow)
        self.imputeAccord.setArrowType(QtCore.Qt.RightArrow)

        if checked:
            self.rowFilterLabel.setVisible(False)
            self.rowFilterBox.setVisible(False)
            self.checkRowNan.setVisible(False)
            self.radiobuttonR1.setVisible(False)
            self.radiobuttonR2.setVisible(False)
            self.rowFiltered.setVisible(False)
            self.rowRemoveLabel.setVisible(False)
            self.rowRemoveBox.setVisible(False)
            self.removeObsButton.setVisible(False)
            self.removeObsInfo.setVisible(False)

        else:
            self.rowFilterLabel.setVisible(True)
            self.rowFilterBox.setVisible(True)
            self.checkRowNan.setVisible(True)
            self.radiobuttonR1.setVisible(True)
            self.radiobuttonR2.setVisible(True)
            self.rowFiltered.setVisible(True)
            self.rowRemoveLabel.setVisible(True)
            self.rowRemoveBox.setVisible(True)
            self.radiobuttonR1.setEnabled(False)
            self.radiobuttonR2.setEnabled(False)
            self.removeObsButton.setVisible(True)
            self.removeObsInfo.setVisible(True)

        self.groupLabel.setVisible(False)
        self.groupBox.setVisible(False)
        self.groupNights.setVisible(False)
        self.filterLabel.setVisible(False)
        self.filterBox.setVisible(False)
        self.checkNan.setVisible(False)
        self.radiobuttonC1.setVisible(False)
        self.radiobuttonC2.setVisible(False)
        self.displayFiltered.setVisible(False)
        self.removeLabel.setVisible(False)
        self.removeBox.setVisible(False)
        self.removeButton.setVisible(False)
        self.removeInfo.setVisible(False)
        self.imputeLabel.setVisible(False)
        self.strategy.setVisible(False)
        self.constantValue.setVisible(False)
        self.constantLabel.setVisible(False)
        self.imputeButton.setVisible(False)
        self.imputeInfo.setVisible(False)
        self.groupInfos.setVisible(False)
        self.groupInfo.setVisible(False)

    def impute_accord(self):
        checked = self.imputeAccord.isChecked()
        self.imputeAccord.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        self.removeSaccord.setArrowType(QtCore.Qt.RightArrow)
        self.removeOaccord.setArrowType(QtCore.Qt.RightArrow)
        self.gn.setArrowType(QtCore.Qt.RightArrow)

        if checked:
            self.imputeLabel.setVisible(False)
            self.strategy.setVisible(False)
            self.constantValue.setVisible(False)
            self.constantLabel.setVisible(False)
            self.imputeButton.setVisible(False)
            self.imputeInfo.setVisible(False)
            
        else:
            self.imputeLabel.setVisible(True)
            self.strategy.setVisible(True)
            self.constantValue.setVisible(True)
            self.constantLabel.setVisible(True)
            self.imputeButton.setVisible(True)
            self.imputeInfo.setVisible(True)

        self.groupLabel.setVisible(False)
        self.groupBox.setVisible(False)
        self.groupNights.setVisible(False)
        self.groupstrategy.setVisible(False)
        self.groupStrategyLabel.setVisible(False)
        self.rowFilterLabel.setVisible(False)
        self.rowFilterBox.setVisible(False)
        self.checkRowNan.setVisible(False)
        self.rowFiltered.setVisible(False)
        self.rowRemoveLabel.setVisible(False)
        self.rowRemoveBox.setVisible(False)
        self.removeObsButton.setVisible(False)
        self.removeObsInfo.setVisible(False)
        self.filterLabel.setVisible(False)
        self.filterBox.setVisible(False)
        self.checkNan.setVisible(False)
        self.radiobuttonC1.setVisible(False)
        self.radiobuttonC2.setVisible(False)
        self.radiobuttonR1.setVisible(False)
        self.radiobuttonR2.setVisible(False)
        self.displayFiltered.setVisible(False)
        self.removeLabel.setVisible(False)
        self.removeBox.setVisible(False)
        self.removeButton.setVisible(False)
        self.removeInfo.setVisible(False)
        self.groupInfos.setVisible(False)
        self.groupInfo.setVisible(False)

#function to filter missing data
    def filter(self):
        if self.filterBox.text() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Filtering % not entered")
            msg.setWindowTitle("Warning")
            msg.exec_()
        else:
            try:
                self.missIndex = []
                self.missCount = []
        
                x = self.df.isnull().sum()
                for (i,j) in zip(x.index,x):
                    if j != 0:
                        if j > float(self.filterBox.text())/100 * self.df.shape[0]:
                            self.missIndex.append(i)
                            self.missCount.append(j)
                        else:
                            pass

                self.radiobuttonC1.setEnabled(True)
                self.radiobuttonC2.setEnabled(True)
                self.missingData = pd.DataFrame({"Star ID": self.missIndex, "Missing Obs": self.missCount})

                self.displayFiltered.setColumnCount(self.missingData.shape[1])
                self.displayFiltered.setRowCount(self.missingData.shape[0])
                self.displayFiltered.setHorizontalHeaderLabels(["Star ID", "Missing Obs"])
                for i in range(len(self.missingData.index)):
                    for j in range(len(self.missingData.columns)):
                        self.displayFiltered.setItem(i,j,QTableWidgetItem(str(self.missingData.iloc[i, j])))

            except ValueError:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("numbers only")
                msg.setWindowTitle("Warning")
                msg.exec_()

#function to filter missing data from rows
    def row_filter(self):
        if self.rowFilterBox.text() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Filtering % not entered")
            msg.setWindowTitle("Warning")
            msg.exec_()
        else:
            try:
                self.row=[]
                self.count=[]
                
                x = self.df.isnull().sum(axis = 1)
                for (i,j) in zip(x.index,x):
                    if j != 0:
                        if j > float(self.rowFilterBox.text())/100 * self.df.shape[1]:
                            self.row.append(i)
                            self.count.append(j)

                self.radiobuttonR1.setEnabled(True)
                self.radiobuttonR2.setEnabled(True)        
                self.missingRowData = pd.DataFrame({"Night": self.row, "Missing Obs": self.count})
                self.missingRowData.drop_duplicates(keep=False, inplace=True)

                self.rowFiltered.setColumnCount(self.missingRowData.shape[1])
                self.rowFiltered.setRowCount(self.missingRowData.shape[0])
                self.rowFiltered.setHorizontalHeaderLabels(["Night", "Missing Obs"])
                for i in range(len(self.missingRowData.index)):
                    for j in range(len(self.missingRowData.columns)):
                        self.rowFiltered.setItem(i,j,QTableWidgetItem(str(self.missingRowData.iloc[i, j])))

            except ValueError:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("numbers only")
                msg.setWindowTitle("Warning")
                msg.exec_()       

#function to select star IDs to remove as column of data
    def onClickedC(self):
        if self.radiobuttonC1.isChecked() == True:
            self.removeBox.setEnabled(True)
            self.removeButton.setEnabled(True)
        if self.radiobuttonC2.isChecked() == True:
            self.removeBox.setEnabled(False)
            self.removeButton.setEnabled(True)

#function to select star IDs to remove as row of data
    def onClickedR(self):
        if self.radiobuttonR1.isChecked() == True:
            self.rowFilterBox.setEnabled(True)
            self.removeObsButton.setEnabled(True)
        if self.radiobuttonR2.isChecked() == True:
            self.rowFilterBox.setEnabled(False)
            self.removeObsButton.setEnabled(True)

#function to remove selected column of data
    def remove(self):
        try:
            os.makedirs(self.dir+'/01Data_Processing')
            os.makedirs(self.dir+'/01Data_Processing/logs')
            os.makedirs(self.dir+'/01Data_Processing/output')
            os.makedirs(self.dir+'/01Data_Processing/plots')
        except:
            pass
        if self.removeBox.text() == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Out of Range")
            msg.setWindowTitle("Warning")
            msg.exec_()

        if self.radiobuttonC1.isChecked() == True and self.removeBox.text() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter Star ID")
            msg.setWindowTitle("Warning")
            msg.exec_()
        else:
            try:
                if self.radiobuttonC1.isChecked() == True:
                    x = self.removeBox.text()
                    x = x.split(",")
                    column = [int(i) for i in x]
                    self.df = self.df.drop(column, axis=1)
                    self.removeInfo.setText(f"Star ID {column} removed")
                else:
                    column = self.missIndex
                    self.df = self.df.drop(column, axis=1)
                    self.removeInfo.setText(f"Star ID {column} removed")
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Invalid Star ID")
                msg.setWindowTitle("Warning")
                msg.exec_()

    def remove_row(self):
        try:
            os.makedirs(self.dir+'/01Data_Processing')
            os.makedirs(self.dir+'/01Data_Processing/logs')
            os.makedirs(self.dir+'/01Data_Processing/output')
            os.makedirs(self.dir+'/01Data_Processing/plots')
        except:
            pass
        if self.rowRemoveBox.text() == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Out of Range")
            msg.setWindowTitle("Warning")
            msg.exec_()
            
        if self.radiobuttonR1.isChecked() == True and self.rowRemoveBox.text() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter Obs. ID")
            msg.setWindowTitle("Warning")
            msg.exec_()
        else:
            try:
                if self.radiobuttonR1.isChecked() == True:
                    x = self.rowRemoveBox.text()
                    x = x.split(",")
                    row = [int(i) for i in x]
                    self.df = self.df.drop(row, axis=0)
                    self.datecol = self.datecol.drop(row, axis=0)
                    self.removeObsInfo.setText(f"Obs {row} removed")
                else:
                    row = self.row
                    self.df = self.df.drop(row, axis=0)
                    self.datecol = self.datecol.drop(row, axis=0)
                    self.removeObsInfo.setText(f"Star ID {row} removed")
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Invalid Obs. ID")
                msg.setWindowTitle("Warning")
                msg.exec_()

#function to enable impute button according to strategy text
    def impute_strategy(self):
        if self.strategy.currentText() == "--Select--":
            self.constantValue.setEnabled(False)
            self.imputeButton.setEnabled(False)
        elif self.strategy.currentText() == "Mean":
            self.constantValue.setEnabled(False)
            self.imputeButton.setEnabled(True)
            self.constantValue.clear()
        elif self.strategy.currentText() == "Median":
            self.constantValue.setEnabled(False)
            self.imputeButton.setEnabled(True)
            self.constantValue.clear()
        elif self.strategy.currentText() == "Backward Fill":
            self.constantValue.setEnabled(False)
            self.imputeButton.setEnabled(True)
            self.constantValue.clear()
        elif self.strategy.currentText() == "Forward Fill":
            self.constantValue.setEnabled(False)
            self.imputeButton.setEnabled(True)
            self.constantValue.clear()
        elif self.strategy.currentText() == "Most Frequent":
            self.constantValue.setEnabled(False)
            self.constantValue.clear()
            self.imputeButton.setEnabled(True)
        elif self.strategy.currentText() == "Custom Value":
            self.constantValue.setEnabled(True)
            self.imputeButton.setEnabled(True)
        else:
            pass

#funtion to calculate mean,median
    def impute(self):
        try:
            os.makedirs(self.dir+'/01Data_Processing')
            os.makedirs(self.dir+'/01Data_Processing/logs')
            os.makedirs(self.dir+'/01Data_Processing/output')
            os.makedirs(self.dir+'/01Data_Processing/plots')
        except:
            pass
        if self.grouping == True:
            self.gn.setEnabled(True)
            self.groupBox.setEnabled(True)
            self.groupNights.setEnabled(True)
        else:
            self.gn.setEnabled(True)
            self.groupBox.setEnabled(False)
            self.groupNights.setEnabled(False)
        columns = self.df.columns
        if self.strategy.currentText() == "Mean":
            imputer = SimpleImputer(strategy="mean")
            imputer.fit(self.df)
            self.df = imputer.transform(self.df)
            self.df = pd.DataFrame(self.df, columns=columns)
            self.imputeInfo.setText("Missing Obs Processed!")
            self.plotButton.setEnabled(True)
        elif self.strategy.currentText() == "Median":
            imputer = SimpleImputer(strategy="median")
            imputer.fit(self.df)
            self.df = imputer.transform(self.df)
            self.df = pd.DataFrame(self.df, columns=columns)
            self.imputeInfo.setText("Missing Obs Processed!")
            self.plotButton.setEnabled(True)
        elif self.strategy.currentText() == "Backward Fill":
            self.df = self.df.bfill(axis = 0).ffill(axis = 0)
            self.imputeInfo.setText("Missing Obs Processed!")
            self.plotButton.setEnabled(True)
        elif self.strategy.currentText() == "Forward Fill":
            self.df = self.df.ffill(axis = 0).bfill(axis = 0)
            self.imputeInfo.setText("Missing Obs Processed!")
            self.plotButton.setEnabled(True)
        elif self.strategy.currentText() == "Most Frequent":
            imputer = SimpleImputer(strategy="most_frequent")
            imputer.fit(self.df)
            self.df = imputer.transform(self.df)
            self.df = pd.DataFrame(self.df, columns=columns)
            self.imputeInfo.setText("Missing Obs Processed!")
            self.plotButton.setEnabled(True)
        elif self.strategy.currentText() == "Custom Value":
            char = ['0','1','2','3','4','5','6','7','8','9','.','-']
            try:
                if self.constantValue.text() != '':  
                    imputer = SimpleImputer(strategy="constant",fill_value = float(self.constantValue.text()))
                    imputer.fit(self.df)
                    self.df = imputer.transform(self.df)
                    self.df = pd.DataFrame(self.df, columns=columns)
                    self.imputeInfo.setText("Missing Obs Processed!")
                    self.gn.setEnabled(True)
                    self.plotButton.setEnabled(True)
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Enter Custom Value")
                    msg.setWindowTitle("Warning")
                    msg.exec_()
            except:
                for i in self.constantValue.text():
                    if i not in char:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("Invalid Custom Value")
                        msg.setWindowTitle("Warning")
                        msg.exec_()
                        break
                    else:
                        pass

#function to enable impute button according to strategy text
    def group_strategy(self):
        if self.groupstrategy.currentText() == "--Select--":
            self.groupNights.setEnabled(False)
            self.groupBox.setEnabled(False)
        elif self.groupstrategy.currentText() == "Drop Remainder":
            self.groupNights.setEnabled(True)
            self.groupBox.setEnabled(True)
        elif self.groupstrategy.currentText() == "Include Remainder":
            self.groupNights.setEnabled(True)
            self.groupBox.setEnabled(True)
        else:
            pass

#function to group nights
    def group(self, df, groups):
        QApplication.processEvents()
        dates = df[0]
        QApplication.processEvents()
        unique = []
        QApplication.processEvents()
        for i in dates:
            QApplication.processEvents()
            unique.append(int(i))
            QApplication.processEvents()

        dateObsCount = Counter(unique)
        groupedDates = []
        ungroupedDates = []
        for i in dateObsCount:
            if dateObsCount[i] < groups:
                ungroupedDates.append(i)
            else:
                groupedDates.append(i)

        allDates = ungroupedDates + groupedDates
        obsNum = []
        for i in dateObsCount:
            obsNum.append(dateObsCount[i])
        maxCount = max(obsNum)

        if groups > maxCount:
            df_new = 0
            return df_new
        else:
            unique = list(set(unique))
            dateHash = {}
            QApplication.processEvents()
            for i in unique:
                QApplication.processEvents()
                dateHash[i] = []
                QApplication.processEvents()

            for i in unique:
                QApplication.processEvents()
                for j in range(df.shape[0]):
                    QApplication.processEvents()
                    if int(df.iloc[j,0]) == i:
                        QApplication.processEvents()
                        dateHash[i].append(df.iloc[j, :])
                        QApplication.processEvents()

            dateHashGrouped = {}
            QApplication.processEvents()
            for i in unique:
                QApplication.processEvents()
                dateHashGrouped[i] = []
                QApplication.processEvents()

            for i in dateHash.keys():
                QApplication.processEvents()
                j = 0
                QApplication.processEvents()
                while j < len(dateHash[i]):
                    QApplication.processEvents()
                    a = j
                    QApplication.processEvents()
                    b = j+groups
                    QApplication.processEvents()
                    if b > len(dateHash[i]):
                        QApplication.processEvents()
                        # mera
                        if self.groupstrategy.currentText() == "Include Remainder":
                            b = a+(len(dateHash[i])%groups) 
                        elif self.groupstrategy.currentText() == "Drop Remainder":
                            j = j + groups
                            continue; 
                        # while a < len(dateHash[i]):
                        #     QApplication.processEvents()
                        #     dateHashGrouped[i].append(((dateHash[i][a])))
                        #     a = a+1
                    # else:
                    # ek backspace piche liya
                    QApplication.processEvents() 
                    # ek backspace piche liya
                    dateHashGrouped[i].append(np.median((dateHash[i][a:b]), axis=0)) 
                    QApplication.processEvents()
                    j = j+groups
                    QApplication.processEvents()
     
            df_new = pd.DataFrame()
            QApplication.processEvents()
            for i in unique:
                QApplication.processEvents()
                intermediate_df = pd.DataFrame(dateHashGrouped[i])
                QApplication.processEvents()
                df_new = df_new.append(intermediate_df, ignore_index = True)
                QApplication.processEvents()
            df_new.columns=df.columns
            return df_new, groupedDates, ungroupedDates, allDates

    def groupByFunction(self):
        char = ['.']
        alph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        try:
            if self.groupBox.text() == '':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please enter a value")
                msg.setWindowTitle("Warning")
                msg.exec_()

            elif int(self.groupBox.text()) < 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Group by value cannot be negative")
                msg.setWindowTitle("Warning")
                msg.exec_()

            elif int(self.groupBox.text()) < 3:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Minimum Group by value is 3")
                msg.setWindowTitle("Warning")
                msg.exec_()

            else:
                QApplication.processEvents()
                self.groupby_value = int(self.groupBox.text())
                QApplication.processEvents()
                self.g_df = []
                QApplication.processEvents()
                self.group_df = []
                QApplication.processEvents()
                self.datecol.index = range(0, len(self.datecol))
                QApplication.processEvents()
                n = self.df.shape[0]
                QApplication.processEvents()
                self.df.index = range(0, n)
                QApplication.processEvents()
                self.group_df = pd.concat([self.datecol, self.df], axis = 1)
                QApplication.processEvents()
                self.g_df = self.group(self.group_df, self.groupby_value)

                if self.g_df == 0:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Grouping factor is greater than maximum possible limit")
                    msg.setWindowTitle("Warning")
                    msg.exec_()
                else:
                    QApplication.processEvents()
                    self.progress.setVisible(True)
                    self.done = self.g_df[1]
                    self.notDone = self.g_df[2]
                    self.all = self.g_df[3]
                    self.g_df = self.g_df[0]
                    QApplication.processEvents()
                    self.grouped_df = self.group(self.group_df, self.groupby_value)
                    self.grouped_df = self.grouped_df[0]
                    self.groupdatecol = self.grouped_df.iloc[: , 0]
                    self.grouped_df.drop(self.grouped_df.columns[[0]], axis = 1, inplace = True)
                    QApplication.processEvents()
                    self.groupInfo.setVisible(True)
                    QApplication.processEvents()
                    self.groupInfo.setText(f"{len(self.done)} out of {len(self.all)} dates grouped!")
                    QApplication.processEvents()
                    self.progress.hide()
                    QApplication.processEvents()
                    self.grouped_df1.append(self.grouped_df)
        except:

            for i in self.groupBox.text():
                if i in char:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Decimal values not allowed")
                    msg.setWindowTitle("Warning")
                    msg.exec_()
                    break
                else:
                    pass
            for i in self.groupBox.text():
                if i in alph:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Only Integer values allowed")
                    msg.setWindowTitle("Warning")
                    msg.exec_()
                    break
                else:
                    pass

#function to show column statistics
    def statistics(self):
        if self.grouped_df1 != []:
            self.df = self.grouped_df
        else:
            pass
        
        stars = self.df.columns

        mean = []
        for i in self.df.mean():
            mean.append(i)

        # median = []
        # for i in self.df.median():
        #     median.append(i)

        maxM = []
        for i in self.df.max():
            maxM.append(i)

        minM = []
        for i in self.df.min():
            minM.append(i)

        std = []
        for i in self.df.std():
            std.append(i)

        starStats = pd.DataFrame({"Star ID": stars,"Mean": mean,"Max": maxM, "Min": minM, "Std Dev": std})
        starStats.drop_duplicates(keep=False, inplace=True)
        starStats = starStats.round(3)
        starStats.to_csv(self.dir+'/01Data_Processing/extras/starStatistics.csv', index = False)
        # self.starLabel.setText("Star Statistics")
        self.statsTable.setVisible(True)
        self.statsTable.setColumnCount(starStats.shape[1])
        self.statsTable.setRowCount(starStats.shape[0])
        self.statsTable.setHorizontalHeaderLabels(["Star ID","Mean", "Max", "Min","Std Dev"])
        for i in range(len(starStats.index)): 
            for j in range(len(starStats.columns)):
                self.statsTable.setItem(i,j,QTableWidgetItem(str(starStats.iloc[i, j])))
        self.statsInfo.setText("Star Statistics Saved!")

#function for generating plots
    def plots(self):
        try:
            os.makedirs(self.dir+'/01Data_Processing')
            os.makedirs(self.dir+'/01Data_Processing/logs')
            os.makedirs(self.dir+'/01Data_Processing/output')
            os.makedirs(self.dir+'/01Data_Processing/plots')
        except:
            pass

        self.statistics()
        self.saveStatus.clear()
        if self.grouped_df1 != []:
            self.df = self.grouped_df
            self.groupdatecol.index = range(0, len(self.groupdatecol))
            n = self.grouped_df.shape[0]
            self.grouped_df.index = range(0, n)
            self.grouped_df = self.grouped_df.round(3)
            self.grouped_df = pd.concat([self.groupdatecol, self.grouped_df], axis=1)
            self.grouped_df = self.grouped_df.sort_values(by=self.grouped_df.columns[0])
            dates1 = self.grouped_df[0]
            unique1 = []
            for i in dates1:
                unique1.append(int(i))
            dateObsCount1 = Counter(unique1)
            date_items1 = dateObsCount1.items()
            date_list1 = list(date_items1)
            newDate1 = pd.DataFrame(date_list1)
            self.line = newDate1
        else:
            self.datecol.index = range(0, len(self.datecol))
            n = self.df.shape[0]
            self.df.index = range(0, n)
            self.lineDF = pd.concat([self.datecol, self.df], axis=1)
            dates2 = self.lineDF[0]
            unique2 = []
            for i in dates2:
                unique2.append(int(i))
            dateObsCount2 = Counter(unique2)
            date_items2 = dateObsCount2.items()
            date_list2 = list(date_items2)
            newDate2 = pd.DataFrame(date_list2)
            self.line = newDate2
            pass

        x = self.df.mean(axis=0)
        self.figure1.clear()
        self.ax=self.figure1.add_subplot()
        self.ax.hist(x)
        self.ax.locator_params(axis='y', integer=True)
        self.ax.set_title("Histogram of Ensemble Data")
        self.ax.set_xlabel("Star Mean Magnitude")
        self.figure1.tight_layout(pad=1.0)
        self.canvas1.draw()

        x1 = self.line[0]
        y1 = self.line[1]
        self.figure2.clear()
        self.ax1=self.figure2.add_subplot()
        self.ax1.plot(x1,y1, linestyle = 'solid', marker = 'o', markerfacecolor = 'yellow', markersize = 16)
        xoffset = 1.0
        yoffset = np.mean(y1)*0.1
        self.ax1.set_xlim(min(x1)-xoffset, max(x1)+ xoffset)
        self.ax1.set_ylim(min(y1)-yoffset, max(y1)+ yoffset)
        for i,j in zip(x1,y1):
            self.ax1.annotate(str(j),  xy=(i, j), color='red', fontsize="small", weight='heavy', horizontalalignment='center', verticalalignment='center')
        self.ax1.locator_params(axis='y', integer=True)
        self.ax1.set_title("Observation Timeline")
        self.ax1.set_xlabel("Julian Date")
        self.ax1.set_ylabel("# of Observations")
        self.figure2.tight_layout(pad=1.0)
        self.canvas2.draw()
        self.toolbar.setVisible(True)
        self.saveButton.setEnabled(True)
        self.ax.figure.savefig(self.dir+'/01Data_Processing/plots/HistogramEnsemble.png')
        self.ax1.figure.savefig(self.dir+'/01Data_Processing/plots/ObservationTimeline.png')
        self.statsInfo.setText('Plots & Stats Saved!')
        self.gn.setEnabled(False)
        self.gn.setArrowType(QtCore.Qt.DownArrow)
        self.removeSaccord.setEnabled(False)
        self.removeSaccord.setArrowType(QtCore.Qt.RightArrow)
        self.removeOaccord.setEnabled(False)
        self.removeOaccord.setArrowType(QtCore.Qt.RightArrow)
        self.imputeAccord.setEnabled(False)
        self.imputeAccord.setArrowType(QtCore.Qt.RightArrow)
        self.rowFilterLabel.setVisible(False)
        self.rowFilterBox.setVisible(False)
        self.checkRowNan.setVisible(False)
        self.rowFiltered.setVisible(False)
        self.rowRemoveLabel.setVisible(False)
        self.rowRemoveBox.setVisible(False)
        self.removeObsButton.setVisible(False)
        self.removeObsInfo.setVisible(False)
        self.filterLabel.setVisible(False)
        self.filterBox.setVisible(False)
        self.checkNan.setVisible(False)
        self.radiobuttonC1.setVisible(False)
        self.radiobuttonC2.setVisible(False)
        self.radiobuttonR1.setVisible(False)
        self.radiobuttonR2.setVisible(False)
        self.displayFiltered.setVisible(False)
        self.removeLabel.setVisible(False)
        self.removeBox.setVisible(False)
        self.removeButton.setVisible(False)
        self.removeInfo.setVisible(False)
        self.imputeLabel.setVisible(False)
        self.strategy.setVisible(False)
        self.constantValue.setVisible(False)
        self.constantLabel.setVisible(False)
        self.imputeButton.setVisible(False)
        self.imputeInfo.setVisible(False)
        self.groupBox.setEnabled(False)
        self.groupNights.setEnabled(False)
        self.groupstrategy.setEnabled(False)

#function for file saving
    def save(self):
        self.saveStatus.clear()
        self.datecol.index = range(0, len(self.datecol))
        n = self.df.shape[0]
        self.df.index = range(0, n)

        self.saveStatus.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#4caf50;"
                                    "}\n"
                                    "")
        self.df = self.df.round(3)
        self.processeddf = pd.concat([self.datecol, self.df], axis=1)
        self.saveStatus.setText('Processed Data Saved!')
        self.viewfile.setVisible(True)
        if self.grouped_df1 != []:
            self.grouped_df.to_csv(self.dir+'/01Data_Processing/output/GroupProcessedEnsemble.csv', index = False)
        else:
            self.processeddf.to_csv(self.dir+'/01Data_Processing/output/ProcessedEnsemble.csv', index = False)
        self.logtime = time.time()
        with open(f"01Data_Processing/logs/DP_{self.logtime}.txt","a") as file:
            file.write(f"Login Date and Time: {datetime.datetime.now()}")
            file.write(f"\nData: {self.fileName.split('/')[-1]}")
            file.write(f"\nColumns removed: {self.removeInfo.text()}")
            file.write(f"\nRows removed: {self.removeObsInfo.text()}")
            if self.strategy.currentText() == "--Select--":
                pass
            else:
                file.write(f"\nImpute Method: {self.strategy.currentText()}")
            if self.strategy.currentText() == "Custom Value":
                file.write(f"\nValue: {self.constantValue.text()}")
            else:
                pass
            if self.grouped_df1 != []:
                file.write(f"\nDataset Grouped")
                file.write(f"\nGroup factor value: {self.groupBox.text()}")
                file.write(f"\nGrouped Dates: {self.done}")
                file.write(f"\nUngrouped Dates: {self.notDone}")

            # else:
            #     file.write(f"\nGrouping not possible")