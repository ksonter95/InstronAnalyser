# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'failure.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QLabel,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Failure(object):
    def setupUi(self, w_Failure):
        if not w_Failure.objectName():
            w_Failure.setObjectName(u"w_Failure")
        self.gl_Failure = QGridLayout(w_Failure)
        self.gl_Failure.setObjectName(u"gl_Failure")
        self.l_Abort = QLabel(w_Failure)
        self.l_Abort.setObjectName(u"l_Abort")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_Abort.sizePolicy().hasHeightForWidth())
        self.l_Abort.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_Abort, 0, 0, 1, 1)

        self.sb_Abort = QDoubleSpinBox(w_Failure)
        self.sb_Abort.setObjectName(u"sb_Abort")
        self.sb_Abort.setDecimals(1)
        self.sb_Abort.setMaximum(100.000000000000000)

        self.gl_Failure.addWidget(self.sb_Abort, 0, 1, 1, 1)

        self.s_Horizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Failure.addItem(self.s_Horizontal, 0, 5, 5, 1)

        self.l_Toughness = QLabel(w_Failure)
        self.l_Toughness.setObjectName(u"l_Toughness")
        sizePolicy.setHeightForWidth(self.l_Toughness.sizePolicy().hasHeightForWidth())
        self.l_Toughness.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_Toughness, 1, 0, 1, 1)

        self.sb_Toughness = QDoubleSpinBox(w_Failure)
        self.sb_Toughness.setObjectName(u"sb_Toughness")
        self.sb_Toughness.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_Toughness, 1, 1, 1, 1)

        self.l_Stiffness = QLabel(w_Failure)
        self.l_Stiffness.setObjectName(u"l_Stiffness")
        sizePolicy.setHeightForWidth(self.l_Stiffness.sizePolicy().hasHeightForWidth())
        self.l_Stiffness.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_Stiffness, 2, 0, 1, 1)

        self.sb_Stiffness = QDoubleSpinBox(w_Failure)
        self.sb_Stiffness.setObjectName(u"sb_Stiffness")
        self.sb_Stiffness.setDecimals(1)
        self.sb_Stiffness.setMinimum(0.000000000000000)

        self.gl_Failure.addWidget(self.sb_Stiffness, 2, 1, 1, 1)

        self.l_Strain1 = QLabel(w_Failure)
        self.l_Strain1.setObjectName(u"l_Strain1")
        sizePolicy.setHeightForWidth(self.l_Strain1.sizePolicy().hasHeightForWidth())
        self.l_Strain1.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_Strain1, 3, 0, 1, 1)

        self.sb_Strain1 = QDoubleSpinBox(w_Failure)
        self.sb_Strain1.setObjectName(u"sb_Strain1")
        self.sb_Strain1.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_Strain1, 3, 1, 1, 1)

        self.l_EModulus = QLabel(w_Failure)
        self.l_EModulus.setObjectName(u"l_EModulus")
        sizePolicy.setHeightForWidth(self.l_EModulus.sizePolicy().hasHeightForWidth())
        self.l_EModulus.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_EModulus, 3, 2, 1, 1)

        self.sb_Strain2 = QDoubleSpinBox(w_Failure)
        self.sb_Strain2.setObjectName(u"sb_Strain2")
        self.sb_Strain2.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_Strain2, 3, 3, 1, 1)

        self.s_Vertical = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gl_Failure.addItem(self.s_Vertical, 4, 0, 1, 4)


        self.retranslateUi(w_Failure)

        QMetaObject.connectSlotsByName(w_Failure)
    # setupUi

    def retranslateUi(self, w_Failure):
#if QT_CONFIG(tooltip)
        self.l_Abort.setToolTip(QCoreApplication.translate("Failure", u"The strain at which the experiment aborts even if the sample has not yet failed", None))
#endif // QT_CONFIG(tooltip)
        self.l_Abort.setText(QCoreApplication.translate("Failure", u"Abort strain", None))
#if QT_CONFIG(tooltip)
        self.sb_Abort.setToolTip(QCoreApplication.translate("Failure", u"The strain at which the experiment aborts even if the sample has not yet failed", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Abort.setSuffix(QCoreApplication.translate("Failure", u"%", None))
#if QT_CONFIG(tooltip)
        self.l_Toughness.setToolTip(QCoreApplication.translate("Failure", u"The strain at which the toughness is calculated", None))
#endif // QT_CONFIG(tooltip)
        self.l_Toughness.setText(QCoreApplication.translate("Failure", u"Toughness strain", None))
#if QT_CONFIG(tooltip)
        self.sb_Toughness.setToolTip(QCoreApplication.translate("Failure", u"The strain at which the toughness is calculated", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Toughness.setSuffix(QCoreApplication.translate("Failure", u"%", None))
#if QT_CONFIG(tooltip)
        self.l_Stiffness.setToolTip(QCoreApplication.translate("Failure", u"The strain at which the stiffness is calculated", None))
#endif // QT_CONFIG(tooltip)
        self.l_Stiffness.setText(QCoreApplication.translate("Failure", u"Stiffness strain", None))
#if QT_CONFIG(tooltip)
        self.sb_Stiffness.setToolTip(QCoreApplication.translate("Failure", u"The strain at which the stiffness is calculated", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Stiffness.setSuffix(QCoreApplication.translate("Failure", u"%", None))
#if QT_CONFIG(tooltip)
        self.l_Strain1.setToolTip(QCoreApplication.translate("Failure", u"The strain range on the stress-strain curve over which the Young's modulus is calculated.  They are the \u03b5 values in the equation E = (\u03c32 - \u03c31) / (\u03b52 - \u03b51)", None))
#endif // QT_CONFIG(tooltip)
        self.l_Strain1.setText(QCoreApplication.translate("Failure", u"Young's modulus", None))
#if QT_CONFIG(tooltip)
        self.sb_Strain1.setToolTip(QCoreApplication.translate("Failure", u"The strain value which defines the first datapoint on the stress-strain curve used to calculate the Young's modulus.  It is \u03b51 in the equation E = (\u03c32 - \u03c31) / (\u03b52 - \u03b51)", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Strain1.setSuffix(QCoreApplication.translate("Failure", u"%", None))
        self.l_EModulus.setText(QCoreApplication.translate("Failure", u"to", None))
#if QT_CONFIG(tooltip)
        self.sb_Strain2.setToolTip(QCoreApplication.translate("Failure", u"The strain value which defines the second datapoint on the stress-strain curve used to calculate the Young's modulus.  It is \u03b52 in the equation E = (\u03c32 - \u03c31) / (\u03b52 - \u03b51)", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Strain2.setSuffix(QCoreApplication.translate("Failure", u"%", None))
        pass
    # retranslateUi

