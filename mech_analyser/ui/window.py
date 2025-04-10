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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QHeaderView, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextBrowser,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.a_OpenDirectory = QAction(MainWindow)
        self.a_OpenDirectory.setObjectName(u"a_OpenDirectory")
        self.a_OpenCsvs = QAction(MainWindow)
        self.a_OpenCsvs.setObjectName(u"a_OpenCsvs")
        self.a_Documentation = QAction(MainWindow)
        self.a_Documentation.setObjectName(u"a_Documentation")
        self.tw_Main = QTabWidget(MainWindow)
        self.tw_Main.setObjectName(u"tw_Main")
        self.t_Files = QWidget()
        self.t_Files.setObjectName(u"t_Files")
        self.gl_Files = QGridLayout(self.t_Files)
        self.gl_Files.setObjectName(u"gl_Files")
        self.pb_SaveAnalysis = QPushButton(self.t_Files)
        self.pb_SaveAnalysis.setObjectName(u"pb_SaveAnalysis")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_SaveAnalysis.sizePolicy().hasHeightForWidth())
        self.pb_SaveAnalysis.setSizePolicy(sizePolicy)

        self.gl_Files.addWidget(self.pb_SaveAnalysis, 0, 0, 1, 1)

        self.tb_SaveAnalysis = QTextBrowser(self.t_Files)
        self.tb_SaveAnalysis.setObjectName(u"tb_SaveAnalysis")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tb_SaveAnalysis.sizePolicy().hasHeightForWidth())
        self.tb_SaveAnalysis.setSizePolicy(sizePolicy1)

        self.gl_Files.addWidget(self.tb_SaveAnalysis, 0, 1, 1, 4)

        self.pb_SaveCollation = QPushButton(self.t_Files)
        self.pb_SaveCollation.setObjectName(u"pb_SaveCollation")
        sizePolicy.setHeightForWidth(self.pb_SaveCollation.sizePolicy().hasHeightForWidth())
        self.pb_SaveCollation.setSizePolicy(sizePolicy)

        self.gl_Files.addWidget(self.pb_SaveCollation, 1, 0, 1, 1)

        self.tb_SaveCollation = QTextBrowser(self.t_Files)
        self.tb_SaveCollation.setObjectName(u"tb_SaveCollation")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tb_SaveCollation.sizePolicy().hasHeightForWidth())
        self.tb_SaveCollation.setSizePolicy(sizePolicy2)

        self.gl_Files.addWidget(self.tb_SaveCollation, 1, 1, 1, 4)

        self.tbl_Files = QTableWidget(self.t_Files)
        if (self.tbl_Files.columnCount() < 4):
            self.tbl_Files.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_Files.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_Files.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_Files.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_Files.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tbl_Files.setObjectName(u"tbl_Files")
        self.tbl_Files.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tbl_Files.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbl_Files.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbl_Files.setRowCount(0)
        self.tbl_Files.setColumnCount(4)
        self.tbl_Files.horizontalHeader().setVisible(True)
        self.tbl_Files.horizontalHeader().setStretchLastSection(True)

        self.gl_Files.addWidget(self.tbl_Files, 2, 0, 1, 5)

        self.pb_Clear = QPushButton(self.t_Files)
        self.pb_Clear.setObjectName(u"pb_Clear")

        self.gl_Files.addWidget(self.pb_Clear, 3, 0, 1, 1)

        self.s_FilesHorizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Files.addItem(self.s_FilesHorizontal, 3, 1, 1, 1)

        self.pb_EditOutput = QPushButton(self.t_Files)
        self.pb_EditOutput.setObjectName(u"pb_EditOutput")
        sizePolicy.setHeightForWidth(self.pb_EditOutput.sizePolicy().hasHeightForWidth())
        self.pb_EditOutput.setSizePolicy(sizePolicy)

        self.gl_Files.addWidget(self.pb_EditOutput, 3, 2, 1, 1)

        self.pb_EditGroup = QPushButton(self.t_Files)
        self.pb_EditGroup.setObjectName(u"pb_EditGroup")
        sizePolicy.setHeightForWidth(self.pb_EditGroup.sizePolicy().hasHeightForWidth())
        self.pb_EditGroup.setSizePolicy(sizePolicy)

        self.gl_Files.addWidget(self.pb_EditGroup, 3, 3, 1, 1)

        self.pb_EditSample = QPushButton(self.t_Files)
        self.pb_EditSample.setObjectName(u"pb_EditSample")
        sizePolicy.setHeightForWidth(self.pb_EditSample.sizePolicy().hasHeightForWidth())
        self.pb_EditSample.setSizePolicy(sizePolicy)

        self.gl_Files.addWidget(self.pb_EditSample, 3, 4, 1, 1)

        self.tw_Main.addTab(self.t_Files, "")
        self.t_Configuration = QWidget()
        self.t_Configuration.setObjectName(u"t_Configuration")
        self.gl_Configuration = QGridLayout(self.t_Configuration)
        self.gl_Configuration.setObjectName(u"gl_Configuration")
        self.l_Instrument = QLabel(self.t_Configuration)
        self.l_Instrument.setObjectName(u"l_Instrument")
        sizePolicy.setHeightForWidth(self.l_Instrument.sizePolicy().hasHeightForWidth())
        self.l_Instrument.setSizePolicy(sizePolicy)

        self.gl_Configuration.addWidget(self.l_Instrument, 0, 0, 1, 1)

        self.cb_Instrument = QComboBox(self.t_Configuration)
        self.cb_Instrument.setObjectName(u"cb_Instrument")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cb_Instrument.sizePolicy().hasHeightForWidth())
        self.cb_Instrument.setSizePolicy(sizePolicy3)

        self.gl_Configuration.addWidget(self.cb_Instrument, 0, 1, 1, 1)

        self.l_Experiment = QLabel(self.t_Configuration)
        self.l_Experiment.setObjectName(u"l_Experiment")
        sizePolicy.setHeightForWidth(self.l_Experiment.sizePolicy().hasHeightForWidth())
        self.l_Experiment.setSizePolicy(sizePolicy)

        self.gl_Configuration.addWidget(self.l_Experiment, 0, 2, 1, 1)

        self.cb_Experiment = QComboBox(self.t_Configuration)
        self.cb_Experiment.setObjectName(u"cb_Experiment")
        sizePolicy3.setHeightForWidth(self.cb_Experiment.sizePolicy().hasHeightForWidth())
        self.cb_Experiment.setSizePolicy(sizePolicy3)

        self.gl_Configuration.addWidget(self.cb_Experiment, 0, 3, 1, 1)

        self.s_MainHorizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Configuration.addItem(self.s_MainHorizontal, 0, 4, 1, 1)

        self.sw_Configuration = QStackedWidget(self.t_Configuration)
        self.sw_Configuration.setObjectName(u"sw_Configuration")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.sw_Configuration.sizePolicy().hasHeightForWidth())
        self.sw_Configuration.setSizePolicy(sizePolicy4)

        self.gl_Configuration.addWidget(self.sw_Configuration, 1, 0, 1, 5)

        self.l_CollatedRawDataColumns = QLabel(self.t_Configuration)
        self.l_CollatedRawDataColumns.setObjectName(u"l_CollatedRawDataColumns")

        self.gl_Configuration.addWidget(self.l_CollatedRawDataColumns, 2, 0, 1, 5)

        self.lst_CollatedRawDataColumns = QListWidget(self.t_Configuration)
        self.lst_CollatedRawDataColumns.setObjectName(u"lst_CollatedRawDataColumns")
        self.lst_CollatedRawDataColumns.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        self.gl_Configuration.addWidget(self.lst_CollatedRawDataColumns, 3, 0, 1, 5)

        self.tw_Main.addTab(self.t_Configuration, "")
        self.t_Output = QWidget()
        self.t_Output.setObjectName(u"t_Output")
        self.gl_Output = QGridLayout(self.t_Output)
        self.gl_Output.setObjectName(u"gl_Output")
        self.tree_Output = QTreeWidget(self.t_Output)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_Output.setHeaderItem(__qtreewidgetitem)
        self.tree_Output.setObjectName(u"tree_Output")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.tree_Output.sizePolicy().hasHeightForWidth())
        self.tree_Output.setSizePolicy(sizePolicy5)
        self.tree_Output.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree_Output.setColumnCount(1)
        self.tree_Output.header().setVisible(False)

        self.gl_Output.addWidget(self.tree_Output, 0, 0, 1, 3)

        self.sw_Output = QStackedWidget(self.t_Output)
        self.sw_Output.setObjectName(u"sw_Output")
        sizePolicy4.setHeightForWidth(self.sw_Output.sizePolicy().hasHeightForWidth())
        self.sw_Output.setSizePolicy(sizePolicy4)

        self.gl_Output.addWidget(self.sw_Output, 0, 3, 2, 1)

        self.pgb_Output = QProgressBar(self.t_Output)
        self.pgb_Output.setObjectName(u"pgb_Output")
        self.pgb_Output.setValue(0)

        self.gl_Output.addWidget(self.pgb_Output, 1, 0, 1, 1)

        self.pb_Cancel = QPushButton(self.t_Output)
        self.pb_Cancel.setObjectName(u"pb_Cancel")

        self.gl_Output.addWidget(self.pb_Cancel, 1, 1, 1, 1)

        self.pb_Run = QPushButton(self.t_Output)
        self.pb_Run.setObjectName(u"pb_Run")

        self.gl_Output.addWidget(self.pb_Run, 1, 2, 1, 1)

        self.tw_Main.addTab(self.t_Output, "")
        MainWindow.setCentralWidget(self.tw_Main)
        self.mb_Main = QMenuBar(MainWindow)
        self.mb_Main.setObjectName(u"mb_Main")
        self.mb_Main.setGeometry(QRect(0, 0, 800, 24))
        self.m_File = QMenu(self.mb_Main)
        self.m_File.setObjectName(u"m_File")
        self.m_Help = QMenu(self.mb_Main)
        self.m_Help.setObjectName(u"m_Help")
        MainWindow.setMenuBar(self.mb_Main)
        QWidget.setTabOrder(self.tbl_Files, self.cb_Instrument)
        QWidget.setTabOrder(self.cb_Instrument, self.cb_Experiment)

        self.mb_Main.addAction(self.m_File.menuAction())
        self.mb_Main.addAction(self.m_Help.menuAction())
        self.m_File.addAction(self.a_OpenDirectory)
        self.m_File.addAction(self.a_OpenCsvs)
        self.m_Help.addAction(self.a_Documentation)

        self.retranslateUi(MainWindow)

        self.tw_Main.setCurrentIndex(0)
        self.sw_Configuration.setCurrentIndex(-1)
        self.sw_Output.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MechAnalyser", None))
        self.a_OpenDirectory.setText(QCoreApplication.translate("MainWindow", u"Open directory...", None))
        self.a_OpenCsvs.setText(QCoreApplication.translate("MainWindow", u"Open CSVs...", None))
        self.a_Documentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
