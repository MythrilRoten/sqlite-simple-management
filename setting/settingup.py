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

from database.database import DataBase



class Settingup():
    def __init__(self, widget: QComboBox, path: str) -> None:
        global db

        db = DataBase(path)
        self.setup_names_of_tables(widget)

    @staticmethod
    def get_data_record(table_widget: QTableWidget) -> dict:
        """Get dict data from current row in table widget

        Args:
            table_widget (QTableWidget): table where locate records, and select a cell

        Returns:
            dict: full info of record
        """
        data = dict()
        row = table_widget.currentRow()
        for column in range(table_widget.columnCount()):
            data[table_widget.horizontalHeaderItem(column).text()] = table_widget.item(row, column).text()
        return data

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
        table_widget.setRowCount(rows + 1)
        table_widget.setColumnCount(columns)

        table_widget.setHorizontalHeaderLabels(header_of_table)
        table_widget.verticalHeader().setDefaultAlignment(Qt.AlignHCenter)

        table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # Insert query row
        table_widget.setVerticalHeaderItem(0, QTableWidgetItem(str('query')))
        [table_widget.setVerticalHeaderItem(i-1, QTableWidgetItem(str(i-1))) for i in range(2, rows + 2)]

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

        # If table empty
        if content_of_db_table == []:
            self.clear_table_widget(table_widget)
            return QMessageBox.information(None, "Information", "There no records in selected table")
        if content_of_db_table != []:
            ...

        columns = len(content_of_db_table[0])

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
            
        self.clear_table_widget(table_widget)
        
        header_of_table = [i[1] for i in db.info[table]['table_info']]
        rows = len(content_of_db_table)
        
        self._ui_qtablewidget(table_widget, header_of_table, rows, columns)

        # Filling table_widget
        for row, record in enumerate(content_of_db_table):
            for column, field in enumerate(record):
                item = QTableWidgetItem(str(field))
                table_widget.setItem(row + 1, column, item)

        # Clear size recent table and resize
        table_widget.horizontalHeader().setStretchLastSection(False)
        table_widget.resizeColumnsToContents()
        table_widget.horizontalHeader().setStretchLastSection(True)
        
    def delete_record_ref(self, table_widget: QTableWidget, table: str) -> bool:
        """Contain a reference to function in database class and fill table after sql operation

        Args:
            table (str): where delete record
            record (dict): record's fields

        Returns:
            bool: status execution
        """
        record = self.get_data_record(table_widget)
        db.delete_record(table, record)
        self.fill_table(table_widget, table)
