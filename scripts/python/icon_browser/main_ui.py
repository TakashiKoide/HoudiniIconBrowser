# -*- coding: utf-8 -*-

import os
import re
from six.moves import reload_module

from PySide2 import QtCore, QtGui, QtWidgets

from . import app_command
from . import icon_view
from .search_bar import SearchBar
from .icon_button import IconButton
reload_module(app_command)
reload_module(icon_view)

class ModeButton(IconButton):
    def __init__(self, icon_file, parent=None):
        super(ModeButton, self).__init__(icon_file, parent)
        self.setObjectName('ModeButton')
        self.setNormalIconColor(QtGui.QColor(128, 128, 128))
        self.setHoverIconColor(QtGui.QColor(230, 230, 230))
        self.setCheckedIconColor(QtGui.QColor(230, 230, 230))
        self.setFixedSize(QtCore.QSize(24, 24))
        self.setIconSize(QtCore.QSize(20, 20))
        self.setCheckable(True)

class IconBrowserWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(IconBrowserWindow, self).__init__(parent)
        #UI Visual
        self.setWindowTitle('Icon Browser')
        self.setObjectName('IconBrowserWindow')

        self.icon_files = app_command.get_all_icon_files()

        self.filter_combo = QtWidgets.QComboBox(self)
        self.filter_combo.addItems(self.icon_files.keys())
        self.search_bar = SearchBar(parent=self)

        self.icon_list_view = icon_view.IconListView(self.icon_files.get('All', []))

        self.item_label = QtWidgets.QLabel()

        icon_dir = os.path.dirname(__file__) + '/icons'
        self.icon_slider = QtWidgets.QSlider(self)
        self.icon_slider.setMinimum(16)
        self.icon_slider.setMaximum(64)
        self.icon_slider.setFixedWidth(128)
        self.icon_slider.setValue(64)
        self.icon_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)

        plus_icon_file = icon_dir + '/plus.svg'
        self.plus_button = IconButton(plus_icon_file, self)
        self.plus_button.setFixedSize(20, 20)
        self.plus_button.setIconSize(QtCore.QSize(16, 16))
        self.plus_button.setNormalIconColor(QtGui.QColor(160, 160, 160))
        self.plus_button.setHoverIconColor(QtGui.QColor(230, 230, 230))

        minus_icon_file = icon_dir + '/minus.svg'
        self.minus_button = IconButton(minus_icon_file, self)
        self.minus_button.setFixedSize(20, 20)
        self.minus_button.setIconSize(QtCore.QSize(16, 16))
        self.minus_button.setNormalIconColor(QtGui.QColor(160, 160, 160))
        self.minus_button.setHoverIconColor(QtGui.QColor(230, 230, 230))

        self.icon_spin = QtWidgets.QSpinBox()
        self.icon_spin.setValue(64)
        self.icon_spin.setRange(16, 64)
        self.icon_spin.setFixedWidth(48)
        self.icon_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        list_mode_icon_file = icon_dir + '/list_mode.svg'
        self.list_mode_button = ModeButton(list_mode_icon_file, self)

        icon_mode_icon_file = icon_dir + '/icon_mode.svg'
        self.icon_mode_button = ModeButton(icon_mode_icon_file, self)
        self.icon_mode_button.setChecked(True)

        self.set_item_label()

        # Signal
        self.search_bar.textChanged.connect(self.filter_items)
        self.filter_combo.activated.connect(self.change_category)

        self.icon_list_view.sel_model.selectionChanged.connect(self.set_item_label)

        self.icon_slider.valueChanged.connect(self.icon_slider_value_changed)
        self.icon_spin.editingFinished.connect(self.icon_spin_value_changed)
        self.plus_button.clicked.connect(self.plus_icon_size)
        self.minus_button.clicked.connect(self.minus_icon_size)

        self.icon_mode_button.clicked.connect(self.set_view_icon_mode)
        self.list_mode_button.clicked.connect(self.set_view_list_mode)

        # Layout

        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(self.search_bar)

        setting_layout = QtWidgets.QHBoxLayout()
        setting_layout.addWidget(self.minus_button)
        setting_layout.addWidget(self.icon_slider)
        setting_layout.addWidget(self.plus_button)
        setting_layout.addWidget(self.icon_spin)
        setting_layout.setSpacing(8)

        option_layout = QtWidgets.QHBoxLayout()
        option_layout.addWidget(self.item_label)
        option_layout.addStretch()
        option_layout.addLayout(setting_layout)
        option_layout.addWidget(self.list_mode_button)
        option_layout.addWidget(self.icon_mode_button)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(filter_layout)
        self.main_layout.addWidget(self.icon_list_view)
        self.main_layout.addLayout(option_layout)

        self.resize(1160, 796)

        style_file = os.path.dirname(__file__) + '/style.qss'
        with open(style_file, 'r') as f:
            style = f.read()
        self.setStyleSheet(style)

    def set_item_label(self):
        item_count = self.icon_list_view.proxy_model.rowCount()
        sel_indexes = self.icon_list_view.selectedIndexes()
        sel_count = len(sel_indexes)
        label_text = '{} items({} selected)'.format(item_count, sel_count)
        if sel_count == 1:
            index = self.icon_list_view.proxy_model.mapToSource(sel_indexes[0])
            name = index.data(QtCore.Qt.ToolTipRole)
            label_text = '{} items({})'.format(item_count, name)
        self.item_label.setText(label_text)

    def filter_items(self, filter_text):
        texts = ['(?=.*{})'.format(text) for text in filter_text.split(' ')]
        text = ''.join(texts)
        filter_text = '^{}.*$'.format(text)
        reg_exp = QtCore.QRegExp(
            filter_text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.icon_list_view.proxy_model.setFilterRegExp(reg_exp)
        self.set_item_label()

    def change_category(self):
        category = self.filter_combo.currentText()
        icon_files = self.icon_files.get(category, [])
        self.icon_list_view.refresh(icon_files)
        self.filter_items(self.search_bar.text())

    def set_view_icon_mode(self):
        self.list_mode_button.setChecked(False)
        self.icon_mode_button.setChecked(True)
        self.icon_list_view.set_view_icon_mode()

    def set_view_list_mode(self):
        self.list_mode_button.setChecked(True)
        self.icon_mode_button.setChecked(False)
        self.icon_list_view.set_view_list_mode()

    def icon_spin_value_changed(self):
        value = self.icon_spin.value()
        self.icon_list_view.setIconSize(QtCore.QSize(value, value))
        self.icon_slider.setValue(value)

    def icon_slider_value_changed(self, value):
        self.icon_list_view.setIconSize(QtCore.QSize(value, value))
        self.icon_spin.setValue(value)

    def plus_icon_size(self):
        size = self.icon_slider.value()
        self.icon_slider.setValue(size + 4)

    def minus_icon_size(self):
        size = self.icon_slider.value()
        self.icon_slider.setValue(size - 4)

    def show_window(self):
        self.setParent(app_command.get_parent_window(), QtCore.Qt.Window)
        self.show()