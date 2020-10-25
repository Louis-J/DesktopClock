import os
import sys
from .Setting import Setting
from .Ui_Frame import Ui_Frame
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtWidgets import QWidget, QLCDNumber

from PyQt5.QtWidgets import QWidget, QMenu, QSystemTrayIcon, QAction
from PyQt5.QtGui import QIcon

# 窗口程序
class Frame(QWidget, Setting):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.SettingLoad()
        self.setGeometry(self.X, self.Y, self.W, self.H)

        self.Tray()
        self.ui = Ui_Frame()
        self.ui.setupUi(self, Qt.darkCyan)
        
        self.dftFlag = self.windowFlags()
        self.TransParent()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ShowLcd)
        self.ShowLcd()

        # 解决无法关闭QAPP的问题
        self.setAttribute(Qt.WA_QuitOnClose, True)

    def __del__(self):
        print(self.geometry())
        self.SettingSave()
        del self.ui

    # 窗口初始设置
    def TransParent(self):
        self.setWindowOpacity(self.TP) # 控件透明
        self.setAttribute(Qt.WA_TranslucentBackground, True) # 窗口透明
        self.setWindowFlags(self.windowFlags() | Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.NoFocus) # 无焦点

        # 鼠标穿透，必须后于前几项
        import win32gui
        import win32con
        win32gui.SetWindowLong(self.winId(), win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.winId(), win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED);
        
    # 更新时间
    def ShowLcd(self):
        timev = QTime.currentTime()
        time = timev.addMSecs(500)
        nextTime = (1500 - (time.msec()) % 1000)

        text = time.toString(self.format)
        self.ui.lcdNumber.display(text)
        # print(nextTime)
        self.timer.start(nextTime)
        # self.timer.setInterval(nextTime)
        self.update()

    # 置顶
    def paintEvent(self, event):
        import win32gui
        import win32con
        hwnd = self.winId()
        # if self.isEnabled() and win32gui.IsWindowEnabled(hwnd):
        if True:
            flags = win32con.SWP_NOMOVE | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, flags)

    # 托盘
    def Tray(self):
        self.tray = QSystemTrayIcon(self) # 创建托盘
        self.tray.setIcon(QIcon(r'./Icon.ico'))
        # 提示信息
        self.tray.setToolTip(u'桌面时钟')
        # 托盘创建出来时显示的信息   
        self.tray.showMessage(u"标题", '托盘信息内容', icon=1) # icon的值  0没有图标  1是提示  2是警告  3是错误     
                    
        # 弹出的信息被点击就会调用messageClicked连接的函数
        # self.tray.messageClicked.connect(message)
        # 托盘图标被激活，
        # self.tray.activated.connect(iconActivated)

        # 创建托盘的右键菜单
        menu = QMenu()
        # # self.setWindow = QAction(u'窗口设置', self, triggered = self.SettingDialog)
        menu.addAction(QAction(u'退出', self, triggered = self.close))
        self.tray.setContextMenu(menu) # 把menu设定为托盘的右键菜单
        self.tray.show()

