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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QGridLayout, QLabel, QRadioButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_w_Failure(object):
    def setupUi(self, w_Failure):
        if not w_Failure.objectName():
            w_Failure.setObjectName(u"w_Failure")
        w_Failure.resize(648, 238)
        self.gl_Failure = QGridLayout(w_Failure)
        self.gl_Failure.setObjectName(u"gl_Failure")
        self.l_Tare = QLabel(w_Failure)
        self.l_Tare.setObjectName(u"l_Tare")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_Tare.sizePolicy().hasHeightForWidth())
        self.l_Tare.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_Tare, 0, 0, 1, 1)

        self.sb_Tare = QDoubleSpinBox(w_Failure)
        self.sb_Tare.setObjectName(u"sb_Tare")
        self.sb_Tare.setDecimals(1)
        self.sb_Tare.setMaximum(10.000000000000000)

        self.gl_Failure.addWidget(self.sb_Tare, 0, 1, 1, 1)

        self.s_Horizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_Failure.addItem(self.s_Horizontal, 0, 6, 8, 1)

        self.l_Abort = QLabel(w_Failure)
        self.l_Abort.setObjectName(u"l_Abort")
        sizePolicy.setHeightForWidth(self.l_Abort.sizePolicy().hasHeightForWidth())
        self.l_Abort.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_Abort, 1, 0, 1, 1)

        self.sb_Abort = QDoubleSpinBox(w_Failure)
        self.sb_Abort.setObjectName(u"sb_Abort")
        self.sb_Abort.setDecimals(1)
        self.sb_Abort.setMaximum(100.000000000000000)

        self.gl_Failure.addWidget(self.sb_Abort, 1, 1, 1, 1)

        self.cb_Toughness = QCheckBox(w_Failure)
        self.cb_Toughness.setObjectName(u"cb_Toughness")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cb_Toughness.sizePolicy().hasHeightForWidth())
        self.cb_Toughness.setSizePolicy(sizePolicy1)

        self.gl_Failure.addWidget(self.cb_Toughness, 2, 0, 1, 1)

        self.sb_Toughness = QDoubleSpinBox(w_Failure)
        self.sb_Toughness.setObjectName(u"sb_Toughness")
        self.sb_Toughness.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_Toughness, 2, 1, 1, 1)

        self.l_EModulus = QLabel(w_Failure)
        self.l_EModulus.setObjectName(u"l_EModulus")
        sizePolicy.setHeightForWidth(self.l_EModulus.sizePolicy().hasHeightForWidth())
        self.l_EModulus.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_EModulus, 3, 0, 1, 1)

        self.rb_FixedRange = QRadioButton(w_Failure)
        self.rb_FixedRange.setObjectName(u"rb_FixedRange")

        self.gl_Failure.addWidget(self.rb_FixedRange, 4, 0, 1, 1)

        self.sb_Strain1 = QDoubleSpinBox(w_Failure)
        self.sb_Strain1.setObjectName(u"sb_Strain1")
        self.sb_Strain1.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_Strain1, 4, 1, 1, 1)

        self.l_To1 = QLabel(w_Failure)
        self.l_To1.setObjectName(u"l_To1")
        sizePolicy.setHeightForWidth(self.l_To1.sizePolicy().hasHeightForWidth())
        self.l_To1.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_To1, 4, 2, 1, 1)

        self.sb_Strain2 = QDoubleSpinBox(w_Failure)
        self.sb_Strain2.setObjectName(u"sb_Strain2")
        self.sb_Strain2.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_Strain2, 4, 3, 1, 1)

        self.rb_AnchorPoint = QRadioButton(w_Failure)
        self.rb_AnchorPoint.setObjectName(u"rb_AnchorPoint")

        self.gl_Failure.addWidget(self.rb_AnchorPoint, 5, 0, 1, 1)

        self.sb_StrainOffset = QDoubleSpinBox(w_Failure)
        self.sb_StrainOffset.setObjectName(u"sb_StrainOffset")
        self.sb_StrainOffset.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_StrainOffset, 5, 1, 1, 1)

        self.l_From = QLabel(w_Failure)
        self.l_From.setObjectName(u"l_From")
        sizePolicy.setHeightForWidth(self.l_From.sizePolicy().hasHeightForWidth())
        self.l_From.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_From, 5, 2, 1, 1)

        self.cbx_AnchorPoint = QComboBox(w_Failure)
        self.cbx_AnchorPoint.addItem("")
        self.cbx_AnchorPoint.addItem("")
        self.cbx_AnchorPoint.addItem("")
        self.cbx_AnchorPoint.addItem("")
        self.cbx_AnchorPoint.addItem("")
        self.cbx_AnchorPoint.addItem("")
        self.cbx_AnchorPoint.setObjectName(u"cbx_AnchorPoint")

        self.gl_Failure.addWidget(self.cbx_AnchorPoint, 5, 3, 1, 1)

        self.l_With1 = QLabel(w_Failure)
        self.l_With1.setObjectName(u"l_With1")
        sizePolicy.setHeightForWidth(self.l_With1.sizePolicy().hasHeightForWidth())
        self.l_With1.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_With1, 5, 4, 1, 1)

        self.sb_StrainRangeWidth = QDoubleSpinBox(w_Failure)
        self.sb_StrainRangeWidth.setObjectName(u"sb_StrainRangeWidth")
        self.sb_StrainRangeWidth.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_StrainRangeWidth, 5, 5, 1, 1)

        self.rb_FindRange = QRadioButton(w_Failure)
        self.rb_FindRange.setObjectName(u"rb_FindRange")

        self.gl_Failure.addWidget(self.rb_FindRange, 6, 0, 1, 1)

        self.sb_StrainMin = QDoubleSpinBox(w_Failure)
        self.sb_StrainMin.setObjectName(u"sb_StrainMin")
        self.sb_StrainMin.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_StrainMin, 6, 1, 1, 1)

        self.l_To2 = QLabel(w_Failure)
        self.l_To2.setObjectName(u"l_To2")
        sizePolicy.setHeightForWidth(self.l_To2.sizePolicy().hasHeightForWidth())
        self.l_To2.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_To2, 6, 2, 1, 1)

        self.sb_StrainMax = QDoubleSpinBox(w_Failure)
        self.sb_StrainMax.setObjectName(u"sb_StrainMax")
        self.sb_StrainMax.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_StrainMax, 6, 3, 1, 1)

        self.l_With2 = QLabel(w_Failure)
        self.l_With2.setObjectName(u"l_With2")
        sizePolicy.setHeightForWidth(self.l_With2.sizePolicy().hasHeightForWidth())
        self.l_With2.setSizePolicy(sizePolicy)

        self.gl_Failure.addWidget(self.l_With2, 6, 4, 1, 1)

        self.sb_StrainWindowWidth = QDoubleSpinBox(w_Failure)
        self.sb_StrainWindowWidth.setObjectName(u"sb_StrainWindowWidth")
        self.sb_StrainWindowWidth.setDecimals(1)

        self.gl_Failure.addWidget(self.sb_StrainWindowWidth, 6, 5, 1, 1)

        self.s_Vertical = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gl_Failure.addItem(self.s_Vertical, 7, 0, 1, 6)


        self.retranslateUi(w_Failure)

        QMetaObject.connectSlotsByName(w_Failure)
    # setupUi

    def retranslateUi(self, w_Failure):
