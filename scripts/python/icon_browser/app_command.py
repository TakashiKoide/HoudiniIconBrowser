# -*- coding: utf-8 -*-

import os
import zipfile
import shutil
import re
from collections import OrderedDict

from PySide2 import QtGui
try:
    import hou
except:
    hou = None

if hou is None:
    install_path = os.path.expandvars('$ProgramFiles/Side Effects Software')
    houdini_versions = []
    folder_names = os.listdir(install_path)
    for folder_name in folder_names:
        if re.fullmatch('Houdini [0-9.]+', folder_name):
            houdini_versions.append(folder_name)
    hh = '{}/{}/houdini'.format(install_path, houdini_versions[-1])
    os.environ['HH'] = hh

ICON_PATH = os.getenv('HH') + '/config/Icons/icons.zip'
if not os.path.exists(ICON_PATH):
    ICON_PATH = os.getenv('HH') + '/help/icons.zip'

def get_parent_window():
    return hou.qt.mainWindow()

def get_all_icon_files():
    zf = zipfile.ZipFile(ICON_PATH, 'r')
    icon_files = OrderedDict()
    for name in sorted(zf.namelist(), key=str.lower):
        if name.startswith('old') or not name.endswith('.svg'):
            continue
        category = name.split('/')[0]
        if '.' in category:
            continue
        if 'All' in icon_files:
            icon_files['All'].append(name)
        else:
            icon_files['All'] = [name]
        if category in icon_files:
            icon_files[category].append(name)
        else:
            icon_files[category] = [name]
    zf.close()
    return icon_files

def get_icon_name(filename):
    icon_name = filename.split('.')[0].replace('/', '_')
    category = icon_name.split('_')[0]
    if category == 'CONVERTED' or category == 'Pics':
        icon_name = icon_name.replace(category + '_', '')
    return icon_name

def get_icon(icon_name):
    try:
        icon = hou.qt.Icon(icon_name, 64, 64)
    except:
        no_icon_file = os.path.dirname(__file__) + '/icons/no_icon.png'
        icon = QtGui.QIcon(no_icon_file)
    return icon

def open_icon_file(icon_file):
    temp_dir = os.getenv('TEMP')
    with zipfile.ZipFile(ICON_PATH, 'r') as zf:
        extract_file = zf.extract(icon_file, temp_dir)
        os.startfile(extract_file)

def save_icon_file(src_filename, dst_filename):
    temp_dir = os.getenv('TEMP')
    with zipfile.ZipFile(ICON_PATH, 'r') as zf:
        extract_file = zf.extract(src_filename, temp_dir)
        shutil.move(extract_file, dst_filename)
        dir_name = os.path.dirname(extract_file)
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)