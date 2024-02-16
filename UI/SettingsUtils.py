import json
import sys
import traceback
from recordclass import RecordClass
from typing import Any, List, Tuple, Type
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QSpinBox, QComboBox, QDialogButtonBox, QFormLayout, QColorDialog, QPushButton, QTextEdit
from PySide6.QtGui import QIcon, QColor

logger = logging.getLogger(__name__)

class SettingType(RecordClass):
    hint: str
    default_value: Any

    def checkValueValid(self, value):
        raise NotImplementedError()

    def getDialogBox(self, parent, value):
        raise NotImplementedError()

    def getChooseValue(self, box):
        raise NotImplementedError()


# for text settings
class SettingTypeText(SettingType):

    def checkValueValid(self, value):
        return isinstance(value, str)

    def getDialogBox(self, parent, value):
        box = QTextEdit(parent)
        box.setPlainText(value)
        return box

    def getChooseValue(self, box: QTextEdit):
        return box.toPlainText()


# for qcolor settings
class QColorPushButton(QPushButton):
    def __init__(self, color_rgb, *args, **kwargs):
        super().__init__(*args, kwargs)
        self.color_value = QColor(color_rgb)
        self.setStyleSheet('QWidget {background-color:%s}' % self.color_value.name())
        self.clicked.connect(self.changeColor)

    def changeColor(self):
        qcd = QColorDialog(self.parent)
        qcd.setWindowTitle('颜色选择')
        qcd.setCurrentColor(self.color_value)
        if qcd.exec() == QDialog.Accepted:
            self.color_value = qcd.selectedColor()
            self.setStyleSheet('QWidget {background-color:%s}' % self.color_value.name())
    
    def getColorRGB(self):
        return self.color_value.rgb()

class SettingTypeQColor(SettingType):
    def checkValueValid(self, value):
        return isinstance(value, int)

    def getDialogBox(self, parent, value):
        return QColorPushButton(value, parent)

    def getChooseValue(self, box: QColorPushButton):
        return box.getColorRGB()



# for enum settings
class SettingTypeEnum(SettingType):
    value_type: type
    value_enum: List

    def checkValueValid(self, value):
        if not isinstance(value, self.value_type):
            return False
        if value not in self.value_enum:
            return False
        return True

    def getDialogBox(self, parent, value):
        box = QComboBox(parent)
        box.addItems(self.value_enum)
        box.setCurrentIndex(self.value_enum.index(value))
        return box

    def getChooseValue(self, box: QComboBox):
        return box.currentText()



# for range settings
class SettingTypeRange(SettingType):
    value_type: type
    value_minmax: Tuple[Any, Any]

    def checkValueValid(self, value):
        if not isinstance(value, self.value_type):
            return False
        if value < self.value_minmax[0] or value > self.value_minmax[1]:
            return False
        return True

    def getDialogBox(self, parent, value):
        box = QSpinBox(parent)
        box.setRange(self.value_minmax[0], self.value_minmax[1])
        box.setValue(value)
        return box

    def getChooseValue(self, box: QSpinBox):
        return box.value()


def load_settings_dict():
    try:
        with open('setting.json', 'r', encoding = 'utf8') as file:
            return json.loads(file.read())
    except Exception as identifier:
        logger.error('load_settings_dict got exception!')
        logger.error('except msg: %s', identifier)
        logger.error('except frame: %s', traceback.format_exception(*sys.exc_info()))
        return {}

def save_settings_dict(obj_dict):
    try:
        with open('setting.json', 'w', encoding = 'utf8') as file:
            json.dump(obj_dict, file)
    except Exception as identifier:
        logger.error('save_settings_dict got exception!')
        logger.error('except msg: %s', identifier)
        logger.error('except frame: %s', traceback.format_exception(*sys.exc_info()))
        pass


class SettingsUnit:
    def __init__(self, collection_type: Type, setting_obj) -> None:
        self.collection_type = collection_type

        for key, type in collection_type.__annotations__.items():
            type: SettingType
            if key not in setting_obj:
                logger.warn(f'{key} load bad! not exist')
                setattr(self, key, type.default_value)
                continue
            value = setting_obj[key]
            if not type.checkValueValid(value):
                logger.warn(f'{key} load bad! check invalid for value {value}')
                setattr(self, key, type.default_value)
                continue
            setattr(self, key, value)


    def settingsDialog(self, parent, funcApplyChange: callable):
        parent = None
        dialog = QDialog(parent)
        dialog.setWindowTitle('设置')
        if hasattr(sys, "_MEIPASS"):
            dialog.setWindowIcon(QIcon(sys._MEIPASS + r'/Icon.ico'))
        else:
            dialog.setWindowIcon(QIcon(r'./Icon.ico'))

        form = QFormLayout(dialog)
        form.addRow(QLabel("设置:"))
        box_dict = {}
        for key, type in self.collection_type.__annotations__.items():
            type: SettingType
            record_value = getattr(self, key)
            box = type.getDialogBox(parent, record_value)
            box_dict[key] = box
            form.addRow(type.hint, box)

        def applyNewRecord():
            has_value_change = False
            for key, type in self.collection_type.__annotations__.items():
                type: SettingType
                box = box_dict[key]
                new_record_value = type.getChooseValue(box)
                if getattr(self, key) != new_record_value:
                    setattr(self, key, new_record_value)
                    has_value_change = True
            
            if has_value_change:
                funcApplyChange()

        button_box = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        button_box.button(QDialogButtonBox.Apply).setText("应用")
        button_box.button(QDialogButtonBox.Ok).setText("确定")
        button_box.button(QDialogButtonBox.Cancel).setText("取消")
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        button_box.button(QDialogButtonBox.Apply).clicked.connect(applyNewRecord)

        form.addRow(button_box)

        dialog.setFixedSize(dialog.sizeHint())

        if dialog.exec() == QDialog.Accepted:
            applyNewRecord()

    def asdict(self):
        return {key: getattr(self, key) for key in self.__annotations__}
