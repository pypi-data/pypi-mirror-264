# importing required modules
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel, QSizePolicy
from asiva.src.periodDetection import Periodogram
from asiva.src.variabledetection import VariableDetection
from asiva.src.dataProcessing import DataProcessing
from asiva.src.dataReduction import DataReduction
from asiva.src.stationarityTest import Stationarity 
from asiva.src.featureExtraction import Feature
from asiva.src.classifyVariables import Classifier
from asiva.src.home import Home
from asiva.src.aboutUs import About
from PyQt5.QtGui import QIcon

# Creating the main window
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'ASIVA'
        self.setWindowIcon(QIcon('icon.ico'))
        #self.setMinimumWidth(1280)
        #self.setMinimumHeight(720)
        self.setWindowTitle(self.title)
  
        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.showMaximized()
        self.show()
        self.update()
  
# Creating tab widgets
class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()

        firstTab = Home()
        firstTab.directoryLoaded.connect(self.firstTabLoaded)

        # Add tabs
        self.tabs.addTab(firstTab, "Home")
        self.tabs.addTab(DataReduction(), "Data Reduction")
        self.tabs.addTab(DataProcessing(), "Data Processing")
        self.tabs.addTab(VariableDetection(), "Variable Detection")
        self.tabs.addTab(Stationarity(), "Stationarity Test")
        self.tabs.addTab(Periodogram(), "Period Detection")
        self.tabs.addTab(Feature(), "Feature Extraction")
        self.tabs.addTab(Classifier(), "Classify Variables")
        self.tabs.addTab(About(), "About Us")

        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
        self.tabs.setTabEnabled(3, False)
        self.tabs.setTabEnabled(4, False)
        self.tabs.setTabEnabled(5, False)
        self.tabs.setTabEnabled(6, False)
        self.tabs.setTabEnabled(7, False)
        self.tabs.setTabEnabled(8, True)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)

#function to disable and enable tabs
    def firstTabLoaded(self, path):
        if path and not self.tabs.isTabEnabled(1):
            self.tabs.setTabEnabled(1, True)
            self.tabs.setTabEnabled(2, True)
            self.tabs.setTabEnabled(3, True)
            self.tabs.setTabEnabled(4, True)
            self.tabs.setTabEnabled(5, True)
            self.tabs.setTabEnabled(6, True)
            self.tabs.setTabEnabled(7, True)
            self.tabs.setTabEnabled(8, True)

        if path == '':
            self.tabs.setTabEnabled(1, False)
            self.tabs.setTabEnabled(2, False)
            self.tabs.setTabEnabled(3, False)
            self.tabs.setTabEnabled(4, False)
            self.tabs.setTabEnabled(5, False)
            self.tabs.setTabEnabled(6, False)
            self.tabs.setTabEnabled(7, False)
            self.tabs.setTabEnabled(8, True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
