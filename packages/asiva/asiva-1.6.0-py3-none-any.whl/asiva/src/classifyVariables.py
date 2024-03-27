import sys
import os, subprocess
from PyQt5.QtWidgets import (QWidget, QFileDialog, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QApplication, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import joblib
import pickle
import datetime
import time
import pandas as pd
import numpy as np
import qtawesome as qta
from sklearn.preprocessing import LabelEncoder
from asiva.src.home import *
from asiva.src.model.assets import asivaRF_model, asivaRF_cm

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#creating a subclass of QWidget
class Classifier(QWidget):
    def __init__(self):

        super(Classifier, self).__init__()
        self.setWindowTitle('Classifier')

#Creating GUI --- Setting up Layouts  
        horizontalLayout = QHBoxLayout()
        verticalLayout = QVBoxLayout()

        predict_icon = qta.icon('fa5s.bolt',
                        color='white')
        
        proceed_icon = qta.icon('fa5s.chevron-circle-right',
                        color='white')

        folder_icon = qta.icon('fa5s.folder-open',
                        color='white')

        files_icon = qta.icon('fa5s.eye',
                        color='#2196f3')

        tips_icon = qta.icon('fa5s.lightbulb',
                        color='#e8a92c')
        
        self.file = QPushButton('Load Features')
        self.file.setIcon(folder_icon)
        self.file.setIconSize(QSize(30, 30))
        self.file.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #7ebdbd;\n"
                                    "min-width:200px;\n"
                                    "max-width:250px;\n"
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

        self.fileInfo = QLabel()
        self.fileInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "color: #ff9800;\n"
                                    "margin-top:10px;\n"
                                    "}\n"
                                    "")

        self.modelLabel = QLabel('Model')
        self.modelLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "margin-top:10px;\n"
                                    "}\n"
                                    "")

        self.modelType = QComboBox()
        self.modelType.setStyleSheet(u"QComboBox{\n"
                                    "background-color: #FAFAFA;\n"
                                    "min-width:200px;\n"
                                    "max-width:250px;\n"
                                    "height:40px;\n"
                                    "padding-left:5px;\n"
                                    "font:14px;\n"
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

        self.modelType.addItem("ASIVA RF")
        self.modelType.addItem("Custom")

        self.customModelPath = QPushButton('Select Custom Model Path')
        self.customModelPath.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #4caf50;\n"
                                    "min-width:200px;\n"
                                    "max-width:250px;\n"
                                    "height:40px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:5px;\n"
                                    "border:2px solid #00838F;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "")

        self.cmInfo = QLabel()
        self.cmInfo.setWordWrap(True)
        self.cmInfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "margin-top:5px;\n"
                                    "color: #007427;\n"
                                    "margin-bottom:20px;\n"
                                    "}\n"
                                    "")

        self.pro = QPushButton('Load Model')
        self.pro.setIcon(proceed_icon)
        self.pro.setIconSize(QSize(30, 30))
        self.pro.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #4caf50;\n"
                                    "min-width:200px;\n"
                                    "max-width:250px;\n"
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
                                    "background-color:#88bb8a;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        self.proinfo = QLabel()
        self.proinfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "width:100%;\n"
                                    "max-height:40px;\n"
                                    "color: #4caf50;\n"
                                    "}\n"
                                    "")

        self.pred = QPushButton('Predict')
        self.pred.setIcon(predict_icon)
        self.pred.setIconSize(QSize(30, 30))
        self.pred.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "min-width:200px;\n"
                                    "max-width:250px;\n"
                                    "height:40px;\n"
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

        self.preinfo = QLabel()
        self.preinfo.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "width:100%;\n"
                                    "max-height:40px;\n"
                                    "color:red;\n"
                                    "}\n"
                                    "")

        self.viewfile = QPushButton("View Files")
        self.viewfile.setIcon(files_icon)
        self.viewfile.setIconSize(QSize(30, 30))
        self.viewfile.setStyleSheet(u"QPushButton{\n"
                                    "min-width:200px;\n"
                                    "max-width:250px;\n"
                                    "height:40px;\n"
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

        verticalLayout.addWidget(self.file)
        verticalLayout.addWidget(self.fileInfo)
        verticalLayout.addWidget(self.modelLabel)
        verticalLayout.addWidget(self.modelType)
        verticalLayout.addWidget(self.customModelPath)
        verticalLayout.addWidget(self.cmInfo)
        verticalLayout.addWidget(self.pro)
        verticalLayout.addWidget(self.proinfo)
        verticalLayout.addWidget(self.pred)
        verticalLayout.addWidget(self.preinfo)
        verticalLayout.addWidget(self.viewfile)
        verticalLayout.addStretch(1)
        verticalLayout.addLayout(horizontalLayout10)
        verticalLayout.addLayout(horizontalLayout9)

        verticalLayout1 = QVBoxLayout()

        self.iname = QLabel('CONFUSION MATRIX')
        self.iname.setStyleSheet(u"QLabel{\n"
                                    "background-color: red;\n"
                                    "max-width:155px;\n"
                                    "max-height:40px;\n"
                                    "margin-left:300px;\n"
                                    "margin-top:50px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "")

        self.image = QPixmap()
        self.imageLabel = QLabel()
        self.imageLabel.setStyleSheet(u"QLabel{\n"
                                    "width:750px;\n"
                                    "height:1000px;\n"
                                    "}\n"
                                    "")   

        self.imageLabel.setPixmap(QPixmap())
        self.imageLabel.show()

        verticalLayout1.addWidget(self.iname)
        verticalLayout1.addWidget(self.imageLabel)
        verticalLayout1.addStretch(1)

        verticalLayout2 = QVBoxLayout()

        self.tableinfo = QLabel('Prediction Results')
        self.tableinfo.setAlignment(Qt.AlignCenter)
        self.tableinfo.setStyleSheet(u"QLabel{\n"
                                    "margin-top:50px;\n"
                                    "max-height:40px;\n"
                                    "text-decoration: underline;\n"
                                    "margin-bottom:30px;\n"
                                    "font:14px;\n"
                                    "font-weight:bold;\n"
                                    "color:red;\n"
                                    "}\n"
                                    "")

        self.classTable = QTableWidget()
        self.classTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.classTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.classTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.classTable.horizontalHeader().setStyleSheet("QHeaderView { font-weight: bold; }")
        self.classTable.setColumnCount(5)
        self.classTable.setRowCount(0)
        self.classTable.setHorizontalHeaderLabels(["File Name","Class 01","Prob 01 (%)","Class 02","Prob 02 (%)"])
        self.classTable.setStyleSheet(u"QTableWidget{\n"
                                    "font:13px;\n"
                                    "min-height:100%;\n"
                                    "color:rgb(84, 84, 84);\n"
                                    "}\n"
                                    "")

        verticalLayout2.addWidget(self.tableinfo)
        verticalLayout2.addWidget(self.classTable)
        
        horizontalLayout.addLayout(verticalLayout,1)
        horizontalLayout.addLayout(verticalLayout1,2)
        horizontalLayout.addLayout(verticalLayout2,3)

        self.setLayout(horizontalLayout)

#connecting signals
        self.file.clicked.connect(self.loadFile)
        self.modelType.activated[str].connect(self.selectModel)
        self.customModelPath.clicked.connect(self.selectCustom)
        self.pro.clicked.connect(self.proceed)
        self.pred.clicked.connect(self.predict)
        self.viewfile.clicked.connect(self.finalfile)
        self.reset.clicked.connect(self.resetWorkspace)
        self.tips.clicked.connect(self.tipsAndTricks)

#default state of widgets
        self.file.setEnabled(True)
        self.modelType.setEnabled(False)
        self.customModelPath.setVisible(False)
        self.cmInfo.setVisible(False)
        self.pro.setEnabled(False)
        self.pred.setEnabled(False)
        self.classTable.setVisible(False)
        self.viewfile.setVisible(False)
        self.iname.setVisible(False)
        self.tableinfo.setVisible(False)

    def tipsAndTricks(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("COMING SOON")
        msg.setWindowTitle("Information")
        msg.exec_()

#function to reset UI
    def resetWorkspace(self):
        self.file.setText("Load New Features")
        self.fileInfo.clear()
        self.modelType.setEnabled(False)
        self.pro.setEnabled(False)
        self.proinfo.clear()
        self.pred.setEnabled(False)
        self.viewfile.setVisible(False)
        self.modelType.setCurrentText("ASIVA RF")
        self.imageLabel.setVisible(False)
        self.tableinfo.setVisible(False)
        self.iname.setVisible(False)
        self.cmInfo.clear()
        self.classTable.setVisible(False)
        self.customModelPath.setVisible(False)
        self.preinfo.clear()
        
#function to view output folder
    def finalfile(self):
        path = self.dir+'/06Classify_Variables'
        path = os.path.realpath(path)
        if sys.platform == "win32":
            os.startfile(path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])

#function to load feature file
    def loadFile(self):
        self.dir=Home.setupdir(self)
        os.chdir(self.dir)
        self.dfileName,_filter = QFileDialog.getOpenFileName(None, "Window name", self.dir, "CSV files (*.csv)")
        if self.dfileName == '':
            if self.fileInfo.text() == '':
                self.fileInfo.setText("Features not uploaded")
            else:
                self.fileInfo.setText(self.fileInfo.text())
        else:
            self.file.setText("Load New Features")
            self.fileInfo.setText(f"File: {self.dfileName.split('/')[-1]}")
            self.modelType.setEnabled(True)
            self.pro.setEnabled(True)
            self.proinfo.clear()
            self.pred.setEnabled(False)
            self.viewfile.setVisible(False)
            self.modelType.setCurrentText("ASIVA RF")
            self.imageLabel.setVisible(False)
            self.tableinfo.setVisible(False)
            self.iname.setVisible(False)
            self.cmInfo.clear()
            self.classTable.setVisible(False)
            self.customModelPath.setVisible(False)
            self.preinfo.clear()

#setting widget view according to selected model type
    def selectModel(self):
        if self.modelType.currentText() == 'ASIVA RF':
            self.proinfo.clear()
            self.preinfo.clear()
            self.imageLabel.setVisible(False)
            self.pro.setEnabled(True)
            self.pred.setEnabled(False)
            self.customModelPath.setVisible(False)
            self.cmInfo.setVisible(False)
            self.classTable.setVisible(False)
            self.tableinfo.setVisible(False)
            self.iname.setVisible(False)
        if self.modelType.currentText() == 'Custom':
            self.proinfo.clear()
            self.preinfo.clear()
            self.cmInfo.clear()
            self.pro.setEnabled(False)
            self.pred.setEnabled(False)
            self.viewfile.setVisible(False)
            self.customModelPath.setVisible(True)
            self.cmInfo.setVisible(True)
            self.tableinfo.setVisible(False)
            self.imageLabel.setVisible(False)
            self.classTable.setVisible(False)
            self.iname.setVisible(False)

#function to load custom model file
    def selectCustom(self):
        self.fileName,_filter = QFileDialog.getOpenFileName(None, "Window name", "", "JOBLIB files (*.joblib) ;; PICKLE files (*.pkl)")
        if self.fileName == '':
            self.cmInfo.setText("Model not selected")
            self.pro.setEnabled(False)
            self.proinfo.setEnabled(False)
            self.preinfo.clear()
            self.proinfo.clear()
        else:
            self.cmInfo.setText(self.fileName)
            self.pro.setEnabled(True)
            self.cmInfo.setVisible(True)
            self.tableinfo.setVisible(False)
            self.classTable.setVisible(False)
            self.preinfo.clear()
            self.proinfo.clear()

#function to load model 
    def proceed(self):
        os.chdir(self.dir)
        if "06Classify_Variables" not in os.listdir(self.dir):
            os.mkdir("06Classify_Variables")
        if "output" not in os.listdir("./06Classify_Variables/"):
            os.mkdir("06Classify_Variables/output")
        if "logs" not in os.listdir("./06Classify_Variables/"):
            os.mkdir("06Classify_Variables//logs")

        self.iname.setVisible(False)

        if self.modelType.currentText() == 'ASIVA RF':
            checkfile = pd.read_csv(self.dfileName)
            checkdf = checkfile.iloc[: , 1:]

            list1 = (list(checkdf.columns.values))

            list2 = ['Period', 'ECDF', 'Entropy', 'FAP', 'RCS', 'StetsonK', 'Kurtosis', 'Skewness', 'Mean', 'StdDev', 'psiCS']           

            if list1==list2:
                clf = asivaRF_model()
                mimage = asivaRF_cm()
                self.imageLabel.setVisible(True)
                self.image.loadFromData(mimage)
                self.imageLabel.setPixmap(QPixmap(self.image))
                self.imageLabel.setVisible(True)
                self.iname.setVisible(True)
                self.proinfo.setText("ASIVA RF Model Loaded!")
                self.pro.setEnabled(False)
                self.pred.setEnabled(True)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("For ASIVA models, please load ASIVA model features only")
                msg.setWindowTitle("Message")
                msg.exec_()

        if self.modelType.currentText() == 'Custom':
            self.proinfo.setText("Custom Model Loaded!")
            self.iname.setVisible(False)
            self.pro.setEnabled(False)
            self.pred.setEnabled(True)
            self.proinfo.setVisible(True)
            self.tableinfo.setVisible(False)

#function to predict
    def predict(self):
        try:
            if self.modelType.currentText() == 'ASIVA RF':
                clf = asivaRF_model()
                df = pd.read_csv(self.dfileName)
                name = df.iloc[:,0]
                pr_df = df.iloc[:, 1:].values

                y_pred_prediction = clf.predict(pr_df)
                y_prob_prediction = clf.predict_proba(pr_df)

                firstClass = []
                secondClass = []     
                firstProb = []
                secondProb = []

                for i in range(y_prob_prediction.shape[0]):
                    one = np.argsort(y_prob_prediction[i])[-1]
                    two = np.argsort(y_prob_prediction[i])[-2]

                    firstClass.append(one)
                    firstProb.append(y_prob_prediction[i][one])

                    if y_prob_prediction[i][two] != 0:
                        secondClass.append(two)
                        secondProb.append(y_prob_prediction[i][two])
                    else:
                        secondClass.append(np.nan)
                        secondProb.append(np.nan)

                    classes = { 0: "DCEP",
                            1: "DSCT",
                            2: "EC",
                            3: "ED",
                            4: "ESD",
                            5: "MIRA",
                            6: "RRAB",
                            7: "RRC"
                        } 

                    y_pred_prediction = [classes.get(x, x) for x in y_pred_prediction]

                    firstClass = [classes.get(x, x) for x in firstClass]
                    secondClass = [classes.get(x, x) for x in secondClass]

                self.pddf = pd.DataFrame(list(zip(name, firstClass, firstProb, secondClass, secondProb)))
                self.pddf.columns=['File Name','Class 01','Prob 01 (%)','Class 02','Prob 02 (%)']
                self.classTable.setColumnCount(self.pddf.shape[1])
                self.classTable.setRowCount(self.pddf.shape[0])
                for i in range(len(self.pddf.index)): 
                    for j in range(len(self.pddf.columns)):
                        self.classTable.setItem(i,j,QTableWidgetItem(str(self.pddf.iloc[i, j])))

                self.pddf.to_csv("06Classify_Variables/output/asivaRF_predictedResults.csv", index=None)
                self.preinfo.setText("Prediction Complete!")
                self.tableinfo.setVisible(True)
                self.classTable.setVisible(True)
                self.viewfile.setVisible(True)
                self.pred.setEnabled(False)

            elif self.modelType.currentText() == 'Custom':
                self.customModelPath.setEnabled(False)
                self.tableinfo.setVisible(False)
                self.classTable.setVisible(False)

                if self.fileName.endswith('.joblib'):
                    clf = joblib.load(self.fileName)
                elif self.fileName.endswith('.pkl'):
                    clf = pickle.load(self.fileName)

                df = pd.read_csv(self.dfileName)
                name = df.iloc[:,0]
                pr_df = df.iloc[:, 1:].values

                y_pred_prediction = clf.predict(pr_df)
                try:
                    y_prob_prediction = clf.predict_proba(pr_df)
                except:
                    y_prob_prediction = clf.predict_on_batch(pr_df)

                firstClass = []
                secondClass = []     
                firstProb = []
                secondProb = []

                for i in range(y_prob_prediction.shape[0]):
                    one = np.argsort(y_prob_prediction[i])[-1]
                    two = np.argsort(y_prob_prediction[i])[-2]

                    firstClass.append(one)
                    firstProb.append(y_prob_prediction[i][one])

                    if y_prob_prediction[i][two] != 0:
                        secondClass.append(two)
                        secondProb.append(y_prob_prediction[i][two])
                    else:
                        secondClass.append(np.nan)
                        secondProb.append(np.nan)

                self.pddf = pd.DataFrame(list(zip(name, firstClass, firstProb, secondClass, secondProb)))
                self.pddf.columns=['File Name','Class 01','Prob 01 (%)','Class 02','Prob 02 (%)']
                self.classTable.setColumnCount(self.pddf.shape[1])
                self.classTable.setRowCount(self.pddf.shape[0])
                for i in range(len(self.pddf.index)): 
                    for j in range(len(self.pddf.columns)):
                        self.classTable.setItem(i,j,QTableWidgetItem(str(self.pddf.iloc[i, j])))
                self.pddf.to_csv("06Classify_Variables/output/customModel_predictedResults.csv", index=None)
                self.preinfo.setText("Prediction Complete!")
                self.tableinfo.setVisible(True)
                self.classTable.setVisible(True)
                self.viewfile.setVisible(True)
                self.pred.setEnabled(False)
                self.customModelPath.setEnabled(True)

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Something went wrong, try with other model formats")
            msg.setWindowTitle("Warning")
            msg.exec_()
            self.tableinfo.setVisible(False)
            self.classTable.setVisible(False)
            self.customModelPath.setEnabled(True)
            self.pro.setEnabled(False)
            self.proinfo.setVisible(False)
            self.cmInfo.setVisible(False)
            self.pred.setEnabled(False)
            self.preinfo.setText("Prediction Failed!")

        self.logtime = time.time()
        with open(f"06Classify_Variables/logs/CV_{self.logtime}.txt","w") as file:
            file.write(f"Login Date and Time: {datetime.datetime.now()}")
            if self.modelType.currentText() == 'Custom':
                file.write(f"\nModel: {self.modelType.currentText()}")
                file.write(f"\nPath : {self.cmInfo.text()}")
            else:
                file.write(f"\nModel: {self.modelType.currentText()}")