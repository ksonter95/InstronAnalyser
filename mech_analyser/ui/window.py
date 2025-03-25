# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextBrowser,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.tw_Main = QTabWidget(MainWindow)
        self.tw_Main.setObjectName(u"tw_Main")
        self.t_Files = QWidget()
        self.t_Files.setObjectName(u"t_Files")
        self.gl_Files = QGridLayout(self.t_Files)
        self.gl_Files.setObjectName(u"gl_Files")
        self.tbl_Files = QTableWidget(self.t_Files)
        if (self.tbl_Files.columnCount() < 3):
            self.tbl_Files.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_Files.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_Files.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_Files.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tbl_Files.setObjectName(u"tbl_Files")
        self.tbl_Files.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbl_Files.setRowCount(0)
        self.tbl_Files.setColumnCount(3)
        self.tbl_Files.horizontalHeader().setVisible(True)
        self.tbl_Files.horizontalHeader().setStretchLastSection(True)

        self.gl_Files.addWidget(self.tbl_Files, 0, 0, 1, 5)

        self.pb_OpenDirectory = QPushButton(self.t_Files)
        self.pb_OpenDirectory.setObjectName(u"pb_OpenDirectory")

        self.gl_Files.addWidget(self.pb_OpenDirectory, 1, 0, 1, 1)

        self.pb_OpenCsv = QPushButton(self.t_Files)
        self.pb_OpenCsv.setObjectName(u"pb_OpenCsv")

        self.gl_Files.addWidget(self.pb_OpenCsv, 1, 1, 1, 1)

        self.s_FilesHorizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Files.addItem(self.s_FilesHorizontal, 1, 2, 1, 1)

        self.pb_Clear = QPushButton(self.t_Files)
        self.pb_Clear.setObjectName(u"pb_Clear")

        self.gl_Files.addWidget(self.pb_Clear, 1, 3, 1, 1)

        self.pb_Configuration = QPushButton(self.t_Files)
        self.pb_Configuration.setObjectName(u"pb_Configuration")

        self.gl_Files.addWidget(self.pb_Configuration, 1, 4, 1, 1)

        self.pb_SaveDirectory = QPushButton(self.t_Files)
        self.pb_SaveDirectory.setObjectName(u"pb_SaveDirectory")

        self.gl_Files.addWidget(self.pb_SaveDirectory, 2, 0, 1, 1)

        self.cb_All = QCheckBox(self.t_Files)
        self.cb_All.setObjectName(u"cb_All")
        self.cb_All.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gl_Files.addWidget(self.cb_All, 2, 1, 1, 1)

        self.tb_SaveDirectory = QTextBrowser(self.t_Files)
        self.tb_SaveDirectory.setObjectName(u"tb_SaveDirectory")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_SaveDirectory.sizePolicy().hasHeightForWidth())
        self.tb_SaveDirectory.setSizePolicy(sizePolicy)

        self.gl_Files.addWidget(self.tb_SaveDirectory, 2, 2, 1, 3)

        self.tw_Main.addTab(self.t_Files, "")
        self.t_Configuration = QWidget()
        self.t_Configuration.setObjectName(u"t_Configuration")
        self.gl_Configuration = QGridLayout(self.t_Configuration)
        self.gl_Configuration.setObjectName(u"gl_Configuration")
        self.l_Instrument = QLabel(self.t_Configuration)
        self.l_Instrument.setObjectName(u"l_Instrument")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.l_Instrument.sizePolicy().hasHeightForWidth())
        self.l_Instrument.setSizePolicy(sizePolicy1)

        self.gl_Configuration.addWidget(self.l_Instrument, 0, 0, 1, 1)

        self.cb_Instrument = QComboBox(self.t_Configuration)
        self.cb_Instrument.setObjectName(u"cb_Instrument")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cb_Instrument.sizePolicy().hasHeightForWidth())
        self.cb_Instrument.setSizePolicy(sizePolicy2)

        self.gl_Configuration.addWidget(self.cb_Instrument, 0, 1, 1, 1)

        self.l_Experiment = QLabel(self.t_Configuration)
        self.l_Experiment.setObjectName(u"l_Experiment")
        sizePolicy1.setHeightForWidth(self.l_Experiment.sizePolicy().hasHeightForWidth())
        self.l_Experiment.setSizePolicy(sizePolicy1)

        self.gl_Configuration.addWidget(self.l_Experiment, 0, 2, 1, 1)

        self.cb_Experiment = QComboBox(self.t_Configuration)
        self.cb_Experiment.setObjectName(u"cb_Experiment")
        sizePolicy2.setHeightForWidth(self.cb_Experiment.sizePolicy().hasHeightForWidth())
        self.cb_Experiment.setSizePolicy(sizePolicy2)

        self.gl_Configuration.addWidget(self.cb_Experiment, 0, 3, 1, 1)

        self.s_MainHorizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Configuration.addItem(self.s_MainHorizontal, 0, 4, 1, 1)

        self.pb_Run = QPushButton(self.t_Configuration)
        self.pb_Run.setObjectName(u"pb_Run")

        self.gl_Configuration.addWidget(self.pb_Run, 0, 5, 1, 1)

        self.sw_Configuration = QStackedWidget(self.t_Configuration)
        self.sw_Configuration.setObjectName(u"sw_Configuration")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.sw_Configuration.sizePolicy().hasHeightForWidth())
        self.sw_Configuration.setSizePolicy(sizePolicy3)

        self.gl_Configuration.addWidget(self.sw_Configuration, 1, 0, 1, 6)

        self.tw_Main.addTab(self.t_Configuration, "")
        self.t_Output = QWidget()
        self.t_Output.setObjectName(u"t_Output")
        self.gl_Output = QGridLayout(self.t_Output)
        self.gl_Output.setObjectName(u"gl_Output")
        self.tbl_Output = QTableWidget(self.t_Output)
        if (self.tbl_Output.columnCount() < 1):
            self.tbl_Output.setColumnCount(1)
        self.tbl_Output.setObjectName(u"tbl_Output")
        self.tbl_Output.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbl_Output.setRowCount(0)
        self.tbl_Output.setColumnCount(1)
        self.tbl_Output.horizontalHeader().setVisible(False)
        self.tbl_Output.horizontalHeader().setStretchLastSection(True)
        self.tbl_Output.verticalHeader().setVisible(False)

        self.gl_Output.addWidget(self.tbl_Output, 0, 0, 1, 2)

        self.s_OutputHorizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Output.addItem(self.s_OutputHorizontal, 1, 0, 1, 1)

        self.pb_Continue = QPushButton(self.t_Output)
        self.pb_Continue.setObjectName(u"pb_Continue")

        self.gl_Output.addWidget(self.pb_Continue, 1, 1, 1, 1)

        self.tw_Main.addTab(self.t_Output, "")
        self.t_Collation = QWidget()
        self.t_Collation.setObjectName(u"t_Collation")
        self.gl_Collation = QGridLayout(self.t_Collation)
        self.gl_Collation.setObjectName(u"gl_Collation")
        self.l_CollationFilename = QLabel(self.t_Collation)
        self.l_CollationFilename.setObjectName(u"l_CollationFilename")

        self.gl_Collation.addWidget(self.l_CollationFilename, 0, 0, 1, 4)

        self.le_CollationFilename = QLineEdit(self.t_Collation)
        self.le_CollationFilename.setObjectName(u"le_CollationFilename")

        self.gl_Collation.addWidget(self.le_CollationFilename, 1, 0, 1, 4)

        self.l_RawData = QLabel(self.t_Collation)
        self.l_RawData.setObjectName(u"l_RawData")

        self.gl_Collation.addWidget(self.l_RawData, 2, 0, 1, 4)

        self.lst_RawData = QListWidget(self.t_Collation)
        self.lst_RawData.setObjectName(u"lst_RawData")
        self.lst_RawData.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        self.gl_Collation.addWidget(self.lst_RawData, 3, 0, 1, 4)

        self.l_Summaries = QLabel(self.t_Collation)
        self.l_Summaries.setObjectName(u"l_Summaries")

        self.gl_Collation.addWidget(self.l_Summaries, 4, 0, 1, 4)

        self.tbl_Summaries = QTableWidget(self.t_Collation)
        if (self.tbl_Summaries.columnCount() < 3):
            self.tbl_Summaries.setColumnCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_Summaries.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tbl_Summaries.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tbl_Summaries.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.tbl_Summaries.setObjectName(u"tbl_Summaries")
        self.tbl_Summaries.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbl_Summaries.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbl_Summaries.horizontalHeader().setStretchLastSection(True)

        self.gl_Collation.addWidget(self.tbl_Summaries, 5, 0, 1, 4)

        self.pb_Collate = QPushButton(self.t_Collation)
        self.pb_Collate.setObjectName(u"pb_Collate")

        self.gl_Collation.addWidget(self.pb_Collate, 6, 0, 1, 1)

        self.s_CollationHorizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Collation.addItem(self.s_CollationHorizontal, 6, 1, 1, 1)

        self.pb_EditSheet = QPushButton(self.t_Collation)
        self.pb_EditSheet.setObjectName(u"pb_EditSheet")

        self.gl_Collation.addWidget(self.pb_EditSheet, 6, 2, 1, 1)

        self.pb_EditSample = QPushButton(self.t_Collation)
        self.pb_EditSample.setObjectName(u"pb_EditSample")

        self.gl_Collation.addWidget(self.pb_EditSample, 6, 3, 1, 1)

        self.tw_Main.addTab(self.t_Collation, "")
        MainWindow.setCentralWidget(self.tw_Main)
        self.mb_Main = QMenuBar(MainWindow)
        self.mb_Main.setObjectName(u"mb_Main")
        self.mb_Main.setGeometry(QRect(0, 0, 800, 24))
        MainWindow.setMenuBar(self.mb_Main)
        QWidget.setTabOrder(self.tbl_Files, self.pb_OpenDirectory)
        QWidget.setTabOrder(self.pb_OpenDirectory, self.pb_OpenCsv)
        QWidget.setTabOrder(self.pb_OpenCsv, self.pb_Configuration)
        QWidget.setTabOrder(self.pb_Configuration, self.cb_Instrument)
        QWidget.setTabOrder(self.cb_Instrument, self.cb_Experiment)
        QWidget.setTabOrder(self.cb_Experiment, self.pb_Run)

        self.retranslateUi(MainWindow)

        self.tw_Main.setCurrentIndex(0)
        self.sw_Configuration.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MechAnalyser", None))
        ___qtablewidgetitem = self.tbl_Files.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem1 = self.tbl_Files.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Input .csv", None));
        ___qtablewidgetitem2 = self.tbl_Files.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Output .xlsx", None));
