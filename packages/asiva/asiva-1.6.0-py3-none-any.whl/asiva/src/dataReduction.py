import sys
import qtawesome as qta
from threading import Thread
from pyqtconsole.console import PythonConsole

from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QMainWindow)

# creating a subclass of QWidget
class DataReduction(QWidget):
    def __init__(self):
        super(DataReduction, self).__init__()
        # self.setWindowTitle("CONSOLE")
        self.setMinimumWidth(1300)
        self.setMinimumHeight(750)

        self.horizontalLayout = QHBoxLayout()
        self.verticalLayout = QVBoxLayout()
        
        self.predict_icon = qta.icon('fa5s.bolt',
                        color='white')

        tips_icon = qta.icon('fa5s.lightbulb',
                        color='#e8a92c')

        self.horizontalLayout1 = QHBoxLayout()
        self.horizontalLayout1.setAlignment(Qt.AlignTop)

        self.ShowConsoleButton = QPushButton("Load Console")
        self.ShowConsoleButton.setIcon(self.predict_icon)
        self.ShowConsoleButton.setIconSize(QSize(30, 30))
        self.ShowConsoleButton.setStyleSheet(u"QPushButton{\n"
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

        self.horizontalLayout1.addWidget(self.ShowConsoleButton)

        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setAlignment(Qt.AlignBottom)

        self.HideConsoleButton = QPushButton('Hide Console')
        self.HideConsoleButton.setStyleSheet(u"QPushButton{\n"
                                    "background-color:white;\n"
                                    "border:2px solid #FF0000;\n"
                                    "color:#FF0000;\n"
                                    "font:18px;\n"
                                    "width:100%;\n"
                                    "height:40px;\n"
                                    "font-weight:bold;\n"
                                    "border-radius: 5px;\n"
                                    "text-align:center;\n"
                                    "padding-left:10px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "color:white;\n"
                                    "background-color:#FF0000;\n"
                                    "border:none;\n"
                                    "}\n"
                                    "QPushButton:disabled {\n"
                                    "color:#cccccc;\n"
                                    "}\n"
                                    "")
        self.horizontalLayout2.addWidget(self.HideConsoleButton)

        self.horizontalLayout3 = QHBoxLayout()
        self.horizontalLayout3.setAlignment(Qt.AlignBottom)

        
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
                                    "QPushButton:disabled {\n"
                                    "background-color:#8ad1d1;\n"
                                    "color:gray;\n"
                                    "}\n"
                                    "")

        self.horizontalLayout3.addWidget(self.tips)

        self.verticalLayout.addLayout(self.horizontalLayout1)
        self.verticalLayout.addStretch()
        self.verticalLayout.addLayout(self.horizontalLayout2)
        self.verticalLayout.addLayout(self.horizontalLayout3)

        self.verticalLayout1 = QVBoxLayout()

        self.console = PythonConsole()
        self.console.eval_queued()

        self.verticalLayout1.addWidget(self.console)
        
        self.horizontalLayout.addLayout(self.verticalLayout,1)
        self.horizontalLayout.addLayout(self.verticalLayout1,4)

        self.setLayout(self.horizontalLayout)

        self.show()

# #Connecting Signals
        self.ShowConsoleButton.clicked.connect(self.consoleShow)
        self.HideConsoleButton.clicked.connect(self.consoleHide)
        self.tips.clicked.connect(self.tipsAndTricks)

#Setting default status of widgets
        self.ShowConsoleButton.setEnabled(True)
        self.console.setVisible(False)
        self.HideConsoleButton.setVisible(False)
        self.HideConsoleButton.setEnabled(False)

    def consoleShow(self):
        self.console.setVisible(True)
        self.HideConsoleButton.setEnabled(True)
        self.HideConsoleButton.setVisible(True)

    def consoleHide(self):
        self.console.setVisible(False)
        self.HideConsoleButton.setEnabled(False)
        self.HideConsoleButton.setVisible(False)

    def tipsAndTricks(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("COMING SOON")
        msg.setWindowTitle("Information")
        msg.exec_()