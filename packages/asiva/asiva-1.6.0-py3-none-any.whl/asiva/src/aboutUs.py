#IMPORTING REQUIRED MODULES
import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, 
                            QFileDialog, 
                            QHBoxLayout, 
                            QVBoxLayout, 
                            QPushButton, 
                            QLabel, 
                            QApplication, 
                            QMessageBox, 
                            QProgressBar, 
                            QTableWidget,
                            QSizePolicy,
                            QTableWidgetItem, 
                            QToolTip,
                            QComboBox)
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import webbrowser
#CREATING SUBCLASS OF WIDGET

class About(QWidget):
    
    def __init__(self):
        super(About, self).__init__()
        self.setWindowTitle('About Us')
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('white'))
        self.setPalette(palette)

#ADDING QWIDGETS IN GUI-- SETTING THE LAYOUT
        
        horizontalLayout = QHBoxLayout()

        verticalLayout = QVBoxLayout()

        header=QLabel("ASIVA 1.6")
        header.setStyleSheet(u"QLabel{\n"
                                    "font:36px;\n"
                                    "font-weight:bold;\n"
                                    "color:red;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")
        title=QLabel("AstroStatistics In Variable Astronomy")
        title.setStyleSheet(u"QLabel{\n"
                                    "font:24px;\n"
                                    "font-weight:bold;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")
        description=QLabel("ASIVA is a public and user-friendly astronomical data analysis platform. The platform helps astronomers, data enthusiast and statisticians to explore the complete process of astronomical & time series analysis at one place. The data analysis process is organized into 6 parts, starting from data preprocessing to predicting class of variables. Below are the details:<br><br><br>1. <b>Data Processing</b>: Detect & handle missing values with standard methods. Shows basic statistical measures of input data.<br><br>2. <b>Variable Detection</b>: Detect variables from star ensemble. Perform differential photometry & generate light curves.<br><br>3. <b>Stationarity Test</b>: Detect seasonality, outliers & transient events in time series. Detrend non-stationary time series.<br><br>4. <b>Period Detection</b>: Perform periodogram analysis with LombScargle algorithm. Generate phased light curve with plots.<br><br>5. <b>Feature Extraction</b>: Bulk extraction of ~50 features at one place. Ready-to-go features for classifying variables.<br><br>6. <b>Classify Variables</b>: Predict type of variables using pre-built models. Load custom model to classify variables.<br><br><br>")
        description.setWordWrap(True)
        description.setTextFormat(Qt.RichText)
        description.setStyleSheet(u"QLabel{\n"
                                    "font:18px;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")
        libraries=QLabel("<b>Libraries Used</b>: <i>astropy, gatspy, hurst, keras, matplotlib, numpy, pandas, seaborn, sklearn, statsmodels, tensorflow</i>.")
        libraries.setWordWrap(True)
        libraries.setTextFormat(Qt.RichText)
        libraries.setStyleSheet(u"QLabel{\n"
                                    "font:18px;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")
        citation=QLabel("<b>Citation</b>: Coming soon...")
        citation.setWordWrap(True)
        citation.setTextFormat(Qt.RichText)
        citation.setStyleSheet(u"QLabel{\n"
                                    "font:18px;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")
        documentation=QLabel("<b>Documentation</b>: <a style='text-decoration:none;color:black'href='https://asiva.readthedocs.io/'>https://asiva.readthedocs.io/</a>")
        documentation.setWordWrap(True)
        documentation.setTextFormat(Qt.RichText)
        documentation.setOpenExternalLinks(True)
        documentation.linkHovered.connect(links_hover)
        documentation.setStyleSheet(u"QLabel{\n"
                                    "font:18px;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")
        license=QLabel("<b>License</b>: The software is freely available at <a style='text-decoration:none;color:black'href='https://github.com/asivaai/asiva_qt'>https://github.com/asivaai/asiva_qt</a> under the MIT License.")
        license.setWordWrap(True)
        license.setTextFormat(Qt.RichText)
        license.setOpenExternalLinks(True)
        license.linkHovered.connect(links_hover)
        license.setStyleSheet(u"QLabel{\n"
                                    "font:18px;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")
        contact=QLabel("<b>Website</b>: <a style='text-decoration:none;color:black'href='https://asivaai.github.io'>https://asivaai.github.io</a> | <b>Contact</b>: <a style='text-decoration:none;color:black'href='mailto:asivaai2021@gmail.com'>asivaai2021@gmail.com</a>")
        contact.setWordWrap(True)
        contact.setTextFormat(Qt.RichText)
        contact.setOpenExternalLinks(True)
        contact.linkHovered.connect(links_hover)
        contact.setStyleSheet(u"QLabel{\n"
                                    "font:18px;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")

        verticalLayout.addWidget(header)
        verticalLayout.addWidget(title)
        verticalLayout.addWidget(description)
        verticalLayout.addWidget(libraries)
        verticalLayout.addWidget(citation)
        verticalLayout.addWidget(documentation)
        verticalLayout.addWidget(license)
        verticalLayout.addWidget(contact)

        verticalLayout.addStretch()

        horizontalLayout1 = QHBoxLayout()
        verticalLayout1 = QVBoxLayout()

        self.imageLabel = QLabel()
        self.imageLabel.setStyleSheet(u"QLabel{\n"
                                    "max-width:620px;\n"
                                    "max-height:620px;\n"
                                    "}\n"
                                    "")

        verticalLayout1.addWidget(self.imageLabel)
        verticalLayout1.addStretch()

        header2=QLabel("ASIVA Team")
        header2.setStyleSheet(u"QLabel{\n"
                                    "font:36px;\n"
                                    "font-weight:bold;\n"
                                    "color:red;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")
        contributors = QLabel("<b>Contributors</b>: <a style='text-decoration:none;color:black'href='https://linkedin.com/in/parvejsaleh/'>Parvej Saleh</a>, <a style='text-decoration:none;color:black'href='https://linkedin.com/in/tanveer-singh-250b02194/'>Tanveer Singh</a> & <a style='text-decoration:none;color:black'href='https://linkedin.com/in/hazarikadebasish/'>Debasish Hazarika</a>")
        contributors.setTextFormat(Qt.RichText)
        contributors.setOpenExternalLinks(True)
        contributors.linkHovered.connect(links_hover)
        contributors.setStyleSheet(u"QLabel{\n"
                                    "font:18px;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")
        developers = QLabel("<b>Developers</b>: <a style='text-decoration:none;color:black'href='https://www.linkedin.com/in/surabhi-rajkumari-789b681a7'>Surabhi Rajkumari</a> & <a style='text-decoration:none;color:black'href='https://www.linkedin.com/in/saurabh-rajkumar-5401611b2/'>Saurabh Rajkumar</a>")
        developers.setTextFormat(Qt.RichText)
        developers.setOpenExternalLinks(True)
        developers.linkHovered.connect(links_hover)
        developers.setStyleSheet(u"QLabel{\n"
                                    "font:18px;\n"
                                    "margin-top:20px;\n"
                                    "}\n"
                                    "")
        mentor = QLabel("<b>Mentors</b>: <a style='text-decoration:none;color:black'href='https://linkedin.com/in/eeshankur-saikia-81193284/'>Dr. Eeshankur Saikia<sup>1</sup></a> & <a style='text-decoration:none;color:black'href='https://linkedin.com/in/padmakar-parihar-784ba1171/'>Dr. Padmakar Singh Parihar<sup>2</sup></a>")
        mentor.setTextFormat(Qt.RichText)
        mentor.setOpenExternalLinks(True)
        mentor.linkHovered.connect(links_hover)
        mentor.setStyleSheet(u"QLabel{\n"
                                    "font:18px;\n"
                                    "margin-top:20px;\n"
                                    "color:black;\n"
                                    "}\n"
                                    "")
        institute = QLabel("<b>Institute</b>: <a style='text-decoration:none;color:black'href='https://www.gauhati.ac.in/'>Gauhati University<sup>1</sup></a> & <a style='text-decoration:none;color:black'href='https://www.iiap.res.in/'>Indian Institute of Astrophysics<sup>2</sup></a>")
        institute.setTextFormat(Qt.RichText)
        institute.setOpenExternalLinks(True)
        institute.linkHovered.connect(links_hover)
        institute.setStyleSheet(u"QLabel{\n"
                                    "font:18px;\n"
                                    "margin-top:20px;\n"
                                    "color:black\n"
                                    "}\n"
                                    "")

        verticalLayout1.addWidget(header2)
        verticalLayout1.addWidget(contributors)
        verticalLayout1.addWidget(developers)
        verticalLayout1.addWidget(mentor)
        verticalLayout1.addWidget(institute)
        verticalLayout1.addStretch()

        
        horizontalLayout1.addLayout(verticalLayout1,1)
        horizontalLayout.addLayout(verticalLayout,2)
        horizontalLayout.addLayout(horizontalLayout1,1)

        self.setLayout(horizontalLayout)

        path = os.path.dirname(os.path.realpath(__file__))
        data = open(f"{path}/model/animated.gif", "rb").read()
        self.bArray = QtCore.QByteArray(data)
        self.bBuffer = QtCore.QBuffer(self.bArray)
        self.bBuffer.open(QtCore.QIODevice.ReadOnly)
        self.movie = QtGui.QMovie(self.bBuffer, b'GIF')
        self.imageLabel.setMovie(self.movie)
        self.movie.start()


