# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Works\DesktopClock\UI\Frame.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

# 窗口绘制
class Ui_Frame(object):
    def setupUi(self, Frame, color):
        Frame.setObjectName("Frame")
        self.gridlayout = QtWidgets.QGridLayout(Frame)
        self.gridlayout.setObjectName("gridlayout")
        self.lcdNumber = QtWidgets.QLCDNumber(Frame)

        palette = self.lcdNumber.palette()
        palette.setColor(palette.ColorRole(), color)
        self.lcdNumber.setPalette(palette)
        self.lcdNumber.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.setObjectName("lcdNumber")
        self.gridlayout.addWidget(self.lcdNumber, 0, 0, 1, 1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def setupLcdColor(self, color):
        palette = self.lcdNumber.palette()
        palette.setColor(palette.ColorRole(), color)
        self.lcdNumber.setPalette(palette)

    def retranslateUi(self, Frame):
        pass

