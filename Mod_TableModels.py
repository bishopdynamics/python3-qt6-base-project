#!/usr/bin/env python3

# Table Models Module
#   QT TableViews need data fed to them via TableModels, these control how data is displayed
#       This is where Column Headers and sizing happens

# Created 2022 by James Bishop (james@bishopdynamics.com)

from PyQt6 import QtCore
from PyQt6.QtCore import Qt

# import operator
# sorted_dict = sorted(unsorted_dict, key=operator.itemgetter('name'))


class LogTableModel(QtCore.QAbstractTableModel):
    # This is the model used to display data in the Log TableView
    def __init__(self, data):
        super().__init__()
        self.horizontalHeaders = [''] * 2
        self.column_widths = [200, 1240]
        self.header_height = 25
        self.setHeaderData(0, Qt.Orientation.Horizontal, 'Timestamp')
        self.setHeaderData(1, Qt.Orientation.Horizontal, 'Message')
        self._data = data

    def setHeaderData(self, section, orientation, data, role=Qt.ItemDataRole.EditRole):
        if orientation == Qt.Orientation.Horizontal and role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            try:
                self.horizontalHeaders[section] = data
                return True
            except:
                return False
        return super().setHeaderData(section, orientation, data, role)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                try:
                    return self.horizontalHeaders[section]
                except:
                    pass
            elif role == Qt.ItemDataRole.SizeHintRole:
                try:
                    return QtCore.QSize(self.column_widths[section], self.header_height)
                except:
                    pass
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
