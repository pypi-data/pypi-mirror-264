# -*- coding: utf-8 -*-

# File generated according to DBore.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .....GUI.Tools.FloatEdit import FloatEdit
from .....GUI.Tools.HelpButton import HelpButton

from pyleecan.GUI.Resources import pyleecan_rc


class Ui_DBore(object):
    def setupUi(self, DBore):
        if not DBore.objectName():
            DBore.setObjectName(u"DBore")
        DBore.resize(820, 600)
        DBore.setMinimumSize(QSize(820, 600))
        icon = QIcon()
        icon.addFile(
            u":/images/images/icon/pyleecan_64.png", QSize(), QIcon.Normal, QIcon.Off
        )
        DBore.setWindowIcon(icon)
        self.main_layout = QVBoxLayout(DBore)
        self.main_layout.setObjectName(u"main_layout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.c_bore_type = QComboBox(DBore)
        self.c_bore_type.addItem("")
        self.c_bore_type.setObjectName(u"c_bore_type")

        self.horizontalLayout_2.addWidget(self.c_bore_type)

        self.b_help = HelpButton(DBore)
        self.b_help.setObjectName(u"b_help")
        self.b_help.setPixmap(QPixmap(u":/images/images/icon/help_16.png"))

        self.horizontalLayout_2.addWidget(self.b_help)

        self.in_alpha = QLabel(DBore)
        self.in_alpha.setObjectName(u"in_alpha")

        self.horizontalLayout_2.addWidget(self.in_alpha)

        self.lf_alpha = FloatEdit(DBore)
        self.lf_alpha.setObjectName(u"lf_alpha")
        self.lf_alpha.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.lf_alpha)

        self.c_alpha_unit = QComboBox(DBore)
        self.c_alpha_unit.addItem("")
        self.c_alpha_unit.addItem("")
        self.c_alpha_unit.setObjectName(u"c_alpha_unit")

        self.horizontalLayout_2.addWidget(self.c_alpha_unit)

        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.main_layout.addLayout(self.horizontalLayout_2)

        self.w_bore = QWidget(DBore)
        self.w_bore.setObjectName(u"w_bore")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_bore.sizePolicy().hasHeightForWidth())
        self.w_bore.setSizePolicy(sizePolicy)

        self.main_layout.addWidget(self.w_bore)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.b_plot = QPushButton(DBore)
        self.b_plot.setObjectName(u"b_plot")

        self.horizontalLayout.addWidget(self.b_plot)

        self.b_cancel = QPushButton(DBore)
        self.b_cancel.setObjectName(u"b_cancel")

        self.horizontalLayout.addWidget(self.b_cancel)

        self.b_ok = QPushButton(DBore)
        self.b_ok.setObjectName(u"b_ok")

        self.horizontalLayout.addWidget(self.b_ok)

        self.main_layout.addLayout(self.horizontalLayout)

        self.retranslateUi(DBore)

        QMetaObject.connectSlotsByName(DBore)

    # setupUi

    def retranslateUi(self, DBore):
        DBore.setWindowTitle(
            QCoreApplication.translate("DBore", u"Uneven bore shape setup", None)
        )
        self.c_bore_type.setItemText(
            0, QCoreApplication.translate("DBore", u"Bore Flower", None)
        )

        self.b_help.setText("")
        self.in_alpha.setText(QCoreApplication.translate("DBore", u"alpha :", None))
        self.c_alpha_unit.setItemText(
            0, QCoreApplication.translate("DBore", u"[rad]", None)
        )
        self.c_alpha_unit.setItemText(
            1, QCoreApplication.translate("DBore", u"[\u00b0]", None)
        )

        self.b_plot.setText(QCoreApplication.translate("DBore", u"Preview", None))
        self.b_cancel.setText(QCoreApplication.translate("DBore", u"Cancel", None))
        self.b_ok.setText(QCoreApplication.translate("DBore", u"Ok", None))

    # retranslateUi
