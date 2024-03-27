#Importing required modules
import sys
import os
import ctypes
import webbrowser
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSizePolicy)                       
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from asiva.src.model.assets import logo
import qtawesome as qta
cmd = 'exit()'

#Creating Subclass of Widget
class Home(QWidget):
    
    directoryLoaded = pyqtSignal(str)

    def __init__(self):
        super(Home, self).__init__()
        self.setWindowTitle('Home')
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

#Adding QWidgets in GUI --- Setting the layout
        verticalLayout = QVBoxLayout()

        verticalLayout1 = QVBoxLayout()
        horizontalLayout = QHBoxLayout()

        home_icon = qta.icon('fa5s.home',
                        color='white')
        power_icon = qta.icon('fa5s.power-off',
                        color='white')

        self.opendir = QPushButton("Select Working Directory")
        self.opendir.setIcon(home_icon)
        self.opendir.setIconSize(QSize(30, 30))
        self.opendir.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #00bcd4;\n"
                                    "min-width:200px;\n"
                                    "max-width:250px;\n"
                                    "margin-top:20px;\n"
                                    "margin-left:10px;\n"
                                    "max-height:40px;\n"
                                    "min-height:40px;\n"
                                    "font:15px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius:7px;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #00838F;\n"
                                    "color:white;\n"
                                    "}\n"
                                    "")

        self.dirLabel = QLabel()
        self.dirLabel.setWordWrap(True)
        self.dirLabel.setStyleSheet(u"QLabel{\n"
                                    "font:13px;\n"
                                    "font-weight:bold;\n"
                                    "color:#6fb5b5;\n"
                                    "margin-top:20px;\n"
                                    "padding-left:10px;\n"
                                    "}\n"
                                    "")
        
        self.shutbtn = QPushButton("Shut Down")
        self.shutbtn.setIcon(power_icon)
        self.shutbtn.setIconSize(QSize(30, 30))
        self.shutbtn.setStyleSheet(u"QPushButton{\n"
                                    "background-color: #f44336;\n"
                                    "margin-top:20px;\n"
                                    "min-width:150px;\n"
                                    "max-width:200px;\n"
                                    "margin-right:10px;\n"
                                    "max-width:120px;\n"
                                    "max-height:40px;\n"
                                    "min-height:40px;\n"
                                    "border-radius:7px;\n"
                                    "color:white;\n"
                                    "font:15px;\n"
                                    "font-weight:bold;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "border:2px solid #cc4f41;\n"
                                    "color: white;\n"
                                    "}\n"
                                    "")

        horizontalLayout.addWidget(self.opendir)
        horizontalLayout.addWidget(self.dirLabel)
        horizontalLayout.addWidget(self.shutbtn)

        verticalLayout2 = QVBoxLayout()
        horizontalLayout1 = QHBoxLayout()

        self.image = QPixmap()
        self.imageLabel = QLabel()
        self.imageLabel.setStyleSheet(u"QLabel{\n"
                                    "max-height:851;\n"
                                    "max-width:981px;\n"
                                    "}\n"
                                    "")

        self.imageLabel.setScaledContents(True)
        self.imageLabel.setPixmap(QPixmap())
        self.imageLabel.show()
        self.imageLabel.setAlignment(Qt.AlignCenter)

        horizontalLayout1.addWidget(self.imageLabel)

        verticalLayout3 = QVBoxLayout()
        horizontalLayout2 = QHBoxLayout()
        
        verticalLayout1.addLayout(horizontalLayout)
        verticalLayout2.addLayout(horizontalLayout1)
        verticalLayout3.addLayout(horizontalLayout2)

        verticalLayout.addLayout(verticalLayout1,1)
        verticalLayout.addLayout(verticalLayout2,1)
        verticalLayout.addLayout(verticalLayout3,1)
         
        self.setLayout(verticalLayout)

#Connecting Signals
        self.opendir.clicked.connect(self.loadworkdir)
        self.shutbtn.clicked.connect(self.shutd)

        mimage = logo()
        self.image.loadFromData(mimage)
        self.imageLabel.setPixmap(self.image)
    
    workdir = os.path.expanduser("~")

#function to load working directory
    def loadworkdir(self):
        global workdir

        self.dialog = QFileDialog()
        workdir = self.dialog.getExistingDirectory(None, "Select Folder",os.path.expanduser("~"))
        if workdir == '':
            self.dirLabel.setText('Selected Directory: None')
            self.opendir.setText("Select Working Directory")
        else:
            self.opendir.setText("Change Working Directory")
            self.dirLabel.setText('Selected Directory : {}'.format(workdir))

            os.chdir(workdir)
            path = workdir+'/config'
            if not os.path.exists(path):
                if sys.platform == "win32":
                    os.mkdir(path)
                    FILE_ATTRIBUTE_HIDDEN = 0x02
                    ret = ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)	
                else:
                    os.mkdir(path)
                #try:
                    #os.mkdir(path)
                    #FILE_ATTRIBUTE_HIDDEN = 0x02
                    #ret = ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)
                #except:
                 #   os.mkdir(path)
                    
            filepath = os.path.dirname(os.path.realpath(__file__))
            sourcefile = filepath+'/features/customFeatures.py'
            destfile = workdir+'/config/customFeatures.py'

            if os.path.exists(destfile):
                pass
            else:
                with open(sourcefile, 'rb') as f, open(destfile, 'wb') as g:
                    while True:
                        block = f.read(16*1024*1024)
                        if not block: 
                            break
                        g.write(block)

        self.directoryLoaded.emit(workdir)

        return workdir

#function to set working directory for all tabs
    def setupdir(self):
        global x
        x = workdir
        return x

#function for shutdown
    def shutd(self):
        os.system(cmd)
        QCoreApplication.instance().quit()