#if QT_CONFIG(tooltip)
        self.pb_SaveAnalysis.setToolTip(QCoreApplication.translate("MainWindow", u"Select the directory to which all analysis outputs will be saved.  By default, the analysis corresponding to the input CSVs will be saved in the same directory as the CSVs.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_SaveAnalysis.setText(QCoreApplication.translate("MainWindow", u"Save analysis to...", None))
#if QT_CONFIG(tooltip)
        self.tb_SaveAnalysis.setToolTip(QCoreApplication.translate("MainWindow", u"Directory to which all analysis outputs will be saved.  If it is blank, the analysis corresponding to the input CSVs will be saved in the same directory as the CSVs.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pb_SaveCollation.setToolTip(QCoreApplication.translate("MainWindow", u"Select the file to which the collated raw data and summaries will be saved.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_SaveCollation.setText(QCoreApplication.translate("MainWindow", u"Save collation to...", None))
#if QT_CONFIG(tooltip)
        self.tb_SaveCollation.setToolTip(QCoreApplication.translate("MainWindow", u"File to which the collated raw data and summaries will be saved.", None))
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem = self.tbl_Files.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Input .csv", None));
        ___qtablewidgetitem1 = self.tbl_Files.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Output .xlsx", None));
        ___qtablewidgetitem2 = self.tbl_Files.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Group name", None));
        ___qtablewidgetitem3 = self.tbl_Files.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Sample name", None));
        self.pb_Clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
#if QT_CONFIG(tooltip)
        self.pb_EditOutput.setToolTip(QCoreApplication.translate("MainWindow", u"Edit the output filename of the Excel file to which the analysis will be written.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_EditOutput.setText(QCoreApplication.translate("MainWindow", u"Edit output...", None))
#if QT_CONFIG(tooltip)
        self.pb_EditGroup.setToolTip(QCoreApplication.translate("MainWindow", u"Edit the group to which the sample belongs.  The summaries of all samples in the same group will be collated into the same sheet within the collated Excel spreadsheet.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_EditGroup.setText(QCoreApplication.translate("MainWindow", u"Edit group...", None))
#if QT_CONFIG(tooltip)
        self.pb_EditSample.setToolTip(QCoreApplication.translate("MainWindow", u"Edit the name of the sample.  If multiple samples are selected, then the given sample name will be applied to each with a numerical suffix to uniquely identify each.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_EditSample.setText(QCoreApplication.translate("MainWindow", u"Edit sample...", None))
        self.tw_Main.setTabText(self.tw_Main.indexOf(self.t_Files), QCoreApplication.translate("MainWindow", u"Files", None))
        self.l_Instrument.setText(QCoreApplication.translate("MainWindow", u"Instrument:", None))
        self.l_Experiment.setText(QCoreApplication.translate("MainWindow", u"Experiment:", None))
#if QT_CONFIG(tooltip)
        self.l_CollatedRawDataColumns.setToolTip(QCoreApplication.translate("MainWindow", u"Select all columns within the raw dataset that will be included in the collated raw dataset", None))
#endif // QT_CONFIG(tooltip)
        self.l_CollatedRawDataColumns.setText(QCoreApplication.translate("MainWindow", u"Collation", None))
#if QT_CONFIG(tooltip)
        self.lst_CollatedRawDataColumns.setToolTip(QCoreApplication.translate("MainWindow", u"Select all columns within the raw dataset that will be included in the collated raw dataset", None))
#endif // QT_CONFIG(tooltip)
        self.tw_Main.setTabText(self.tw_Main.indexOf(self.t_Configuration), QCoreApplication.translate("MainWindow", u"Configuration", None))
#if QT_CONFIG(tooltip)
        self.pb_Cancel.setToolTip(QCoreApplication.translate("MainWindow", u"Cancel the running analysis and collation.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_Cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
#if QT_CONFIG(tooltip)
        self.pb_Run.setToolTip(QCoreApplication.translate("MainWindow", u"Run the analysis on all samples and collate the raw data and summaries of each.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_Run.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.tw_Main.setTabText(self.tw_Main.indexOf(self.t_Output), QCoreApplication.translate("MainWindow", u"Output", None))
        self.m_File.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.m_Help.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

