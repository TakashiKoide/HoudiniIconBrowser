# -*- coding: utf-8 -*-

import os
import subprocess

from PySide2 import QtCore, QtGui, QtWidgets

try:
    from . import app_command
except:
    import app_command

class IconItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(IconItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        view = self.parent()
        if view.accessibleDescription() == 'ListMode':
            option.displayAlignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
            option.decorationPosition = QtWidgets.QStyleOptionViewItem.Left
        return super(IconItemDelegate, self).paint(painter, option, index)

class IconListModel(QtCore.QAbstractListModel):
    def __init__(self, icon_files, parent=None):
        super(IconListModel, self).__init__(parent)
        self.icon_files = icon_files

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.icon_files)

    def refresh(self, icon_files):
        self.icon_files = icon_files
        self.layoutAboutToBeChanged.emit()
        self.beginResetModel()
        self.endResetModel()
        self.layoutChanged.emit()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        icon_file = self.icon_files[row]
        icon_name = app_command.get_icon_name(icon_file)

        if role == QtCore.Qt.DisplayRole:
            return icon_file.split('/')[-1].split('.')[0]

        if role == QtCore.Qt.SizeHintRole:
            size = self.parent().iconSize()
            if self.parent().accessibleDescription() == 'ListMode':
                size += QtCore.QSize(200, 24)
            else:
                size += QtCore.QSize(64, 24)
            return size

        if role == QtCore.Qt.ToolTipRole:
            return icon_name

        elif role == QtCore.Qt.DecorationRole:
            icon = app_command.get_icon(icon_name)
            return icon

        elif role == QtCore.Qt.WhatsThisRole:
            return icon_file

        else:
            return None

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

class IconListView(QtWidgets.QListView):
    def __init__(self, icon_files, parent=None):
        super(IconListView, self).__init__(parent)
        self.copy_popup = None
        self.copy_pos = QtCore.QPoint(0, 0)
        self.setMouseTracking(True)
        # Base Settings
        self.icon_files = icon_files
        self.setObjectName('IconListView')
        self.setIconSize(QtCore.QSize(64, 64))
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setUniformItemSizes(True)
        self.setWordWrap(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.set_view_icon_mode()

        # Context Menu
        self.menu = QtWidgets.QMenu(self)
        self.copy_action = self.menu.addAction('Copy Name')
        self.open_action = self.menu.addAction('Open Icon File')
        self.save_action = self.menu.addAction('Save Icon File...')

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # Set Model
        self.model = IconListModel(self.icon_files, self)
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.setModel(self.proxy_model)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterRole(QtCore.Qt.ToolTipRole)
        self.sel_model = QtCore.QItemSelectionModel(self.proxy_model)
        self.setSelectionModel(self.sel_model)

        # Set Delegate
        delegate = IconItemDelegate(self)
        self.setItemDelegate(delegate)

        # Signal
        self.copy_action.triggered.connect(self.copy_icon_name)
        self.open_action.triggered.connect(self.open_icon_file)
        self.save_action.triggered.connect(self.save_icon_file)

        self.doubleClicked.connect(self.copy_icon_name)

    def mouseMoveEvent(self, event):
        pos = self.cursor().pos() + QtCore.QPoint(-32, -32)
        distance = (pos - self.copy_pos).manhattanLength()
        if distance > 5:
            self.close_copy_popup()
        return super(IconListView, self).mouseMoveEvent(event)

    def close_copy_popup(self):
        if self.copy_popup:
            self.copy_popup.close()
            self.copy_action = None

    def on_context_menu(self, point):
        self.menu.exec_(self.mapToGlobal(point))

    def refresh(self, icon_files):
        self.icon_files = icon_files
        self.model.refresh(icon_files)

    def set_view_icon_mode(self):
        self.setAccessibleDescription('IconMode')
        self.setSpacing(8)

    def set_view_list_mode(self):
        self.setAccessibleDescription('ListMode')
        self.setSpacing(2)

    def save_icon_file(self):
        sel_index = self.sel_model.selectedIndexes()
        if not sel_index:
            return
        save_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Save Directory', 'D:/')
        if not save_dir:
            return
        if save_dir[-1] == '/':
            save_dir = save_dir[:-1]
        saved_file = ''
        for index in sel_index:
            index = self.proxy_model.mapToSource(index)
            icon_file = index.data(QtCore.Qt.WhatsThisRole)
            dst_filename = '{}/{}'.format(save_dir, icon_file.split('/')[-1])
            saved_file = os.path.normpath(dst_filename)
            app_command.save_icon_file(icon_file, dst_filename)
        if saved_file:
            subprocess.Popen('explorer /select,"{}"'.format(saved_file), shell=True)

    def open_icon_file(self, *args):
        sel_index = self.sel_model.selectedIndexes()
        if not sel_index:
            return
        index = self.proxy_model.mapToSource(sel_index[0])
        icon_file = index.data(QtCore.Qt.WhatsThisRole)
        app_command.open_icon_file(icon_file)

    def copy_icon_name(self, *args):
        sel_index = self.sel_model.selectedIndexes()
        if not sel_index:
            return
        index = self.proxy_model.mapToSource(sel_index[0])
        icon_name = index.data(QtCore.Qt.ToolTipRole)
        clipboard = QtGui.QGuiApplication.clipboard()
        clipboard.setText(icon_name)
        self.copy_pos = self.cursor().pos() + QtCore.QPoint(-32, -32)
        self.copy_popup = QtWidgets.QWidget(self)
        self.copy_label = QtWidgets.QLabel('Copied to Clipboard.', self.copy_popup)
        self.copy_popup.setWindowFlags(QtCore.Qt.ToolTip)
        self.copy_popup.move(self.copy_pos)
        copy_layout = QtWidgets.QVBoxLayout(self.copy_popup)
        copy_layout.addWidget(self.copy_label)
        self.copy_popup.show()
        QtCore.QTimer.singleShot(1000, self.close_copy_popup)

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    icon_files = app_command.get_all_icon_files()
    view = IconListView(icon_files['All'])
    view.show()
    app.exec_()