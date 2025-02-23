# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHeaderView,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStackedWidget,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextBrowser,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, w_MainWindow):
        if not w_MainWindow.objectName():
            w_MainWindow.setObjectName(u"w_MainWindow")
        w_MainWindow.resize(800, 600)
        self.tw_Main = QTabWidget(w_MainWindow)
        self.tw_Main.setObjectName(u"tw_Main")
        self.t_Files = QWidget()
        self.t_Files.setObjectName(u"t_Files")
        self.gl_Files = QGridLayout(self.t_Files)
        self.gl_Files.setObjectName(u"gl_Files")
        self.tbl_Files = QTableWidget(self.t_Files)
        self.tbl_Files.setObjectName(u"tbl_Files")

        self.gl_Files.addWidget(self.tbl_Files, 0, 0, 1, 4)

        self.pb_FilesOpen = QPushButton(self.t_Files)
        self.pb_FilesOpen.setObjectName(u"pb_FilesOpen")

        self.gl_Files.addWidget(self.pb_FilesOpen, 1, 0, 1, 1)

        self.pb_FilesSave = QPushButton(self.t_Files)
        self.pb_FilesSave.setObjectName(u"pb_FilesSave")

        self.gl_Files.addWidget(self.pb_FilesSave, 1, 1, 1, 1)

        self.s_FilesHorizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Files.addItem(self.s_FilesHorizontal, 1, 2, 1, 1)

        self.pb_FilesContinue = QPushButton(self.t_Files)
        self.pb_FilesContinue.setObjectName(u"pb_FilesContinue")

        self.gl_Files.addWidget(self.pb_FilesContinue, 1, 3, 1, 1)

        self.tw_Main.addTab(self.t_Files, "")
        self.t_Configuration = QWidget()
        self.t_Configuration.setObjectName(u"t_Configuration")
        self.gl_Configuration = QGridLayout(self.t_Configuration)
        self.gl_Configuration.setObjectName(u"gl_Configuration")
        self.l_Instrument = QLabel(self.t_Configuration)
        self.l_Instrument.setObjectName(u"l_Instrument")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_Instrument.sizePolicy().hasHeightForWidth())
        self.l_Instrument.setSizePolicy(sizePolicy)

        self.gl_Configuration.addWidget(self.l_Instrument, 0, 0, 1, 1)

        self.cb_Instrument = QComboBox(self.t_Configuration)
        self.cb_Instrument.addItem("")
        self.cb_Instrument.addItem("")
        self.cb_Instrument.setObjectName(u"cb_Instrument")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cb_Instrument.sizePolicy().hasHeightForWidth())
        self.cb_Instrument.setSizePolicy(sizePolicy1)

        self.gl_Configuration.addWidget(self.cb_Instrument, 0, 1, 1, 1)

        self.l_Experiment = QLabel(self.t_Configuration)
        self.l_Experiment.setObjectName(u"l_Experiment")
        sizePolicy.setHeightForWidth(self.l_Experiment.sizePolicy().hasHeightForWidth())
        self.l_Experiment.setSizePolicy(sizePolicy)

        self.gl_Configuration.addWidget(self.l_Experiment, 0, 2, 1, 1)

        self.cb_Experiment = QComboBox(self.t_Configuration)
        self.cb_Experiment.addItem("")
        self.cb_Experiment.addItem("")
        self.cb_Experiment.addItem("")
        self.cb_Experiment.setObjectName(u"cb_Experiment")
        sizePolicy1.setHeightForWidth(self.cb_Experiment.sizePolicy().hasHeightForWidth())
        self.cb_Experiment.setSizePolicy(sizePolicy1)

        self.gl_Configuration.addWidget(self.cb_Experiment, 0, 3, 1, 1)

        self.s_MainHorizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Configuration.addItem(self.s_MainHorizontal, 0, 4, 1, 1)

        self.pb_Run = QPushButton(self.t_Configuration)
        self.pb_Run.setObjectName(u"pb_Run")

        self.gl_Configuration.addWidget(self.pb_Run, 0, 5, 1, 1)

        self.sw_Configuration = QStackedWidget(self.t_Configuration)
        self.sw_Configuration.setObjectName(u"sw_Configuration")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sw_Configuration.sizePolicy().hasHeightForWidth())
        self.sw_Configuration.setSizePolicy(sizePolicy2)

        self.gl_Configuration.addWidget(self.sw_Configuration, 1, 0, 1, 6)

        self.tw_Main.addTab(self.t_Configuration, "")
        self.t_Output = QWidget()
        self.t_Output.setObjectName(u"t_Output")
        self.gl_Output = QGridLayout(self.t_Output)
        self.gl_Output.setObjectName(u"gl_Output")
        self.sa_Output = QScrollArea(self.t_Output)
        self.sa_Output.setObjectName(u"sa_Output")
        self.sa_Output.setWidgetResizable(True)
        self.tb_OutputText = QTextBrowser()
        self.tb_OutputText.setObjectName(u"tb_OutputText")
        self.sa_Output.setWidget(self.tb_OutputText)

        self.gl_Output.addWidget(self.sa_Output, 0, 0, 1, 1)

        self.tw_Main.addTab(self.t_Output, "")
        w_MainWindow.setCentralWidget(self.tw_Main)
        self.mb_Main = QMenuBar(w_MainWindow)
        self.mb_Main.setObjectName(u"mb_Main")
        self.mb_Main.setGeometry(QRect(0, 0, 800, 24))
        w_MainWindow.setMenuBar(self.mb_Main)

        self.retranslateUi(w_MainWindow)

        self.tw_Main.setCurrentIndex(1)
        self.sw_Configuration.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(w_MainWindow)
    # setupUi

    def retranslateUi(self, w_MainWindow):
        w_MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.pb_FilesOpen.setToolTip(QCoreApplication.translate("MainWindow", u"Choose the directory containing the experiment output files", None))
