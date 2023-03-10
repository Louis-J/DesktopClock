from collections import namedtuple
import sys
import json
from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QDialog, QColorDialog
from PyQt5.QtGui import QIcon, QColor

SettingKeyType = namedtuple('SettingKeyType', ('type', 'range', 'defaultValue'))
class Settings:
    settingKeys: dict[str, SettingKeyType] = {
        # keyName: [type, range defaultValue]
        'X' : SettingKeyType(int, [0, 9999], 1320),
        'Y' : SettingKeyType(int, [0, 9999], 850),
        'W' : SettingKeyType(int, [0, 9999], 600),
        'H' : SettingKeyType(int, [0, 9999], 300),
        'TP' : SettingKeyType(float, [0, 1.0], 0.5),
        'CL' : SettingKeyType(QColor, None, QColor(Qt.darkCyan).rgb()),
        'FM' : SettingKeyType(str, ['hh:mm:ss', 'hh:mm'], 'hh:mm'),
    }

    def __init__(self) -> None:
        try:
            with open('setting.json', 'r', encoding = 'utf8') as file:
                settingJson = json.loads(file.read())
                self.settings = {k: self.SettingLoadOne(settingJson, k, True) for k in Settings.settingKey}
        except Exception as identifier:
            print(('setting.json load error!', identifier))
            self.settings = {k: v[-1] for k, v in Settings.settingKey.items()}

    def __getattr__(self, __name: str) -> Any:
        return self.settings[__name]

    def SettingLoadOne(self, settingJson, name):
        keyInfo = Settings.settingKeys[name]
        if name not in settingJson:
            print(f'{name} load bad! key is not exist')
            return keyInfo.defaultValue
        value = settingJson[name]
        if name not in type(value) != keyInfo.type:
            print(f'{name} load bad! type should be{keyInfo.type}, not {type(value)}')
            return keyInfo.defaultValue
        if keyInfo.range is not None:
            if keyInfo.type in (int, float) and value < keyInfo.range[0] or value > keyInfo.range[1]:
                print(f'{name} load bad! value is out of range')
                return keyInfo[-1]
            elif keyInfo.type in (str,) and value not in keyInfo.range:
                print(f'{name} load bad! value is out of range')
                return keyInfo[-1]
        else:
            return value

    def SettingSave(self):
        try:
            with open('setting.json', 'w', encoding = 'utf8') as file:
                json.dump(self.settings, file)
        except Exception as identifier:
            print(('setting.json save error!', identifier))
            pass


    def SettingDialog(self, ApplyChange):
        from PyQt5.QtWidgets import (QDialog, QSpinBox, QComboBox, QDialogButtonBox, QFormLayout, QColorDialog, QPushButton, QSizePolicy)

        dialog = self.dialog = QDialog()
        dialog.setWindowTitle('设置')
        if hasattr(sys, "_MEIPASS"):
            dialog.setWindowIcon(QIcon(sys._MEIPASS + r'/Icon.ico'))
        else:
            dialog.setWindowIcon(QIcon(r'./Icon.ico'))

        boxX = QSpinBox(dialog)
        boxX.setRange(Settings.settingKeys['X'].range[0], Settings.settingKeys['X'].range[1])
        boxX.setValue(self.settings['X'])
        boxY = QSpinBox(dialog)
        boxY.setRange(Settings.settingKeys['Y'].range[0], Settings.settingKeys['Y'].range[1])
        boxY.setValue(self.settings['Y'])
        boxW = QSpinBox(dialog)
        boxW.setRange(Settings.settingKeys['W'].range[0], Settings.settingKeys['W'].range[1])
        boxW.setValue(self.settings['W'])
        boxH = QSpinBox(dialog)
        boxH.setRange(Settings.settingKeys['H'].range[0], Settings.settingKeys['H'].range[1])
        boxH.setValue(self.settings['H'])

        boxTP = QSpinBox(dialog)
        boxTP.setRange(0, 100)
        boxTP.setValue(self.TP*100)

        self.buttonColorVal = QColor(self.settings['CL'])
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
        boxFM.addItems(Settings.settingKeys['FM'].range)
        boxFM.setCurrentIndex(boxFM.findText(self.FM))

        def Apply():
            newSettings = {
                'X': boxX.value(),
                'Y': boxY.value(),
                'W': boxW.value(),
                'H': boxH.value(),
                'TP': boxTP.value()/100.0,
                'CL': self.buttonColorVal.rgb(),
                'FM': boxFM.currentText(),
            }
            if newSettings != self.settings:
                self.settings = newSettings
            ApplyChange()
            self.SettingSave()
            
        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        buttonBox.button(QDialogButtonBox.Apply).setText("应用")
        buttonBox.button(QDialogButtonBox.Ok).setText("确定")
        buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(Apply)

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
            Apply()
