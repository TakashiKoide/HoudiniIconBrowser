# -*- coding: utf-8 -*-

from PySide2.QtWidgets import (
    QPushButton
)
from PySide2.QtGui import (
    QIcon
)

class IconButton(QPushButton):
    def __init__(self, fileName, parent=None):
        super(IconButton, self).__init__(parent)
        self.setObjectName('IconButton')
        self.__normal_icon = QIcon(fileName)
        self.__hover_icon = None
        self.__checked_icon = None
        self.setIcon(self.__normal_icon)
        self.setFlat(True)

        self.toggled.connect(self.__toggle_icon)

    def __set_icon_color(self, icon, color):
        pixmap = icon.pixmap(self.size() * 2)
        mask = pixmap.mask()
        pixmap.fill(color)
        pixmap.setMask(mask)
        return QIcon(pixmap)

    def setNormalIconColor(self, color):
        self.__normal_icon = self.__set_icon_color(self.__normal_icon, color)
        self.setIcon(self.__normal_icon)

    def setHoverIconColor(self, color):
        if self.__hover_icon:
            icon = self.__hover_icon
        else:
            icon = self.__normal_icon
        self.__hover_icon = self.__set_icon_color(icon, color)

    def setCheckedIconColor(self, color):
        if self.__checked_icon:
            icon = self.__checked_icon
        else:
            icon = self.__normal_icon
        self.__checked_icon = self.__set_icon_color(icon, color)

    def setNormalIcon(self, icon):
        self.__normal_icon = icon
        self.setIcon(icon)

    def setNormalIconFromFile(self, fileName):
        self.__normal_icon = QIcon(fileName)
        self.setIcon(self.__normal_icon)

    def setHoverIcon(self, icon):
        self.__hover_icon = icon

    def setHoverIconFromFile(self, fileName):
        self.__hover_icon = QIcon(fileName)

    def setCheckedIcon(self, icon):
        self.__checked_icon = icon

    def setCheckedIconFromFile(self, fileName):
        self.__checked_icon = QIcon(fileName)

    def __toggle_icon(self):
        if self.__checked_icon and self.isCheckable:
            if self.isChecked():
                self.setIcon(self.__checked_icon)
            else:
                self.setIcon(self.__normal_icon)


    def enterEvent(self, event):
        if self.__hover_icon:
            if self.__checked_icon and self.isChecked():
                return super(IconButton, self).enterEvent(event)
            else:
                self.setIcon(self.__hover_icon)
        return super(IconButton, self).enterEvent(event)

    def leaveEvent(self, event):
        if self.__hover_icon:
            if self.__checked_icon and self.isChecked():
                self.setIcon(self.__checked_icon)
            else:
                self.setIcon(self.__normal_icon)
        return super(IconButton, self).leaveEvent(event)