import json
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QVBoxLayout, QApplication, QWidget, QApplication, QPushButton, QMessageBox, QLabel)

class Setting:
    settingDefault = {'X' : 1320, 'Y' : 850, 'W' : 600, 'H' : 300, 'TP' : 0.5, 'format' : 'hh:mm'}
    settingMinMax  = {'X' : [0, 9999], 'Y' : [0, 9999], 'W' : [0, 9999], 'H' : [0, 9999], 'TP' : [0, 1], 'format' : ['hh:mm:ss', 'hh:mm']}

    def SettingSave(self):
        try:
            with open('setting.json', 'w', encoding = 'utf8') as file:
                setting = dict()
                setting['X'] = self.X
                setting['Y'] = self.Y
                setting['W'] = self.W
                setting['H'] = self.H
                setting['TP'] = self.TP
                setting['format'] = self.format
                json.dump(setting, file)
        except Exception as identifier:
            print(identifier)
            # self.PaintStatusBar(identifier)
            pass
        
    def SettingLoadOne(self, setting, name, continued):
        if continued:
            if name not in setting or type(setting[name]) != int or setting[name] < self.settingMinMax[name][0] or setting[name] > self.settingMinMax[name][1]:
                return self.settingDefault[name]
            else:
                return setting[name]
        else:
            if name not in setting or type(setting[name]) != type(self.settingDefault[name]) or setting[name] not in self.settingMinMax[name]:
                return self.settingDefault[name]
            else:
                return setting[name]

    def SettingLoad(self):
        try:
            with open('setting.json', 'r', encoding = 'utf8') as file:
                setting = json.loads(file.read())
                self.X = self.SettingLoadOne(setting, 'X', True)
                self.Y = self.SettingLoadOne(setting, 'Y', True)
                self.W = self.SettingLoadOne(setting, 'W', True)
                self.H = self.SettingLoadOne(setting, 'H', True)
                self.TP = self.SettingLoadOne(setting, 'TP', True)
                self.format = self.SettingLoadOne(setting, 'format', False)
        except Exception as identifier:
            print('setting.json error!')
            print(identifier)
            self.X = self.settingDefault['X']
            self.Y = self.settingDefault['Y']
            self.W = self.settingDefault['W']
            self.H = self.settingDefault['H']
            self.TP = self.settingDefault['TP']
            self.format = self.settingDefault['format']
            # self.PaintStatusBar(identifier)
        
    # def SettingDialog(self, ui):
    #     from PyQt5.QtWidgets import (QDialog, QSpinBox, QComboBox, QDialogButtonBox, QFormLayout)
    #     dialog = QDialog(ui)
    #     boxDifficult = QSpinBox(dialog)
    #     boxDifficult.setRange(1, 5)
    #     boxDifficult.setValue(self.Difficult)

    #     boxWhoFirst = QComboBox(dialog)
    #     boxWhoFirst.addItems(['player', 'AI', 'random'])
    #     boxWhoFirst.setCurrentIndex(boxWhoFirst.findText(self.WhoFirst))

    #     buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog);

    #     form = QFormLayout(dialog)
    #     form.addRow(QLabel("设置:"))
    #     form.addRow("难度(1-5):", boxDifficult)
    #     form.addRow("先手:", boxWhoFirst)
    #     form.addRow(buttonBox)

    #     buttonBox.accepted.connect(dialog.accept)
    #     buttonBox.rejected.connect(dialog.reject)
    #     if dialog.exec() == QDialog.Accepted:
    #         self.Difficult = boxDifficult.value()
    #         self.WhoFirst = boxWhoFirst.currentText()
