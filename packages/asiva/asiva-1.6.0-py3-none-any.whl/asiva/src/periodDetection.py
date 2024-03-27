#importing required modules
import sys
import math
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton,QFileDialog
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout
from PyQt5.QtWidgets import QWidget,QTableWidgetItem
from PyQt5.QtWidgets import QLabel, QCheckBox
from PyQt5.QtWidgets import QTableWidget,QComboBox,QMessageBox
from PyQt5.QtWidgets import QProgressBar, QDoubleSpinBox, QToolButton
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import pandas as pd
import os, subprocess
import datetime
import time
from statsmodels.tsa.stattools import adfuller
from gatspy.periodic import LombScargleFast, LombScargle
from astropy import timeseries
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import seaborn as sns
import qtawesome as qta
from asiva.src.home import *
sns.set()

#creating a subclass of QWidget
class Periodogram(QWidget):
    def __init__(self):
        super(Periodogram, self).__init__()
#creating the user interface layout  

        verticallayout1 = QVBoxLayout()

        search_icon = qta.icon('fa5s.search',
                        color='white')

        graph_icon = qta.icon('fa5s.chart-area',
                        color='white')

        reset_icon = qta.icon('fa5s.redo',
                        color='white')

        folder_icon = qta.icon('fa5s.folder-open',
                        color='white')

        files_icon = qta.icon('fa5s.eye',
                        color='#2196f3')

        group_icon = qta.icon('fa5s.layer-group',
                        color='white')

        tips_icon = qta.icon('fa5s.lightbulb',
                        color='#e8a92c')
        
        self.openFiles = QPushButton("Load Light Curve")
        self.openFiles.setIcon(folder_icon)
        self.openFiles.setIconSize(QSize(30, 30))
        self.openFiles.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #7ebdbd;\n"
                                    "width:100%;\n"
                                    "min-height:35px;\n"
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
        
        self.dataName = QLabel()
        self.dataName.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #ff9800;\n"
                                    "}\n"
                                    "")
        self.fileDetail = QLabel()
        self.fileDetail.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #007427;\n"
                                    "}\n"
                                    "")

        self.stationarityLabel = QLabel()
        self.stationarityLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: red;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "")

        self.gn = QToolButton(text='Group Nights', checkable=True, checked=False)
        self.gn.setStyleSheet(u"QToolButton{\n"
                                    "background-color: #ebebeb;\n"
                                    "width:400%;\n"
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

        self.algoName =QLabel("Algorithm")
        self.algoName.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-style: italic;\n"
                                    "margin-top:5px;\n"
                                    "}\n"
                                    "")

        self.algo = QComboBox()
        self.algo.setStyleSheet(u"QComboBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:200%;\n"
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

        self.algo.addItem("Custom")
        self.algo.addItem("LombScargle")
        self.algo.addItem("LombScargle Fast")

        self.algo.setCurrentText("LombScargle")
        self.minimumLabel = QLabel("Min Period")
        self.minimumLabel.setStyleSheet(u"QLabel{\n"
                                    "min-width:60%;\n"
                                    "font:13px;\n"
                                    "font-style: italic;\n"
                                    "}\n"
                                    "")

        self.minimumValue = QDoubleSpinBox()
        self.minimumValue.setMaximum(9999999999);
        self.minimumValue.setValue(0.1)
        self.minimumValue.setStyleSheet(u"QDoubleSpinBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:200%;\n"
                                    "min-height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QDoubleSpinBox:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.maximumLabel = QLabel("Max Period")
        self.maximumLabel.setStyleSheet(u"QLabel{\n"
                                    "min-width:60%;\n"
                                    "font:13px;\n"
                                    "font-style: italic;\n"
                                    "}\n"
                                    "")

        self.maximumValue = QDoubleSpinBox()
        self.maximumValue.setMaximum(9999999999);
        self.maximumValue.setValue(1)
        self.maximumValue.setStyleSheet(u"QDoubleSpinBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:200%;\n"
                                    "min-height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QDoubleSpinBox:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.df_period_Label = QLabel("Std Dev")
        self.df_period_Label.setStyleSheet(u"QLabel{\n"
                                    "min-width:60%;\n"
                                    "font:13px;\n"
                                    "font-style: italic;\n"
                                    "}\n"
                                    "")

        self.df_period_Value = QDoubleSpinBox()
        self.df_period_Value.setMaximum(9999999999);
        self.df_period_Value.setValue(0.1)
        self.df_period_Value.setStyleSheet(u"QDoubleSpinBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:200%;\n"
                                    "min-height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QDoubleSpinBox:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.t0Label = QLabel("Epoch (t0)")
        self.t0Label.setStyleSheet(u"QLabel{\n"
                                    "min-width:60%;\n"
                                    "font:13px;\n"
                                    "font-style: italic;\n"
                                    "}\n"
                                    "")
        self.t0Value = QDoubleSpinBox()
        self.t0Value.setMaximum(9999999999)
        self.t0Value.setDecimals(5)
        self.t0Value.setValue(0)
        self.t0Value.setStyleSheet(u"QDoubleSpinBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:200%;\n"
                                    "min-height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QDoubleSpinBox:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.calculatePeriod = QPushButton("Calculate period")
        self.calculatePeriod.setIcon(search_icon)
        self.calculatePeriod.setIconSize(QSize(30, 30))
        self.calculatePeriod.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #f44336;\n"
                                    "width:100%;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #ffb3a6;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#f88e86;\n"
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

        self.falseAlarmLabel = QLabel()
        self.falseAlarmLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "margin-top:10px;\n"
                                    "margin-bottom:10px;\n"
                                    "}\n"
                                    "")

        self.periodLabel = QLabel("Period")
        self.periodLabel.setStyleSheet(u"QLabel{\n"
                                    "min-width:60%;\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "")

        self.periodValue = QDoubleSpinBox()
        self.periodValue.setMaximum(9999999999)
        self.periodValue.setDecimals(10)
        self.periodValue.setValue(1.00)
        self.periodValue.setStyleSheet(u"QDoubleSpinBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "width:200%;\n"
                                    "min-height:30px;\n"
                                    "font:13px;\n"
                                    "border-radius:5px;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "border:1px solid rgb(84, 84, 84);\n"
                                    "}\n"
                                    "\n"
                                    "QDoubleSpinBox:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:#00838F;\n"
                                    "}\n"
                                    "")

        self.modifyLabel = QLabel("Modify period")
        self.modifyLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "margin-top:10px;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "")

        self.doublePeriod = QPushButton("Double period")
        self.doublePeriod.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #2196f3;\n"
                                    "width:110%;\n"
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

        self.halfPeriod = QPushButton("Half period")
        self.halfPeriod.setStyleSheet(u"QPushButton{\n"
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
                                    "border:2px solid #398714;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#88bb8a;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        self.resetPeriod = QPushButton("Reset")
        self.resetPeriod.setIcon(reset_icon)
        self.resetPeriod.setIconSize(QSize(30, 30))
        self.resetPeriod.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #f44336;\n"
                                    "width:90%;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #ffb3a6;\n"
                                    "color:white;\n"
                                    "}\n""QPushButton:disabled {\n"
                                    "background-color:#f88e86;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        self.PC = QPushButton("Plot Phased LC")
        self.PC.setIcon(graph_icon)
        self.PC.setIconSize(QSize(30, 30))
        self.PC.setStyleSheet(u"QPushButton{\n"
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

        self.viewfile = QPushButton("View Files")
        self.viewfile.setIcon(files_icon)
        self.viewfile.setIconSize(QSize(30, 30))
        self.viewfile.setStyleSheet(u"QPushButton{\n"
                                    "width:100%;\n"
                                    "min-height:35px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border:2px solid #2196f3;\n"
                                    "border-radius:5px;\n"
                                    "color:#2196f3;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:disabled {\n"
                                    "background-color:#8ad1d1;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        horizontalLayout13 = QHBoxLayout()
        horizontalLayout13.setAlignment(Qt.AlignBottom)
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

        horizontalLayout13.addWidget(self.tips)

        horizontalLayout9 = QHBoxLayout()
        horizontalLayout9.setAlignment(Qt.AlignBottom)
        self.resetButton = QPushButton('Reset Workspace')
        self.resetButton.setStyleSheet(u"QPushButton{\n"
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
        
        horizontalLayout9.addWidget(self.resetButton)

        verticallayout1.addWidget(self.openFiles)
        verticallayout1.addWidget(self.dataName)
        verticallayout1.addWidget(self.fileDetail)
        verticallayout1.addWidget(self.stationarityLabel)

        verticallayout1.addWidget(self.gn)
        verticallayout1.addWidget(self.groupStrategyLabel)
        verticallayout1.addWidget(self.groupstrategy)
        verticallayout1.addWidget(self.groupLabel)

        horizontalLayout12 = QHBoxLayout()
        horizontalLayout12.addWidget(self.groupBox)
        horizontalLayout12.addWidget(self.groupNights)

        verticallayout1.addLayout(horizontalLayout12)
        verticallayout1.addWidget(self.groupInfos)
        verticallayout1.addWidget(self.groupInfo)

        verticallayout1.addWidget(self.progress)

        horizontallayout2 = QHBoxLayout()
        horizontallayout3 = QHBoxLayout()
        horizontallayout4 = QHBoxLayout()
        horizontallayout5 = QHBoxLayout()
        horizontallayout6 = QHBoxLayout()
        horizontallayout7 = QHBoxLayout()
        horizontallayout8 = QHBoxLayout()
        horizontallayout9 = QHBoxLayout()
        horizontallayout10 = QHBoxLayout()
        horizontallayout11 = QHBoxLayout()
        
        horizontallayout2.addWidget(self.minimumLabel)
        horizontallayout2.addWidget(self.minimumValue)

        horizontallayout3.addWidget(self.maximumLabel)
        horizontallayout3.addWidget(self.maximumValue)

        horizontallayout4.addWidget(self.t0Label)
        horizontallayout4.addWidget(self.t0Value)

        horizontallayout5.addWidget(self.df_period_Label)
        horizontallayout5.addWidget(self.df_period_Value)

        horizontallayout6.addWidget(self.calculatePeriod)
        horizontallayout6.addWidget(self.PC)

        horizontallayout8.addWidget(self.periodLabel)
        horizontallayout8.addWidget(self.periodValue)
        
        horizontallayout9.addWidget(self.modifyLabel)

        horizontallayout10.addWidget(self.doublePeriod)
        horizontallayout10.addWidget(self.halfPeriod)
        horizontallayout10.addWidget(self.resetPeriod)
        
        horizontallayout7.addWidget(self.algoName)

        horizontallayout7.addWidget(self.algo)

        verticallayout1.addLayout(horizontallayout7)
        verticallayout1.addLayout(horizontallayout2)
        verticallayout1.addLayout(horizontallayout3)
        verticallayout1.addLayout(horizontallayout4)
        verticallayout1.addLayout(horizontallayout5)
        verticallayout1.addLayout(horizontallayout8)        
        verticallayout1.addWidget(self.progress)        
        verticallayout1.addWidget(self.falseAlarmLabel)
        verticallayout1.addLayout(horizontallayout6)
        verticallayout1.addLayout(horizontallayout11)
        verticallayout1.addLayout(horizontallayout9)
        verticallayout1.addLayout(horizontallayout10)
        verticallayout1.addWidget(self.viewfile)
        verticallayout1.addStretch()
        verticallayout1.addLayout(horizontalLayout13)
        verticallayout1.addLayout(horizontalLayout9)

        verticallayout2 = QVBoxLayout()
        self.ODataFrame = QLabel("Original Light Curve Data")
        self.ODataFrame.setStyleSheet(u"QLabel{\n"
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
                                    "background-color:white;\n"
                                    "font:13px;\n"
                                    "max-width:300px;\n"
                                    "margin-top:10px;\n"
                                    "}\n"
                                    "")

        self.PhaseDataFrame = QLabel("Phased Light Curve Data")
        self.PhaseDataFrame.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "text-decoration:underline;\n"
                                    "}\n"
                                    "")

        self.phaseTable = QTableWidget()
        self.phaseTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.phaseTable.horizontalHeader().setStyleSheet("QHeaderView { font-weight: bold; }")
        self.phaseTable.setColumnCount(0)
        self.phaseTable.setRowCount(0)
        self.phaseTable.setStyleSheet(u"QTableWidget{\n"
                                    "background-color:white;\n"
                                    "font:13px;\n"
                                    "max-width:300px;\n"
                                    "}\n"
                                    "")

        verticallayout2.addWidget(self.ODataFrame)
        verticallayout2.addWidget(self.dataTable)
        verticallayout2.addWidget(self.PhaseDataFrame)
        verticallayout2.addWidget(self.phaseTable)

        verticallayout3 = QVBoxLayout()
        verticallayout3.addStretch()

        self.figure1 = plt.Figure()
        self.canvas1 = FigureCanvas(self.figure1)

        verticallayout3.addWidget(self.canvas1)

        horizontallayout1 = QHBoxLayout()
        horizontallayout1.addStretch()

        self.figure3 = plt.Figure()
        self.canvas3 = FigureCanvas(self.figure3)
        
        horizontallayout1.addStretch()

        self.figure2 = plt.Figure()
        self.canvas2 = FigureCanvas(self.figure2)

        horizontallayout1.addWidget(self.canvas3)
        horizontallayout1.addWidget(self.canvas2)
        
        verticallayout3.addLayout(horizontallayout1)

        horizontallayout = QHBoxLayout(self)
        horizontallayout.addLayout(verticallayout1, 1)
        horizontallayout.addLayout(verticallayout2, 1)
        horizontallayout.addLayout(verticallayout3, 3)
        self.setLayout(horizontallayout)

        self.openFiles.clicked.connect(self.fileExplorer)
        self.algo.activated[str].connect(self.selectAlgo)
        self.PC.clicked.connect(self.phase)
        self.calculatePeriod.clicked.connect(self.calPeriod)
        self.doublePeriod.clicked.connect(self.calDoublePeriod)
        self.halfPeriod.clicked.connect(self.calHalfPeriod)
        self.resetPeriod.clicked.connect(self.reset)
        self.viewfile.clicked.connect(self.finalfile)
        self.resetButton.clicked.connect(self.resetWorkspace)
        self.tips.clicked.connect(self.tipsAndTricks)

        self.gn.pressed.connect(self.group_nights)
        self.groupNights.clicked.connect(self.groupByFunction)
        self.groupstrategy.activated[str].connect(self.group_strategy)


        self.openFiles.setEnabled(True)
        self.algo.setEnabled(False)
        self.minimumValue.setEnabled(False)
        self.maximumValue.setEnabled(False)
        self.periodValue.setEnabled(False)
        self.t0Value.setEnabled(False)
        self.df_period_Value.setEnabled(False)
        self.calculatePeriod.setEnabled(False)
        self.progress.setVisible(False)
        self.PC.setEnabled(False)
        self.doublePeriod.setEnabled(False)
        self.halfPeriod.setEnabled(False)
        self.resetPeriod.setEnabled(False)
        self.viewfile.setVisible(False)
        self.ODataFrame.setVisible(False)
        self.dataTable.setVisible(False)
        self.PhaseDataFrame.setVisible(False)
        self.phaseTable.setVisible(False)

        self.groupLabel.setVisible(False)
        self.groupBox.setVisible(False)
        self.groupNights.setVisible(False)
        self.groupInfo.setVisible(False)
        self.groupInfos.setVisible(False)
        self.gn.setEnabled(False)
        self.groupstrategy.setVisible(False)
        self.groupStrategyLabel.setVisible(False)

    def tipsAndTricks(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("COMING SOON")
        msg.setWindowTitle("Information")
        msg.exec_()

#function to reset UI
    def resetWorkspace(self):
        self.dataName.clear()
        self.fileDetail.clear()
        self.stationarityLabel.clear()

        self.gn.setEnabled(False)
        self.gn.setArrowType(QtCore.Qt.RightArrow)
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
        self.groupInfos.setVisible(False)

        self.algo.setEnabled(False)
        self.t0Value.setValue(self.t0max())
        self.t0Value.setEnabled(False)
        self.PC.setEnabled(False)
        self.periodValue.setEnabled(False)
        self.periodValue.setValue(1)
        self.algo.setCurrentText("LombScargle")
        self.minimumValue.setValue(0.1)
        self.minimumValue.setEnabled(False)
        self.maximumValue.setValue(1)
        self.maximumValue.setEnabled(False)
        self.df_period_Value.setValue(0.1)
        self.df_period_Value.setEnabled(False)
        self.calculatePeriod.setEnabled(False)
        self.falseAlarmLabel.clear()
        self.doublePeriod.setEnabled(False)
        self.halfPeriod.setEnabled(False)
        self.resetPeriod.setEnabled(False)
        self.viewfile.setVisible(False)
        self.PhaseDataFrame.clear()
        self.phaseTable.setRowCount(0)
        self.phaseTable.setColumnCount(0)
        self.phaseTable.setVisible(False)
        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(0)
        self.dataTable.setVisible(False)
        self.ODataFrame.clear()
        self.figure1.clear()
        self.figure2.clear()
        self.figure3.clear()
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()
#function to view output folder
    def finalfile(self):
        path = self.dir+'/04Period_Detection'
        path = os.path.realpath(path)
        if sys.platform == "win32":
            os.startfile(path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])

#function to load LC file
    def fileExplorer(self):
        self.dir=Home.setupdir(self)
        os.chdir(self.dir)
        self.fileName,_filter = QFileDialog.getOpenFileName(None, "Window name", self.dir, "CSV files (*.csv)")
        if self.fileName == '':
            if self.dataName.text() == '':
                self.dataName.setText("No file selected")
            else:
                self.dataName.setText(self.dataName.text())
        else:
            if "04Period_Detection" not in os.listdir(self.dir):
                os.mkdir("04Period_Detection")
            self.openFiles.setText("Load New Light Curve")

            try:
                self.df = pd.read_csv(self.fileName, header = None)
                str_values=0
                for rowIndex, row in self.df.iterrows():
                    for columnIndex, value in row.items():
                        if type(value) == int or type(value) ==float:
                            pass
                        else:
                            str_values = str_values+1

                if str_values > 0:
                    self.resetWorkspace()
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("String data not allowed. Please remove header or non numerical data before loading the file")
                    msg.setWindowTitle("Warning")
                    msg.exec_()
                else:
                    if self.df[self.df.columns[0]].count() == self.df[self.df.columns[1]].count():
                        self.dataName.setText(f"File Name: {self.fileName.split('/')[-1]}")
                        self.file = self.fileName.split('/')[-1].replace('.csv','')
                        self.fileDetail.setText(f"Details: {self.df.shape[0]} Obs, No missing values")

                    # check stationarity while loading a light curve
                        self.stationarity = []
                        test = adfuller(self.df[self.df.columns[1]], autolag="AIC")
                        if (test[1] < 0.05):
                            self.stationarity.append(1)
                        elif (test[1] > 0.05):
                            if (test[0] < test[4]["1%"]) and (test[0] < test[4]["5%"]) and (test[0] < test[4]["10%"]):
                                self.stationarity.append(1)
                            else:
                                self.stationarity.append(0)
                        status = {0: "True", 1: "False"}
                        self.stationarity = [status.get(x, x) for x in self.stationarity]
                        self.stationarityLabel.setText('Stationarity: '+str(self.stationarity))

                        if self.file not in os.listdir(self.dir+"/04Period_Detection/"):
                            os.mkdir(f"04Period_Detection/{self.file}")
                        if "logs" not in os.listdir(self.dir+f"/04Period_Detection/{self.file}"): 
                            os.mkdir(f"04Period_Detection/{self.file}/logs")
                        if "output" not in os.listdir(self.dir+f"/04Period_Detection/{self.file}"): 
                            os.mkdir(f"04Period_Detection/{self.file}/output")
                        if "plots" not in os.listdir(self.dir+f"/04Period_Detection/{self.file}"): 
                            os.mkdir(f"04Period_Detection/{self.file}/plots")

                        self.df = self.df.round(3)
                        self.ODataFrame.setVisible(True)
                        self.ODataFrame.setText("Original Light Curve Data")
                        self.dataTable.setVisible(True)
                        self.dataTable.setColumnCount(self.df.shape[1])
                        self.dataTable.setRowCount(self.df.shape[0])
                        self.dataTable.setHorizontalHeaderLabels(['Date','Magnitude'])
                        for i in range(len(self.df.index)):
                            for j in range(len(self.df.columns)):
                                self.dataTable.setItem(i,j,QTableWidgetItem(str(self.df.iloc[i, j])))

                        self.gn.setEnabled(True)
                        self.algo.setEnabled(True)
                        self.t0Value.setValue(self.t0max())
                        self.t0Value.setEnabled(True)
                        self.lightCurve()
                        self.PC.setEnabled(True)
                        self.periodValue.setEnabled(False)
                        self.periodValue.setValue(1)
                        self.algo.setCurrentText("LombScargle")
                        self.minimumValue.setValue(0.1)
                        self.minimumValue.setEnabled(True)
                        self.maximumValue.setValue(1)
                        self.maximumValue.setEnabled(True)
                        self.df_period_Value.setValue(0.1)
                        self.df_period_Value.setEnabled(True)
                        self.calculatePeriod.setEnabled(True)
                        self.falseAlarmLabel.clear()
                        self.doublePeriod.setEnabled(False)
                        self.halfPeriod.setEnabled(False)
                        self.resetPeriod.setEnabled(False)
                        self.viewfile.setVisible(False)
                        self.PhaseDataFrame.clear()
                        self.phaseTable.setRowCount(0)
                        self.phaseTable.setColumnCount(0)
                        self.phaseTable.setVisible(False)
                        self.canvas2.hide()
                        self.canvas3.hide()
                    else:
                        self.dataTable.setColumnCount(0)
                        self.dataTable.setRowCount(0)
                        self.dataName.setText('') 
                        self.fileDetail.setText('') 
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("Missing values found")
                        msg.setWindowTitle("Warning")
                        msg.exec_()

            except pd.errors.EmptyDataError:  
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("No columns to parse from file")
                msg.setWindowTitle("Warning")
                msg.exec_()

#function to set accordian view
    def group_nights(self):
        checked = self.gn.isChecked()
        self.gn.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)

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

#function to set strategy text
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

#function to select an algorithm to calculate the Phased Light CUrve 
    def selectAlgo(self):
        if self.algo.currentText() == "Custom":
            self.custom()
            self.falseAlarmLabel.setVisible(False)
        elif self.algo.currentText() == "LombScargle":
            self.LombScarglePeriod()
            self.falseAlarmLabel.setVisible(False)
        elif self.algo.currentText() == "LombScargle Fast":
            self.LombScarglePeriod()
            self.falseAlarmLabel.setVisible(False)
        else:
            pass

#function to calculate Phased Light Curve manually
    def custom(self):
        
        self.periodValue.setValue(1)
        self.minimumValue.setValue(0.1)
        self.minimumValue.setEnabled(False)
        self.maximumValue.setValue(1)
        self.maximumValue.setEnabled(False)
        
        self.t0Value.setEnabled(True)
        self.df_period_Value.setValue(0.1)
        self.df_period_Value.setEnabled(False)
        self.periodValue.setEnabled(True)
        self.calculatePeriod.setEnabled(False)
        self.doublePeriod.setEnabled(False)
        self.halfPeriod.setEnabled(False)
        self.resetPeriod.setEnabled(False)
        

#function to calculate Phased Light Curve using Lomb Scargle method
    def LombScarglePeriod(self):
        self.minimumValue.setValue(0.1)
        self.minimumValue.setEnabled(True)

        self.maximumValue.setValue(1)    
        self.maximumValue.setEnabled(True)

        self.t0Value.setValue(self.t0max())  
        self.t0Value.setEnabled(True)

        self.df_period_Value.setValue(0.1)
        self.df_period_Value.setEnabled(True)

        self.periodValue.setValue(1)    
        self.periodValue.setEnabled(False)

        self.calculatePeriod.setEnabled(True)

#function to calculate the 'period'
    def calPeriod(self):
        try:
            os.makedirs(self.dir+'/04Period_Detection')
            os.makedirs(self.dir+ f'/04Period_Detection/{self.file}')
            os.makedirs(self.dir+f'/04Period_Detection/{self.file}/logs')
            os.makedirs(self.dir+f'/04Period_Detection/{self.file}/output')
            os.makedirs(self.dir+f'/04Period_Detection/{self.file}/plots')
        except:
            pass
        try:
            QApplication.sendPostedEvents()
            QApplication.processEvents()

            if self.algo.currentText() == 'LombScargle Fast':
                QApplication.processEvents()
                self.progress.setVisible(True)
                QApplication.processEvents()
                self.progress.setMinimum(0)
                QApplication.processEvents()
                self.progress.setMaximum(0)
                QApplication.processEvents()
                gatspy_period = LombScargleFast()
                QApplication.processEvents()
                gatspy_period.fit(self.df[self.df.columns[0]], self.df[self.df.columns[1]], float(self.df_period_Value.text()))
                QApplication.processEvents()
                gatspy_period.optimizer.period_range = (float(self.minimumValue.text()), float(self.maximumValue.text()))
                QApplication.processEvents()
                self.period = gatspy_period.best_period
                QApplication.processEvents()  
                generatedPeriod_periodogram = np.linspace(float(self.minimumValue.text()), float(self.maximumValue.text()), 10000)
                QApplication.processEvents()
                score = gatspy_period.score(generatedPeriod_periodogram)
                QApplication.processEvents()
                self.periodValue.setValue(self.period)  
                QApplication.processEvents()  
                
            elif self.algo.currentText() == 'LombScargle':
                QApplication.processEvents()
                self.progress.setVisible(True)
                QApplication.processEvents()
                self.progress.setMinimum(0)
                QApplication.processEvents()
                self.progress.setMaximum(0)
                QApplication.processEvents()
                gatspy_period = LombScargle()
                QApplication.processEvents()
                gatspy_period.fit(self.df[self.df.columns[0]], self.df[self.df.columns[1]], float(self.df_period_Value.text()))
                QApplication.processEvents()
                gatspy_period.optimizer.period_range = (float(self.minimumValue.text()), float(self.maximumValue.text()))
                QApplication.processEvents()
                self.period = gatspy_period.best_period
                QApplication.processEvents()
                generatedPeriod_periodogram = np.linspace(float(self.minimumValue.text()), float(self.maximumValue.text()), 10000)
                QApplication.processEvents()
                score = gatspy_period.score(generatedPeriod_periodogram)
                QApplication.processEvents()
                self.periodValue.setValue(self.period)
                QApplication.processEvents()
    
            ls = timeseries.LombScargle(self.df[self.df.columns[0]], self.df[self.df.columns[1]], 1.0)
            QApplication.processEvents()
            freq, power = ls.autopower()
            QApplication.processEvents()
            fa = ls.false_alarm_probability(power.max())
            QApplication.processEvents()
            self.falseAlarmLabel.setVisible(True)
            QApplication.processEvents()
            self.falseAlarmLabel.setText('False Alarm Probability: '+str(fa))
            QApplication.processEvents()

            plt.clf()
            plt.plot(generatedPeriod_periodogram, score)
            plt.xlabel("Period")
            plt.ylabel("Lomb-Scargle Power")
            plt.title("Lomb-Scargle periodogram as a function of period")
            plt.savefig(self.dir+f'/04Period_Detection/{self.file}/plots/{self.file}_Power_Plot.png')
            plt.close

            self.canvas3.setVisible(True)
            self.figure3.clear()
            self.ax2 = self.figure3.add_subplot()
            self.ax2.plot(generatedPeriod_periodogram, score)
            self.ax2.set_xlabel("Period")
            self.ax2.set_ylabel("Lomb-Scargle Power")
            self.ax2.set_title("Lomb-Scargle periodogram as a function of period")

            self.figure3.tight_layout(pad=1.0)
            self.canvas3.draw()
            #plt.show()
            self.progress.hide()

            self.PC.setEnabled(True)
            self.doublePeriod.setEnabled(True)
            self.halfPeriod.setEnabled(True)
            self.resetPeriod.setEnabled(True) 
            
        except ValueError:  
            self.progress.hide()          
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("The optimizer is not designed to search for periods larger than the data baseline")
            msg.setWindowTitle("Warning")
            msg.exec_()

#function to double the value of above calculated period            
    def calDoublePeriod(self):
        period=float(self.period)
        double_period = period*2
        self.periodValue.setValue(double_period)
        self.phase()

#function to half the value of above calculated period  
    def calHalfPeriod(self):
        period=float(self.period)
        half_period= period/2
        self.periodValue.setValue(half_period)
        self.phase()

    def reset(self):
        self.periodValue.setValue(self.period)
        self.phase()

#function to plot the time series data and the calculated Phased light curve  
    def lightCurve(self):
        try:
            os.makedirs(self.dir+'/04Period_Detection')
            os.makedirs(self.dir+ f'/04Period_Detection/{self.file}')
            os.makedirs(self.dir+f'/04Period_Detection/{self.file}/logs')
            os.makedirs(self.dir+f'/04Period_Detection/{self.file}/output')
            os.makedirs(self.dir+f'/04Period_Detection/{self.file}/plots')
        except:
            pass

        self.figure1.clear()
        self.ax1 = self.figure1.add_subplot()
        self.ax1.scatter(self.df[self.df.columns[0]], self.df[self.df.columns[1]], s=20, alpha=0.8)
        self.ax1.set_xlabel("Julian Date")
        self.ax1.set_ylabel("Magnitude")
        # self.ax1.invert_yaxis()
        self.ax1.set_title("Original Light Curve")
        self.figure1.tight_layout(pad=1.0)
        self.canvas1.draw()
        self.ax1.figure.savefig(self.dir+f'/04Period_Detection/{self.file}/plots/{self.file}_OrgLC_Plot.png')

    def phase(self):
        try:
            os.makedirs(self.dir+'/04Period_Detection')
            os.makedirs(self.dir+ f'/04Period_Detection/{self.file}')
            os.makedirs(self.dir+f'/04Period_Detection/{self.file}/logs')
            os.makedirs(self.dir+f'/04Period_Detection/{self.file}/output')
            os.makedirs(self.dir+f'/04Period_Detection/{self.file}/plots')
        except:
            pass
        try:
            self.phaseDf = self.df.values
            self.t0 = float(self.t0Value.text())

            m = []
            for i in self.phaseDf[:, 0]:  
                x = i - self.t0      
                m.append((x / float(self.periodValue.text())) - math.floor(x / float(self.periodValue.text())))

            self.phaseDf = pd.DataFrame({"Phase": m, "Mag": self.phaseDf[:, 1]})
            self.phaseDf = self.phaseDf.round(3)
            self.PhaseDataFrame.setVisible(True)
            self.PhaseDataFrame.setText("Phased Light Curve Data")
            self.phaseTable.setVisible(True)
            self.phaseTable.setColumnCount(self.phaseDf.shape[1])
            self.phaseTable.setRowCount(self.phaseDf.shape[0])
            self.phaseTable.setHorizontalHeaderLabels(['Phase','Magnitude'])
            
            for i in range(len(self.phaseDf.index)):
                for j in range(len(self.phaseDf.columns)):
                    self.phaseTable.setItem(i,j,QTableWidgetItem(str(self.phaseDf.iloc[i, j])))

            self.canvas2.setVisible(True)
            self.figure2.clear()
            self.ax2 = self.figure2.add_subplot()
            self.ax2.set_xlabel("Phase")
            self.ax2.set_ylabel("Magnitude")
            self.ax2.set_title("Phased Light Curve")
            # self.ax2.invert_yaxis()


            self.ax2.scatter(self.phaseDf[self.phaseDf.columns[0]], self.phaseDf[self.phaseDf.columns[1]], s=20, alpha=0.8)
            self.figure2.tight_layout(pad=1.0)
            self.canvas2.draw()

            self.phaseDf.to_csv(self.dir+f'/04Period_Detection/{self.file}/output/{self.file}_Phased_LC.csv', index = False)
            self.ax2.figure.savefig(self.dir+f'/04Period_Detection/{self.file}/plots/{self.file}_PhasedLC_Plot.png')
            self.logtime = time.time()
            with open(self.dir+f"/04Period_Detection/{self.file}/logs/{self.file}_log.txt","a") as file:
                file.write(f"Login Date and Time: {datetime.datetime.now()}")
                file.write(f"\nAlgorithm: {self.algo.currentText()}")
                file.write(f"\nMin Period: {self.minimumValue.text()}")
                file.write(f"\nMax Period: {self.maximumValue.text()}")
                file.write(f"\nEpoch (t0): {self.t0Value.text()}")
                file.write(f"\nStd Dev: {self.df_period_Value.text()}")
                file.write(f"\nPeriod: {self.periodValue.text()}")
                file.write(f"\n{self.falseAlarmLabel.text()}")
                file.write(f"\n")
                file.write(f"\n")
            self.viewfile.setVisible(True)

        except AttributeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Choose file first")
            msg.setWindowTitle("Warning")
            msg.exec_()

#function for calculating the Epoch value
    def t0max(self):

        for i,j in zip(self.df[self.df.columns[0]],self.df[self.df.columns[1]]):
            if j == max(self.df[self.df.columns[1]]):
                t0 = i

        return t0
        

        