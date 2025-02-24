# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QGridLayout,
    QLabel, QSizePolicy, QSpacerItem, QSpinBox,
    QWidget)

class Ui_w_Stepwise(object):
    def setupUi(self, w_Stepwise):
        if not w_Stepwise.objectName():
            w_Stepwise.setObjectName(u"w_Stepwise")
        w_Stepwise.resize(472, 157)
        self.gl_Stepwise = QGridLayout(w_Stepwise)
        self.gl_Stepwise.setObjectName(u"gl_Stepwise")
        self.l_RelaxationStrains = QLabel(w_Stepwise)
        self.l_RelaxationStrains.setObjectName(u"l_RelaxationStrains")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_RelaxationStrains.sizePolicy().hasHeightForWidth())
        self.l_RelaxationStrains.setSizePolicy(sizePolicy)

        self.gl_Stepwise.addWidget(self.l_RelaxationStrains, 0, 0, 1, 1)

        self.sb_RelaxationStrainsIntervals = QSpinBox(w_Stepwise)
        self.sb_RelaxationStrainsIntervals.setObjectName(u"sb_RelaxationStrainsIntervals")

        self.gl_Stepwise.addWidget(self.sb_RelaxationStrainsIntervals, 0, 2, 1, 1)

        self.l_RelaxationStrainsText = QLabel(w_Stepwise)
        self.l_RelaxationStrainsText.setObjectName(u"l_RelaxationStrainsText")
        sizePolicy.setHeightForWidth(self.l_RelaxationStrainsText.sizePolicy().hasHeightForWidth())
        self.l_RelaxationStrainsText.setSizePolicy(sizePolicy)

        self.gl_Stepwise.addWidget(self.l_RelaxationStrainsText, 0, 3, 1, 1)

        self.sb_RelaxationStrainsStart = QDoubleSpinBox(w_Stepwise)
        self.sb_RelaxationStrainsStart.setObjectName(u"sb_RelaxationStrainsStart")
        self.sb_RelaxationStrainsStart.setDecimals(1)

        self.gl_Stepwise.addWidget(self.sb_RelaxationStrainsStart, 0, 4, 1, 1)

        self.s_Horizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Stepwise.addItem(self.s_Horizontal, 0, 5, 4, 1)

        self.l_Epsilon = QLabel(w_Stepwise)
        self.l_Epsilon.setObjectName(u"l_Epsilon")
        sizePolicy.setHeightForWidth(self.l_Epsilon.sizePolicy().hasHeightForWidth())
        self.l_Epsilon.setSizePolicy(sizePolicy)

        self.gl_Stepwise.addWidget(self.l_Epsilon, 1, 0, 1, 1)

        self.sb_Epsilon = QDoubleSpinBox(w_Stepwise)
        self.sb_Epsilon.setObjectName(u"sb_Epsilon")
        self.sb_Epsilon.setMaximum(1.000000000000000)

        self.gl_Stepwise.addWidget(self.sb_Epsilon, 1, 2, 1, 1)

        self.l_RegressionPoints = QLabel(w_Stepwise)
        self.l_RegressionPoints.setObjectName(u"l_RegressionPoints")
        sizePolicy.setHeightForWidth(self.l_RegressionPoints.sizePolicy().hasHeightForWidth())
        self.l_RegressionPoints.setSizePolicy(sizePolicy)

        self.gl_Stepwise.addWidget(self.l_RegressionPoints, 2, 0, 1, 1)

        self.cb_RegressionPoints = QCheckBox(w_Stepwise)
        self.cb_RegressionPoints.setObjectName(u"cb_RegressionPoints")
        sizePolicy.setHeightForWidth(self.cb_RegressionPoints.sizePolicy().hasHeightForWidth())
        self.cb_RegressionPoints.setSizePolicy(sizePolicy)

        self.gl_Stepwise.addWidget(self.cb_RegressionPoints, 2, 1, 1, 1)

        self.sb_RegressionPoints = QSpinBox(w_Stepwise)
        self.sb_RegressionPoints.setObjectName(u"sb_RegressionPoints")
        self.sb_RegressionPoints.setMaximum(100000)

        self.gl_Stepwise.addWidget(self.sb_RegressionPoints, 2, 2, 1, 1)

        self.s_Vertical = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gl_Stepwise.addItem(self.s_Vertical, 3, 0, 1, 5)


        self.retranslateUi(w_Stepwise)

        QMetaObject.connectSlotsByName(w_Stepwise)
    # setupUi

    def retranslateUi(self, w_Stepwise):
#if QT_CONFIG(tooltip)
        self.l_RelaxationStrains.setToolTip(QCoreApplication.translate("w_Stepwise", u"The strains at which the sample has been configured to relax", None))
#endif // QT_CONFIG(tooltip)
        self.l_RelaxationStrains.setText(QCoreApplication.translate("w_Stepwise", u"Relaxation strains", None))
#if QT_CONFIG(tooltip)
        self.sb_RelaxationStrainsIntervals.setToolTip(QCoreApplication.translate("w_Stepwise", u"The number of intervals at which the sample has been configured to relax.  This in combination with the step size gives the relaxation strains.  For instance, if the step size is 5%, and the number of intervals is 6, then the experiment will relax the sample at 5%, 10%, 15%, 20%, 25%, 30%.", None))
#endif // QT_CONFIG(tooltip)
        self.l_RelaxationStrainsText.setText(QCoreApplication.translate("w_Stepwise", u"intervals, with step size", None))
#if QT_CONFIG(tooltip)
        self.sb_RelaxationStrainsStart.setToolTip(QCoreApplication.translate("w_Stepwise", u"The step between consecutive strains at which the sample has been configured to relax.  This in combination with the number of intervals gives the relaxation strains.  For instance, if the step size is 5%, and the number of intervals is 6, then the experiment will relax the sample at 5%, 10%, 15%, 20%, 25%, 30%.", None))
#endif // QT_CONFIG(tooltip)
        self.sb_RelaxationStrainsStart.setSuffix(QCoreApplication.translate("w_Stepwise", u"%", None))
#if QT_CONFIG(tooltip)
        self.l_Epsilon.setToolTip(QCoreApplication.translate("w_Stepwise", u"Allowable percentage tolerance on the strain for creating the dataset at the required relaxation strain", None))
#endif // QT_CONFIG(tooltip)
        self.l_Epsilon.setText(QCoreApplication.translate("w_Stepwise", u"Epsilon", None))
#if QT_CONFIG(tooltip)
        self.sb_Epsilon.setToolTip(QCoreApplication.translate("w_Stepwise", u"Allowable percentage tolerance on the strain for creating the dataset at the required relaxation strain", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Epsilon.setSuffix(QCoreApplication.translate("w_Stepwise", u"%", None))
#if QT_CONFIG(tooltip)
        self.l_RegressionPoints.setToolTip(QCoreApplication.translate("w_Stepwise", u"Number of data points to include in the regression analysis", None))
#endif // QT_CONFIG(tooltip)
        self.l_RegressionPoints.setText(QCoreApplication.translate("w_Stepwise", u"Regression points", None))
#if QT_CONFIG(tooltip)
        self.cb_RegressionPoints.setToolTip(QCoreApplication.translate("w_Stepwise", u"If unchecked, all datapoints will be used in the regression analysis", None))
#endif // QT_CONFIG(tooltip)
        self.cb_RegressionPoints.setText("")
#if QT_CONFIG(tooltip)
        self.sb_RegressionPoints.setToolTip(QCoreApplication.translate("w_Stepwise", u"Number of data points to include in the regression analysis", None))
#endif // QT_CONFIG(tooltip)
        pass
    # retranslateUi

