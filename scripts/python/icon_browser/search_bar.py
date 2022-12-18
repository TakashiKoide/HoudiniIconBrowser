# -*- coding: utf-8 -*-
from os import path
from functools import partial

from PySide2.QtWidgets import (
    QLineEdit,
    QCompleter
)
from PySide2.QtGui import (
    QIcon,
    QColor
)
from PySide2.QtCore import (
    Qt,
    QStringListModel
)

class EditableCompleter(QCompleter):
    def __init__(self, completions, parent=None):
        super(EditableCompleter, self).__init__(parent)
        self.__completions = completions
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.__model = QStringListModel(completions)
        self.setModel(self.__model)

    def addCompletion(self, completion):
        self.__completions.append(completion)
        self.__model.setStringList(self.__completions)

    def addCompletions(self, completions):
        self.__completions += completions
        self.__model.setStringList(self.__completions)

    def setCompletions(self, completions):
        self.__completions = completions
        self.__model.setStringList(self.__completions)

    def completions(self):
        return self.__completions

class MultipleWordEdit(QLineEdit):
    def __init__(self, words, parent=None):
        super(MultipleWordEdit, self).__init__(parent)
        self.__multi_completer = EditableCompleter(words)
        self.setMultipleCompleter(self.__multi_completer)

    def addWord(self, word):
        self.__multi_completer.addCompletion(word)

    def addWords(self, words):
        self.__multi_completer.addCompletions(words)

    def setWords(self, words):
        self.__multi_completer.setCompletions(words)

    def words(self):
        return self.__multi_completer.completions()

    def keyPressEvent(self, event):
        QLineEdit.keyPressEvent(self, event)
        if not self.__multi_completer:
            return
        completer = self.__multi_completer
        word = self.text().split(' ')[-1]
        completer.setCompletionPrefix(word)
        if len(completer.completionPrefix()) < 1:
            completer.popup().hide()
            return
        completer.complete()

    def __insert_completion(self, text):
        line_text = self.text()
        p = line_text.rfind(' ')
        if p == -1:
            self.setText(text)
        else:
            self.setText(line_text[:p + 1] + text)

    def multipleCompleter(self):
        return self.__multi_completer

    def setMultipleCompleter(self, completer):
        self.__multipleCompleter = completer
        self.__multipleCompleter.setWidget(self)
        completer.activated.connect(self.__insert_completion)

class SearchBar(MultipleWordEdit):
    def __init__(self, completions=[], parent=None):
        super(SearchBar, self).__init__(completions, parent)
        self.setObjectName('SearchBar')
        self.setPlaceholderText('Search...')
        self.__search_icon = QIcon(path.dirname(__file__) + '/icons/search.svg')
        self.__close_icon = QIcon(path.dirname(__file__) + '/icons/close.svg')
        self.__close_hover_icon = self.__get_hover_icon()
        action = self.addAction(self.__search_icon, QLineEdit.LeadingPosition)
        action.triggered.connect(self.clear)

        self.textChanged.connect(partial(self.__change_icon, False))

    def __get_hover_icon(self):
        pixmap = self.__close_icon.pixmap(128, 128)
        mask = pixmap.mask()
        pixmap.fill(QColor(190, 190, 190))
        pixmap.setMask(mask)
        return QIcon(pixmap)

    def __change_icon(self, *args):
        text = self.text()
        action = self.actions()[0]
        if text:
            if args[0]:
                action.setIcon(self.__close_hover_icon)
            else:
                action.setIcon(self.__close_icon)
        else:
            action.setIcon(self.__search_icon)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if pos.x() < 28:
            self.__change_icon(True)
        else:
            self.__change_icon(False)
        super(SearchBar, self).mouseMoveEvent(event)