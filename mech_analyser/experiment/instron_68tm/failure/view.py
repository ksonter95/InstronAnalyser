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
    QLabel, QRadioButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_w_Failure(object):
    def setupUi(self, w_Failure):
        if not w_Failure.objectName():
            w_Failure.setObjectName(u"w_Failure")
        w_Failure.resize(648, 238)
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

        self.gl_Failure.addItem(self.s_Horizontal, 0, 6, 6, 1)

        self.cb_Toughness = QCheckBox(w_Failure)
        self.cb_Toughness.setObjectName(u"cb_Toughness")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cb_Toughness.sizePolicy().hasHeightForWidth())
        self.cb_Toughness.setSizePolicy(sizePolicy1)

        self.gl_Failure.addWidget(self.cb_Toughness, 1, 0, 1, 1)

        self.sb_Toughness = QDoubleSpinBox(w_Failure)
        self.sb_Toughness.setObjectName(u"sb_Toughness")
        self.sb_Toughness.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_Toughness, 1, 1, 1, 1)

        self.l_EModulus = QLabel(w_Failure)
        self.l_EModulus.setObjectName(u"l_EModulus")
        sizePolicy.setHeightForWidth(self.l_EModulus.sizePolicy().hasHeightForWidth())
        self.l_EModulus.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_EModulus, 2, 0, 1, 1)

        self.rb_FixedRange = QRadioButton(w_Failure)
        self.rb_FixedRange.setObjectName(u"rb_FixedRange")

        self.gl_Failure.addWidget(self.rb_FixedRange, 3, 0, 1, 1)

        self.sb_Strain1 = QDoubleSpinBox(w_Failure)
        self.sb_Strain1.setObjectName(u"sb_Strain1")
        self.sb_Strain1.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_Strain1, 3, 1, 1, 1)

        self.l_To1 = QLabel(w_Failure)
        self.l_To1.setObjectName(u"l_To1")
        sizePolicy.setHeightForWidth(self.l_To1.sizePolicy().hasHeightForWidth())
        self.l_To1.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_To1, 3, 2, 1, 1)

        self.sb_Strain2 = QDoubleSpinBox(w_Failure)
        self.sb_Strain2.setObjectName(u"sb_Strain2")
        self.sb_Strain2.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_Strain2, 3, 3, 1, 1)

        self.rb_FindRange = QRadioButton(w_Failure)
        self.rb_FindRange.setObjectName(u"rb_FindRange")

        self.gl_Failure.addWidget(self.rb_FindRange, 4, 0, 1, 1)

        self.sb_StrainMin = QDoubleSpinBox(w_Failure)
        self.sb_StrainMin.setObjectName(u"sb_StrainMin")
        self.sb_StrainMin.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_StrainMin, 4, 1, 1, 1)

        self.l_To2 = QLabel(w_Failure)
        self.l_To2.setObjectName(u"l_To2")
        sizePolicy.setHeightForWidth(self.l_To2.sizePolicy().hasHeightForWidth())
        self.l_To2.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_To2, 4, 2, 1, 1)

        self.sb_StrainMax = QDoubleSpinBox(w_Failure)
        self.sb_StrainMax.setObjectName(u"sb_StrainMax")
        self.sb_StrainMax.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_StrainMax, 4, 3, 1, 1)

        self.l_With = QLabel(w_Failure)
        self.l_With.setObjectName(u"l_With")
        sizePolicy.setHeightForWidth(self.l_With.sizePolicy().hasHeightForWidth())
        self.l_With.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_With, 4, 4, 1, 1)

        self.sb_StrainWindowWidth = QDoubleSpinBox(w_Failure)
        self.sb_StrainWindowWidth.setObjectName(u"sb_StrainWindowWidth")
        self.sb_StrainWindowWidth.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_StrainWindowWidth, 4, 5, 1, 1)

        self.s_Vertical = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gl_Failure.addItem(self.s_Vertical, 5, 0, 1, 6)


        self.retranslateUi(w_Failure)

        QMetaObject.connectSlotsByName(w_Failure)
    # setupUi

    def retranslateUi(self, w_Failure):
#if QT_CONFIG(tooltip)
        self.l_Abort.setToolTip(QCoreApplication.translate("w_Failure", u"The strain at which the experiment aborts even if the sample has not yet failed", None))
#endif // QT_CONFIG(tooltip)
        self.l_Abort.setText(QCoreApplication.translate("w_Failure", u"Abort strain", None))
