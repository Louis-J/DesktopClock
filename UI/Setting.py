import sys
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QDialog, QColorDialog
from PyQt5.QtGui import QIcon, QColor

class Setting:
    settingDefault = {
        'X' : 1320,
        'Y' : 850,
        'W' : 600,
        'H' : 300,
        'TP' : 0.5,
        'CL' : QColor(Qt.darkCyan).rgb(),
        'FM' : 'hh:mm'
    }
    settingMinMax  = {
        'X' : [0, 9999],
        'Y' : [0, 9999],
        'W' : [0, 9999],
        'H' : [0, 9999],
        'TP' : [0.0, 1.0],
        'CL' : [QColor(0,0,0).rgb(), QColor(255,255,255).rgb()],
        'FM' : ['hh:mm:ss', 'hh:mm']
    }

    def SettingSave(self):
        # print('SettingSave')
        try:
            with open('setting.json', 'w', encoding = 'utf8') as file:
                setting = dict()
                setting['X'] = self.X
                setting['Y'] = self.Y
                setting['W'] = self.W
                setting['H'] = self.H
                setting['TP'] = self.TP
                setting['CL'] = self.CL
                setting['FM'] = self.FM
                json.dump(setting, file)
                # print(setting)
        except Exception as identifier:
            print(identifier)
            pass
        
    def SettingLoadOne(self, setting, name, continued):
        if continued:
            if name not in setting or type(setting[name]) != type(self.settingDefault[name]) or setting[name] < self.settingMinMax[name][0] or setting[name] > self.settingMinMax[name][1]:
                print('%s load bad!' % name)
                return self.settingDefault[name]
            else:
                return setting[name]
        else:
            if name not in setting or type(setting[name]) != type(self.settingDefault[name]) or setting[name] not in self.settingMinMax[name]:
                print('%s load bad!' % name)
                return self.settingDefault[name]
            else:
                return setting[name]

    def SettingLoad(self):
        print('SettingLoad')
        try:
            with open('setting.json', 'r', encoding = 'utf8') as file:
                setting = json.loads(file.read())
                self.X = self.SettingLoadOne(setting, 'X', True)
                self.Y = self.SettingLoadOne(setting, 'Y', True)
                self.W = self.SettingLoadOne(setting, 'W', True)
                self.H = self.SettingLoadOne(setting, 'H', True)
                self.TP = self.SettingLoadOne(setting, 'TP', True)
                self.CL = self.SettingLoadOne(setting, 'CL', True)
                self.FM = self.SettingLoadOne(setting, 'FM', False)
                print(setting)
        except Exception as identifier:
            print('setting.json error!')
            print(identifier)
            self.X = self.settingDefault['X']
            self.Y = self.settingDefault['Y']
            self.W = self.settingDefault['W']
            self.H = self.settingDefault['H']
            self.TP = self.settingDefault['TP']
            self.CL = self.settingDefault['CL']
            self.FM = self.settingDefault['FM']

    def SettingDialog(self):
        from PyQt5.QtWidgets import (QDialog, QSpinBox, QComboBox, QDialogButtonBox, QFormLayout, QColorDialog, QPushButton, QSizePolicy)

        dialog = self.dialog = QDialog()
        dialog.setWindowTitle('设置')
        if hasattr(sys, "_MEIPASS"):
            dialog.setWindowIcon(QIcon(sys._MEIPASS + r'/Icon.ico'))
        else:
            dialog.setWindowIcon(QIcon(r'./Icon.ico'))

        boxX = QSpinBox(dialog)
        boxX.setRange(-100000, 100000)
        boxX.setValue(self.X)
        boxY = QSpinBox(dialog)
        boxY.setRange(-100000, 100000)
        boxY.setValue(self.Y)
        boxW = QSpinBox(dialog)
        boxW.setRange(0, 100000)
        boxW.setValue(self.W)
        boxH = QSpinBox(dialog)
        boxH.setRange(0, 100000)
        boxH.setValue(self.H)
        
        boxTP = QSpinBox(dialog)
        boxTP.setRange(0, 100)
        boxTP.setValue(self.TP*100)

        self.buttonColorVal = QColor(self.CL)
        self.buttonColor = QPushButton(parent = dialog)
        self.buttonColor.setStyleSheet('QWidget {background-color:%s}' % self.buttonColorVal.name())
        def ChangeCol():
            qcd = QColorDialog(dialog)
            qcd.setWindowTitle('颜色选择')
            qcd.setCurrentColor(self.buttonColorVal)
            if qcd.exec() == QDialog.Accepted:
                self.buttonColorVal = qcd.selectedColor()
                self.buttonColor.setStyleSheet('QWidget {background-color:%s}' % self.buttonColorVal.name())
        self.buttonColor.clicked.connect(ChangeCol)

        boxFM = QComboBox(dialog)
        boxFM.addItems(self.settingMinMax['FM'])
        boxFM.setCurrentIndex(boxFM.findText(self.FM))

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog);
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        form = QFormLayout(dialog)
        form.addRow(QLabel("设置:"))
        form.addRow("坐标X:", boxX)
        form.addRow("坐标Y:", boxY)
        form.addRow("大小W:", boxW)
        form.addRow("大小H:", boxH)
        form.addRow("透明度:", boxTP)
        form.addRow("颜色:", self.buttonColor)
        form.addRow("格式:", boxFM)
        form.addRow(buttonBox)

        dialog.setFixedSize(dialog.sizeHint())

        if dialog.exec() == QDialog.Accepted:
            self.X = boxX.value()
            self.Y = boxY.value()
            self.W = boxW.value()
            self.H = boxH.value()
            self.TP = boxTP.value()/100.0
            self.CL = self.buttonColorVal.rgb()
            self.FM = boxFM.currentText()
            return True
        else:
            return False