#if QT_CONFIG(tooltip)
        self.pb_OpenDirectory.setToolTip(QCoreApplication.translate("MainWindow", u"Choose the directory containing the experiment output files", None))
#endif // QT_CONFIG(tooltip)
        self.pb_OpenDirectory.setText(QCoreApplication.translate("MainWindow", u"Open Directory...", None))
#if QT_CONFIG(tooltip)
        self.pb_OpenCsv.setToolTip(QCoreApplication.translate("MainWindow", u"Choose the experiment output files saved as .csv", None))
#endif // QT_CONFIG(tooltip)
        self.pb_OpenCsv.setText(QCoreApplication.translate("MainWindow", u"Open CSVs...", None))
        self.pb_Clear.setText(QCoreApplication.translate("MainWindow", u"Clear...", None))
#if QT_CONFIG(tooltip)
        self.pb_Configuration.setToolTip(QCoreApplication.translate("MainWindow", u"Configure the experiment analysis", None))
#endif // QT_CONFIG(tooltip)
        self.pb_Configuration.setText(QCoreApplication.translate("MainWindow", u"Configure...", None))
#if QT_CONFIG(tooltip)
        self.pb_SaveDirectory.setToolTip(QCoreApplication.translate("MainWindow", u"Choose the directory to which the processed Excel spreadsheets will be written", None))