link_title = {'https://github.com/asivaai/asiva_qt': 'View GitHub repository',
                'https://asivaai.github.io': 'View Website',
                'https://asiva.readthedocs.io/': 'View Documentation',
                'https://linkedin.com/in/parvejsaleh/': 'View LinkedIn profile',
                'https://linkedin.com/in/tanveer-singh-250b02194/': 'View LinkedIn profile',
                'https://linkedin.com/in/hazarikadebasish/': 'View LinkedIn profile',
                'https://linkedin.com/in/surabhi-rajkumari-789b681a7': 'View LinkedIn profile',
                'https://linkedin.com/in/saurabh-rajkumar-5401611b2/': 'View LinkedIn profile',
                'https://linkedin.com/in/eeshankur-saikia-81193284/': 'View LinkedIn profile',
                'https://linkedin.com/in/padmakar-parihar-784ba1171/': 'View LinkedIn profile',
                'https://www.gauhati.ac.in/': 'View Website',
                'https://www.iiap.res.in/': 'View Website',
                'mailto:asivaai2021@gmail.com': 'Contact via e-mail'}

def links_hover(url):
    if url:
        try:
            QToolTip.showText(QCursor.pos(), link_title.get(url, url))
        except:
            QToolTip.hideText()
    else:
        QToolTip.hideText()