#if QT_CONFIG(tooltip)
        self.sb_Abort.setToolTip(QCoreApplication.translate("w_Failure", u"The strain at which the experiment aborts even if the sample has not yet failed", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Abort.setSuffix(QCoreApplication.translate("w_Failure", u"%", None))
#if QT_CONFIG(tooltip)
        self.cb_Toughness.setToolTip(QCoreApplication.translate("w_Failure", u"If unchecked, the toughness will be calculated at the failure or abort strain.  Check the box if it is desirable to have the toughness calculated at a fixed strain", None))
#endif // QT_CONFIG(tooltip)
        self.cb_Toughness.setText(QCoreApplication.translate("w_Failure", u"Toughness strain", None))
#if QT_CONFIG(tooltip)
        self.sb_Toughness.setToolTip(QCoreApplication.translate("w_Failure", u"The strain at which the toughness is calculated", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Toughness.setSuffix(QCoreApplication.translate("w_Failure", u"%", None))
#if QT_CONFIG(tooltip)
        self.l_EModulus.setToolTip(QCoreApplication.translate("w_Failure", u"The parameters to define the strain range on the stress-strain curve over which the Young's modulus is calculated.", None))
#endif // QT_CONFIG(tooltip)
        self.l_EModulus.setText(QCoreApplication.translate("w_Failure", u"Young's modulus", None))
#if QT_CONFIG(tooltip)
        self.rb_FixedRange.setToolTip(QCoreApplication.translate("w_Failure", u"Use the fixed strain range on the stress-strain curve over which the Young's modulus is calculated.", None))
#endif // QT_CONFIG(tooltip)
        self.rb_FixedRange.setText(QCoreApplication.translate("w_Failure", u"Use fixed range", None))
#if QT_CONFIG(tooltip)
        self.sb_Strain1.setToolTip(QCoreApplication.translate("w_Failure", u"The strain value which defines the first datapoint on the stress-strain curve used to calculate the Young's modulus.  It is \u03b51 in the equation E = (\u03c32 - \u03c31) / (\u03b52 - \u03b51)", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Strain1.setSuffix(QCoreApplication.translate("w_Failure", u"%", None))
        self.l_To1.setText(QCoreApplication.translate("w_Failure", u"to", None))
#if QT_CONFIG(tooltip)
        self.sb_Strain2.setToolTip(QCoreApplication.translate("w_Failure", u"The strain value which defines the second datapoint on the stress-strain curve used to calculate the Young's modulus.  It is \u03b52 in the equation E = (\u03c32 - \u03c31) / (\u03b52 - \u03b51)", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Strain2.setSuffix(QCoreApplication.translate("w_Failure", u"%", None))
#if QT_CONFIG(tooltip)
        self.rb_FindRange.setToolTip(QCoreApplication.translate("w_Failure", u"Automatically find the strain range over which the stress-strain curve is most linear and use this range to calculate the Young's modulus.", None))
#endif // QT_CONFIG(tooltip)
        self.rb_FindRange.setText(QCoreApplication.translate("w_Failure", u"Find linear range", None))
#if QT_CONFIG(tooltip)
        self.sb_StrainMin.setToolTip(QCoreApplication.translate("w_Failure", u"The strain value which defines the minimum strain that can be used to find the best approximation of the linear region of the stress-strain curve.", None))
#endif // QT_CONFIG(tooltip)
        self.sb_StrainMin.setSuffix(QCoreApplication.translate("w_Failure", u"%", None))
        self.l_To2.setText(QCoreApplication.translate("w_Failure", u"to", None))
#if QT_CONFIG(tooltip)
        self.sb_StrainMax.setToolTip(QCoreApplication.translate("w_Failure", u"The strain value which defines the maximum strain that can be used to find the best approximation of the linear region of the stress-strain curve.", None))
#endif // QT_CONFIG(tooltip)
        self.sb_StrainMax.setSuffix(QCoreApplication.translate("w_Failure", u"%", None))
        self.l_With.setText(QCoreApplication.translate("w_Failure", u"with width", None))
#if QT_CONFIG(tooltip)
        self.sb_StrainWindowWidth.setToolTip(QCoreApplication.translate("w_Failure", u"The width of the strain window which will be used to find the best approximation of the linear region of the stress-strain curve for all possible regions between the minimum and maximum strains.", None))
#endif // QT_CONFIG(tooltip)
        self.sb_StrainWindowWidth.setSuffix(QCoreApplication.translate("w_Failure", u"%", None))
        pass
    # retranslateUi

