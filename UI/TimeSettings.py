from recordclass import RecordClass

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from .SettingsUtils import SettingTypeEnum, SettingTypeQColor, SettingTypeRange, SettingsUnit

class TimeSettingsCollection(RecordClass):
    x:            SettingTypeRange('坐标X:', 1320, int, (0, 9999))
    y:            SettingTypeRange('坐标Y:', 850, int, (0, 9999))
    w:            SettingTypeRange('大小W:', 600, int, (0, 9999))
    h:            SettingTypeRange('大小H:', 300, int, (0, 9999))
    transparent:  SettingTypeRange('透明度:', 50, int, (0, 100))
    timeColor:    SettingTypeQColor('时间颜色:', QColor(Qt.darkCyan).rgb())
    timeFormat:   SettingTypeEnum('时间格式:', 'hh:mm', str, ['hh:mm:ss', 'hh:mm'])

class TimeSettingsUnit(SettingsUnit):
    x:            int
    y:            int
    w:            int
    h:            int
    transparent:  int
    timeColor:    int
    timeFormat:   str

    def __init__(self, setting_obj) -> None:
        super().__init__(TimeSettingsCollection, setting_obj)
