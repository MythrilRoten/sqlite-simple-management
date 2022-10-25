from datetime import datetime
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, Slot)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
                               QHeaderView, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QSizePolicy, QStatusBar, QTableWidget,
                               QTableWidgetItem, QWidget, QLineEdit, QAbstractItemView,
                               QMessageBox)
from typing import Sequence

from database.database import DataBase

SYSTEM_ROWS = 2

class Settingup():
    
    def __init__(self, widget: QComboBox, path: str) -> None:
        global db

        db = DataBase(path)
        self.setup_names_of_tables(widget)



    @staticmethod
    def _ui_combobox(combo_widget: QComboBox) -> None:
        """- Set place holder text

        Args:
            combo_widget (QComboBox): combobox, which will have UI
        """
        combo_widget.clear()
        combo_widget.setPlaceholderText(' ')
        combo_widget.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)

    @staticmethod
    def _ui_qtablewidget(table_widget: QTableWidget, header_of_table: list, rows: int, columns: int) -> None:
        """- Set row / column count
        - Set horizontal / vertical labels
        - Set horizontal / vertical scrollbar mode
        - Insert a row of query

        Args:
            table_widget (QTableWidget):  tablewidget, which will have UI
            header_of_table (list): info about fields in database table
            rows (int): amount of rows in database table
            columns (int): amount of columns in database table
        """
        table_widget.setRowCount(rows + SYSTEM_ROWS)
        table_widget.setColumnCount(columns)

        table_widget.setHorizontalHeaderLabels(header_of_table)
        table_widget.verticalHeader().setDefaultAlignment(Qt.AlignHCenter)

        table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # Insert query row
        table_widget.setVerticalHeaderItem(0, QTableWidgetItem(str('query')))
        
        # Insert add row
        table_widget.setVerticalHeaderItem(1, QTableWidgetItem(str('add')))
        [table_widget.setVerticalHeaderItem(i - 1, QTableWidgetItem(str(i - SYSTEM_ROWS))) for i in range(3, rows + SYSTEM_ROWS + 1)]

    @staticmethod
    def clear_combobox_widget(combobox_widget: QComboBox) -> None:
        """Make combobox widget like a snow

        Args:
            combobox_widget (QComboBox): combobox, which will be cleared
        """
        combobox_widget.clear()
    
    @staticmethod
    def clear_table_widget(table_widget: QTableWidget) -> None:
        """Make table widget like a snow

        Args:
            table_widget (QTableWidget): tablewidget, which will be cleared
        """
        table_widget.clearContents()
        table_widget.clear()
        table_widget.setRowCount(0)
        table_widget.setColumnCount(0)

    def setup_names_of_tables(self, combo_widget: QComboBox) -> None:
        """Add current name of tables in QComboBox and call UI function

        Args:
            combo_widget (QComboBox): combobox, which will contain current tables in database
        """
        self._ui_combobox(combo_widget)
        combo_widget.addItems(db.name_of_tables)

    def fill_table(self, table_widget: QTableWidget, table: str, query: bool = False) -> None | QMessageBox:
        """Fill QTableWidget of existing records or filter records by query and call UI function

        Args:
            table_widget (QTableWidget): tablewidget, which will contain current data of table
            table (str): name of table in database
            query (bool): recognize who send signal - [combobox, pushbutton[Filter]]. Defaults to False - combobox
        """ 
        content_of_db_table = db.get_content(table)

        header_of_table = [i[1] for i in db.info[table]['table_info']]
        columns = len(header_of_table)

        # Replace content_of_db_table with query
        if query:
            list_of_conditions = []
            for column in range(columns):
                try: 
                    item = table_widget.item(0, column).text()
                    if item == '' or item == ' ':
                        raise AttributeError
                    item = table_widget.horizontalHeaderItem(column).text() + table_widget.item(0, column).text(); list_of_conditions.append(item) 
                except AttributeError: ...
            query = ' AND '.join(list_of_conditions)    
            content_of_db_table = db.get_content(table, query)

        
        rows = len(content_of_db_table)

        # If table empty
        if content_of_db_table == []:
            self.clear_table_widget(table_widget)
            self._ui_qtablewidget(table_widget, header_of_table, rows, columns)
            for column in range(table_widget.columnCount()):
                if table_widget.horizontalHeaderItem(column).text() == db.get_pk(db.info, table): # ReadOnly Pk
                    ######## Insert in add row a new pk id
                    if table_widget.item(1, column) is None:
                        last_pk = QTableWidgetItem(str(db.get_last_pk(table)+1))
                        last_pk.setFlags(Qt.ItemIsEnabled)
                        table_widget.setItem(1, column, last_pk)
                    #########
            return QMessageBox.information(None, "Information", "There no records in selected table")
        if content_of_db_table != []:
            ...


     
        self.clear_table_widget(table_widget)
        
        self._ui_qtablewidget(table_widget, header_of_table, rows, columns)
        
        # Filling table_widget
        for row, record in enumerate(content_of_db_table):
            for column, field in enumerate(record):
                item = QTableWidgetItem(str(field))
                if table_widget.horizontalHeaderItem(column).text() == db.get_pk(db.info, table): # ReadOnly Pk
                    item.setFlags(Qt.ItemIsEnabled)
                    ######## Insert in add row a new pk id
                    if table_widget.item(1, column) is None:
                        last_pk = QTableWidgetItem(str(db.get_last_pk(table)+1))
                        last_pk.setFlags(Qt.ItemIsEnabled)
                        table_widget.setItem(1, column, last_pk)
                    #########
                table_widget.setItem(row + SYSTEM_ROWS, column, item)

        # Clear size recent table and resize
        table_widget.horizontalHeader().setStretchLastSection(False)
        table_widget.resizeColumnsToContents()
        table_widget.horizontalHeader().setStretchLastSection(True)

    @staticmethod
    def get_data_record(table_widget: QTableWidget, row: int = None) -> dict:
        """Get dict data from current row in table widget

        Args:
            table_widget (QTableWidget): table where locate records, and select a cell
            row (int): row of record in table widget

        Returns:
            dict: full info of record
        """
        data = dict()
        
        if row is None:
            row = table_widget.currentRow()
            
        for column in range(table_widget.columnCount()):
            data[table_widget.horizontalHeaderItem(column).text()] = table_widget.item(row, column).text()
        return data

    def get_data_table_foreign_keys(self, table_widget: QTableWidget, table: str) -> Sequence[dict]:
        ...

    def get_data_table(self, table_widget: QTableWidget, table: str) -> Sequence[dict] | bool:
        """Return list of dict of table_widget values like [{field: value, ...}, {...}]

        Args:
            table_widget (QTableWidget): from which table widget take data
            table (str): name of table current db's table

        Returns:
            Sequence[dict]: data of table widget
        """
        data = list()
        for row in range(SYSTEM_ROWS, table_widget.rowCount()):
            temp = dict()
            for column in range(table_widget.columnCount()):
                item = table_widget.item(row, column).text() if table_widget.item(row, column) != None else ''
                name_column = table_widget.horizontalHeaderItem(column).text()
                # If trouble with type
                type_of_value = db.info[table]['table_info'][column][2]
                try:
                    if type_of_value in ["INT", "INTEGER"]:
                        item = int(item)
                    if type_of_value in ["REAL", "DOUBLE", "DOUBLE PRECISION", "FLOAT"]:
                        item = float(item)
                    if type_of_value in ["DATE"]:
                        item = datetime.strptime(item, '%Y-%m-%d')
                except:
                    return 0
                # 
                temp[name_column] = item
            data.append(temp)
        return data

    def delete_record_ref(self, table_widget: QTableWidget, table: str) -> QMessageBox:
        """Contain a reference to delete function in database class and fill table after sql operation

        Args:
            table_widget (QTableWidget): from which widget get record to delete
            table (str): name of table
        Returns:
            QMessageBox: status execution
        """
        
        # If selected row is "query" or "add"
        if table_widget.currentRow() in (0, 1):
            return QMessageBox.information(None, "Information", "You can't delete system row")

        
        record = self.get_data_record(table_widget)
        if db.delete_record(table, record):
            self.fill_table(table_widget, table)
            return QMessageBox.information(None, "Information", "The operation was successful")
        else:
            self.clear_table_widget(table_widget)
            self.fill_table(table_widget, table)
            return QMessageBox.information(None, "Information", "The operation was denied")
        
       
    def create_record_ref(self, table_widget: QTableWidget, table: str) -> None:
        """Contain a reference to create function in database class and fill table after sql operation

        Args:
            table_widget (QTableWidget): from which widget get record to create
            table (str): name of table
        Returns:
            QMessageBox: status execution
        """
        if type(self.get_data_record(table_widget, 1)) != dict:
            self.clear_table_widget(table_widget)
            self.fill_table(table_widget, table)
            return QMessageBox.information(None, "Information", "Invalid data")
        else:
            record = self.get_data_record(table_widget, 1) # Second row of creation
        
        if db.create_record(table, record):
            self.fill_table(table_widget, table)
            return QMessageBox.information(None, "Information", "The operation was successful")
        else:
            self.clear_table_widget(table_widget)
            self.fill_table(table_widget, table)
            return QMessageBox.information(None, "Information", "The operation was denied")
        
    def update_records_ref(self, table_widget: QTableWidget, table: str) -> None:
        """Contain a reference to update function in database class and fill table after sql operation

        Args:
            table_widget (QTableWidget): from which widget get record to update
            table (str): name of table
        Returns:
            QMessageBox: status execution
        """
        if table_widget.rowCount() == 2: # If table empty, only system rows
            return QMessageBox.information(None, "Information", "There are nothing to update")
        
        if self.get_data_table(table_widget, table) != dict:
            self.clear_table_widget(table_widget)
            self.fill_table(table_widget, table)
            return QMessageBox.information(None, "Information", "Invalid data")
        else:
            records = self.get_data_table(table_widget, table)
            
        if db.update_records(table, records):
            self.fill_table(table_widget, table)
            return QMessageBox.information(None, "Information", "The operation was successful")
        else:
            self.clear_table_widget(table_widget)
            self.fill_table(table_widget, table)
            return QMessageBox.information(None, "Information", "The operation was denied")
