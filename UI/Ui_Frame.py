# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Frame.ui'
##
## Created by: Qt User Interface Compiler version 5.15.11
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName(u"Frame")
        self.gridLayout = QGridLayout(Frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lcdNumber = QLCDNumber(Frame)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setFrameShape(QFrame.NoFrame)
        self.lcdNumber.setDigitCount(8)

        self.gridLayout.addWidget(self.lcdNumber, 0, 0, 1, 1)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        pass
    # retranslateUi


    ## custom add
    def setupLcdColor(self, color):
        palette = self.lcdNumber.palette()
        palette.setColor(palette.ColorRole.WindowText, color)
        self.lcdNumber.setPalette(palette)