#endif // QT_CONFIG(tooltip)
        self.pb_SaveDirectory.setText(QCoreApplication.translate("MainWindow", u"Save to...", None))
#if QT_CONFIG(tooltip)
        self.cb_All.setToolTip(QCoreApplication.translate("MainWindow", u"If checked, all output Excel file will be saved to this directory", None))
#endif // QT_CONFIG(tooltip)
        self.cb_All.setText(QCoreApplication.translate("MainWindow", u"All CSVs", None))
#if QT_CONFIG(tooltip)
        self.tb_SaveDirectory.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.tw_Main.setTabText(self.tw_Main.indexOf(self.t_Files), QCoreApplication.translate("MainWindow", u"Files", None))
        self.l_Instrument.setText(QCoreApplication.translate("MainWindow", u"Instrument:", None))
        self.l_Experiment.setText(QCoreApplication.translate("MainWindow", u"Experiment:", None))
#if QT_CONFIG(tooltip)
        self.pb_Run.setToolTip(QCoreApplication.translate("MainWindow", u"Process the experiment outputs and save the results to the Excel files", None))
#endif // QT_CONFIG(tooltip)
        self.pb_Run.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.tw_Main.setTabText(self.tw_Main.indexOf(self.t_Configuration), QCoreApplication.translate("MainWindow", u"Configuration", None))
        self.pb_Continue.setText(QCoreApplication.translate("MainWindow", u"Continue...", None))
        self.tw_Main.setTabText(self.tw_Main.indexOf(self.t_Output), QCoreApplication.translate("MainWindow", u"Output", None))
