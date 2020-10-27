import sys

from .Setting import Setting
from .Ui_Frame import Ui_Frame

from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtWidgets import QWidget, QMenu, QSystemTrayIcon, QAction
from PyQt5.QtGui import QIcon, QColor

# 窗口程序
class Frame(QWidget, Setting):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.SettingLoad()
        self.inSetting = False
        self.setGeometry(self.X, self.Y, self.W, self.H)

        self.Tray()
        self.ui = Ui_Frame()
        self.ui.setupUi(self, QColor(self.CL))
        
        self.dftFlag = self.windowFlags()
        self.TransParent()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ShowLcd)
        self.ShowLcd()

        self.timerT = QTimer(self)
        self.timerT.timeout.connect(self.TopMost)
        self.timerT.start(10)

        # 解决无法关闭QAPP的问题
        self.setAttribute(Qt.WA_QuitOnClose, True)

    def close(self):
        if self.inSetting:
            self.tray.showMessage(u"错误", '用户正在修改设置中, 无法退出', icon=3) # icon的值  0没有图标  1是提示  2是警告  3是错误
        else:
            print(self.geometry())
            self.SettingSave()
            del self.ui
            # python不保证析构, 因此托盘可能无法消失, 需要手动hide
            self.tray.hide()
            del self.tray
            return QWidget.close(self)

    # 窗口初始设置
    def TransParent(self):
        self.setWindowOpacity(self.TP) # 控件透明
        self.setAttribute(Qt.WA_TranslucentBackground, True) # 窗口透明
        self.setWindowFlags(self.windowFlags() | Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.NoFocus) # 无焦点

        # 鼠标穿透，必须后于前几项
        import win32gui
        import win32con
        self.hwnd = int(self.winId())
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE);
        
    # 更新时间
    def ShowLcd(self):
        timev = QTime.currentTime()
        time = timev.addMSecs(500)
        nextTime = (1500 - (time.msec()) % 1000)

        text = time.toString(self.FM)
        self.ui.lcdNumber.display(text)
        self.timer.start(nextTime)
        # self.update()

    def TopMost(self):
        import win32gui
        import win32con
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

    def SettingChange(self):
        if self.inSetting:
            self.tray.showMessage(u"错误", '正在修改设置中', icon=3) # icon的值  0没有图标  1是提示  2是警告  3是错误
        else:
            self.inSetting = True
            from PyQt5.QtGui import QColor
            if self.SettingDialog():
                self.setGeometry(self.X, self.Y, self.W, self.H)
                self.setWindowOpacity(self.TP)
                self.ui.setupLcdColor(QColor(self.CL))
            self.inSetting = False
            
    # 托盘
    def Tray(self):
        self.tray = QSystemTrayIcon(self) # 创建托盘

        if hasattr(sys, "_MEIPASS"):
            self.tray.setIcon(QIcon(sys._MEIPASS + r'/Icon.ico'))
        else:
            self.tray.setIcon(QIcon(r'./Icon.ico'))
        # 提示信息
        self.tray.setToolTip(u'桌面时钟')

        # 创建托盘的右键菜单
        menu = QMenu()
        menu.addAction(QAction(u'窗口设置', self, triggered = self.SettingChange))
        menu.addAction(QAction(u'退出', self, triggered = self.close))
        self.tray.setContextMenu(menu) # 把menu设定为托盘的右键菜单
        self.tray.show()