#if QT_CONFIG(tooltip)
        self.l_Tare.setToolTip(QCoreApplication.translate("w_Failure", u"The force which will be used to tare the experiment.  All data points with force less than the tare force will be discarded, and all data points with force greater than the tare force will be offset accordingly", None))
#endif // QT_CONFIG(tooltip)
        self.l_Tare.setText(QCoreApplication.translate("w_Failure", u"Tare force", None))
#if QT_CONFIG(tooltip)
        self.sb_Tare.setToolTip(QCoreApplication.translate("w_Failure", u"The force which will be used to tare the experiment.  All data points with force less than the tare force will be discarded, and all data points with force greater than the tare force will be offset accordingly", None))
#endif // QT_CONFIG(tooltip)
        self.sb_Tare.setSuffix(QCoreApplication.translate("w_Failure", u"N", None))
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
        self.rb_AnchorPoint.setToolTip(QCoreApplication.translate("w_Failure", u"Anchor a point on the stress-strain curve over which the Young's modulus is calculated to a specific point on the curve.", None))
#endif // QT_CONFIG(tooltip)
        self.rb_AnchorPoint.setText(QCoreApplication.translate("w_Failure", u"Anchor point", None))
#if QT_CONFIG(tooltip)
        self.sb_StrainOffset.setToolTip(QCoreApplication.translate("w_Failure", u"The strain offset from the specific point on the stress-strain curve from/to which the Young's modulus will be calculated.  It, in combination with the anchor point, specifies \u03b51 in the equation E = (\u03c32 - \u03c31) / (\u03b52 - \u03b51).", None))
#endif // QT_CONFIG(tooltip)
        self.sb_StrainOffset.setSuffix(QCoreApplication.translate("w_Failure", u"%", None))
        self.l_From.setText(QCoreApplication.translate("w_Failure", u"from", None))
        self.cbx_AnchorPoint.setItemText(0, QCoreApplication.translate("w_Failure", u"Start Strain", None))
        self.cbx_AnchorPoint.setItemText(1, QCoreApplication.translate("w_Failure", u"Toe Strain", None))
        self.cbx_AnchorPoint.setItemText(2, QCoreApplication.translate("w_Failure", u"Yield Strain", None))
        self.cbx_AnchorPoint.setItemText(3, QCoreApplication.translate("w_Failure", u"Ultimate Strain", None))
        self.cbx_AnchorPoint.setItemText(4, QCoreApplication.translate("w_Failure", u"Failure Strain", None))
        self.cbx_AnchorPoint.setItemText(5, QCoreApplication.translate("w_Failure", u"End Strain", None))

#if QT_CONFIG(tooltip)
        self.cbx_AnchorPoint.setToolTip(QCoreApplication.translate("w_Failure", u"The point used to anchor the strain range over which the Young's modulus is to be calculated", None))
#endif // QT_CONFIG(tooltip)
        self.l_With1.setText(QCoreApplication.translate("w_Failure", u"with width", None))
#if QT_CONFIG(tooltip)
        self.sb_StrainRangeWidth.setToolTip(QCoreApplication.translate("w_Failure", u"The width of the range on the stress-strain curve over which the Young's modulus will be calculated.  It, in combination with the strain offset and anchor point, specifies \u03b52 in the equation E = (\u03c32 - \u03c31) / (\u03b52 - \u03b51).", None))
#endif // QT_CONFIG(tooltip)
        self.sb_StrainRangeWidth.setSuffix(QCoreApplication.translate("w_Failure", u"%", None))
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
        self.l_With2.setText(QCoreApplication.translate("w_Failure", u"with width", None))
#if QT_CONFIG(tooltip)
        self.sb_StrainWindowWidth.setToolTip(QCoreApplication.translate("w_Failure", u"The width of the strain window which will be used to find the best approximation of the linear region of the stress-strain curve for all possible regions between the minimum and maximum strains.", None))
#endif // QT_CONFIG(tooltip)
        self.sb_StrainWindowWidth.setSuffix(QCoreApplication.translate("w_Failure", u"%", None))
        pass
    # retranslateUi

