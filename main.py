
# APP Imports
import sys
import os
import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QTimer, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

##############################
# Import user interface file
##############################
from Club.BinaryClock.BinaryClock_1 import Ui_MainWindow
from datetime import datetime, time

# Global value for the windows status
WINDOW_SIZE = 0


# This will help us determine if the window is minimized or maximized

# Main class
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Apply shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(2)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        # Apply shadow to central widget
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        # Button click events to our top bar buttons
        #
        # Minimize window
        if hasattr(self.ui, "minimizeButton"):
            self.ui.minimizeButton.clicked.connect(lambda: self.showMinimized())
        # Close window
        if hasattr(self.ui, "closeButton"):
            self.ui.closeButton.clicked.connect(lambda: self.close())
        # Restore/Maximize window
        if hasattr(self.ui, "restoreButton"):
            self.ui.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())

        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        if hasattr(self.ui, "title_bar"):
            # Remove window tlttle bar
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

            # Set main background to transparent
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            self.ui.title_bar.mouseMoveEvent = moveWindow

        ##########################################
        # Timer Setting ##########################
        ##########################################
        self.timer = QTimer()
        self.timer.start(1000)
        self.time = QTime().currentTime()

        self.timer.timeout.connect(lambda : [self.ui.time_label.setText(QTime().currentTime().toString("hh : mm : ss")), self.updateClock()])
        ##########################################
        # Clock Array ############################
        ##########################################
        # 4 by 4 array
        # == this shows clock buttons configurations
        #  eg) [[-1,  0, -1,  1, -1,  0],
        #       [-1,  1,  0,  1,  0,  1],
        #       [ 0,  1,  1,  0,  0,  0],
        #       [ 1,  1,  0,  0,  1,  0]]
        # -1 is empty icon, 0 is off icon, 1 is on icon
        # update icons depending on icons
        self.clock_array = [[self.ui.hour_ten_8, self.ui.hour_one_8, self.ui.minute_ten_8, self.ui.minute_one_8, self.ui.second_ten_8, self.ui.second_one_8],
                            [self.ui.hour_ten_4, self.ui.hour_one_4, self.ui.minute_ten_4, self.ui.minute_one_4, self.ui.second_ten_4, self.ui.second_one_4],
                            [self.ui.hour_ten_2, self.ui.hour_one_2, self.ui.minute_ten_2, self.ui.minute_one_2, self.ui.second_ten_2, self.ui.second_one_2],
                            [self.ui.hour_ten_1, self.ui.hour_one_1, self.ui.minute_ten_1, self.ui.minute_one_1, self.ui.second_ten_1, self.ui.second_one_1]]


        # Show window
        self.show()

    #################
    # Timer function
    #################
    # change button icons each seconds
    # How to change icon of push button ?
    # == self.pushButton.setIcon(QIcon("file_path"))

    def updateClock(self):
        def toBinary(timeValue):
            return "{0:04b}".format(int(timeValue))

        def getRealTimeBstr():
            now = datetime.now()

            current_time = now.strftime("%H%M%S")
            Bstr = ""

            for i in current_time:
                Bstr += toBinary(i)

            return Bstr

        def OriginalArr(Bstr):

            count = 0

            Oarr = [[-1 for i in range(6)] for j in range(4)]
            for x in range(6):

                for y in range(4):
                    Oarr[y][x] = int(Bstr[count])
                    count += 1

            return Oarr

        def FinalBTime(Oarr):
            Oarr[0][0] = -1
            Oarr[1][0] = -1
            Oarr[0][2] = -1
            Oarr[0][4] = -1
            return Oarr

        def timeToBinary():
            return FinalBTime(OriginalArr(getRealTimeBstr()))


        binary_time = timeToBinary()
        print(binary_time)
        for i in range(len(self.clock_array)):
            for j in range(len(self.clock_array[0])):
                if binary_time[i][j] == -1:
                    continue
                elif binary_time[i][j] == 0:
                    self.clock_array[i][j].setIcon(QIcon("Binary_clock_assets/dim_circle.png"))
                elif binary_time[i][j] == 1:
                    self.clock_array[i][j].setIcon(QIcon("Binary_clock_assets/blue_circle.png"))


    #################
    # Update array
    #################
    # update binary clock array according to current time.
    def binaryClock_array(self):
        return

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    # Restore or maximize your window
    def restore_or_maximize_window(self):

        # Global windows state
        global WINDOW_SIZE  # The default value is zero to show that the size is not maximized
        win_status = WINDOW_SIZE

        if win_status == 0:
            # If the window is not maximized
            WINDOW_SIZE = 1  # Update value to show that the window has been maxmized
            self.showMaximized()
            # Update button icon
            # self.ui.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-maximize.png"))  # Show maximized icon
        else:
            # If the window is on its default size
            WINDOW_SIZE = 0  # Update value to show that the window has been minimized/set to normal size (which is 800 by 400)
            self.showNormal()
            # Update button icon
            # self.ui.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-restore.png"))  # Show minized icon




# Execute app
#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
else:
    print(__name__, "hh")
# press ctrl+b in sublime to run
