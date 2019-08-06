import sys
import re
import os
import hashlib
import subprocess
import time
import threading
import win32con
import win32api
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

startTiming = True
second = 1
step = 0

def getChordPixSum(): 
    num=0
    for root, dirs, files in os.walk('./picture/'):
        for name in files:
            if(name.endswith(".png")):
                num = num+1
    return num  

def getChordPixName(step):
    num=0
    for root, dirs, files in os.walk('./picture/'):
        for name in files:
            if(name.endswith(".png")):
                num = num+1
                if step is num:
                    return name;
    return None

num = getChordPixSum()   
#---------------------------------------------------------------------------
class UI_init(QWidget):
    close_signal = pyqtSignal()
    def __init__(self):
        super(UI_init, self).__init__()
        # 窗口标题
        self.setWindowTitle('尤克里里')
        # 定义窗口大小
        self.resize(700, 500)
        self.setFixedSize(700,500)

        self.btnRandomChord = QPushButton('和弦练习',self)
        self.btnRandomChord.setFont(QFont("Timers", 13))
        self.btnRandomChord.move(280, 30)


    def closeEvent(self, event):
        self.close_signal.emit()
        self.close()

    def handle_click(self):
        if not self.isVisible():
            self.show()

        
#---------------------------------------------------------------------------
class RandomChordWindow(QWidget):
    close_signal = pyqtSignal()
    def __init__(self):
        super(RandomChordWindow, self).__init__()
        self.setWindowTitle('和弦练习')
        self.resize(750, 500)
        self.setFixedSize(750,500)


        self.picture = QLabel(self)
        self.picture.setGeometry(0,0,600,500)
        self.picture.setStyleSheet("border: 2px solid red")
        self.picture.setScaledContents(True)

        self.timeLine = QLineEdit(self)
        self.timeLine.setFont(QFont("Timers", 10))
        self.timeLine.setGeometry(600,10,100,20)
        self.timeLine.setText('时间：%d s'%second)
        self.timeLine.setEnabled(False)

        self.startDisplayLine = QLineEdit(self)
        self.startDisplayLine.setFont(QFont("Timers", 10))
        self.startDisplayLine.setGeometry(600,30,100,20)
        self.startDisplayLine.setText('开始播放')
        self.startDisplayLine.setEnabled(False)

        self.fixedOne = QLabel(self)
        self.fixedOne.setFont(QFont("Timers", 10))
        self.fixedOne.setGeometry(600,50,100,20)
        self.fixedOne.setText('↑:时间加')

        self.fixedOne = QLabel(self)
        self.fixedOne.setFont(QFont("Timers", 10))
        self.fixedOne.setGeometry(600,70,100,20)
        self.fixedOne.setText('↓:时间减')

        self.fixedOne = QLabel(self)
        self.fixedOne.setFont(QFont("Timers", 10))
        self.fixedOne.setGeometry(600,90,100,20)
        self.fixedOne.setText('←:上一张图片')

        self.fixedOne = QLabel(self)
        self.fixedOne.setFont(QFont("Timers", 10))
        self.fixedOne.setGeometry(600,110,100,20)
        self.fixedOne.setText('→:下一张图片')

        self.fixedOne = QLabel(self)
        self.fixedOne.setFont(QFont("Timers", 10))
        self.fixedOne.setGeometry(600,130,150,20)
        self.fixedOne.setText('Space:返回上一个界面')

        self.fixedOne = QLabel(self)
        self.fixedOne.setFont(QFont("Timers", 10))
        self.fixedOne.setGeometry(600,150,150,20)
        self.fixedOne.setText('Esc:开始/停止播放')

        self.btnReturnPrior = QRadioButton('返回上一个界面',self)
        self.btnReturnPrior.setFont(QFont("Timers", 13))
        self.btnReturnPrior.move(600, 170)
        self.btnReturnPrior.setShortcut('Space')
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0)
        self.btnReturnPrior.setGraphicsEffect(op)
      #  self.btnReturnPrior.setEnabled(False)
       
        

        self.timer = QTimer(self)
    #    self.timer.start(1000)
        self.timer.timeout.connect(self.funTimer)


    # 检测键盘按键
    def keyPressEvent(self, event):
        print("按下：" + str(event.key()))
        # 举例
        global step
        global second
        global num
        global startTiming
        if(event.key() == Qt.Key_Escape):
            global timer
            print(startTiming)
            if(startTiming == True):
                startTiming = False
                self.startDisplayLine.setText('停止播放')
                self.timer.stop()
            elif(startTiming == False):
                startTiming = True
                self.startDisplayLine.setText('开始播放')
                self.timer.start(second*1000)
            print('测试：ESC')
            
        if(event.key() == Qt.Key_Space):
            startTiming = False
            self.timer.stop()
            self.startDisplayLine.setText('停止播放')
            print('测试：Space')
            
        if event.key()==Qt.Key_Up:
            second += 1
            if(second >= 10):
                second = 10
            self.timeLine.setText('时间：%d s'%second)
            if(startTiming == True):
                self.timer.start(second*1000)
            print('测试：Key_Up')
            
        if event.key()==Qt.Key_Down:
            second -= 1
            if(second <= 1):
                second = 1
            self.timeLine.setText('时间：%d s'%second)
            if(startTiming == True):
                self.timer.start(second*1000)
            print('测试：Key_Down')
            
        if event.key()==Qt.Key_Left:
            step -= 1
            self.PixShow()
            print('测试：K_LEFT')
            
        if event.key()==Qt.Key_Right:
            step += 1
            self.PixShow()
            print('测试：Key_Right')   
            

    def PixShow(self):
        global step
        global num
        num = getChordPixSum()
        if(step > num):
            step = 1
        if(step <= 0):
            step = num
        name = getChordPixName(step)
        name = './picture/'+ name
        print(name)
        pix = QPixmap(name)
        self.picture.setPixmap(pix)

    def funTimer(self):
        global step 
        print('1111')
        step += 1
        self.PixShow()


    def handle_click(self):
        if not self.isVisible():
            self.show()
            global step 
            step += 1
            self.PixShow()
            self.timer.start(second*1000)

    def closeEvent(self, event):
        self.close()
        self.timer.stop()

    def hideEvent(self, event):
        self.timer.stop()
#---------------------------------------------------------------------------
        
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    initialize = UI_init()
    randomChord = RandomChordWindow()
    
    initialize.btnRandomChord.clicked.connect(randomChord.handle_click)
    initialize.btnRandomChord.clicked.connect(initialize.hide)
    initialize.close_signal.connect(initialize.close)

    randomChord.btnReturnPrior.clicked.connect(initialize.handle_click)
    randomChord.btnReturnPrior.clicked.connect(randomChord.hide)
    randomChord.close_signal.connect(randomChord.close)
    
    initialize.show()
    sys.exit(app.exec_())