#if QT_CONFIG(tooltip)
        self.l_CollationFilename.setToolTip(QCoreApplication.translate("MainWindow", u"Name of the file to which the collated raw data and summaries are to be written", None))
#endif // QT_CONFIG(tooltip)
        self.l_CollationFilename.setText(QCoreApplication.translate("MainWindow", u"Filename", None))
#if QT_CONFIG(tooltip)
        self.le_CollationFilename.setToolTip(QCoreApplication.translate("MainWindow", u"Name of the file to which the collated raw data and summaries are to be written", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.l_RawData.setToolTip(QCoreApplication.translate("MainWindow", u"Select all columns within the raw dataset that will be included in the collated raw dataset", None))
#endif // QT_CONFIG(tooltip)
        self.l_RawData.setText(QCoreApplication.translate("MainWindow", u"Raw data", None))
#if QT_CONFIG(tooltip)
        self.l_Summaries.setToolTip(QCoreApplication.translate("MainWindow", u"Configure the collated summaries", None))
#endif // QT_CONFIG(tooltip)
        self.l_Summaries.setText(QCoreApplication.translate("MainWindow", u"Summaries", None))
        ___qtablewidgetitem3 = self.tbl_Summaries.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Filename", None));
        ___qtablewidgetitem4 = self.tbl_Summaries.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Sheet Name", None));
        ___qtablewidgetitem5 = self.tbl_Summaries.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Sample Name", None));
        self.pb_Collate.setText(QCoreApplication.translate("MainWindow", u"Collate...", None))
#if QT_CONFIG(tooltip)
        self.pb_EditSheet.setToolTip(QCoreApplication.translate("MainWindow", u"Change the sheet name of the selected samples", None))
#endif // QT_CONFIG(tooltip)
        self.pb_EditSheet.setText(QCoreApplication.translate("MainWindow", u"Edit sheet...", None))
#if QT_CONFIG(tooltip)
        self.pb_EditSample.setToolTip(QCoreApplication.translate("MainWindow", u"Change the name of the selected sample", None))
#endif // QT_CONFIG(tooltip)
        self.pb_EditSample.setText(QCoreApplication.translate("MainWindow", u"Edit sample...", None))
        self.tw_Main.setTabText(self.tw_Main.indexOf(self.t_Collation), QCoreApplication.translate("MainWindow", u"Collation", None))
    # retranslateUi