#endif // QT_CONFIG(tooltip)
        self.pb_FilesOpen.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
#if QT_CONFIG(tooltip)
        self.pb_FilesSave.setToolTip(QCoreApplication.translate("MainWindow", u"Choose the directory to which the processed Excel spreadsheets will be written", None))
#endif // QT_CONFIG(tooltip)
        self.pb_FilesSave.setText(QCoreApplication.translate("MainWindow", u"Save to...", None))
#if QT_CONFIG(tooltip)
        self.pb_FilesContinue.setToolTip(QCoreApplication.translate("MainWindow", u"Continue on to the experiment analysis configuration", None))
#endif // QT_CONFIG(tooltip)
        self.pb_FilesContinue.setText(QCoreApplication.translate("MainWindow", u"Continue...", None))
        self.tw_Main.setTabText(self.tw_Main.indexOf(self.t_Files), QCoreApplication.translate("MainWindow", u"Files", None))
        self.l_Instrument.setText(QCoreApplication.translate("MainWindow", u"Instrument:", None))
        self.cb_Instrument.setItemText(0, QCoreApplication.translate("MainWindow", u"Instron 68TM", None))
        self.cb_Instrument.setItemText(1, QCoreApplication.translate("MainWindow", u"MicroTester G2", None))

        self.l_Experiment.setText(QCoreApplication.translate("MainWindow", u"Experiment:", None))
        self.cb_Experiment.setItemText(0, QCoreApplication.translate("MainWindow", u"Stepwise compression", None))
        self.cb_Experiment.setItemText(1, QCoreApplication.translate("MainWindow", u"Compression-to-failure", None))
        self.cb_Experiment.setItemText(2, QCoreApplication.translate("MainWindow", u"Cyclic indentation", None))

#if QT_CONFIG(tooltip)
        self.pb_Run.setToolTip(QCoreApplication.translate("MainWindow", u"Process the experiment outputs and save the results to the Excel files", None))
#endif // QT_CONFIG(tooltip)
        self.pb_Run.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.tw_Main.setTabText(self.tw_Main.indexOf(self.t_Configuration), QCoreApplication.translate("MainWindow", u"Configuration", None))
        self.tw_Main.setTabText(self.tw_Main.indexOf(self.t_Output), QCoreApplication.translate("MainWindow", u"Output", None))
    # retranslateUi

